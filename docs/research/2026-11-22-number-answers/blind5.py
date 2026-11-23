"""The D749 $0 writer test (SMALL-DESIGN.md §5 [D749]): cases S, E and P-v8 built from the repaired request (judging-v13s.txt, the
"decide the side before you size it" sentence), a fresh Claude and Codex writer each, readers under the D747 definitions, and two
reader controls carried from the targeted test with the request they were written for: U05 (E Codex, an invented 10% cut; expected
not supported) and U02 (S Claude, a floor above its own total; expected the part-above-whole defect upheld).

  python3 blind5.py build <out>      # the three requests and writer prompts (refuses an existing folder)
  python3 blind5.py check <out>      # every first answer through the schema, from_answer, check and publish_decision
  python3 blind5.py packets <out>    # 6 replies + 2 controls, shuffled X01–X08; key beside
  python3 blind5.py tally <out>      # the registered lines, after readings, recorded reasons and any adjudication
"""
import hashlib
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import blind4 as b4  # noqa: E402
from blind_rules import format_material  # noqa: E402

CASES = b4.CASES                                                     # ('S', 'E', 'P-v8')
BLIND4 = HERE.parents[2] / 'poc/data/judging-v13s-blind4-2026-11-23'
CONTROLS = {'K-invented-cut': ('E', 'codex'), 'K-impossible-floor': ('S', 'claude')}     # blind4 U05 and U02, unchanged
FLOOR_DEFECT = ('part above or added into its whole', ('F11', 'F12', 'F15'))
READER_BRIEF = b4.REREAD_BRIEF.replace('re-read under the comparison ruling, D747', 'writer test, D749')
REQUEST_SHA256 = 'ac707fa96890cee1f69dcf84e6c5242ec014b00b502214ece84b1318252a9859'   # judging-v13s.txt as registered (council 64)
if 'D749' not in READER_BRIEF:
    raise SystemExit('the D749 reader brief is not built')


def build(out):
    request = (HERE / 'judging-v13s.txt').read_bytes()
    if hashlib.sha256(request).hexdigest() != REQUEST_SHA256:
        raise SystemExit('judging-v13s.txt is not the registered D749 request')
    b4.build(out)
    for name in CASES:
        if (out / name / 'system.txt').read_bytes() != request:
            raise SystemExit(f'{name}: the built system text is not the registered D749 request')


def check(out):
    b4.check(out)


def packets(out):
    rows = json.loads((out / 'CHECKED.json').read_text())
    unreadable = [f'{r["case"]}/{r["writer"]} ({r["stage"]})' for r in rows if r['stage'] != 'checked']
    if unreadable:      # a reply refused before the checks has no answer to read; the run has already failed (registered)
        print('FAIL: first replies refused before the code checks:', ', '.join(unreadable), '- readers are not needed for the verdict')
    items = [{'label': f'fresh {r["case"]}/{r["writer"]}', 'case': r['case'], 'writer': r['writer'],
              'answer': str(out / r['case'] / 'answers' / f'{r["writer"]}.json'), 'case_dir': str(out / r['case'])}
             for r in rows if r['stage'] == 'checked']
    for name, (case, writer) in CONTROLS.items():
        items.append({'label': name, 'case': case, 'writer': name, 'answer': str(BLIND4 / case / 'answers' / f'{writer}.json'),
                      'case_dir': str(BLIND4 / case)})
    order = list(range(len(items)))
    random.Random(hashlib.sha256(b'D749 ' + (out / 'CHECKED.json').read_bytes()).hexdigest()).shuffle(order)
    folder = out / 'reader-packets'
    folder.mkdir(exist_ok=False)
    key = {}
    for n, i in enumerate(order, 1):
        item = items[i]
        case_dir = Path(item['case_dir'])
        pid = f'X{n:02d}'
        key[pid] = item
        (folder / f'{pid}.md').write_text('\n'.join([READER_BRIEF, format_material(case_dir), '', '# The request as the writer saw it', '',
                                                     (case_dir / 'user.txt').read_text(), '', '# The answer', '',
                                                     b4._display(item['answer']), '']))
        (folder / f'{pid}.codex-prompt.txt').write_text(
            f'Read the file {folder / f"{pid}.md"} and nothing else (no other file, no web). Follow the brief at its top: read the request '
            'and the answer it contains, and return only the JSON the brief asks for, with no text before or after it.\n')
    (out / 'reader-key.json').write_text(json.dumps(key, indent=1))
    print(f'{len(order)} packets in {folder}; key in reader-key.json (keep from readers)')


