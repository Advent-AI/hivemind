"""Code counts for design-seq.md (S1–S6) on the sequential run (arm SEQ-v53R-d1..3 with ledger-SEQ-v53R-d<d>.json; control REF-v53-d1..3
with ledger-REF-v53-d<d>.json from the same opening rule), and the blind packets: blind-seq/opened.json (every question either arm opened,
labels apart) and blind-seq/links.json (40 arm links).

    python3 score_seq.py counts | packets [seed]
"""
import collections
import json
import random
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score_ref as sr  # noqa: E402

fs, sg = sr.fs, sr.sg
ARM, CONTROL = 'SEQ-v53R', 'REF-v53'
if len(sys.argv) > 2 and sys.argv[2].startswith('SEQ-'):      # python3 score_seq.py counts SEQ-v67 [seed]: another arm tag (its ledger files and answers)
    ARM = sys.argv.pop(2)
articles = {a['input_id']: a for a in sr.articles}


def ledger(tag, draw):
    return json.loads((HERE / f'ledger-{tag}-d{draw}.json').read_text())


def shown_for(tag, draw, iid):
    day = articles[iid]['publication_day']
    return [q for q in ledger(tag, draw)['questions'] if q['opened_day'] < day]


def counts():
    fs.PREFIX = 'REF'
    control_rows = fs.per_article('v53', sr.articles)
    fs.PREFIX = 'SEQ'
    arm_rows = fs.per_article(ARM.split('-', 1)[1], sr.articles)
    print('== S1 gold-rejected kept per draw (D250 unit), all 118')
    for name, rows in (('control', control_rows), ('arm', arm_rows)):
        print(f'   {name}:', [sum(r['nk_hits'][d] for r in rows.values()) for d in range(3)], '| statements', [sum(r['stmts'][d] for r in rows.values()) for d in range(3)])
    print('   paired, arm minus control:', fs.paired(arm_rows, control_rows, 'not-kept kept (mean of draws)'))
    print('== S5 core every draw / supporting >=2 draws (counting aid)')
    for name, rows in (('control', control_rows), ('arm', arm_rows)):
        t = fs.totals(rows)
        print(f'   {name}: core every {t["core every draw"]}/{t["core total"]} per-draw {t["core per draw"]} never {t["core never"]} | supp>=2 {t["supporting >=2 draws"]}/{t["supporting total"]} per-draw {t["supporting per draw"]}')
    print('== S2/S3 questions opened over the 14 days and candidates before the opening rule, per draw')
    for name, tag in (('control', CONTROL), ('arm', ARM)):
        for d in (1, 2, 3):
            L = ledger(tag, d)
            print(f'   {name} d{d}: candidates {sum(x["candidates"] for x in L["days"])}, opened {len(L["questions"])}')
    print('== S4 links (arm): statements linked to an open question of its own ledger, and the gold class of linked vs unlinked statements')
    tab = collections.Counter()
    for d in (1, 2, 3):
        for iid, a in articles.items():
            ids = {q['id'] for q in shown_for(ARM, d, iid)}
            if not ids:
                continue
            data = sr.raw(f'{ARM}-d{d}', iid) or {}
            kept = [i for i in a['items'] if i['weight'] in ('core', 'supporting')]
            for e in data.get('evidence', []):
                linked = any(l in ids for l in e.get('links', []))
                g = ('core/supp' if any(sg.same_matter(i, e) for i in kept) else 'not_kept' if any(sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'not_kept')
                     else 'optional/unlisted')
                tab[('linked' if linked else 'unlinked', g)] += 1
    for k in ('linked', 'unlinked'):
        row = {g: tab[(k, g)] for g in ('core/supp', 'not_kept', 'optional/unlisted')}
        n = sum(row.values())
        print(f'   {k}: {row} | not_kept share {row["not_kept"] / max(n, 1):.0%}')
    print('== S6 stability: statements per draw sd; candidate mentions recurring in all three draws')
    for name, rows, tag in (('control', control_rows, CONTROL), ('arm', arm_rows, ARM)):
        sd = statistics.pstdev([sum(r['stmts'][d] for r in rows.values()) for d in range(3)])
        stable = unstable = 0
        for iid in articles:
            sets = [[(c.get('question', '') + ' ' + c.get('looks_at', '')) for c in (sr.raw(f'{tag}-d{d}', iid) or {}).get('candidates', [])] for d in (1, 2, 3)]
            for i, s in enumerate(sets):
                for q in s:
                    if all(any(sr.same_question(q, x) for x in o) for j, o in enumerate(sets) if j != i):
                        stable += 1
                    else:
                        unstable += 1
        print(f'   {name}: statements sd {sd:.1f}; candidate mentions recurring {stable}/{stable + unstable}')


def packets(seed):
    rng = random.Random(seed)
    folder = HERE / ('blind-seq' if ARM == 'SEQ-v53R' else f'blind-{ARM.lower()}')
    folder.mkdir(exist_ok=True)
    opened, key = [], {}
    for name, tag in (('control', CONTROL), ('arm', ARM)):
        for d in (1, 2, 3):
            for q in ledger(tag, d)['questions']:
                oid = f'Q{len(opened) + 1:03d}'
                a = articles[q['from']]
                key[oid] = {'arm': name, 'draw': d, 'input_id': q['from'], 'id': q['id']}
                opened.append({'id': oid, 'article': a['title'], 'day': a['publication_day'], 'question': q['question'], 'looks_at': q['looks_at'],
                               'gold_must_open': [g['gist'] for g in a['questions'].get('must_open', [])],
                               'gold_may_open': [g['gist'] for g in a['questions'].get('may_open', [])],
                               'gold_must_not': [g['gist'] for g in a['questions'].get('must_not', [])],
                               'earlier_questions_in_this_run': [f'{x["id"]}: {x["question"]}' for x in ledger(tag, d)['questions'] if x['opened_day'] < q['opened_day']]})
    rng.shuffle(opened)
    (folder / 'opened.json').write_text(json.dumps(opened, ensure_ascii=False, indent=1))
    (folder / 'opened.key.json').write_text(json.dumps(key, ensure_ascii=False, indent=1))
    links = []
    for d in (1, 2, 3):
        for iid, a in articles.items():
            qs = {q['id']: q for q in shown_for(ARM, d, iid)}
            for e in (sr.raw(f'{ARM}-d{d}', iid) or {}).get('evidence', []):
                for l in e.get('links', []):
                    if l in qs:
                        links.append({'article': a['title'], 'day': a['publication_day'], 'quote': e['quote'], 'one_line': e.get('one_line', ''),
                                      'question': qs[l]['question'], 'question_id': l, 'draw': d, 'input_id': iid})
    sample = rng.sample(links, min(40, len(links)))
    for n, s in enumerate(sample, 1):
        s['id'] = f'L{n:02d}'
    (folder / 'links.json').write_text(json.dumps(sample, ensure_ascii=False, indent=1))
    print(len(opened), 'opened questions (both arms, 3 draws);', len(links), 'arm links,', len(sample), 'sampled')


if __name__ == '__main__':
    counts() if sys.argv[1] == 'counts' else packets(int(sys.argv[2]) if len(sys.argv) > 2 else 20261031)
