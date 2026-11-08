"""Close-out scores for the Step 2 forward run (no model calls).

Line 1, search: over records with a known same-statement earlier counterpart (reference v2 plus the agreed v3 labels), whether a group
holding a counterpart is among the record's candidates; reported apart: whether that group's original record (what Jev compares) is
itself a known counterpart. Recall over known labelled counterparts only, not over all real repeats.
Line 2, merges: every repeat judged by two blind readers (merge-answer-*). Every pair either reader rejected went to a third reader
(merge-third-answer.json) with three verdicts: acceptable, overlap (imperfect but not misleading to a reader of the record's own text)
and wrong (misleading). Clear wrong merges are the third reader's 'wrong'.
Line 3, structure: every record placed with its own text; the reader test is scored by score_reader_test.py.

Usage: score_final.py <validation folder> <forward run folder>"""
import collections, glob, json, sys
from pathlib import Path


def load(pattern):
    rows = {}
    for path in sorted(glob.glob(pattern)):
        for row in json.loads(Path(path).read_text()):
            rows[row['id']] = row
    return rows


def main():
    folder, run = Path(sys.argv[1]), Path(sys.argv[2])
    relation = {(r['earlier'], r['later']): r['relation'] for r in json.loads((folder / 'reference-v2.json').read_text())}
    e, f = load(str(folder / 'v3-answer-E-*.json')), load(str(folder / 'v3-answer-F-*.json'))
    for vid, pair in json.loads((folder / 'v3-key.json').read_text()).items():
        if e[vid]['relation'] == f[vid]['relation']:
            relation[(pair['earlier'], pair['later'])] = e[vid]['relation']
    decisions = json.loads((run / 'decisions.json').read_text())
    placement = json.loads((run / 'library.json').read_text())['placement']
    groups = json.loads((run / 'library.json').read_text())['groups']
    true_same = collections.defaultdict(set)
    for (earlier, later), rel in relation.items():
        if rel == 'same_statement':
            true_same[later].add(earlier)
    judged = found = original_known = 0
    for d in decisions:
        counterparts = true_same.get(d['id'], set())
        if not counterparts:
            continue
        judged += 1
        target_groups = {placement[c] for c in counterparts if c in placement}
        hit = target_groups & set(d['candidates'])
        found += bool(hit)
        original_known += bool({g for g in hit if groups[g]['original']['id'] in counterparts})
    print(f'line 1, search: records with a known same-statement counterpart {judged}; a group holding one among the candidates {found} '
          f'({found / judged:.1%}); of those, the group original itself a known counterpart {original_known}')
    print(f'placed {len(placement)} of {len(decisions)} records; refused {sum("refused" in d for d in decisions)}')
    key = json.loads((run / 'merge-key.json').read_text())
    a, b = load(str(run / 'merge-answer-MA-*.json')), load(str(run / 'merge-answer-MB-*.json'))
    third = load(str(run / 'merge-third-answer*.json'))
    verdict, disputed = {}, []
    for mid in key:
        if a[mid]['merge_acceptable'] and b[mid]['merge_acceptable']:
            verdict[mid] = 'acceptable'
        elif mid in third:
            verdict[mid] = third[mid]['verdict']
        else:
            disputed.append(mid)
    counts = collections.Counter(verdict.values())
    wrong = [m for m, v in verdict.items() if v == 'wrong']
    print(f'line 2, merges: {len(key)}; both readers accept {sum(1 for m in key if a[m]["merge_acceptable"] and b[m]["merge_acceptable"])}; '
          f'sent to the third reader {len(third)}; unjudged {len(disputed)}; verdicts {dict(counts)}; clear wrong {len(wrong)} = {len(wrong) / len(key):.1%}')
    print('  relation, reader A:', dict(collections.Counter(a[m]['relation'] for m in key)))
    (run / 'merge-disputed.json').write_text(json.dumps(disputed))
    (run / 'merge-wrong.json').write_text(json.dumps([{**key[m], 'id': m} for m in wrong], indent=1))
    if disputed:   # a share over all merges is not a verdict while any pair is unjudged
        raise SystemExit(f'line 2 has no verdict: {len(disputed)} pairs unjudged (send them to the third reader)')


if __name__ == '__main__':
    main()
