"""Fix golden-v3 under the signed standard (D243): every entry gets its final weight.

Input golden-v3.json (the draft with weight_current, weight_proposed and depends_on). Output golden-v3-signed.json:
items hold what the extraction must or may keep (weight core, supporting or optional); not_kept holds what it must not
keep (weight not_kept) or may keep (weight optional). Proposals 1-4 and 6-12 were signed at their leans; proposal 5 was
decided stricter by Alex: a typical claim or background statement (common knowledge, what an analyst following the
company knew before this item) is kept only when it carries a number and a specific narrative; new information is
judged by the keep rule as any statement is. Each entry changed here names its reason.
"""
import hashlib, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
R5 = 'D243 第 5 条：典型的主张或背景，是跟这家公司的分析员读这篇之前就知道的常识，没有数字和具体的叙事，不收'
RO = '与起草者写了理由的不留句是同一句；按 D243 定为不留'
# (article id suffix, span prefix): reason. The item leaves items and is not kept.
EXCLUDE = {
    ('5e8e95cf02', 'The Chinese government has to date locked'): R5,
    ('d01d0d285b', "there's Broadcom, vicious competitor"): R5,
    ('ddee1d18c2', 'since DRAM manufacturers have locked'): R5,
    ('92ede72145', 'concerns around a "circular-financing boom"'): R5,
    ('555d592587', 'The delays "should not be over analyzed'): R5,
    ('e00aa3c572', 'Collaborations with Nokia focus'): R5 + '（股票文章里重提的已有合作）',
    ('e00aa3c572', "Nvidia's tie-up with Marvell"): R5 + '（股票文章里重提的已有合作）',
    ('e00aa3c572', 'Additional partnerships with Coherent'): R5 + '（股票文章里重提的已有合作）',
    ('7edb9756d6', 'it became clear that chip production'): R5,
    ('7edb9756d6', 'it is clear that financing will now'): R5,
    ('7edb9756d6', 'When it comes to shorter-dated rentals'): R5,
    ('7edb9756d6', 'This broadens the base of buyers'): R5,
    ('bb99432e1a', "The company's Blackwell and Vera Rubin platforms"): R5,
    ('d008bc0a32', 'Samsung, SK Hynix, and Micron have avoided'): R5,
    ('d008bc0a32', 'NVIDIA has been smart about locking'): R5,
    ('28924ebb57', 'NVIDIA has partly funded its own demand'): R5,
    ('4257a59b2b', '“China’s drive to substitute'): R5,
    ('4257a59b2b', 'a global memory chip shortage is likely'): R5,
    ('a657e5f677', 'Nvidia said that this plan highlights'): R5,
    ('df5a71ff08', 'NVIDIA is collaborating with Nokia'): R5 + '（技术博客里描述已有合作）',
    ('ae9bb6c995', 'Blackwell and current Rubin systems remain'): R5,
    ('51fe1f063a', 'the same export rules that have effectively'): R5,
    ('233ee7b05c', 'Analyst Joshua Buchalter said'): R5,
    ('ec9773812b6e', 'Broadcom expects major growth'): R5 + '（博通定制芯片的增长是常识，没有数字）',
    ('2e0636c2db', 'Huang took a strong stance'): 'D243 第 10 条：只有形容的引语，不收',
    ('4d8bac9b65', 'a collaboration with Taiwanese fabless'): RO,
    ('b95e766c96', "analysts expect IREN's massive deals"): RO,
    ('064de3b095', 'The first production deployment, the Mercedes'): RO,
    ('1ab0afc348', 'Intel has led here for years'): RO + '（有数字，但是长期状况，不是新信息）',
    ('u-at-scale', 'NVIDIA’s next-generation Rosa CPU'): RO,
    ('51fe1f063a', 'OpenAI and Anthropic have both disclosed'): RO,
    ('efficiency', 'That’s why leading AI labs such as Anthropic'): RO + '（谁在用什么的长期状况）',
}
# Items kept with a weight other than weight_proposed.
REWEIGH = {('51fe1f063a', 'DeepSeek recently closed a record'): ('optional', 'D243 第 6 条：重提的过去实际数（几周前的融资），可选'),
           ('7edb9756d6', 'Nvidia’s backstop program is only getting started'): ('supporting', 'D243 第 1 条：在谈但没有量，不是确定状态，辅助')}
# not_kept sentences that a kept item now covers: removed as duplicates.
NK_DUPLICATE = [('n-robotics', 'connects NVIDIA’s 3 million robotics'), ('n-robotics', 'The largest open source physical AI dataset'),
                ('09dd8aa7fc', 'Under an expanded partnership between Hesai'), ('51fe1f063a', 'DeepSeek recently closed a record'),
                ('820aab5c1c', 'Nvidia is now working to release'), ('6b2b508b1d', 'LangChain developers can access'),
                ('open-stack', 'LangChain developers can access')]