def _keys(reading, floor):
    """A reading's defect keys; on the floor control, every part-above-whole mark naming F12 is one key (council 64)."""
    keys = set()
    for d in reading.get('defects', []):
        k = b4._defect_key(d)
        keys.add((FLOOR_DEFECT[0], ('F12',)) if floor and k[0] == FLOOR_DEFECT[0] and 'F12' in k[1] else k)
    return keys


def _decisions(reading, floor):
    found = {}
    for d in reading.get('defects', []):
        k = b4._defect_key(d)
        k = (FLOOR_DEFECT[0], ('F12',)) if floor and k[0] == FLOOR_DEFECT[0] and 'F12' in k[1] else k
        if found.get(k) != 'uphold':          # a key both listed as upheld and as rejected counts as upheld only if upheld once
            found[k] = d.get('decision')
    return found


def _vote(value, where):
    if value not in ('yes', 'no'):
        raise SystemExit(f'{where}: no valid vote ({value!r})')
    return value


def tally(out):
    """[D749] Scored as registered (SMALL-DESIGN.md §5 [D749], with council 64's changes).
    Fail: a fresh reply refused or held by the code; a fresh P-v8 reply that is not a forecast; a settled no on a fresh reply; a settled
    defect on a fresh reply; K-invented-cut not settled no; K-impossible-floor's floor defect rejected by both adjudicators or marked by
    neither reader. Inconclusive: a support split, a defect split on a fresh reply, or a floor split left after adjudication. A settled
    vote is final only after Claude records its two reasons as compatible (`reasons.json`)."""
    checked = {(r['case'], r['writer']): r for r in json.loads((out / 'CHECKED.json').read_text())}
    refused = [f'{k[0]}/{k[1]} ({v["stage"]}, {v.get("decision", "-")})' for k, v in checked.items()
               if v['stage'] != 'checked' or v.get('decision') != 'publish']
    if refused:                                 # decided before any reading is needed (council 64)
        (out / 'TALLY.json').write_text(json.dumps({'verdict': 'fail', 'refused_or_held': refused}, indent=1))
        print('fresh replies refused or held:', refused)
        print('VERDICT: fail')
        return
    key = json.loads((out / 'reader-key.json').read_text())
    expected_labels = {f'fresh {c}/{w}' for c in CASES for w in ('claude', 'codex')} | set(CONTROLS)
    if {i['label'] for i in key.values()} != expected_labels or len(key) != len(expected_labels):
        raise SystemExit(f'the key does not hold exactly the registered answers: {sorted(i["label"] for i in key.values())}')
    reasons_path = out / 'reasons.json'
    reasons = json.loads(reasons_path.read_text()) if reasons_path.exists() else {}
    lines, need, fails, splits, settled_defects, split_defects = [], [], [], [], [], []
    floor_state = None
    for pid, item in sorted(key.items()):
        floor = item['label'] == 'K-impossible-floor'
        fresh = item['label'].startswith('fresh ')
        answer = json.loads(b4._display(item['answer']))
        if fresh and item['case'] == 'P-v8':
            for a in answer['answers']:
                if a['shape'] != 'forecast':
                    fails.append(f'{pid} {item["label"]}: {a["view_id"]} is {a["shape"]}, not a forecast')
        first = [b4._reading(out / 'reader-packets' / f'{pid}.{w}.json') for w in ('codex', 'claude')]
        adjudicated = [out / 'adjudication' / f'{pid}.{w}.json' for w in ('codex', 'claude')]
        adj = [b4._reading(p) for p in adjudicated] if all(p.exists() for p in adjudicated) else None
        record = reasons.get(pid, {})
        marks = [_keys(r, floor) for r in first]
        disputed = (marks[0] | marks[1]) - (marks[0] & marks[1])
        defect_state = {d: 'settled' for d in marks[0] & marks[1]}
        if disputed and adj is None:
            need.append(f'{pid} (a defect marked by one reader)')
        elif disputed:
            decisions = [_decisions(x, floor) for x in adj]
            for d in disputed:
                pair = [decisions[0].get(d), decisions[1].get(d)]
                if None in pair:                # an adjudicator left this defect undecided: pending, not a split (council 66)
                    need.append(f'{pid} (an adjudicator did not decide {d[0]} {list(d[1])})')
                    continue
                defect_state[d] = 'settled' if pair == ['uphold', 'uphold'] else 'rejected' if pair == ['reject', 'reject'] else 'split'
        for d, state in defect_state.items():
            row = [pid, item['label'], d[0], list(d[1]), state]
            (settled_defects if state == 'settled' else split_defects if state == 'split' else []).append(row)
            if fresh and state == 'settled':
                fails.append(f'{pid} {item["label"]}: settled defect {d[0]} {list(d[1])}')
            if fresh and state == 'split':
                splits.append(f'{pid} {item["label"]}: defect split {d[0]} {list(d[1])}')
        if floor:
            floor_state = defect_state.get((FLOOR_DEFECT[0], ('F12',)), 'missed')
        for a in answer['answers']:
            view = a['view_id']
            votes = [_vote(r['members'].get(view, {}).get('supported'), f'{pid} first reading') for r in first]
            premise_needed = fresh and item['case'] in ('S', 'E')     # council 66: the decisive premise's support must be named
            if premise_needed and record.get('first') == 'compatible' and not record.get('premise'):
                need.append(f'{pid} (the decisive premise and what supports it are not recorded)')
                continue
            if votes[0] == votes[1] and record.get('first') == 'compatible':
                value = votes[0]
            elif votes[0] == votes[1] and 'first' not in record:
                need.append(f'{pid} (reasons not yet recorded)')
                continue
            elif adj is None:
                need.append(f'{pid} (support)')
                continue
            else:
                second = [_vote(x['members'].get(view, {}).get('supported'), f'{pid} adjudication') for x in adj]
                votes += second
                if second[0] != second[1]:
                    value = 'split'
                elif 'adjudicated' not in record:
                    need.append(f'{pid} (adjudicated reasons not yet recorded)')
                    continue
                elif premise_needed and record['adjudicated'] == 'compatible' and not record.get('adjudicated_premise'):
                    need.append(f'{pid} (the adjudicators\' decisive premise is not recorded)')
                    continue
                else:
                    value = second[0] if record['adjudicated'] == 'compatible' else 'split'
            if item['label'] == 'K-invented-cut':
                rule, ok = 'control expects not supported', value == 'no'
            elif floor:
                rule, ok = 'support not scored; the floor defect is', True
            elif item['case'] == 'P-v8':
                rule, ok = 'a supported forecast', a['shape'] == 'forecast' and value == 'yes'
            else:
                rule, ok = 'a supported forecast or a justified unresolved answer', value == 'yes'
            if not ok:                      # the invented-cut control fails unless settled no, a split included (council 66)
                bucket = fails if value != 'split' or item['label'] == 'K-invented-cut' else splits
                bucket.append(f'{pid} {item["label"]}: {view} settled={value} [{rule}]')
            lines.append(f'{pid} {item["label"]:22} {view} {a["shape"]:10} settled={value:6} votes={votes} [{rule}] {"ok" if ok else "MISS"}')
    if need:
        print('not final; needed:', ' | '.join(sorted(set(need))))
        return
    if floor_state in ('missed', 'rejected'):
        fails.append(f'K-impossible-floor: the floor defect was {floor_state}')
    elif floor_state == 'split':
        splits.append('K-impossible-floor: the floor defect split')
    verdict = 'fail' if fails else 'inconclusive' if splits else 'pass'
    result = {'verdict': verdict, 'fails': fails, 'splits': splits, 'lines': lines, 'settled_defects': settled_defects,
              'split_defects': split_defects, 'floor_control': floor_state}
    (out / 'TALLY.json').write_text(json.dumps(result, indent=1, ensure_ascii=False))
    print('\n'.join(lines))
    print('settled defects:', settled_defects)
    print('split defects:', split_defects)
    print('floor control:', floor_state)
    print('fails:', fails)
    print('splits:', splits)
    print('VERDICT:', verdict)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) == 3 else ''
    target = Path(sys.argv[2]).resolve() if len(sys.argv) == 3 else None
    {'build': build, 'check': check, 'packets': packets, 'tally': tally}.get(
        cmd, lambda _: (_ for _ in ()).throw(SystemExit(__doc__)))(target)
