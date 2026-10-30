"""Count v38 pre-filing links and compare historical research harness coverage."""
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind/poc')
ARCHIVE = ROOT / 'data/english-v38-nvda-1w-2026-10-28/archive.sqlite'
RESEARCH = ROOT / 'reports/2026-10-27-stage34-gold/fresh2/prepared.json'
PATHS = Path(__file__).with_name('placement-path-census-2026-10-29.json')

with sqlite3.connect(f'file:{ARCHIVE}?mode=ro', uri=True) as db:
    rows = list(db.execute("select call_id,answer_json from model_calls where purpose='extract' and answer_json is not null and request_sha256 not like '%:%'"))
if not rows:
    raise ValueError('no successful extraction answers')
pieces = [(call_id, piece) for call_id, answer in rows for piece in json.loads(answer).get('evidence', [])]
links = [link for _, piece in pieces for link in piece['links']]
if not links or any(not re.fullmatch(r'[cv]\d+', link) for link in links):
    raise ValueError('missing or unknown link shape')
if not any(call == 7 and piece['id'] == 'e1' and 'c1' in piece['links'] for call, piece in pieces):
    raise ValueError('known candidate link missing')
question_links = [link for link in links if re.fullmatch(r'v\d+', link)]
print(f'raw answers {len(rows)}; evidence {len(pieces)}; pieces with links {sum(bool(p[1]["links"]) for p in pieces)}; candidate references {len(links)-len(question_links)}; existing-question references {len(question_links)}')
paths = json.loads(PATHS.read_text())
path_rows = paths['rows']
excluded = [r for r in path_rows if not r['candidate_links'] and not r['placement_links'] and r['final_status'] == 'dropped']
known = next(r for r in excluded if r['input_id'] == 'gnews:3854aeddaa3f31de00cf2816' and r['id'] == 'e6')
if '72 MW' not in known['one_line']:
    raise ValueError('known user-reviewed example changed')
assert sum(r['count'] for r in paths['routes'] if not r['has_candidate'] and r['placement'] in (False, 'missing') and r['final_status'] == 'dropped') == len(excluded)
print(f'placement inputs {len(path_rows)}; no candidate and no question chosen, dropped {len(excluded)} (including a missing model answer)')
prepared = json.loads(RESEARCH.read_text())
if not prepared:
    raise ValueError('no historical research cases')
print(f'historical fresh2 cases {len(prepared)}; linked question present {sum(bool(c["linked"]) for c in prepared.values())}')
