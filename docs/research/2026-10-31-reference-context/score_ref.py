"""Code counts for design.md's predictions P1–P6 on run REF (control REF-v53, arm REF-v53R), and the two blind packets a reader judges
(P3 links, P4 duplicate candidates). Code counts structure only; meaning is the blind reader's.

    python3 score_ref.py counts            # P1, P2 (via final_scores rows), P4 code count, P5, P6, sink share
    python3 score_ref.py packets [seed]    # blind/links.json (40 links, arm only), blind/candidates.json (both arms, label key apart)
"""
import collections
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LEDGER = ROOT / 'docs/research/2026-10-29-ledger-standard'
sys.path[:0] = [str(LEDGER), str(LEDGER / 'final-2026-10-30'), str(HERE)]
import final_scores as fs  # noqa: E402
import score_gold as sg  # noqa: E402
import reference_arm as ra  # noqa: E402

CONTROL, ARM = 'REF-v53', 'REF-v53R'
SINKS = {'v2', 'v6'}          # FY2027 total revenue and gross margin: the company-wide quantities D207 found absorbing links
articles = json.loads(Path(fs.GOLDS['dev']).read_text())['articles']
sizes = json.loads((HERE / 'list-sizes.json').read_text())


def raw(tag, iid):
    row = sg.answers(tag).get(iid)
    if not row or not row[0]:
        return None
    try:
        return json.loads(row[0])
    except json.JSONDecodeError:
        return None


def shown(iid):
    a = next(x for x in articles if x['input_id'] == iid)
    return ra.open_questions_before(a['publication_day'])


def same_question(text_a, text_b):
    """fs.matches without the opens_as condition: at least QUESTION_SHARE of the shorter question's words shared."""
    g, q = sg.words(text_a) - sg.STOP, sg.words(text_b) - sg.STOP
    return bool(g and q) and len(g & q) >= fs.QUESTION_SHARE * min(len(g), len(q))


def counts():
    fs.PREFIX = 'REF'
    rows = {v: fs.per_article(v, articles) for v in ('v53', 'v53R')}
    with_list = [a['input_id'] for a in articles if sizes[a['input_id']] > 0]
    empty = [a['input_id'] for a in articles if sizes[a['input_id']] == 0]
    print('== P1 gold-rejected kept per draw (D250 unit), articles with a list:', len(with_list))
    for v in ('v53', 'v53R'):
        print(f'   {v}:', [sum(rows[v][i]['nk_hits'][d] for i in with_list) for d in range(3)], '| extra (gold lists nothing):', [sum(rows[v][i]['extra'][d] for i in with_list) for d in range(3)])
    print('   paired bootstrap, arm minus control over these articles:', fs.paired({i: rows['v53R'][i] for i in with_list}, {i: rows['v53'][i] for i in with_list}, 'not-kept kept (mean of draws)'))
    print('== P2 core every draw / supporting >=2 draws (counting aid, all 118)')
    for v in ('v53', 'v53R'):
        t = fs.totals(rows[v])
        print(f'   {v}: core every {t["core every draw"]}/{t["core total"]} per-draw {t["core per draw"]} | supp>=2 {t["supporting >=2 draws"]}/{t["supporting total"]} per-draw {t["supporting per draw"]}')
    print('== P6 statements per draw on the', len(empty), 'articles with an empty list')
    for v in ('v53', 'v53R'):
        print(f'   {v}:', [sum(rows[v][i]['stmts'][d] for i in empty) for d in range(3)], '| gold-rejected kept', [sum(rows[v][i]['nk_hits'][d] for i in empty) for d in range(3)])
    # P3 code part: links to shown questions, sink share
    print('== P3 links (arm): kept statements linked to a shown question, and the share on the two company-wide quantities')
    for d in (1, 2, 3):
        linked = to_sink = total = 0
        for iid in with_list:
            data = raw(f'{ARM}-d{d}', iid)
            ids = {q['view_id'] for q in shown(iid)}
            for e in (data or {}).get('evidence', []):
                total += 1
                hits = [l for l in e.get('links', []) if l in ids]
                linked += bool(hits)
                to_sink += any(l in SINKS for l in hits)
        print(f'   d{d}: statements {total}, linked to a shown question {linked}, of which to v2/v6 {to_sink} ({to_sink / max(linked, 1):.0%})')
    # P4: candidates that duplicate a shown question (code), per draw, both arms
    print('== P4 candidates duplicating a shown open question (code: word share), articles with a list')
    for tag in (CONTROL, ARM):
        per = []
        for d in (1, 2, 3):
            dup = cands = 0
            for iid in with_list:
                data = raw(f'{tag}-d{d}', iid)
                qs = shown(iid)
                for c in (data or {}).get('candidates', []):
                    cands += 1
                    dup += any(same_question(c.get('question', '') + ' ' + c.get('looks_at', ''), q['question']) for q in qs)
            per.append((cands, dup))
        print(f'   {tag}: (candidates, duplicates) per draw {per}')
    # P5: gold must-open questions not yet open at the day: proposed by each arm
    print('== P5 gold must-open questions (v3 opening part, a lead) not yet open at the day: raised per draw')
    pending = []
    for a in articles:
        qs = shown(a['input_id'])
        for gq in a.get('questions', {}).get('must_open', []):
            already = any(same_question(gq['gist'], q['question']) for q in qs)
            pending.append((a['input_id'], gq, already))
    print(f'   must-open total {len(pending)}, already open at the day (code) {sum(p[2] for p in pending)}')
    for tag in (CONTROL, ARM):
        raised = [0, 0, 0]
        for d in (1, 2, 3):
            for iid, gq, already in pending:
                if already:
                    continue
                data = raw(f'{tag}-d{d}', iid)
                raised[d - 1] += any(fs.matches(gq, c) for c in (data or {}).get('candidates', []))
        print(f'   {tag}: not-yet-open must-open raised per draw {raised} of {sum(not p[2] for p in pending)}')


