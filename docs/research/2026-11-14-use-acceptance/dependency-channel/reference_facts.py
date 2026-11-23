"""Where did the system put the facts the frozen judgement reference uses for total revenue (q01) and data-center revenue (q02)?
($0; D535, part a.) For each reference fact, located by a phrase: how many distinct statements carrying it were ever shown to each
of the two questions over all their stored requests (matched by statement id), which supporting question's last conclusion carries it in the 600 characters a
request would show, and under which questions the system filed it. A locating aid for reading, not a score: every row was then
read in the stored requests and conclusions. Reads the frozen files and the stored draw only.

  python3 reference_facts.py
"""
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
RUN = ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03/d1'
FACTS = [                     # (the reference's items, the fact, the reference questions that use it, a phrase that locates it)
    ('i037', 'consensus of $392 billion for the year', 'q01 q02', r'\$?392'),
    ('i090 i174', 'analysts project 82% growth', 'q01', r'82\s?%'),
    ('i280', 'first-quarter revenue of $81.6 billion', 'q01', r'81\.6'),
    ('i281', 'second-quarter guidance of $91 billion', 'q01 q02', r'\$?91(\.0)? ?(billion|bn)'),
    ('i295', 'management: growth accelerating toward $100 billion quarters', 'q01 q02', r'accelerat\w+ growth'),
    ('i106 i208', 'SemiAnalysis: second-half data-center compute 20% above consensus', 'q01 q02', r'20\s?% above'),
    ('i111', 'the market materially lower on shipment volumes', 'q01', r'materially lower'),
    ('i219 i105', 'the Rubin shipping schedule (full production; first shipments, then a volume ramp)', 'q01 q02', r'Rubin[^\n]{0,160}(ship|production|ramp)|(ship|production|ramp)[^\n]{0,160}Rubin'),
    ('i216', 'a Rubin rack at about $7.8 million against $4 million', 'q01 q02', r'7\.8 ?(m|million)'),
    ('i288', 'the Vera CPU target of $20 billion', 'q01', r'(CPU|Vera)[^\n]{0,80}\$?20 ?(bn|billion)|\$?20 ?(bn|billion)[^\n]{0,60}(CPU|Vera)'),
    ('i133', 'reports of delays across the Rubin line-up', 'q01 q02', r'delays across|Rubin[^\n]{0,80}delay'),
    ('i252', 'memory tight until 2028', 'q01', r'until 2028'),
    ('i129 i151', 'first-quarter data-center revenue of $75.25 billion, 92% of sales', 'q02', r'75\.25?'),
    ('i156 i281', 'guidance assumes no China data-center compute revenue', 'q01 q02', r'effectively zero|zero China|no China|excluding China|assum\w+ (zero|no)[^\n]{0,40}China'),
    ('i270', 'China may allow purchases of the H200', 'q02', r'H200'),
]


def main():
    store = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True)
    archive = sqlite3.connect(f"file:{RUN / 'archive.sqlite'}?mode=ro", uri=True)
    shown = {}
    for view in ('v1', 'v2'):
        lines = {}
        for (sha,) in store.execute('select request_sha256 from judgements where view_id = ? order by judgement_id', (view,)):
            user = json.loads(archive.execute('select request_json from model_calls where request_sha256 = ?', (sha,)).fetchone()[0])['messages'][-1]['content']
            lines.update({line.split(' ')[1]: line for line in user.split('\n') if line.startswith('- e')})
        shown[view] = lines
    edges = [(row[0], row[1]) for row in store.execute("select d.view_id, coalesce((select r.resolved_to from dependency_resolutions r where r.dependency_id = d.dependency_id order by r.id desc limit 1), d.depends_on) from dependencies d") if row[1]]
    supporters = {view: sorted(supporting for supporting, supported in edges if supported == view) for view in ('v1', 'v2')}
    conclusion = {view: (store.execute('select reasons from judgements where view_id = ? order by judgement_id desc limit 1', (view,)).fetchone() or [''])[0][:600] for view in set(supporters['v1'] + supporters['v2'])}
    rows = []
    for items, fact, used_for, phrase in FACTS:
        pattern = re.compile(phrase, re.I)
        filed, carrying = {}, set()
        for evidence_id, one_line, quote in store.execute('select evidence_id, one_line, quote from evidence'):
            if pattern.search(one_line + ' ' + quote):
                carrying.add(evidence_id)
                for (view,) in store.execute('select view_id from evidence_links where evidence_id = ?', (evidence_id,)):
                    filed[view] = filed.get(view, 0) + 1
        rows.append({'reference_items': items, 'fact': fact, 'reference_uses_it_for': used_for,
                     'statements_ever_shown_to_total_revenue': len(carrying & set(shown['v1'])),       # by statement id: the summary shown may word the fact differently from its passage
                     'statements_ever_shown_to_data_center_revenue': len(carrying & set(shown['v2'])),
                     'direct_supporters_of_total_revenue_whose_conclusion_carries_it': [view for view in supporters['v1'] if pattern.search(conclusion[view])],
                     'direct_supporters_of_data_center_revenue_whose_conclusion_carries_it': [view for view in supporters['v2'] if pattern.search(conclusion[view])],
                     'filed_under': dict(sorted(filed.items(), key=lambda pair: -pair[1]))})
    out = {'run': str(RUN.relative_to(ROOT)), 'distinct_statements_ever_shown': {view: len(lines) for view, lines in shown.items()}, 'supporters': supporters, 'facts': rows}
    (Path(__file__).parent / 'reference-facts-d1.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    print(f"distinct statements ever shown: total revenue {len(shown['v1'])}, data-center revenue {len(shown['v2'])}")
    for row in rows:
        print(f"{row['fact'][:62]:62} | used for {row['reference_uses_it_for']:7} | shown to total {row['statements_ever_shown_to_total_revenue']:2}, to data-center {row['statements_ever_shown_to_data_center_revenue']:2} | "
              f"in a direct supporter's conclusion: of total {row['direct_supporters_of_total_revenue_whose_conclusion_carries_it']}, of data-center {row['direct_supporters_of_data_center_revenue_whose_conclusion_carries_it']} | filed {row['filed_under']}")


if __name__ == '__main__':
    main()
