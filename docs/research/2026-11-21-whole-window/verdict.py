"""The verdict of the paid comparison from the read worksheet and the harm findings (PAID-DESIGN.md §4), written before the run.

  python3 verdict.py <out folder> <read P packet> <read H packet> <read gains packet> <key.json>      # the verdict
  python3 verdict.py --checks                              # $0: the verdict checks, including round 25's and 26's three cases

Each worksheet row carries the reader's class (definite, overlap, clear, unresolved) for a pair of answers and the dates it covers;
dates inherit their pair's class; each arm's 73 dates are counted definite (D), not definite (N) or unresolved (U).
`findings.json` holds `gain_reviews` {pair: {date: 'credit' | 'none' | 'unresolved' | <a class>}} covering every gain of every pair that is
provisionally improved (a gain: linked not definite, control definite, on that date; only gains may be adjusted), and `flags`, every one
an explicit boolean: `h1`, `h3`, `h4_double_count`, `h5`, and the four the run summaries decide (`linked_double_refusal`,
`infrastructure_stop`, `control_double_refusal`, `trajectory_difference`), which must agree with the six `summary.json` files.
The input is refused when the worksheet does not hold, for each of the six sequences, exactly one read class for each of the 73 window
dates, when a class is not one of the four, when a flag is missing or not a boolean, when a gain review is missing or invalid, or when a
summary-decided flag disagrees with the summaries.
"""
import datetime
from pathlib import Path
import json
import sys

WINDOW_DATES = 73
SPAN = ('2026-07-10', '2026-09-20')
CLASSES = ('definite', 'overlap', 'clear', 'unresolved')
FLAGS = ('linked_double_refusal', 'infrastructure_stop', 'control_double_refusal', 'trajectory_difference', 'h1', 'h3', 'h4_double_count', 'h5')
SEQUENCES = ('linked-1', 'linked-2', 'linked-3', 'control-1', 'control-2', 'control-3')


class Refused(SystemExit):
    pass


def calendar():
    day, end = datetime.date.fromisoformat(SPAN[0]), datetime.date.fromisoformat(SPAN[1])
    out = []
    while day <= end:
        out.append(day.isoformat())
        day += datetime.timedelta(days=1)
    return out


import math

P_CONTENT = ('dates', 'segment forecast', 'segment reasons', 'company forecast', 'company reasons')


def finite_range(low, high):
    return all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in (low, high)) and low <= high


def readings_complete(fields, key_field, allowed, *source_texts):
    """The reading record: the first (Claude) and second (blind) readers' values, each one of `allowed`; when they differ, a third value
    from a source-backed read whose `third source` is a quote of at least 12 characters from the regenerated evidence (`source_texts`),
    and which must be the final one; when they agree, the final value is theirs."""
    first, second, third = fields.get(f'first {key_field}'), fields.get(f'second {key_field}'), fields.get(f'third {key_field}')
    if first not in allowed or second not in allowed:
        return False
    if first == second:
        return fields.get(key_field) == first
    source = fields.get('third source')
    return third in allowed and quoted(source, *source_texts) and len(source.strip()) >= 12 and fields.get(key_field) == third


def quoted(excerpt, *texts):
    """An excerpt counts only when it is a non-empty piece of the text it was read from."""
    return isinstance(excerpt, str) and len(excerpt.strip()) >= 4 and any(excerpt in (text or '') for text in texts)


def check_p_row(row):
    """A read P row: the reading record complete; a resolved class carries finite, ordered FY2027 ranges for both answers with their
    excerpts, and the class must be the one the ranges give (definite: segment low above company high; clear: segment high at or below
    company low; overlap otherwise)."""
    fields = row['reader']
    if not readings_complete(fields, 'class', CLASSES, row['segment forecast'], row['segment reasons'], row['company forecast'], row['company reasons']):
        raise Refused(f'{row["sequence"]} {row["segment judgement"]}/{row["company judgement"]}: the reading record is incomplete')
    if fields['class'] == 'unresolved':
        return
    s, c = (fields.get('segment low'), fields.get('segment high')), (fields.get('company low'), fields.get('company high'))
    if not finite_range(*s) or not finite_range(*c):
        raise Refused(f'{row["sequence"]} {row["segment judgement"]}/{row["company judgement"]}: a resolved class needs both ranges')
    if not quoted(fields.get('segment excerpt'), row['segment forecast'], row['segment reasons']) or \
            not quoted(fields.get('company excerpt'), row['company forecast'], row['company reasons']):
        raise Refused(f'{row["sequence"]} {row["segment judgement"]}/{row["company judgement"]}: an excerpt is not from its answer')
    derived = 'definite' if s[0] > c[1] else ('clear' if s[1] <= c[0] else 'overlap')
    if derived != fields['class']:
        raise Refused(f'{row["sequence"]} {row["segment judgement"]}/{row["company judgement"]}: class {fields["class"]} but the ranges give {derived}')


