"""Aggregate the analyst readers' verdicts (verdicts/*.json) and set them beside the frozen gold: each statement's reader
worth against its gold class (core / supporting / optional / not kept / outside the gold), field errors by field, the
readers' misses against the gold's core and supporting entries, questions, grades. The reader never saw the gold.

    python3 aggregate.py
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_gold as sg  # noqa: E402


def gold_class(a, quote):
    g = [it for it in a['items'] if sg.same(it['span'], quote)]
    if g:
        return g[0]['weight']
    nk = [n for n in a['not_kept'] if sg.same(n['span'], quote)]
    if nk:
        return 'optional' if all(n['weight'] != 'not_kept' for n in nk) else 'not_kept'
    return 'outside gold'


def main():
    dev = json.load(open(HERE.parent / 'golden-v3/golden-v3-signed.json'))['articles']
    test = json.load(open(HERE.parent / 'test-set/golden-test-signed.json'))['articles']
    gold = {a['input_id']: a for a in dev + test}
    cross = collections.Counter()
    fields = collections.Counter()
    field_examples = collections.defaultdict(list)
    grades = collections.Counter()
    q = collections.Counter()
    missed = []
    gold_missed_by_output = []
    n_statements = 0
    files = sorted((HERE / 'verdicts').glob('*.json'))
    for f in files:
        v = json.loads(f.read_text())
        packet = json.loads((HERE / 'packets' / f.name).read_text())
        a = gold[packet['input_id']]
        by_id = {e['id']: e for e in (packet['output'] or {}).get('statements', [])}
        grades[v.get('grade')] += 1
        for s in v.get('statements', []):
            e = by_id.get(s['id'])
            if not e:
                continue
            n_statements += 1
            cls = gold_class(a, e['quote'])
            cross[(s.get('worth'), cls)] += 1
            for k in ('one_line_ok', 'who_ok', 'day_ok', 'tier_ok'):
                if s.get(k) is False:
                    fields[k] += 1
                    note = s.get({'one_line_ok': 'one_line_problem', 'day_ok': 'day_note', 'tier_ok': 'tier_note'}.get(k, 'worth_reason'))
                    field_examples[k].append((packet['input_id'], s['id'], e.get('original_day'), e['quote'][:120], note))
            if s.get('duplicate_of'):
                fields['duplicate'] += 1
        for m in v.get('missed', []):
            cls = gold_class(a, m['quote'])
            missed.append((m.get('importance'), cls, packet['input_id'], m['quote'][:160], m.get('why', '')[:160]))
        kept_quotes = [e['quote'] for e in by_id.values()]
        for it in a['items']:
            if it['weight'] in ('core', 'supporting') and not any(sg.same(it['span'], qq) for qq in kept_quotes):
                flagged = any(sg.same(it['span'], m['quote']) for m in v.get('missed', []))
                gold_missed_by_output.append((it['weight'], packet['input_id'], it['span'][:150], 'reader also flagged' if flagged else 'reader did not flag'))
        for qq in v.get('questions', []):
            q['sensible' if qq.get('sensible') else 'not sensible'] += 1
        for mq in v.get('missing_questions', []):
            q[f'missing question ({mq.get("importance")})'] += 1
    out = {'packets read': len(files), 'statements judged': n_statements, 'grades': dict(grades),
           'reader worth x gold class': {f'{w} | {c}': n for (w, c), n in sorted(cross.items(), key=lambda x: (str(x[0][0]), str(x[0][1])))},
           'field errors': dict(fields), 'questions': dict(q),
           'reader misses by importance x gold class': {f'{i} | {c}': n for (i, c), n in collections.Counter((m[0], m[1]) for m in missed).most_common()}}
    print(json.dumps(out, ensure_ascii=False, indent=1))
    print('\n## field examples')
    for k, xs in field_examples.items():
        print('#', k, len(xs))
        for x in xs:
            print('  ', x)
    print('\n## reader misses')
    for m in sorted(missed, key=lambda m: str(m[0])):
        print('  ', m)
    print('\n## gold core/supporting not in this draw')
    for g in gold_missed_by_output:
        print('  ', g)
    (HERE / 'aggregate.json').write_text(json.dumps({'summary': out, 'field_examples': field_examples, 'missed': missed,
                                                      'gold_missed_by_output': gold_missed_by_output}, ensure_ascii=False, indent=1) + '\n')


if __name__ == '__main__':
    main()