# not_kept sentences that become optional under proposal 4 (the covered company's valuation, market value, bare targets).
NK_OPTIONAL_4 = ['I think the stock could easily reach $300', 'AMD is worth about 18%', 'the combined value of Micron, SK Hynix',
                 'NVIDIA trades at $196 against', '$NVDA Stock Price Target', 'The largest company in the world',
                 'leaving its market cap around', 'GuruFocus analysis flags NVDA', 'Broadcom is also more than 50% more expensive']
# not_kept sentences tagged to proposal 6 that stay not kept: another company's deal (D238) or no number and no narrative (proposal 5).
NK_STAY_6 = ['Google inked a multiyear deal', 'Huang has said that robotics', 'The launch also drove a surge',
             'NVIDIA’s NVLink Fusion strategy lets']

def match(article_id, span, key):
    return article_id.endswith(key[0]) and span.startswith(key[1])

draft = json.loads((HERE / 'golden-v3.json').read_text())
used = set(); log = []
articles = []
for a in draft['articles']:
    iid = a['input_id']; items = []; not_kept = []
    for it in a['items']:
        hit = [k for k in EXCLUDE if match(iid, it['span'], k)]
        rw = [k for k in REWEIGH if match(iid, it['span'], k)]
        if hit:
            used.update(hit)
            if EXCLUDE[hit[0]] != RO and not EXCLUDE[hit[0]].startswith(RO):
                not_kept.append({'span': it['span'], 'row': EXCLUDE[hit[0]], 'weight': 'not_kept', 'was': it['weight_current']})
            log.append(f'{iid[-10:]} item -> not kept: {it["span"][:70]}')
            continue
        weight = it['weight_proposed']
        if rw:
            used.update(rw); weight = REWEIGH[rw[0]][0]; it['rule'] = it['rule'] + '；' + REWEIGH[rw[0]][1]
        if weight == 'excluded':
            raise SystemExit(f'an item with no final weight: {iid} {it["span"][:60]}')
        it['weight'] = weight
        items.append(it)
    for nk in a['not_kept']:
        dup = [k for k in NK_DUPLICATE if match(iid, nk['span'], k)]
        if dup:
            used.update(dup); log.append(f'{iid[-10:]} duplicate not_kept removed: {nk["span"][:70]}'); continue
        deps = set(nk.get('depends_on') or [])
        weight = 'not_kept'
        if 3 in deps:
            weight = 'optional'
        elif 4 in deps and any(nk['span'].startswith(p) for p in NK_OPTIONAL_4):
            weight = 'optional'
        elif 6 in deps and not any(nk['span'].startswith(p) for p in NK_STAY_6):
            if 5 not in deps or re.search(r'\d', nk['span']) or 'Singapore' in nk['span']:
                weight = 'optional'
        nk['weight'] = weight
        not_kept.append(nk)
    articles.append({**{k: a[k] for k in ('set', 'input_id', 'title', 'publication_day')}, 'items': items, 'not_kept': not_kept,
                     'questions': a['questions'], 'notes': a.get('notes', [])})
missing = set(EXCLUDE) | set(REWEIGH) | set(NK_DUPLICATE)
missing -= used
assert not missing, missing
PAGE = HERE.parents[3] / 'docs/prd/05-extraction-standard.html'
version = re.search(r'<meta name="standard-version" content="(\d+)">', PAGE.read_text()).group(1)
out = {'standard_version': int(version), 'about': 'Golden reference v3, signed (D243): 118 bench articles traced to the article text and to docs/prd/05-extraction-standard.html. '
                'items: weight core, supporting or optional; not_kept: weight not_kept or optional. Optional entries are never penalised. '
                'Model-authored (Claude drafters and adjudication, Codex blind readers); the 20 holdout articles were seen in the earlier prompt loop.',
       'standard': 'docs/prd/05-extraction-standard.html', 'articles': articles}
path = HERE / 'golden-v3-signed.json'
path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
(HERE / 'finalize-log.txt').write_text('\n'.join(log) + '\n')
from collections import Counter
c = Counter((x['set'], it['weight']) for x in articles for it in x['items'])
n = Counter((x['set'], nk['weight']) for x in articles for nk in x['not_kept'])
print(dict(sorted(c.items()))); print(dict(sorted(n.items())))
print(len(log), 'changes'); print(hashlib.sha256(path.read_bytes()).hexdigest())