def bind_p(rows, key, out):
    """Every read P row must be a row the stores give, content included (the two supplying judgement ids, the dates, both answers' full
    forecast and reasons), and every row the stores give must be read; each row's reading is then checked (`check_p_row`)."""
    import worksheet
    expected = {}
    for label, name in key.items():
        for row in worksheet.p_rows(Path(out) / name, label):
            expected[(label, row['segment judgement'], row['company judgement'])] = {k: row[k] for k in P_CONTENT}
    read = {}
    for row in rows:
        if row.get('part') != 'P':
            continue
        k = (row['sequence'], row['segment judgement'], row['company judgement'])
        if k in read:
            raise Refused(f'{k}: read twice')
        read[k] = {f: row.get(f) for f in P_CONTENT}
    if read != expected:
        missing, extra = set(expected) - set(read), set(read) - set(expected)
        changed = [k for k in set(read) & set(expected) if read[k] != expected[k]]
        raise Refused(f'the P reading is not the stores\' pairs: {len(missing)} missing, {len(extra)} not in the stores, {len(changed)} changed')
    ranges = {}
    for row in rows:
        if row.get('part') == 'P':
            check_p_row(row)
            if row['reader']['class'] != 'unresolved':
                for side in ('segment', 'company'):
                    k = (row['sequence'], side, row[f'{side} judgement'])
                    value = (row['reader'][f'{side} low'], row['reader'][f'{side} high'])
                    if ranges.setdefault(k, value) != value:
                        raise Refused(f'{k}: one answer read with two different ranges')


def read_classes(rows, key, sequences=SEQUENCES):
    """{sequence: {date: class}}, refusing anything but exactly one valid class per window date per sequence."""
    window = calendar()
    out = {name: {} for name in sequences}
    for row in rows:
        if row.get('part') != 'P':
            continue
        name = key.get(row['sequence'])
        if name not in out:
            raise Refused(f'unknown sequence label {row["sequence"]!r}')
        value = row['reader']['class']
        if value not in CLASSES:
            raise Refused(f'{row["sequence"]}: class {value!r} is not one of {CLASSES}')
        for date in row['dates']:
            if date not in window:
                raise Refused(f'{row["sequence"]}: date {date} is outside the window')
            if date in out[name]:
                raise Refused(f'{row["sequence"]}: date {date} read twice')
            out[name][date] = value
    for name, classes in out.items():
        if sorted(classes) != window:
            raise Refused(f'{name}: {len(classes)} dates read, not the window\'s {len(window)}')
    return out


def summary_flags(out):
    summaries = {name: json.loads((Path(out) / name / 'summary.json').read_text()) for name in SEQUENCES}

    def terminal(name):
        return summaries[name]['terminal'].get('outcome')
    return {'linked_double_refusal': any(terminal(n) == 'double refusal' for n in SEQUENCES if n.startswith('linked')),
            'control_double_refusal': any(terminal(n) == 'double refusal' for n in SEQUENCES if n.startswith('control')),
            'infrastructure_stop': any(terminal(n) == 'infrastructure stop' for n in SEQUENCES),
            'trajectory_difference': any(not all(s['trajectory (H2)'].values()) for s in summaries.values())}
READABLE = 60
CONTROL_FLOOR = 2


def date_classes(rows, sequence):
    out = {}
    for row in rows:
        if row['sequence'] == sequence:
            for date in row['dates']:
                out[date] = row['reader']['class']
    return out


def counts(classes, all_dates):
    d = sum(1 for date in all_dates if classes.get(date) == 'definite')
    u = sum(1 for date in all_dates if classes.get(date) in (None, 'unresolved'))
    return d, u


