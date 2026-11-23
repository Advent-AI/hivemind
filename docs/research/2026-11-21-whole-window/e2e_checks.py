"""$0 end-to-end checks of the reading path on the dry stores (round 29): the worksheet packets built, a synthetic reading, and the
verdict, then each false-pass and refusal case the review named.

  python3 e2e_checks.py <dry out folder> <scratch>
"""
import copy
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verdict                                                           # noqa: E402
import worksheet                                                         # noqa: E402


def tree(out, scratch, name, edit=None):
    """A copy of the out folder's six sequences (stores linked, summaries copied) with `edit` applied to the summaries."""
    target = Path(scratch) / name
    if target.exists():
        shutil.rmtree(target)
    for sequence in verdict.SEQUENCES:
        (target / sequence).mkdir(parents=True)
        for item in (Path(out) / sequence).iterdir():
            if item.name != 'summary.json':
                os.symlink(item, target / sequence / item.name)
        summary = json.loads((Path(out) / sequence / 'summary.json').read_text())
        if edit:
            edit(sequence, summary)
        (target / sequence / 'summary.json').write_text(json.dumps(summary))
    return target


def read_all(packets, key, control_definite=3):
    p, h = packets
    p, h = copy.deepcopy(p), copy.deepcopy(h)
    first = {}
    for row in p:
        first.setdefault(key[row['sequence']], []).append(row)
    for name, rows in first.items():
        rows.sort(key=lambda r: r['dates'][0])
        for i, row in enumerate(rows):
            mark(row, 'definite' if name.startswith('control') and i < control_definite else 'clear')
    for row in h:
        finding = 'pass' if row['part'] == 'H5' else 'ok'
        row['reader'].update({'finding': finding, 'first finding': finding, 'second finding': finding, 'excerpt': row['forecast'][:9]})
    return p, h


def mark(row, value, segment=None):
    """A P reading with its record: both readers agree; ranges and excerpts consistent with the class."""
    s = segment if segment is not None else (420.0 if value == 'definite' else 380.0)
    row['reader'].update({'class': value, 'first class': value, 'second class': value, 'segment low': s, 'segment high': s,
                          'company low': 400.0, 'company high': 400.0, 'segment excerpt': row['segment forecast'][:9],
                          'company excerpt': row['company forecast'][:9]})


def write(folder, p, h, gains):
    for name, data in (('p.json', p), ('h.json', h), ('gains.json', gains)):
        (Path(folder) / name).write_text(json.dumps(data))
    return [str(Path(folder) / n) for n in ('p.json', 'h.json', 'gains.json')]


def outcome(out, files, key_path):
    try:
        return verdict.main(out, *files, key_path)
    except verdict.Refused as error:
        return ('refused', str(error)[:120])


