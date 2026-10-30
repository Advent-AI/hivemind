"""Merge the six golden-v3 drafts into one reference, normalising what the drafters recorded differently, and freeze it.

Normalisation (each a written rule of standard-v2.13 or a recording convention; every override listed below with its reason):
- weight values: 'none' / 'excluded' / None -> 'excluded' (not kept under that rule).
- an unsized named party's action recorded optional under the current rule and supporting under proposal 1 (batch 1) ->
  supporting under both: the signed §4 defines supporting as "支持或反驳上述判断", which these do (D240).
- restatements (depends_on 6), item by item (RESTATED below): past actuals and the company's own quarterly guidance are
  excluded under the current rule (signed §2); past actuals are optional under proposal 6, guidance keeps its weight;
  still-valid forecasts and plans keep their weight under both (signed §0, Alex D215 question 7) and lose the 6 tag.
- valuation multiples and market value (depends_on 4): excluded under the current rule, optional under proposal 4.
- another company's share price -> not_kept (D238 row).
- a question whether China permits H200 imports is a theme question (role-v12: licensing is a theme example).
- a not_kept descriptive-only quote depends on proposal 10 (signed standard has no such row).
- WEIGHT_FIX: one consistency fix across batches, listed with its reason.
- depends_on keeps 1 only where the two weights differ.
"""
import hashlib, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
E, O, S, C = 'excluded', 'optional', 'supporting', 'core'
RESTATED = {  # (batch, input_id suffix, item index): (current, proposed)
    (1, '0c6ef85a', 0): (S, S), (1, '0c6ef85a', 1): (S, S), (1, '0c6ef85a', 3): (E, O), (1, 'e4081dd0', 0): (E, S), (1, 'e4081dd0', 2): (E, S),
    (1, 'ca3e7b45', 3): (C, C), (1, 'ca3e7b45', 4): (E, O), (1, 'ca3e7b45', 5): (E, O), (1, 'ca3e7b45', 6): (E, O),
    (1, '00cf2816', 3): (E, O), (1, '00cf2816', 4): (E, O), (1, '00cf2816', 5): (E, O),
    (2, 'f3ba56b0', 3): (E, O), (2, '8e95cf02', 7): (E, O), (2, '5e766c96', 0): (E, O), (2, 'e4c486e1', 1): (E, O),
    (2, 'e4c486e1', 2): (C, C), (2, 'e4c486e1', 3): (C, C), (2, '60340128', 3): (E, O), (2, '60340128', 4): (E, O),
    (3, '0f43f048', 0): (E, O), (3, '0aa3c572', 0): (E, O), (3, 'c500960f', 0): (C, C),
    (4, 'db9756d6', 1): (E, O), (4, 'db9756d6', 18): (E, O), (4, 'db9756d6', 20): (S, S), (4, '99432e1a', 0): (E, O), (4, '99432e1a', 1): (E, S),
    (4, '99432e1a', 2): (E, O), (4, '08bc0a32', 1): (E, O), (4, '08bc0a32', 2): (E, O), (4, '08bc0a32', 8): (S, S),
    (4, '924ebb57', 4): (S, C), (4, '924ebb57', 6): (S, S), (4, '32f116b3', 0): (E, O), (4, '32f116b3', 1): (E, O), (4, '32f116b3', 2): (E, S),
    (4, '32f116b3', 3): (E, O), (4, '32f116b3', 5): (S, C), (4, '32f116b3', 6): (E, O), (4, 'f8857512', 3): (E, O),
    (4, '39aee250', 4): (C, C), (4, '39aee250', 6): (E, O),
    (5, '80ce7ba9', 0): (E, O), (5, '140c8cce', 3): (E, O),
    (6, '624481fb', 3): (E, O), (6, '624481fb', 4): (E, O), (6, '624481fb', 6): (E, O), (6, 'c317d209', 2): (E, O), (6, 'c317d209', 3): (E, O),
    (6, '3d256f9e', 4): (E, O), (6, '3d256f9e', 5): (E, S), (6, '3ee7b05c', 2): (C, C), (6, '3ee7b05c', 8): (E, O), (6, '0636c2db', 1): (E, O), (6, '0636c2db', 2): (E, O),
}
TO_NOT_KEPT = {(4, '08bc0a32', 3): '别家公司的股价（D238）'}
WEIGHT_FIX = {(2, '2e75e806', 1): (S, S, 'another smuggling case, supporting like the Thailand case in batch 3')}