def pair_outcome(linked, control, credit, all_dates):
    """(outcome, details): outcome is improved / not improved / undecided, or untestable / unreadable."""
    readable = {arm: sum(1 for date in all_dates if classes.get(date) in ('definite', 'overlap', 'clear'))
                for arm, classes in (('linked', linked), ('control', control))}
    adjusted = dict(linked)
    for date, value in (credit or {}).items():
        gain = linked.get(date) in ('overlap', 'clear') and control.get(date) == 'definite'
        if not gain:
            raise ValueError(f'{date}: credit may adjust only a gain (linked not definite, control definite)')
        adjusted[date] = {'none': 'definite', 'unresolved': 'unresolved'}.get(value, value)
    d_l, u_l = counts(adjusted, all_dates)
    d_c, u_c = counts(control, all_dates)
    details = {'D_L': d_l, 'U_L': u_l, 'D_C': d_c, 'U_C': u_c, 'readable': readable}
    if min(readable.values()) < READABLE:
        return 'unreadable', details
    if d_c < CONTROL_FLOOR:
        return 'untestable', details
    if d_l + u_l < d_c:
        return 'improved', details
    if d_l >= d_c + u_c:
        return 'not improved', details
    return 'undecided', details


def verdict(outcomes, flags):
    """§4's precedence over the three pairs' outcomes and the run's harm flags."""
    if flags.get('linked_double_refusal'):
        return 'fail', 'a linked double refusal'
    if flags.get('infrastructure_stop') or flags.get('control_double_refusal') or flags.get('trajectory_difference') or 'unreadable' in outcomes:
        return 'inconclusive', 'invalid or incomplete'
    if any(flags.get(h) for h in ('h1', 'h3', 'h4_double_count', 'h5')):
        return 'fail', 'confirmed harm'
    if 'untestable' in outcomes:
        return 'inconclusive', 'the class did not recur in a control'
    if all(o == 'improved' for o in outcomes):
        return 'pass', 'all three pairs improved'
    if 'not improved' in outcomes:
        return 'fail', 'a pair not improved'
    return 'inconclusive', 'a pair undecided'


H_FINDINGS = {'H3': ('ok', 'grounding error'), 'H4': ('ok', 'double count', 'supported increment', 'unresolved overlap'),
              'H5': ('pass', 'material failure')}
ERROR_TYPES = ('own figure as market', 'company as segment consensus')
H1_EXCESS = 4
H5_EXCESS = 2


def h_key(row):
    return (row['part'], row['sequence'], row['view'], row['judgement'], row.get('fixed_date'))


def h1(summaries):
    """Per pair: model refusals of readers on matched reader-days (judged in both arms), linked minus control; harm at 4 or more."""
    harm = {}
    for n in ('1', '2', '3'):
        linked, control = summaries[f'linked-{n}'], summaries[f'control-{n}']
        days = {(j['view'], j['day']) for j in linked['reader judgements']} & {(j['view'], j['day']) for j in control['reader judgements']}

        def refusals(summary):
            return sum(1 for r in summary['archive judge rows written (dated)'] if r['reader'] and r['refused'] and (r['view'], r['day']) in days)
        harm[n] = refusals(linked) - refusals(control) >= H1_EXCESS
    return harm


def h_flags(h_rows):
    """H3, H4 and H5 from the read H rows."""
    by_key = {h_key(r): r for r in h_rows}
    h3 = False
    for row in h_rows:
        if row['part'] == 'H3' and row['sequence'].startswith('linked') and row['reader']['finding'] == 'grounding error':
            paired = row.get('paired arm in force') or {}
            matched = [r for r in h_rows if r['part'] == 'H3' and r['sequence'] == paired.get('sequence') and r['judgement'] == paired.get('judgement')
                       and r['reader']['finding'] == 'grounding error' and r['reader']['error type'] == row['reader']['error type']]
            if not matched:
                h3 = True
    h4 = any(r['part'] == 'H4' and r['reader']['finding'] == 'double count' for r in h_rows)
    h5 = False
    for n in ('1', '2', '3'):
        def failures(name):
            return sum(1 for r in h_rows if r['part'] == 'H5' and r['sequence'] == name and r['reader']['finding'] == 'material failure')
        if failures(f'linked-{n}') - failures(f'control-{n}') >= H5_EXCESS:
            h5 = True
    return {'h3': h3, 'h4_double_count': h4, 'h5': h5}, by_key


