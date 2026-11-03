"""The reader packet of the judgement ruler (ruler-v1.md §1): the 309 items of golden-v5 dev (the signed standard's reading of the 14
days) with ids, and the 23 gold questions (the 22 seeds plus the one must_open bet no seed covers) with their units, rungs and the
must_open gists each one covers. Code only; nothing here judges.

    python3 build_packet.py            # writes packet-v1.json and questions-v1.json beside this file and prints their sha256
"""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GOLD = ROOT / 'docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json'
SEEDS = ROOT / 'poc/seeds/nvda-2026-07-01-v2.json'

# The must_open gists of the gold, mapped to the gold question they are the same bet as (D248: wordings, deadlines and periods of one bet
# are one question). Keyed by a distinctive phrase of the gist; 'q23' is the one bet no seed covers.
MUST_OPEN_MAP = [
    ('Ohio', 'q23'), ('credit support', 'q09'), ('credit-support', 'q09'), ('AI Compute Partnership obligation', 'q09'), ('backstop commitments to neoclouds', 'q09'),
    ('Kyber', 'q18'), ('2027 data-center capital expenditure', 'q13'), ('calendar-2027 data-center capital expenditure', 'q13'),
    ('calendar-2026 data-center capital expenditure', 'q04'), ('DRAM', 'q05'), ('H200', 'q08'),
]
UNITS = {'q01': 'USD', 'q02': 'USD', 'q03': 'percent (75 means 75%)', 'q04': 'USD', 'q05': 'percent change 2027 vs 2026 (10 means up 10%)', 'q06': 'percent',
         'q07': 'yes/no', 'q08': 'yes/no', 'q09': 'USD', 'q10': 'percent', 'q11': 'USD per share', 'q12': 'USD', 'q13': 'USD', 'q14': 'wafers per month',
         'q15': 'percent growth 2026 vs 2025', 'q16': 'USD', 'q17': 'percent', 'q18': 'yes/no', 'q19': 'USD', 'q20': 'USD', 'q21': 'yes/no',
         'q22': 'USD', 'q23': 'yes/no'}   # the units the seed rungs' lo/hi are written in


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    gold = json.loads(GOLD.read_text(encoding='utf-8'))
    seeds = json.loads(SEEDS.read_text(encoding='utf-8'))
    articles = sorted(gold['articles'], key=lambda a: (a['publication_day'], a['input_id']))
    items, n = [], 0
    for a in articles:
        for it in a['items']:
            n += 1
            items.append({'id': f'i{n:03d}', 'day': a['publication_day'], 'title': a['title'], 'input_id': a['input_id'], 'tier': it.get('tier') or 'unknown',
                          'who': it.get('who') or '', 'passage': it['span'], 'meaning': it.get('meaning') or '', 'weight': it['weight']})
    questions = []
    for k, s in enumerate(seeds['questions'], 1):
        qid = f'q{k:02d}'
        assert s['view_id'] == f'v{k}', (s['view_id'], qid)
        questions.append({'id': qid, 'seed_view_id': s['view_id'], 'kind': s['kind'], 'question': s['question'], 'due_day': s['due_day'],
                          'unit': UNITS[qid], 'rungs': s['rungs'], 'covers_must_open': []})
    ohio = next(q for a in articles for q in a['questions']['must_open'] if 'Ohio' in q['gist'])
    questions.append({'id': 'q23', 'seed_view_id': None, 'kind': 'asset',
                      'question': "Will NVIDIA sign a guarantee of OpenAI's Ohio data-center lease by 2027-06-30?", 'due_day': '2027-06-30', 'unit': UNITS['q23'],
                      'rungs': [{'label': 'Yes', 'condition': 'NVIDIA has signed the guarantee by the due day.'}, {'label': 'No', 'condition': 'It has not.'}],
                      'covers_must_open': [], 'source': {'must_open_gist': ohio['gist'], 'rule': ohio['rule']}})
    by_id = {q['id']: q for q in questions}
    unmapped = []
    for a in articles:
        for q in a['questions']['must_open']:
            target = next((qid for phrase, qid in MUST_OPEN_MAP if phrase.lower() in q['gist'].lower()), None)
            if target is None:
                unmapped.append((a['publication_day'], q['gist'][:100])); continue
            by_id[target]['covers_must_open'].append({'day': a['publication_day'], 'input_id': a['input_id'], 'gist': q['gist']})
    assert not unmapped, unmapped
    packet = {'ruler_version': 1, 'about': 'golden-v5 dev items (the signed standard\'s reading of 2026-07-01..07-14), ids assigned in day order; see ruler-v1.md',
              'gold_sha256': sha(GOLD), 'items': items}
    qfile = {'ruler_version': 1, 'about': '22 seed questions (poc/seeds/nvda-2026-07-01-v2.json) + the one must_open bet no seed covers; must_open gists mapped by bet (D248)',
             'seeds_sha256': sha(SEEDS), 'gold_sha256': sha(GOLD), 'questions': questions}
    (HERE / 'packet-v1.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    (HERE / 'questions-v1.json').write_text(json.dumps(qfile, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    covered = sum(len(q['covers_must_open']) for q in questions)
    print(f'packet: {len(items)} items, {sum(len(i["passage"]) + len(i["meaning"]) for i in items):,} chars; sha256 {sha(HERE / "packet-v1.json")}')
    print(f'questions: {len(questions)}; must_open gists covered {covered}; sha256 {sha(HERE / "questions-v1.json")}')
    for q in questions:
        print(f'  {q["id"]} {q["kind"]:<5} unit={q["unit"]:<28} must_open x{len(q["covers_must_open"])}  {q["question"][:80]}')


if __name__ == '__main__':
    main()