# From the blind spot check (spotcheck.md): statements the reader kept that the drafts missed, read against the text by Claude.
ADDITIONS = [
    ('gnews:f66e1689ec2e27e7eab2a2dd', 'Morgan Stanley notes that a hyperscaler self-sourcing certain memory modules could bring the rack price down to around $6', 3, S, S, 'third_party_view', 'pricing and installed base', '§5.1 第 3 类：具名一方的估计（客户自采内存时的机架价格）'),
    ('nvblog:nvidia-vera-max-single-threaded-cpu-at-scale', 'NVIDIA’s next-generation Rosa CPU with the Rigel core will continue the company’s CPU roadmap for the agentic AI era.', 1, S, S, 'party_statement', 'product cycle', '§5.1 第 1 类：公司的产品路线（没有日期）'),
    ('gnews:8c9d215416b714064de3b095', 'The first production deployment, the Mercedes-Benz CLA on the DRIVE platform, reached the US market this year.', 2, S, S, 'fact', 'demand', '§5.1 第 2 类：具名客户的量产采用（D240）'),
    ('gnews:8c9d215416b714064de3b095', 'Cadence, Schneider Electric, Siemens, Vertiv, Eaton, Jacobs, and others contributing SimReady assets and integrating their design tools', 2, S, S, 'fact', 'demand', '§5.1 第 2 类：具名伙伴的集成（D240）'),
    ('gnews:295fceb25273abae9bb6c995', 'A larger sibling, the NVL576, designed to link eight racks via optical connections, is also likely delayed or limited to small initial volumes, according to SemiAnalysis.', 3, S, S, 'third_party_view', 'product cycle', '§5.1 第 3 类：研究机构称主力产品的一种配置可能推迟（"可能"，不是确定状态）'),
    ('gnews:295fceb25273abae9bb6c995', 'Blackwell and current Rubin systems remain in short supply.', 3, S, S, 'rumour', 'supply and inputs', '§5.1：关键产品供给状况，没有数（待拍 5 可能判为背景）'),
    ('gnews:d0f3f83296df884fae64921e', "new capacity for many in this industry won't be online until 2027 or later, creating a low supply of inventory for at least the next year and a half", 3, S, C, 'third_party_view', 'supply and inputs', '§5.1 第 3 类：作者对关键投入供给的带期间预测'),
    ('gnews:07610e55de6cc86b2b508b1d', 'LangChain developers can access Nemotron 3 Ultra on Baseten , Crusoe Cloud , DeepInfra, Fireworks , Nebius and Together AI platforms', 2, S, S, 'fact', 'demand', '§5.1 第 2 类：具名平台提供公司的模型（D240）'),
    ('nvblog:nemotron-langchain-agents-open-stack', 'LangChain developers can access Nemotron 3 Ultra on Baseten , Crusoe Cloud , DeepInfra, Fireworks , Nebius and Together AI platforms', 2, S, S, 'fact', 'demand', '§5.1 第 2 类：具名平台提供公司的模型（D240）'),
]
ADDITIONS2 = json.loads((HERE / 'pass2-additions.json').read_text())  # second blind pass, decided by Claude (pass2-decisions.json)
FIELDS = json.loads((HERE / 'additions-fields.json').read_text())  # who and meaning for the blind-check additions, read beside the article text
SPAN_WEIGHT_FIX = {('gnews:f66e1689ec2e27e7eab2a2dd', 'First shipments are scheduled for the third quarter'): (C, C, 'spot check: the shipping date of the product generation that carries the value is key product progress (signed §4 core)')}
DEPS_ADD = {('gnews:295fceb25273abae9bb6c995', 'Blackwell and current Rubin systems remain in short supply.'): [5]}
MAY_OPEN_ADD = {'gnews:c8c39f971721fd820aab5c1c': {'type': 'B', 'opens_as': 'main_driver', 'kind': 'asset', 'gist': 'Will NVIDIA release the Rubin line-up in the second half of 2026?', 'settled_by': 'company launch or shipment announcement', 'rule': '§3.1 B（第二轮盲读）'}, 'gnews:f66e1689ec2e27e7eab2a2dd': {'type': 'B', 'opens_as': 'main_driver', 'kind': 'asset', 'gist': 'Will Vera Rubin (VR200 NVL72) first shipments start by the end of Q3 2026, as the article reports?', 'settled_by': 'company shipment announcement or earnings call', 'rule': '§3.1 B（spot check）'}}
log = []


def norm(w):
    return E if w in (None, 'none', 'excluded') else w


