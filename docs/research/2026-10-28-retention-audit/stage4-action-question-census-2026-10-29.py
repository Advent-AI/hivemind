"""Count answers with a new question despite a non-propose action; source evidence, not model quality."""
import json
from pathlib import Path

ROOT=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-retention-audit')
OLD=Path('/Users/lchingen/hivemind/poc/reports/2026-10-27-stage34-gold')


def contradicts(a):
    if not isinstance(a,dict) or 'action' not in a or 'new_question' not in a:raise ValueError('unidentifiable answer')
    return a['action']!='propose_new' and bool((a['new_question'] or '').strip())

if not contradicts({'action':'background_only','new_question':'What is the investment impact?'}) or contradicts({'action':'propose_new','new_question':'What is the investment impact?'}) or contradicts({'action':'background_only','new_question':''}):
    raise ValueError('positive or negative control failed')
run=ROOT/'stage4-scope-arm-2026-10-29';summary=json.loads((run/'run-v5-summary.json').read_text())
files=[run/f"{s['case']}-{s['provider']}-{s['sample']}.json" for s in summary['samples']]
if len(files)!=36 or len(set(files))!=36:raise ValueError('scope sample population changed')
rows=[]
for f in files:
    record=json.loads(f.read_text());a=record.get('answer')
    if contradicts(a):rows.append((f.name,a['action'],a['new_question']))
if len(rows)!=1 or rows[0][0]!='nn-control-haiku-1.json':raise ValueError('known contradiction control changed')
print('scope answers',len(files),'contradictions',len(rows))
for name,action,q in rows:print(name,action,q)
for arm in ('arm2','fresh2'):
    files=list((OLD/arm).glob('*.analyst.answer.json'))
    if not files:raise ValueError('historical answers missing')
    bad=[f.name for f in files if contradicts(json.loads(f.read_text()))]
    print(arm,'answers',len(files),'contradictions',len(bad))
