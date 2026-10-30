"""D244: the test-set gold. Three drafts (Claude opus, each read only the signed page and the articles) merged, checked
against an independent blind read (Codex, blind-codex.json), every disagreement decided against the article text by
Claude with its reason below, frozen with the standard's version. Model-authored (AGENTS section 7). Never tuned on."""
import glob, hashlib, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE = HERE.parents[3] / 'docs/prd/05-extraction-standard.html'
SUP = 'supporting'
ADD = [  # (id suffix, span, weight, tier, who, reason)
    ('Elon Musk Makes Massive', 'Colossus 2 currently runs 110,000 Nvidia GB200 chips and 440,000 GB300s, according to Musk.', SUP, 'party_statement', 'Elon Musk',
     '盲读补：客户说出现有的装机量，带数，是新的需求信息（第 6 节辅助：别家公司的经营数字）'),
    ('Elon Musk Makes Massive', 'Musk added that a further 220,000 GB300s could come online by late December if we get lucky.', SUP, 'party_statement', 'Elon Musk',
     '盲读补：又一批带数和期间的部署，带条件"运气好的话"（第 5.4 节条件格）'),
    ('OPEC Expected', 'Production at OPEC+ is about 5 million bpd lower compared to pre-war levels', SUP, 'third_party_view', 'the article (Oilprice)',
     '盲读补：研究名单上有中东冲突和油价主题；供给缺口带数，是新的事实'),
    ('Run:ai Is Now Open Source', 'AWS : Model Streamer ships in the vLLM Deep Learning Container and is the recommended fast path in the official EKS documentation', SUP, 'party_statement', 'NVIDIA (its blog), on AWS',
     '盲读补：有名有姓的采用（D240），和开发集金标里平台上架英伟达模型的判法一致'),
    ('Run:ai Is Now Open Source', 'Google Cloud : Native Cloud Storage support built in collaboration with NVIDIA', SUP, 'party_statement', 'NVIDIA (its blog), on Google Cloud',
     '盲读补：有名有姓的采用（D240），同上'),
    ('Run:ai Is Now Open Source', 'Microsoft Azure : Azure Blob Storage integration, jointly developed by Microsoft and NVIDIA Run:ai', SUP, 'party_statement', 'NVIDIA (its blog), on Microsoft',
     '盲读补：起草稿列为产品细节；它是有名有姓的合作开发（D240），和 AWS、Google Cloud 两条同判'),
]
REWEIGH = {('Greg Lui', 'Greg Lui of Earthmade is accused'): (SUP, '起草稿按新加坡转运案件一行列可选；这是 2026 年 10 月的新案子（经马来西亚和新加坡），不是 D231 说的那个案件；司法部的执法动作是出口管制的新增量（第 5.1 节第 4 类）')}
TO_NOT_KEPT = {
    ('Greg Lui', 'China builds the alternative at home'): 'D243 第 5 条：中国在本土造替代品是常识，没有数字',
    ('Greg Lui', 'DeepSeek and Huawei are also working on TileLang'): 'D243 第 5 条：已知的状况，没有数字，不是新信息',
    ('$5,000 Invested', 'some even increasing their capex guidance for the fiscal year 2026'): 'D243 第 5 条：没有数字的泛泛说法',
}
MAY_OPEN_ADD = {'Credo vs. Nvidia': {'type': 'C', 'opens_as': 'binding_obligation', 'kind': 'asset',
    'gist': 'Will NVIDIA complete its approximately $12.9 billion acquisition of Hugging Face within the check period?', 'settled_by': 'NVIDIA closing announcement or filing',
    'rule': '盲读的另一种合理写法：还没完成的收购问成能否完成（D243 第 7 条）'}}

arts = {a['input_id']: a for f in sorted(glob.glob(str(HERE / 'batches/batch-*.json'))) for a in json.loads(Path(f).read_text())}
drafts = {a['input_id']: a for f in sorted(glob.glob(str(HERE / 'draft-batch-*.json'))) for a in json.loads(Path(f).read_text())}
def key_match(iid, span, key):
    a = arts[iid]
    return (iid.endswith(key[0]) or key[0] in a['title']) and span.startswith(key[1])
used, log, out = set(), [], []
for iid, art in arts.items():
    d = drafts[iid]
    items, not_kept = [], []
    for it in d['items']:
        hit = [k for k in TO_NOT_KEPT if key_match(iid, it['span'], k)]
        if hit:
            used.update(hit); not_kept.append({'span': it['span'], 'row': TO_NOT_KEPT[hit[0]], 'weight': 'not_kept', 'was': it['weight']}); log.append(f'{art["title"][:40]}: to not kept: {it["span"][:60]}'); continue
        rw = [k for k in REWEIGH if key_match(iid, it['span'], k)]
        if rw:
            used.update(rw); it['weight'], why = REWEIGH[rw[0]]; it['rule'] = (it.get('rule') or '') + '；' + why; log.append(f'{art["title"][:40]}: reweigh: {it["span"][:60]}')
        items.append(it)
    for nk in d['not_kept']:
        if any(nk['span'].startswith(a[1][:40]) for a in ADD if (iid.endswith(a[0]) or a[0] in art['title'])):
            log.append(f'{art["title"][:40]}: not-kept sentence now kept: {nk["span"][:60]}'); continue
        not_kept.append(nk)
    for suf, span, w, tier, who, why in ADD:
        if iid.endswith(suf) or suf in art['title']:
            assert span in art['text'], span
            items.append({'span': span, 'weight': w, 'tier': tier, 'who': who, 'rule': why, 'meaning': {}}); used.add(('ADD', span)); log.append(f'{art["title"][:40]}: add: {span[:60]}')
    qs = d['questions']
    for t, q in MAY_OPEN_ADD.items():
        if t in art['title']:
            qs.setdefault('may_open', []).append(q); used.add(('Q', t))
    for e in items + not_kept:
        assert e['span'] in art['text'], (iid, e['span'][:60])
        assert e['weight'] in (('core', 'supporting', 'optional') if e in items else ('not_kept', 'optional')), (iid, e['weight'])
    out.append({'set': 'test', 'input_id': iid, 'title': art['title'], 'publication_day': art['publication_day'], 'items': items,
                'not_kept': not_kept, 'questions': qs, 'notes': d.get('notes', [])})
expected = set(TO_NOT_KEPT) | set(REWEIGH) | {('ADD', a[1]) for a in ADD} | {('Q', t) for t in MAY_OPEN_ADD}
assert used == expected, expected - used
version = int(re.search(r'<meta name="standard-version" content="(\d+)">', PAGE.read_text()).group(1))
gold = {'standard_version': version, 'about': 'Test-set gold (D244): 30 articles from 2026-09-01..10-27 (test-pick.json), drafted by three readers from the signed page, '
        'checked against a blind read, disagreements decided against the text (finalize_test.py). Model-authored. Scored once per configuration; never tuned on.',
        'standard': 'docs/prd/05-extraction-standard.html', 'articles': out}
path = HERE / 'golden-test-signed.json'
path.write_text(json.dumps(gold, ensure_ascii=False, indent=1) + '\n')
(HERE / 'finalize-test-log.txt').write_text('\n'.join(log) + '\n')
from collections import Counter
print(Counter(it['weight'] for a in out for it in a['items']), Counter(n['weight'] for a in out for n in a['not_kept']))
print('questions', Counter(k for a in out for k in ('must_open', 'may_open', 'must_not') for _ in a['questions'].get(k, [])))
print(len(log), 'changes'); print(hashlib.sha256(path.read_bytes()).hexdigest())
