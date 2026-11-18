"""D505's gap on the fortnight, the readers' part joined to the key ($0; D564). It judges nothing.

  python3 tally_figures.py <key folder>
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')


def lines_of(path):
    out = []
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        if line.strip().startswith('{'):
            out.append(json.loads(line))
    return out


def main(keys):
    key = json.loads((Path(keys) / 'key-figures-reading.json').read_text())
    packets = [json.loads((HERE / f'packet-figures-{n}.json').read_text()) for n in (1, 2)]
    statements = {s['ref']: s for s in packets[0]['statements']}
    rows = {f: {r['question']: r for n in (1, 2) for r in lines_of(HERE / f'{f}-figures-{n}.jsonl')} for f in FAMILIES}
    questions = [q['ref'] for p in packets for q in p['questions']]
    for f in FAMILIES:
        print(f'{f}: {len(rows[f])} of {len(questions)} questions answered')
    print()
    for ref in sorted(questions, key=lambda r: int(r[1:])):
        named = {f: {s['ref']: s for s in rows[f].get(ref, {}).get('statements', [])} for f in FAMILIES}
        both = sorted(set(named['codex']) & set(named['claude']), key=lambda r: int(r[1:]))
        either = sorted(set(named['codex']) | set(named['claude']), key=lambda r: int(r[1:]))
        print(f"{ref} ({key['questions'][ref]}): named by both {len(both)}, by either {len(either)}")
        for s in either:
            effects = {f: named[f].get(s, {}).get('effect', '-') for f in FAMILIES}
            source = key['statements'][s][0]
            flag = '' if source == 'group' else f'  <{source}>'
            print(f"    {s} codex {effects['codex']:<12} claude {effects['claude']:<12}{flag} | {statements[s]['statement'][:120]}")
    print('\nCONTROLS')
    positive = [s for s, src in key['statements'].items() if src[0] == 'positive control']
    control_q = next(r for r, v in key['questions'].items() if 'positive control' in v)
    for f in FAMILIES:
        named = {s['ref']: s['effect'] for s in rows[f].get(control_q, {}).get('statements', [])}
        print(f"  positive ({control_q}, {len(positive)} facts): {f} named {sum(s in named for s in positive)}, of them 'answer' {sum(named.get(s) == 'answer' for s in positive)}")
    negative = next((s for s, src in key['statements'].items() if str(src[0]).startswith('negative')), None)
    if negative:
        target = key['negative']['question']
        for f in FAMILIES:
            named = {s['ref'] for s in rows[f].get(target, {}).get('statements', [])}
            print(f"  negative ({negative}, already shown to {target}): {f} named it as absent: {negative in named}")
    answer_both = [(ref, s) for ref in questions for s in rows['codex'].get(ref, {}).get('statements', [])
                   if s['effect'] == 'answer' and any(t['ref'] == s['ref'] and t['effect'] == 'answer' for t in rows['claude'].get(ref, {}).get('statements', []))]
    print('\npairs both families say would move the answer:', [(ref, key['questions'][ref], s['ref']) for ref, s in answer_both])


if __name__ == '__main__':
    main(sys.argv[1])
