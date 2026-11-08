"""Carry the Step 2 reference labels onto a new Step 1 run's records (no model calls).

The labels (reference-v2.json and the agreed v3 labels) name records of the K6b dev run ('<sequence>:<local id>'). A record of the new
run stands for an old record when both come from the same article (the same input id) and share a verbatim passage of at least 40 characters, or
one passage contains the other; when several new records qualify, the one sharing the most passage characters is taken, and a new record
stands for at most one old record per pair. Pairs whose two records both map are written with the new ids; the rest are reported
unmapped. The mapping is an identity rule on text, not a judgement of meaning.

Usage: map_reference.py <validation folder> <old step1 trace> <new step1 trace> <output folder>"""
import json, shutil, sqlite3, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'step2'))
import run_forward  # noqa: E402


def overlap(a, b):
    best = 0
    for p in a:
        for q in b:
            if p in q or q in p:
                best = max(best, min(len(p), len(q)))
            else:
                for size in (200, 120, 80, 40):
                    if any(p[i:i + size] in q for i in range(0, max(1, len(p) - size + 1), 20)):
                        best = max(best, size)
                        break
    return best


def records(trace):
    articles, _questions, _opened = run_forward.step1_records(trace)
    return {r['id']: r for a in articles for r in a}


def main():
    folder, old_trace, new_trace, out = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4])
    old, new = records(old_trace), records(new_trace)
    by_article = {}
    for rid, r in new.items():
        by_article.setdefault(r['input_id'], []).append(r)
    mapping = {}
    for rid, r in old.items():
        scored = [(overlap(r['passages'], n['passages']), n['id']) for n in by_article.get(r['input_id'], [])]
        scored = [s for s in scored if s[0] >= 40]
        if scored:
            mapping[rid] = max(scored)[1]
    out.mkdir(parents=True, exist_ok=True)
    reference = json.loads((folder / 'reference-v2.json').read_text())
    mapped = [dict(r, earlier=mapping[r['earlier']], later=mapping[r['later']]) for r in reference
              if r['earlier'] in mapping and r['later'] in mapping and mapping[r['earlier']] != mapping[r['later']]]
    (out / 'reference-v2.json').write_text(json.dumps(mapped, indent=1))
    key = json.loads((folder / 'v3-key.json').read_text())
    (out / 'v3-key.json').write_text(json.dumps({v: dict(p, earlier=mapping[p['earlier']], later=mapping[p['later']]) for v, p in key.items()
                                                 if p['earlier'] in mapping and p['later'] in mapping}, indent=1))
    for path in folder.glob('v3-answer-[EF]-*.json'):
        shutil.copy(path, out / path.name)
    (out / 'mapping.json').write_text(json.dumps(mapping, indent=1))
    same = [r for r in reference if r['relation'] == 'same_statement']
    same_mapped = [r for r in mapped if r['relation'] == 'same_statement']
    print(f'old records {len(old)}, mapped {len(mapping)} ({len(mapping) / len(old):.0%}); reference pairs {len(reference)}, mapped {len(mapped)}; '
          f'same-statement pairs {len(same)}, mapped {len(same_mapped)}')


if __name__ == '__main__':
    main()
