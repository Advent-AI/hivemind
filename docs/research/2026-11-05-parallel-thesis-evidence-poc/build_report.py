# -*- coding: utf-8 -*-
"""Render the diagnostic and its original prompts, articles and raw answers for inspection."""
import html,json,sqlite3,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT/'src'))
from hivemind import testdb
from prepare import ARTICLES
RUN=ROOT/'poc/data/parallel-thesis-evidence-poc-2026-11-05'
esc=lambda s:html.escape(str(s),quote=True)
frozen=json.loads((HERE/'frozen-requests.json').read_text())
c=sqlite3.connect(str(ROOT/'poc/data/parallel-thesis-evidence-input-2026-11-05/items.sqlite'));c.row_factory=sqlite3.Row
results=[]
for ident,seq in ARTICLES:
 item=testdb.item_of(c.execute('select * from items where input_id=?',(ident,)).fetchone());arms={}
 for arm in ('control','new','existing'):
  arms[arm]=json.loads((RUN/(ident.replace(':','_')+'-'+arm)/'result.json').read_text())
 results.append((item,seq,arms))
c.close()
notes=[
 '单 prompt 开了 FY2027 总收入问题，但季度总收入及下一季度收入指引均因没有关联问题而丢弃。新观点 prompt 开了 Azure 收入问题并保留两条 Azure 证据，但没有开总收入问题；旧观点 prompt 找到一条资本开支信息。',
 '旧观点 prompt 把 FY2028 增长约 70%、市场预期 44%、无供应约束超过 100% 一起挂到已有问题 v70。对照也挂到 v70，但摘要没写 44%。旧观点一路把若干宽泛的循环融资观点挂到具体担保问题 v1；相关性要谨慎核查。',
 '旧观点 prompt 把 1080 亿美元季度指引挂到全年收入问题，但“假设中国没有计算产品销售”没有关联而被丢弃。新观点 prompt 提出 2790 亿美元采购承诺问题，编号为 n1。对照提出 FY2028 毛利率问题。',
 '已有问题 v22 是 DLSS 5 是否在年底前发布。两种方法都找到了发布时点及相关信息；新观点一路没有再开问题。对照把提前流出的版本与正式发布时间拆成两条，并行旧证据一路合在一起。'
]
def evidence(e):
 return '<div class="ev"><div class="evtop"><b>'+esc(e['id'])+'</b><span>关联：'+esc(', '.join(e['links']) or '无')+'</span></div><p>'+esc(e['one_line'])+'</p><blockquote>'+esc(e['quote'])+'</blockquote><small>来源：'+esc(e.get('speaker',''))+' · 原始发言人：'+esc(e.get('original_who','') or '未写')+' · 原始日期：'+esc(e.get('original_day','') or '未写')+' · 类型：'+esc(e.get('tier',''))+'</small></div>'
def armcard(arm,r):
 title={'control':'单 prompt 对照','new':'新观点 + 文章证据','existing':'已有观点的证据'}[arm];h=r['handover'];chunks=['<section class="arm"><h4>'+title+'</h4><p class="meta">原始抽取 '+str(len(r['answer']['evidence']))+' 条 · 检查后 '+str(len(h['evidence']))+' 条 · 新问题 '+str(len(h['candidates']))+' 个</p>']
 for q in h['candidates']:
  chunks.append('<div class="question"><b>新问题 '+esc(q['id'])+'</b><p>'+esc(q['question'])+'</p><small>关联证据：'+esc(', '.join(q['evidence_ids']))+'</small></div>')
 for e in h['evidence']:chunks.append(evidence(e))
 if h['dropped']:chunks.append('<details><summary>被丢掉或合并的内容（'+str(len(h['dropped']))+'）</summary><pre>'+esc(json.dumps(h['dropped'],ensure_ascii=False,indent=2))+'</pre></details>')
 chunks.append('<details><summary>查看这一路的完整原始模型回答</summary><pre>'+esc(json.dumps(r['answer'],ensure_ascii=False,indent=2))+'</pre></details></section>');return ''.join(chunks)