def main(out, scratch):
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    key_path = scratch / 'key.json'
    packets = worksheet.build(out, str(scratch / 'packet'), str(key_path), seed=7)
    key = json.loads(key_path.read_text())
    p, h = read_all(packets, key)
    (scratch / 'p-read.json').write_text(json.dumps(p))
    gains = worksheet.gains(out, str(scratch / 'p-read.json'), str(key_path), str(scratch / 'gains.json'))
    for g in gains:
        g['reader'].update({'rule B material failure': False, 'cpu increment': 'none', 'rule B inputs': [g['forecast'][:9]], 'rule B reasoning': 'the quoted forecast follows from its stated inputs with no unsupported step'})
    results = {}
    files = write(scratch, p, h, gains)
    results['a complete synthetic reading passes'] = outcome(out, files, key_path) == ('pass', 'all three pairs improved')
    results['P rows only (no H review) is refused'] = outcome(out, write(scratch, p, [], gains), key_path)[0] == 'refused'
    h_none = copy.deepcopy(h)
    h_none[0]['reader']['finding'] = None
    results['an unread H row is refused'] = outcome(out, write(scratch, p, h_none, gains), key_path)[0] == 'refused'
    g_bad = copy.deepcopy(gains)
    g_bad[0]['reader']['cpu increment'] = None
    results['an incomplete gain review is refused'] = outcome(out, write(scratch, p, h, g_bad), key_path)[0] == 'refused'
    g_fail = copy.deepcopy(gains)
    for g in g_fail:
        g['reader'].update({'rule B material failure': True, 'reliance by date': {d: True for d in g['gain dates']}})
    results['every gain withdrawn by its reviews: not improved, fail'] = outcome(out, write(scratch, p, h, g_fail), key_path)[0] == 'fail'
    h4 = copy.deepcopy(h)
    next(r for r in h4 if r['part'] == 'H4')['reader'].update({'finding': 'double count', 'first finding': 'double count', 'second finding': 'double count'})
    results['an H4 double count fails'] = outcome(out, write(scratch, p, h4, gains), key_path) == ('fail', 'confirmed harm')
    h3 = copy.deepcopy(h)
    row = next(r for r in h3 if r['part'] == 'H3' and r['sequence'].startswith('linked'))
    row['reader'].update({'finding': 'grounding error', 'first finding': 'grounding error', 'second finding': 'grounding error',
                          'error type': 'own figure as market'})
    results['a linked grounding error the control lacks fails'] = outcome(out, write(scratch, p, h3, gains), key_path) == ('fail', 'confirmed harm')
    h5 = copy.deepcopy(h)
    for r in [r for r in h5 if r['part'] == 'H5' and r['sequence'] == 'linked-1'][:2]:
        r['reader'].update({'finding': 'material failure', 'first finding': 'material failure', 'second finding': 'material failure'})
    results['two more H5 failures in a linked sequence fail'] = outcome(out, write(scratch, p, h5, gains), key_path) == ('fail', 'confirmed harm')
    rejected = tree(out, scratch, 'rejected', lambda s, summary: summary['acceptance'].update(accepted=False) if s == 'control-1' else None)
    results['a sequence the gate rejected makes it inconclusive'] = outcome(str(rejected), files, key_path)[0] == 'inconclusive'
    double = tree(out, scratch, 'double', lambda s, summary: summary.update(terminal={'outcome': 'double refusal', 'view': 'v9'}) if s == 'linked-2' else None)
    results['a linked double refusal fails even with no P rows'] = outcome(str(double), write(scratch, [], [], []), key_path) == ('fail', 'a linked double refusal')

    files = write(scratch, p, h, gains)     # the complete reading again (the cases above overwrote the packet files)
    control_days = {(j['view'], j['day']) for j in json.loads((Path(out) / 'control-1' / 'summary.json').read_text())['reader judgements']}

    def refusals(sequence, summary):
        if sequence == 'linked-1':          # four refusals on reader-days judged in both arms (H1 counts matched reader-days only)
            days = [(j['view'], j['day']) for j in summary['reader judgements'] if j['must be fresh'] and (j['view'], j['day']) in control_days][:4]
            summary['archive judge rows written (dated)'] += [{'call_id': 0, 'view': v, 'day': d, 'refused': True, 'reader': True} for v, d in days]
    refused_tree = tree(out, scratch, 'refusals', refusals)
    results['four more linked refusals on matched reader-days fail (H1)'] = outcome(str(refused_tree), files, key_path) == ('fail', 'confirmed harm')

    def three(sequence, summary):
        refusals(sequence, summary)
        if sequence == 'linked-1':
            summary['archive judge rows written (dated)'].pop()
    results['three more are tolerated (H1)'] = outcome(str(tree(out, scratch, 'refusals-3', three)), files, key_path)[0] == 'pass'
    g_no_reliance = copy.deepcopy(gains)
    g_no_reliance[0]['reader']['rule B material failure'] = True
    results['a material failure without a reliance finding is refused'] = outcome(out, write(scratch, p, h, g_no_reliance), key_path)[0] == 'refused'
    p_sub = copy.deepcopy(p)
    p_sub[0]['segment judgement'] += 100000
    results['a substituted P judgement is refused'] = outcome(out, write(scratch, p_sub, h, gains), key_path)[0] == 'refused'
    results.update(pilot_checks(out, scratch))
    print(json.dumps(results, indent=1))
    return all(results.values())