articles = []
for b in range(1, 7):
    src = {a['input_id']: a for a in json.loads((HERE / 'batches' / f'batch-{b}.json').read_text())}
    for a in json.loads((HERE / f'draft-batch-{b}.json').read_text()):
        art = src[a['input_id']]
        items, not_kept = [], list(a.get('not_kept', []))
        for i, it in enumerate(a['items']):
            key = (b, a['input_id'][-8:], i)
            it = dict(it, weight_current=norm(it.get('weight_current')), weight_proposed=norm(it.get('weight_proposed')))
            deps = set(it.get('depends_on') or [])
            if key in TO_NOT_KEPT:
                not_kept.append({'span': it['span'], 'row': TO_NOT_KEPT[key], 'depends_on': []}); log.append(f'{key} -> not_kept'); continue
            if key in RESTATED:
                cur, prop = RESTATED[key]
                if (cur, prop) != (it['weight_current'], it['weight_proposed']):
                    log.append(f'{key} restatement {it["weight_current"]}/{it["weight_proposed"]} -> {cur}/{prop}')
                it['weight_current'], it['weight_proposed'] = cur, prop
                if cur == E:
                    deps.add(6)
                else:
                    deps.discard(6)
            elif 6 in deps:
                raise SystemExit(f'restatement not classified: {key} {it["span"][:80]}')
            if key in WEIGHT_FIX:
                it['weight_current'], it['weight_proposed'] = WEIGHT_FIX[key][:2]; log.append(f'{key} {WEIGHT_FIX[key][2]}')
            if b == 1 and it['weight_current'] == O and it['weight_proposed'] == S and deps <= {1, 5}:
                it['weight_current'] = S; log.append(f'{key} unsized named action optional -> supporting (current)')
            if 4 in deps and it['weight_current'] == O and it['weight_proposed'] == O:
                it['weight_current'] = E; log.append(f'{key} valuation: current -> excluded')
            if '81%' in it['span'] and 5 in deps:
                deps.discard(5); log.append(f'{key} 81% share has a figure: depends_on 5 removed')
            if it['weight_current'] == it['weight_proposed']:
                deps.discard(1)
            else:
                deps.add(1)
            it['depends_on'] = sorted(deps)
            assert it['span'] in art['text'], key
            items.append(it)
        for nk in not_kept:
            if '形容' in str(nk.get('row') or nk.get('rule') or ''):
                nk['depends_on'] = sorted(set(nk.get('depends_on') or []) | {10})
        for (iid, span, kind, cur, prop, tier, drv, rule, *extra) in ADDITIONS + [tuple(x) for x in ADDITIONS2]:
            if iid == a['input_id']:
                assert span in art['text'], span[:60]
                deps = sorted(set(DEPS_ADD.get((iid, span), [])) | set(extra[0] if extra else []) | ({1} if cur != prop and not (extra and extra[0]) else set()))
                items.append({'span': span, 'kind': kind, 'weight_current': cur, 'weight_proposed': prop, 'depends_on': deps, 'tier': tier, 'driver': drv, 'rule': rule, 'was': 'not in reference_v2; added after the blind spot check'})
                log.append(f'({a["input_id"][-8:]}) spot-check addition: {span[:60]}')
        for it in items:
            if not it.get('who') and not it.get('meaning'):
                found = [f for f in FIELDS if a['input_id'].endswith(f[0]) and it['span'].startswith(f[1])]
                assert len(found) == 1, ('who/meaning for an added item', a['input_id'], it['span'][:60], len(found))
                it['who'], it['meaning'] = found[0][2], found[0][3]
            for (iid, pre), (cur, prop, why) in SPAN_WEIGHT_FIX.items():
                if iid == a['input_id'] and it['span'].startswith(pre):
                    it['weight_current'], it['weight_proposed'] = cur, prop; it['depends_on'] = sorted(set(it['depends_on']) - {1}); log.append(f'({iid[-8:]}) {why}')
        qs = a.get('questions', {})
        if a['input_id'] in MAY_OPEN_ADD:
            qs.setdefault('may_open', []).append(MAY_OPEN_ADD[a['input_id']]); log.append(f'({a["input_id"][-8:]}) spot-check may_open B')
        for q in qs.get('must_open', []) + qs.get('may_open', []):
            if q.get('opens_as') == 'policy_stage' and 'H200' in (q.get('gist') or '') and q.get('kind') != 'theme':
                log.append(f'({b}, {a["input_id"][-8:]}) H200 question asset -> theme'); q['kind'] = 'theme'
        articles.append({'set': art['set'], 'input_id': a['input_id'], 'title': art['title'], 'publication_day': art['publication_day'],
                         'items': items, 'not_kept': not_kept, 'questions': qs, 'notes': a.get('notes', [])})
out = {'about': 'Golden reference v3 (2026-10-29, D241): 118 bench articles (98 week, 20 holdout) traced to the article text and to standard-v2.14.md. '
                 'weight_current: the signed standard (D229) as in force; weight_proposed: the proposals at their leans; depends_on: the proposal numbers whose decision changes the entry. '
                 'Drafted article by article from the text (six drafters, the older reference_v2 as a starting point only), normalised by merge.py, read by Claude; spans checked by code.',
       'standard': 'docs/prd/05-extraction-standard.html (rules as standard-v2.14.md)', 'articles': articles}
path = HERE / 'golden-v3.json'
path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
(HERE / 'merge-log.txt').write_text('\n'.join(log) + '\n')
print(len(articles), sum(len(a['items']) for a in articles), 'items;', len(log), 'normalisations')
print(hashlib.sha256(path.read_bytes()).hexdigest())