def gain_credit(gain_rows, gain_dates, segment_ends, company_ends=None):
    """{date: adjustment} from the reviews of each gain's two supplying linked answers (rounds 29–33). Every review quotes its rule-B trace
    from the answer (`rule B inputs`, `rule B reasoning`); a material failure must say, for each gain date the answer supplies, whether that
    date's reconciliation rests on it (`reliance by date`), and withdraws that date's credit when it does
    ('none'); a CPU increment is reviewed only on the company (v14) answer: unquantifiable makes the date unresolved (every such date
    marked before the pair's bounds are recomputed once); quantified needs the increment removed and a corrected range equal to the
    company's read range minus it, compared on each gain date with that date's segment range: definite when the segment's low end exceeds
    the corrected high end, clear when the segment's high end is at or below the corrected low end, overlap otherwise."""
    by_judgement = {}
    for r in gain_rows:
        if r['judgement'] in by_judgement:
            raise Refused(f'gain review of judgement {r["judgement"]} given twice')
        by_judgement[r['judgement']] = r
    credit = {}
    for date, judgement_ids in gain_dates.items():
        reviews = [by_judgement.get(j) for j in judgement_ids]
        if any(r is None for r in reviews):
            raise Refused(f'{date}: a supplying answer has no gain review')
        for r in reviews:
            fields = r['reader']
            if not isinstance(fields.get('rule B material failure'), bool) or fields.get('cpu increment') not in ('none', 'quantified', 'unquantifiable'):
                raise Refused(f'gain review of judgement {r["judgement"]} is incomplete')
            inputs = fields.get('rule B inputs')
            if not isinstance(inputs, list) or not inputs or not all(quoted(q, r.get('forecast'), r.get('reasons'), r.get('request')) for q in inputs) \
                    or not isinstance(fields.get('rule B reasoning'), str) or len(fields['rule B reasoning'].strip()) < 40:
                raise Refused(f'gain review of judgement {r["judgement"]}: rule B needs its quoted inputs and the reasoning from them to the finding')
            if fields['rule B material failure']:
                reliance = fields.get('reliance by date')
                supplied = [d for d, ids in gain_dates.items() if r['judgement'] in ids]
                if not isinstance(reliance, dict) or sorted(reliance) != sorted(supplied) or not all(isinstance(v, bool) for v in reliance.values()):
                    raise Refused(f'gain review of judgement {r["judgement"]}: a material failure needs a reliance finding for each gain date it '
                                  f'supplies ({len(supplied)})')
            if fields['cpu increment'] != 'none' and r.get('view') != 'v14':
                raise Refused(f'gain review of judgement {r["judgement"]}: a CPU increment is reviewed only on the total-revenue answer')
            if fields['cpu increment'] == 'quantified':
                increment = fields.get('increment removed')
                original = (company_ends or {}).get(r['judgement'])
                if not finite_range(fields.get('corrected low'), fields.get('corrected high')) or not finite_range(0.0, increment if isinstance(increment, (int, float)) else float('nan')) \
                        or increment <= 0 or original is None or \
                        abs(fields['corrected low'] - (original[0] - increment)) > 0.05 or abs(fields['corrected high'] - (original[1] - increment)) > 0.05:
                    raise Refused(f'gain review of judgement {r["judgement"]}: the corrected range is not the read range minus the increment removed')
        if any(r['reader']['rule B material failure'] and r['reader']['reliance by date'][date] for r in reviews):
            credit[date] = 'none'
        elif any(r['reader']['cpu increment'] == 'unquantifiable' for r in reviews):
            credit[date] = 'unresolved'
        else:
            corrected = [r['reader'] for r in reviews if r['reader']['cpu increment'] == 'quantified']
            if corrected:
                from decimal import Decimal
                low, high = (Decimal(str(v)) for v in segment_ends[date])
                company = next(r for r in reviews if r['reader']['cpu increment'] == 'quantified')
                original, increment = company_ends[company['judgement']], Decimal(str(company['reader']['increment removed']))
                corrected_low = Decimal(str(original[0])) - increment               # computed in decimal, never the transcription
                corrected_high = Decimal(str(original[1])) - increment
                credit[date] = 'definite' if low > corrected_high else ('clear' if high <= corrected_low else 'overlap')
    return credit