def pilot_checks(out, scratch):
    """D708's pilot path on linked-1 and control-1 of the dry stores."""
    folder = Path(scratch) / 'pilot'
    folder.mkdir(parents=True, exist_ok=True)
    key_path = folder / 'key.json'
    p, h4 = worksheet.build_pilot(out, str(folder / 'packet'), str(key_path), seed=3)
    key = json.loads(key_path.read_text())
    p, h4 = copy.deepcopy(p), copy.deepcopy(h4)
    by = {}
    for row in p:
        by.setdefault(key[row['sequence']], []).append(row)
    for name, rows in by.items():
        rows.sort(key=lambda r: r['dates'][0])
        for i, row in enumerate(rows):
            mark(row, 'definite' if name == 'control-1' and i < 3 else 'clear')
    for row in h4:
        row['reader'].update({'finding': 'ok', 'first finding': 'ok', 'second finding': 'ok', 'excerpt': row['forecast'][:9]})
    (folder / 'p-read.json').write_text(json.dumps(p))
    gains = worksheet.gains(out, str(folder / 'p-read.json'), str(key_path), str(folder / 'gains.json'))
    for g in gains:
        g['reader'].update({'rule B material failure': False, 'cpu increment': 'none', 'rule B inputs': [g['forecast'][:9]], 'rule B reasoning': 'the quoted forecast follows from its stated inputs with no unsupported step'})

    def decide(p_, h4_, gains_):
        for name, data in (('p.json', p_), ('h4.json', h4_), ('g.json', gains_)):
            (folder / name).write_text(json.dumps(data))
        try:
            return verdict.pilot_decision(out, str(folder / 'p.json'), str(folder / 'h4.json'), str(folder / 'g.json'), str(key_path), allow_dry=True)
        except verdict.Refused as error:
            return ('refused', str(error)[:100])
    results = {'pilot: a complete reading of an improved pair continues': decide(p, h4, gains)[0] == 'continue'}
    results['pilot: never gives the comparison\'s pass'] = 'pass' not in {decide(p, h4, gains)[0]}
    sub = copy.deepcopy(p)
    sub[0]['company judgement'] += 100000
    results['pilot: a substituted P judgement is refused'] = decide(sub, h4, gains)[0] == 'refused'
    results['pilot: a missing H4 reading is refused'] = decide(p, h4[1:], gains)[0] == 'refused'
    double = copy.deepcopy(h4)
    double[0]['reader'].update({'finding': 'double count', 'first finding': 'double count', 'second finding': 'double count'})
    results['pilot: an H4 double count stops'] = decide(p, double, gains) == ('stop', 'confirmed harm (H4 double count)')
    corrected = copy.deepcopy(gains)
    for g in corrected:
        if g['view'] == 'v14':
            g['reader'].update({'cpu increment': 'quantified', 'increment removed': 30.0, 'corrected low': 370.0,
                                'corrected high': 370.0})                       # $400B less $30B, below the linked segment's 380
    results['pilot: a quantified CPU correction is applied per gain date (the gains become definite: stop)'] = \
        decide(p, h4, corrected) == ('stop', 'pair 1 not improved')
    unquantified = copy.deepcopy(gains)
    for g in unquantified:
        if g['view'] == 'v14':
            g['reader']['cpu increment'] = 'unquantifiable'
    results['pilot: every unquantifiable CPU gain unresolved together (stop: undecided)'] = decide(p, h4, unquantified) == ('stop', 'pair 1 undecided')
    try:
        verdict.pilot_decision(out, str(folder / 'p.json'), str(folder / 'h4.json'), str(folder / 'g.json'), str(key_path))
        results['pilot: the official decision refuses dry summaries'] = False
    except verdict.Refused:
        results['pilot: the official decision refuses dry summaries'] = True
    no_text = copy.deepcopy(p)
    no_text[0]['segment forecast'] = ''
    results['pilot: a P row with its forecast text removed is refused'] = decide(no_text, h4, gains)[0] == 'refused'
    wrong_class = copy.deepcopy(p)
    target = next(r for r in wrong_class if r['reader']['class'] == 'clear')
    target['reader'].update({'segment low': 420.0, 'segment high': 420.0})
    results['pilot: a class the ranges contradict is refused'] = decide(wrong_class, h4, gains)[0] == 'refused'
    one_reader = copy.deepcopy(p)
    one_reader[0]['reader']['second class'] = None
    results['pilot: a P row without the second reading is refused'] = decide(one_reader, h4, gains)[0] == 'refused'
    swapped = copy.deepcopy(h4)
    swapped[0]['request'] = swapped[1]['request']
    results['pilot: an H4 row with another request is refused'] = decide(p, swapped, gains)[0] == 'refused'
    no_pair = copy.deepcopy(h4)
    no_pair[0]['paired arm in force'] = None
    results['pilot: an H4 row without the control answer is refused'] = decide(p, no_pair, gains)[0] == 'refused'
    nan = copy.deepcopy(gains)
    for g in nan:
        if g['view'] == 'v14':
            g['reader'].update({'cpu increment': 'quantified', 'increment removed': 30.0, 'corrected low': 370.0, 'corrected high': float('nan')})
    results['pilot: a NaN corrected range is refused'] = decide(p, h4, nan)[0] == 'refused'
    short = copy.deepcopy(p)
    for row in [r for r in short if key[r['sequence']] == 'linked-1'][:15]:
        mark(row, 'unresolved')
        row['reader'].update({k: None for k in ('segment low', 'segment high', 'company low', 'company high')})
    short_double = copy.deepcopy(h4)
    short_double[0]['reader'].update({'finding': 'double count', 'first finding': 'double count', 'second finding': 'double count'})
    results['pilot: coverage short comes before harm (inconclusive)'] = decide(short, short_double, gains) == ('inconclusive', 'coverage short')
    # one corrected company answer carried across two gain dates: the segment below it on one date, above it on the other
    rows = [{'judgement': 1, 'view': 'v14', 'forecast': 'about $405B', 'reader': {'rule B material failure': False, 'cpu increment': 'quantified',
                                                                                  'increment removed': 30.0, 'corrected low': 375.0,
                                                                                  'corrected high': 375.0, 'rule B inputs': ['$405B'], 'rule B reasoning': 'the quoted total less the quoted CPU increment, carried as stated'}},
            {'judgement': 2, 'view': 'v9', 'forecast': 'about $360B', 'reader': {'rule B material failure': False, 'cpu increment': 'none', 'rule B inputs': ['$360B'], 'rule B reasoning': 'the quoted segment forecast as stated, arithmetic checked'}},
            {'judgement': 3, 'view': 'v9', 'forecast': 'about $390B', 'reader': {'rule B material failure': False, 'cpu increment': 'none', 'rule B inputs': ['$390B'], 'rule B reasoning': 'the quoted segment forecast as stated, arithmetic checked'}}]
    credit = verdict.gain_credit(rows, {'d1': (2, 1), 'd2': (3, 1)}, {'d1': (360.0, 360.0), 'd2': (390.0, 390.0)}, {1: (405.0, 405.0)})
    results['credit: a carried corrected answer gives a class per date'] = credit == {'d1': 'clear', 'd2': 'definite'}
    bad_values = copy.deepcopy(p)
    bad_values[0]['reader'].update({'first class': False, 'second class': 7, 'third class': bad_values[0]['reader']['class'], 'third source': 'x'})
    results['pilot: readings outside the allowed values are refused'] = decide(bad_values, h4, gains)[0] == 'refused'
    made_up = copy.deepcopy(p)
    made_up[0]['reader']['segment excerpt'] = 'a sentence that is not in the answer'
    results['pilot: an excerpt not from its answer is refused'] = decide(made_up, h4, gains)[0] == 'refused'
    no_trace = copy.deepcopy(gains)
    no_trace[0]['reader']['rule B inputs'] = []
    results['pilot: a gain review without its rule-B trace is refused'] = decide(p, h4, no_trace)[0] == 'refused'
    on_segment = copy.deepcopy(gains)
    for g in on_segment:
        if g['view'] == 'v9':
            g['reader'].update({'cpu increment': 'quantified', 'increment removed': 10.0, 'corrected low': 390.0, 'corrected high': 390.0})
    results['pilot: a CPU correction on the Data Center answer is refused'] = decide(p, h4, on_segment)[0] == 'refused'
    raised = copy.deepcopy(gains)
    for g in raised:
        if g['view'] == 'v14':
            g['reader'].update({'cpu increment': 'quantified', 'increment removed': -10.0, 'corrected low': 410.0, 'corrected high': 410.0})
    results['pilot: a correction that raises the total is refused'] = decide(p, h4, raised)[0] == 'refused'
    for label, source in (('true', True), ('spaces', '      ')):
        disputed = copy.deepcopy(p)
        disputed[0]['reader'].update({'second class': 'overlap' if disputed[0]['reader']['class'] != 'overlap' else 'clear',
                                      'third class': disputed[0]['reader']['class'], 'third source': source})
        results[f'pilot: a disputed P reading settled with {label} as its source is refused'] = decide(disputed, h4, gains)[0] == 'refused'
    disputed_h4 = copy.deepcopy(h4)
    disputed_h4[0]['reader'].update({'first finding': 'double count', 'second finding': 'ok', 'third finding': 'ok', 'third source': '     '})
    results['pilot: a disputed H4 finding settled without a quoted source is refused'] = decide(p, disputed_h4, gains)[0] == 'refused'
    rounding_p = copy.deepcopy(p)
    for row in rounding_p:
        if key[row['sequence']] == 'linked-1':
            row['reader'].update({'segment low': 380.02, 'segment high': 380.02})
    rounding = copy.deepcopy(gains)
    for g in rounding:
        if g['view'] == 'v14':
            g['reader'].update({'cpu increment': 'quantified', 'increment removed': 20.0, 'corrected low': 380.04, 'corrected high': 380.04})
    results['pilot: the corrected range is computed, not transcribed (380.02 above 380.00: stop)'] = \
        decide(rounding_p, h4, rounding) == ('stop', 'pair 1 not improved')
    two_ranges = copy.deepcopy(p)
    control_rows = sorted([r for r in two_ranges if key[r['sequence']] == 'control-1'], key=lambda r: r['dates'][0])
    shared = {}
    for r in control_rows:
        shared.setdefault(r['company judgement'], []).append(r)
    pair_rows = next((rows for rows in shared.values() if len(rows) > 1 and all(r['reader']['class'] == 'clear' for r in rows)), None)
    if pair_rows:                                     # the same class either way (round 35): only the one-range rule can refuse it
        pair_rows[1]['reader'].update({'company low': 390.0, 'company high': 390.0})
        results['pilot: one control answer read with two ranges of the same class is refused'] = decide(two_ranges, h4, gains)[0] == 'refused'
    # decimal: $400.2B less $20.1B equals the $380.1B segment: not above it, so clear (credit kept: continue)
    equal_p = copy.deepcopy(p)
    for row in equal_p:
        if key[row['sequence']] == 'linked-1':
            row['reader'].update({'segment low': 380.1, 'segment high': 380.1, 'company low': 400.2, 'company high': 400.2})
    equal_g = copy.deepcopy(gains)
    for g in equal_g:
        if g['view'] == 'v14':
            g['reader'].update({'cpu increment': 'quantified', 'increment removed': 20.1, 'corrected low': 380.1, 'corrected high': 380.1})
    results['credit: 400.2 less 20.1 equals 380.1 in decimal (not definite: continue)'] = decide(equal_p, h4, equal_g)[0] == 'continue'
    # reliance per gain date: one company answer, material failure, reliance on one of its gain dates only
    rows = [{'judgement': 1, 'view': 'v14', 'forecast': 'about $410B', 'reader': {'rule B material failure': True,
             'reliance by date': {'d1': False, 'd2': True}, 'cpu increment': 'none', 'rule B inputs': ['$410B'],
             'rule B reasoning': 'the quoted total carries an unsupported uplift of twenty billion dollars'}},
            {'judgement': 2, 'view': 'v9', 'forecast': 'about $380B', 'reader': {'rule B material failure': False, 'cpu increment': 'none',
             'rule B inputs': ['$380B'], 'rule B reasoning': 'the quoted segment forecast as stated, arithmetic checked'}},
            {'judgement': 3, 'view': 'v9', 'forecast': 'about $395B', 'reader': {'rule B material failure': False, 'cpu increment': 'none',
             'rule B inputs': ['$395B'], 'rule B reasoning': 'the quoted segment forecast as stated, arithmetic checked'}}]
    credit = verdict.gain_credit(rows, {'d1': (2, 1), 'd2': (3, 1)}, {'d1': (380.0, 380.0), 'd2': (395.0, 395.0)}, {1: (410.0, 410.0)})
    results['credit: reliance recorded per gain date withdraws only the date that rests on the failure'] = credit == {'d2': 'none'}
    one_flag = copy.deepcopy(rows)
    one_flag[0]['reader']['reliance by date'] = {'d2': True}
    try:
        verdict.gain_credit(one_flag, {'d1': (2, 1), 'd2': (3, 1)}, {'d1': (380.0, 380.0), 'd2': (395.0, 395.0)}, {1: (410.0, 410.0)})
        results['credit: a material failure missing a gain date\'s reliance is refused'] = False
    except verdict.Refused:
        results['credit: a material failure missing a gain date\'s reliance is refused'] = True
    return results


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