css='''*{box-sizing:border-box}body{font:16px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f5f6f2;color:#172825;margin:0}main{max-width:1360px;margin:auto;padding:36px 26px 100px}h1{font-size:34px;line-height:1.2;margin:12px 0}h2{font-size:25px;margin:36px 0 12px}h3{font-size:21px;margin:0}.lead{font-size:19px;color:#50615b;max-width:960px}.tag{display:inline-block;border-radius:30px;background:#dcebe0;color:#2d6244;padding:4px 12px;font-weight:700}.card,.case{background:#fff;border:1px solid #dde5de;border-radius:16px;padding:22px;margin:14px 0}.warning{background:#fff8e6;border-left:5px solid #c48a25}.flow{display:grid;grid-template-columns:1fr 1fr;gap:14px}.box{border:1px solid #cbdad1;border-radius:12px;background:#eff6f0;padding:18px}.shared{grid-column:span 2;text-align:center;background:#e1eee6}.arrow{grid-column:span 2;text-align:center;font-size:24px;color:#64816f;line-height:1}.three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.arm{border:1px solid #e1e8e1;border-radius:12px;padding:15px;min-width:0}.arm h4{margin:0;font-size:17px}.meta,small{color:#65746d}.ev,.question{border-top:1px solid #e6ece6;padding:12px 0}.ev p,.question p{margin:5px 0}.evtop{display:flex;justify-content:space-between;gap:8px;font-size:13px}.evtop span{color:#397051}blockquote{margin:8px 0;border-left:3px solid #c2d4c5;padding-left:10px;color:#64736b;font-size:13px}details{margin:10px 0}summary{cursor:pointer;color:#28634e;font-weight:650}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f6f3;border-radius:8px;padding:14px;font:12px/1.5 ui-monospace,monospace;max-height:600px;overflow:auto}.case-head{display:flex;gap:14px;align-items:baseline;flex-wrap:wrap}.number{font-size:13px;color:#38745b;font-weight:800}.takeaway{background:#f0f6f0;padding:13px;border-radius:8px}.case>details>summary{font-size:18px}a{color:#256b51}@media(max-width:900px){.three,.flow{display:block}.box,.arm{margin:10px 0}main{padding:20px 15px}.arrow{margin:8px}}'''
chunks=['<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>拆分观点和证据 · POC</title><style>'+css+'</style><main><span class="tag">真实 POC · 2026-11-05 · 每组各跑一次</span><h1>把新观点和已有观点的证据分开</h1><p class="lead">同一篇文章、同一份最新题库，交给两条同时运行的 prompt。下面可以逐篇看原文、模型原始回答、保留下来的证据和被丢掉的内容。</p><div class="card warning"><b>目前的结论：拆分值得继续研究，但这次不能证明更好。</b>微软的全年收入新问题在拆分版里漏了；已有问题的证据有找得更完整的例子，也有遗漏和关联不清楚的例子。4 篇文章、每组 1 次，只是诊断。还没有跑真实的匹配、写入和最终判断。</div><h2>流程怎么走</h2><div class="flow"><div class="box shared"><b>同一篇真实文章 + 文章到来前的已有问题快照</b><br>两路看到完全相同的输入；不带 22 个预设题，也不额外导入财报。</div><div class="arrow">↓ 同时开始 ↓</div><div class="box"><b>A · 找新观点</b><p>找题库没有的新问题，并把这篇文章里能支持或反驳它的证据一起带出来。</p></div><div class="box"><b>B · 找旧观点的证据</b><p>只找能支持或反驳已有问题的文章信息，不创建问题。</p></div><div class="arrow">↓ 两路完成后汇合 ↓</div><div class="box shared"><b>按各自编号检查原文、保留关联，再并排展示</b><br>重复原句只标为可能重叠，不偷偷合并。真正的匹配、入库和判断还没在这个 POC 中验证。</div></div><div class="card"><b>为什么 A 一定要带证据？</b> B 开始时看不到 A 刚创建的问题；如果 A 只提问题，不带文章证据，那些证据可能没有地方去。</div><h2>测试发现</h2><div class="card warning"><b>需要处理的编号风险：</b>一次真实输出把新问题编号为 n1。现有 handover 代码有一处只按 c+数字识别新问题。用这次输出构造失败场景时，问题被丢掉后，证据仍可能指向不存在的 n1；本次真实输出中的 n1 仍然存活，未实际出现这条失败。它说明接入生产前需要修好并验证，而不是说此次已写入错误数据。</div><div class="card"><b>测试条件：</b>4 篇历史文章；单 prompt 4 次，两个并行 prompt 各 4 次。每次是一轮。题库从过去测试记录中重建到文章到来之前，每篇 69 个问题，属于实验配置；生产当前不一定这样读取。微软文章上游只标了 AI 资本开支，本实验为三组统一补了 MSFT 标签。文章及日期来自保存的数据，未另行核实原始报道。<a href="independent-review.md">查看独立逐条复核</a>。</div><h2>逐篇看原文和输出</h2>']
for i,(item,seq,arms) in enumerate(results):
 snap=next(x['snapshot'] for x in frozen if x['id']==item['input_id'])
 chunks+=['<article class="case"><div class="case-head"><span class="number">0'+str(i+1)+'</span><h3>'+esc(item.get('title') or item['input_id'])+'</h3></div><p class="takeaway">'+esc(notes[i])+'</p><p class="meta">文章 ID '+esc(item['input_id'])+' · 历史处理序号 '+str(seq)+' · 快照 '+str(len(snap))+' 个问题</p><details><summary>查看完整文章原文</summary><pre>'+esc(item['text'])+'</pre></details><details><summary>查看这篇文章看到的完整题库</summary><pre>'+esc('\n'.join(v['view_id']+' | '+v['question'] for v in snap))+'</pre></details><div class="three">']
 for arm in ('control','new','existing'):chunks.append(armcard(arm,arms[arm]))
 chunks.append('</div></article>')
chunks.append('<h2>两套实际使用的 prompt</h2><div class="card"><p>以下是系统指令原文。每次调用还附带文章、题库、分类说明和输出格式；完整请求保存在 <a href="frozen-requests.json">frozen-requests.json</a>。</p>')
for title,name in [('A · 新观点 + 文章内证据','new-thesis.txt'),('B · 已有观点的证据','existing-evidence.txt')]:chunks.append('<details><summary>'+title+'：展开原文</summary><pre>'+esc((HERE/name).read_text())+'</pre></details>')
chunks.append('</div><p class="meta">实验调用结束于抽取检查交接；未改变线上默认配置。独立复核已完成。</p></main></html>')
(HERE/'report.html').write_text(''.join(chunks));print(HERE/'report.html')