def pair_credit(p_read, key, n, linked, control, gain_rows, window):
    rows = [r for r in p_read if key[r['sequence']] == f'linked-{n}']
    supplying = {d: (r['segment judgement'], r['company judgement']) for r in rows for d in r['dates']}
    ends = {d: (r['reader']['segment low'], r['reader']['segment high']) for r in rows for d in r['dates']}
    company_ends = {}
    for r in rows:
        value = (r['reader']['company low'], r['reader']['company high'])
        if r['reader']['class'] != 'unresolved':
            if company_ends.setdefault(r['company judgement'], value) != value:
                raise Refused(f'company judgement {r["company judgement"]} read with two different ranges')
    gain_dates = {d: supplying[d] for d in window if linked[d] in ('overlap', 'clear') and control[d] == 'definite'}
    return gain_credit([g for g in gain_rows if g['pair'] == n], gain_dates, ends, company_ends)


H4_CONTENT = ('view', 'judgement', 'day', 'forecast', 'reasons', 'reference', 'request', 'shown', 'trace', 'paired arm in force', 'cpu_shown')
GAIN_CONTENT = ('pair', 'judgement', 'view', 'day', 'forecast', 'reasons', 'reference', 'request', 'gain dates')


def bind_rows(read, expected, content, label):
    by_read, by_expected = {}, {r['judgement']: r for r in expected}
    for r in read:
        if r['judgement'] in by_read:
            raise Refused(f'{label}: judgement {r["judgement"]} read twice')
        by_read[r['judgement']] = r
    if set(by_read) != set(by_expected):
        raise Refused(f'{label}: {len(set(by_expected) - set(by_read))} expected rows missing, {len(set(by_read) - set(by_expected))} unexpected')
    for j, r in by_read.items():
        if any(r.get(k) != by_expected[j].get(k) for k in content):
            raise Refused(f'{label}: judgement {j} differs from the row the stores give')


def pilot_decision(out, p_path, h4_path, gains_path, key_path, allow_dry=False):
    """The pilot's decision (D708) on pair 1 alone: continue, stop (not improved, undecided, or a harm), fail (a linked double refusal) or
    inconclusive. It never gives the comparison's pass, which needs three pairs. The official decision needs the paid pair-1 summaries
    (`allow_dry` is for the $0 checks only). Order (PAID-DESIGN.md §4): a linked double refusal; validity; coverage; harm; the control
    floor; credited P."""
    import tempfile
    import worksheet
    summaries = {name: json.loads((Path(out) / name / 'summary.json').read_text()) for name in ('linked-1', 'control-1')}
    if not allow_dry and any(s.get('transport') != 'paid' for s in summaries.values()):
        raise Refused('the official pilot decision reads the paid pair-1 summaries')
    if summaries['linked-1']['terminal'].get('outcome') == 'double refusal':
        return report('fail', 'a linked double refusal')
    if any(s['terminal'].get('outcome') != 'complete' for s in summaries.values()) or not all(s['acceptance']['accepted'] for s in summaries.values()):
        return report('inconclusive', 'invalid or incomplete')
    key = json.loads(Path(key_path).read_text())
    if sorted(key.values()) != ['control-1', 'linked-1']:
        raise Refused('the pilot key must name linked-1 and control-1')
    p_read = json.loads(Path(p_path).read_text())
    bind_p(p_read, key, out)
    classes = read_classes(p_read, key, ('linked-1', 'control-1'))
    h4 = [r for r in json.loads(Path(h4_path).read_text()) if r.get('part') == 'H4']
    bind_rows(h4, [r for r in worksheet.h_rows(out, 'linked-1', None) if r['part'] == 'H4'], H4_CONTENT, 'H4')
    for r in h4:
        if r['reader'].get('finding') not in H_FINDINGS['H4'] or \
                not readings_complete(r['reader'], 'finding', H_FINDINGS['H4'], r['forecast'], r['reasons'], r['reference'], r['request']) or \
                not quoted(r['reader'].get('excerpt'), r['forecast'], r['reasons'], r['reference'], r['request']):
            raise Refused(f'H4 judgement {r["judgement"]}: the finding, its reading record or its quoted excerpt is missing')
    window = calendar()
    linked, control = classes['linked-1'], classes['control-1']
    raw, detail = pair_outcome(linked, control, {}, window)
    if raw == 'unreadable':
        return report('inconclusive', 'coverage short', details=detail)
    if any(r['reader']['finding'] == 'double count' for r in h4):
        return report('stop', 'confirmed harm (H4 double count)')
    pair_summaries = {f'{k}-{n}': summaries[f'{k}-1'] for k in ('linked', 'control') for n in ('1', '2', '3')}
    if h1(pair_summaries)['1']:
        return report('stop', 'confirmed harm (H1)')
    if raw == 'untestable':
        return report('inconclusive', 'control-1 under 2 definite dates', details=detail)
    credit = {}
    if raw == 'improved':
        gains = json.loads(Path(gains_path).read_text())
        with tempfile.TemporaryDirectory() as scratch:
            (Path(scratch) / 'p.json').write_text(json.dumps(p_read))
            expected = worksheet.gains(out, str(Path(scratch) / 'p.json'), key_path, str(Path(scratch) / 'g.json'))
        bind_rows(gains, expected, GAIN_CONTENT, 'gain review')
        credit = pair_credit(p_read, key, '1', linked, control, gains, window)
    outcome, detail = pair_outcome(linked, control, credit, window)
    decision = {'improved': ('continue', 'pair 1 improved after the gain review, H1 and H4 clear'),
                'not improved': ('stop', 'pair 1 not improved'), 'undecided': ('stop', 'pair 1 undecided'),
                'untestable': ('inconclusive', 'control-1 under 2 definite dates'), 'unreadable': ('inconclusive', 'coverage short')}[outcome]
    return report(*decision, details=dict(detail, provisional=raw, adjusted=credit))