def packets(seed):
    rng = random.Random(seed)
    (HERE / 'blind').mkdir(exist_ok=True)
    links = []
    for d in (1, 2, 3):
        for a in articles:
            iid = a['input_id']
            qs = {q['view_id']: q for q in shown(iid)}
            data = raw(f'{ARM}-d{d}', iid)
            for e in (data or {}).get('evidence', []):
                for l in e.get('links', []):
                    if l in qs:
                        links.append({'article': a['title'], 'day': a['publication_day'], 'quote': e['quote'], 'one_line': e.get('one_line', ''),
                                      'question': qs[l]['question'], 'question_id': l, 'draw': d, 'input_id': iid})
    sample = rng.sample(links, min(40, len(links)))
    for n, s in enumerate(sample, 1):
        s['id'] = f'L{n:02d}'
    (HERE / 'blind/links.json').write_text(json.dumps(sample, ensure_ascii=False, indent=1))
    cands, key = [], {}
    for tag, label in ((CONTROL, 'control'), (ARM, 'arm')):
        for d in (1, 2, 3):
            for a in articles:
                iid = a['input_id']
                if sizes[iid] == 0:
                    continue
                data = raw(f'{tag}-d{d}', iid)
                for c in (data or {}).get('candidates', []):
                    cid = f'C{len(cands) + 1:03d}'
                    key[cid] = {'arm': label, 'draw': d, 'input_id': iid}
                    cands.append({'id': cid, 'article': a['title'], 'day': a['publication_day'], 'candidate_question': c.get('question', ''),
                                  'looks_at': c.get('looks_at', ''), 'open_questions': [f'{q["view_id"]}: {q["question"]}' for q in shown(iid)]})
    rng.shuffle(cands)
    (HERE / 'blind/candidates.json').write_text(json.dumps(cands, ensure_ascii=False, indent=1))
    (HERE / 'blind/candidates.key.json').write_text(json.dumps(key, ensure_ascii=False, indent=1))
    print(len(links), 'links in the arm;', len(sample), 'sampled;', len(cands), 'candidates in both arms (key written apart)')


if __name__ == '__main__':
    if sys.argv[1] == 'counts':
        counts()
    else:
        packets(int(sys.argv[2]) if len(sys.argv) > 2 else 20261031)
