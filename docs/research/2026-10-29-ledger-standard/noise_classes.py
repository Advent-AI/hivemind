"""Count the gold's not-kept sentences an answer kept, by the gold's reason, per draw (a lead for which noise class to
take next; the sentences themselves are read). python3 noise_classes.py GOLD TAG [TAG ...]"""
import collections, json, sys
import score_gold as sg
gold = {a['input_id']: a for a in json.loads(open(sys.argv[1]).read())['articles']}
def rowclass(r):
    r = r or ''
    for k, lab in [('D243 第 5', 'common-knowledge claim'), ('背景', 'background/framing'), ('产品', 'product detail'), ('股价', 'share price/positions'),
                   ('重述', 'restatement'), ('重提', 'restatement'), ('复述', 'same fact retold'), ('模板', 'template'), ('D238', 'other firm valuation/deal'),
                   ('看法', 'author view/risk list'), ('新加坡', 'Singapore case'), ('政治', 'political statement'), ('形容', 'characterising quote'), ('按留的规则', 'not evidence (5.1)'), ('5.1', 'not evidence (5.1)')]:
        if k in r:
            return lab
    return 'other'
for tag in sys.argv[2:]:
    c = collections.Counter()
    for iid, row in sg.answers(tag).items():
        if iid not in gold:
            continue
        s = sg.kept(row, iid)
        if not s:
            continue
        a = gold[iid]
        for e in s['evidence']:
            if any(sg.same(it['span'], e['quote']) for it in a['items']):
                continue
            nk = [n for n in a['not_kept'] if sg.same(n['span'], e['quote']) and n['weight'] == 'not_kept']
            if nk:
                c[rowclass(nk[0].get('row'))] += 1
    print(tag, sum(c.values()), dict(c.most_common()))