def report(outcome, reason, details=None):
    print(json.dumps({'decision': [outcome, reason], **({'pair 1': details} if details else {})}, indent=1))
    return outcome, reason


def main(out, p_path, h_path, gains_path, key_path):
    import worksheet
    summaries = {name: json.loads((Path(out) / name / 'summary.json').read_text()) for name in SEQUENCES}
    flags = summary_flags(out)
    if flags['linked_double_refusal']:                          # precedence (1), before any worksheet is required
        print(json.dumps({'verdict': ('fail', 'a linked double refusal')}))
        return 'fail', 'a linked double refusal'
    if flags['infrastructure_stop'] or flags['control_double_refusal'] or flags['trajectory_difference'] or \
            not all(s['acceptance']['accepted'] for s in summaries.values()):
        print(json.dumps({'verdict': ('inconclusive', 'invalid or incomplete'), 'flags': flags,
                          'rejected': [n for n, s in summaries.items() if not s['acceptance']['accepted']]}))
        return 'inconclusive', 'invalid or incomplete'
    key = json.loads(Path(key_path).read_text())
    p_read = json.loads(Path(p_path).read_text())
    bind_p(p_read, key, out)
    classes = read_classes(p_read, key)
    h_rows = json.loads(Path(h_path).read_text())
    regenerated = {h_key(r): r for name in SEQUENCES for r in worksheet.h_rows(out, name, None)}
    expected = set(regenerated)
    read = {}
    for r in h_rows:
        if h_key(r) in read:
            raise Refused(f'{h_key(r)}: read twice')
        read[h_key(r)] = r
    if set(read) != expected:
        raise Refused(f'the H packet holds {len(set(read) & expected)} of the {len(expected)} expected rows '
                      f'({len(set(read) - expected)} unexpected)')
    for k, row in read.items():
        source = regenerated[k]
        texts = (source.get('forecast'), source.get('reasons'), source.get('reference'), source.get('request'))
        if row['reader']['finding'] not in H_FINDINGS[row['part']] or not readings_complete(row['reader'], 'finding', H_FINDINGS[row['part']], *texts) or \
                not quoted(row['reader'].get('excerpt'), *texts):
            raise Refused(f'{k}: the finding, its reading record or its quoted excerpt is missing')
        if row['part'] == 'H3' and row['reader']['finding'] == 'grounding error' and row['reader']['error type'] not in ERROR_TYPES:
            raise Refused(f'{k}: a grounding error needs its type, one of {ERROR_TYPES}')
    derived, _ = h_flags(h_rows)
    flags.update(derived)
    flags['h1'] = any(h1(summaries).values())
    gain_rows = json.loads(Path(gains_path).read_text())
    window = calendar()
    outcomes, details = [], {}
    for n in ('1', '2', '3'):
        linked, control = classes[f'linked-{n}'], classes[f'control-{n}']
        provisional = pair_outcome(linked, control, {}, window)[0]
        credit = {}
        if provisional == 'improved':
            credit = pair_credit(p_read, key, n, linked, control, gain_rows, window)
        outcome, detail = pair_outcome(linked, control, credit, window)
        outcomes.append(outcome)
        details[n] = dict(detail, outcome=outcome, provisional=provisional, adjusted=credit)
    result = verdict(outcomes, flags)
    print(json.dumps({'pairs': details, 'flags': flags, 'verdict': result}, indent=1))
    return result


# ---------- the $0 verdict checks ----------

def synthetic(definite_control=(), definite_linked=(), unresolved_linked=(), total=WINDOW_DATES):
    dates = [f'd{i:02d}' for i in range(total)]
    control = {d: ('definite' if d in definite_control else 'clear') for d in dates}
    linked = {d: ('definite' if d in definite_linked else 'unresolved' if d in unresolved_linked else 'clear') for d in dates}
    return dates, linked, control


def checks():
    results = {}
    dates, linked, control = synthetic(definite_control=('d01', 'd02'))
    results['control 2 definite, linked none: improved'] = pair_outcome(linked, control, {}, dates)[0] == 'improved'
    results['round 25: both gains reviewed and withdrawn: a tie, not improved'] = \
        pair_outcome(linked, control, {'d01': 'none', 'd02': 'none'}, dates)[0] == 'not improved'
    results['round 25: one gain withdrawn alone still improved (so every gain must be reviewed)'] = \
        pair_outcome(linked, control, {'d01': 'none'}, dates)[0] == 'improved'
    try:
        pair_outcome(linked, control, {'d05': 'none'}, dates)       # d05 is clear in both arms: a shared error moves no date
        results['round 25: a shared error on a clear date cannot be adjusted'] = False
    except ValueError:
        results['round 25: a shared error on a clear date cannot be adjusted'] = True
    results['round 26: both gains on unquantifiable CPU increments: undecided'] = \
        pair_outcome(linked, control, {'d01': 'unresolved', 'd02': 'unresolved'}, dates)[0] == 'undecided'
    dates, linked, control = synthetic(definite_control=('d01',))
    results['a control with one definite date: untestable'] = pair_outcome(linked, control, {}, dates)[0] == 'untestable'
    dates, linked, control = synthetic(definite_control=('d01', 'd02', 'd03'), unresolved_linked=tuple(f'd{i:02d}' for i in range(10, 24)))
    results['14 unresolved linked dates: unreadable'] = pair_outcome(linked, control, {}, dates)[0] == 'unreadable'
    dates, linked, control = synthetic(definite_control=('d01', 'd02', 'd03', 'd04', 'd05'), unresolved_linked=tuple(f'd{i:02d}' for i in range(10, 23)))
    results['round 24: 5 control definite, 13 linked unresolved: undecided'] = pair_outcome(linked, control, {}, dates)[0] == 'undecided'
    dates, linked, control = synthetic(definite_control=('d01', 'd02'), definite_linked=('d03', 'd04'))
    results['linked as many definite dates as the control: not improved'] = pair_outcome(linked, control, {}, dates)[0] == 'not improved'
    results['precedence: a linked double refusal fails even with every pair improved'] = \
        verdict(['improved'] * 3, {'linked_double_refusal': True}) == ('fail', 'a linked double refusal')
    results['precedence: an infrastructure stop is inconclusive'] = verdict(['improved'] * 3, {'infrastructure_stop': True})[0] == 'inconclusive'
    results['precedence: confirmed harm fails'] = verdict(['improved'] * 3, {'h4_double_count': True}) == ('fail', 'confirmed harm')
    results['precedence: an undecided pair is inconclusive'] = verdict(['improved', 'improved', 'undecided'], {})[0] == 'inconclusive'
    results['precedence: all improved passes'] = verdict(['improved'] * 3, {})[0] == 'pass'
    print(json.dumps(results, indent=1))
    return all(results.values())


if __name__ == '__main__':
    if sys.argv[1:] == ['--checks']:
        sys.exit(0 if checks() else 1)
    if sys.argv[1] == '--pilot':
        pilot_decision(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        sys.exit(0)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
