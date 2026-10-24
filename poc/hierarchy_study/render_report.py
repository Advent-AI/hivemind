"""Build a self-contained review surface for the completed experiment, without network calls."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    root = Path(args.out)
    source = json.loads((root / 'input.json').read_text())['snapshots'][-1]
    variants = []
    names = {
        'A_density': 'A · Vector density', 'B_graph': 'B · Dependency communities',
        'C_global_llm': 'C · Global LLM grouping', 'D_incremental_llm': 'D · Incremental grouping',
        'E_argument-first': 'E · Main thesis first',
    }
    for sample in [1, 2, 3]:
        folder = root / f'sample-{sample}'
        for method, name in names.items():
            if method.startswith('E'):
                path = folder / 'E_result.json'
                if not path.exists():
                    continue
                value = json.loads(path.read_text())
                partition = None
                unused = value['unused_ids']
            else:
                path = folder / f'{method}-heads.json'
                if not path.exists():
                    continue
                value = json.loads(path.read_text())
                partition = json.loads((folder / f'{method}-partition.json').read_text())
                unused = partition['unassigned']
            probe = json.loads((folder / f'{method}-agent.json').read_text())['answer']
            checks = json.loads((folder / f'{method}-agent-checks.json').read_text())
            variants.append({'key': f'{method}-{sample}', 'name': f'{name} · sample {sample}', 'heads': value['heads'], 'partition': partition, 'unused': unused, 'probe': probe, 'checks': checks})
    budget = json.loads((root / 'budget.json').read_text())
    payload = json.dumps({'variants': variants, 'source': source, 'budget': budget}, ensure_ascii=False).replace('<', '\\u003c')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Main thesis experiments</title>
<style>
:root{font-family:system-ui,sans-serif;color:#18241c;background:#f5f4ef}*{box-sizing:border-box}body{margin:0}header{padding:30px 5vw 22px;background:white;border-bottom:1px solid #dddcd3}h1{font-size:26px;margin:0 0 8px}p{line-height:1.6}header p{margin:6px 0;color:#626a61}.controls{display:flex;flex-wrap:wrap;gap:12px;margin-top:20px}select,button{font:inherit;background:white;border:1px solid #cbcfc5;border-radius:7px;padding:9px 12px}button{cursor:pointer}button.active{background:#18241c;color:white}main{max-width:1320px;margin:28px auto;padding:0 24px;display:grid;grid-template-columns:minmax(0,1.7fr) minmax(280px,1fr);gap:24px}article,.panel{background:white;border:1px solid #deded3;border-radius:12px;padding:24px;margin-bottom:18px}h2{font-size:19px;margin:0 0 12px}h3{font-size:15px;margin:20px 0 8px}small,.muted{color:#70786c}.claim{padding:12px 0;border-top:1px solid #ededdf;line-height:1.6}.pill{display:inline-block;font-size:12px;font-weight:600;padding:2px 8px;border-radius:5px;background:#f0f2eb;margin-right:8px}.refs{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}.refs button{font-size:12px;padding:3px 7px}li{line-height:1.6;margin:5px 0}aside{position:sticky;top:20px;align-self:start;max-height:85vh;overflow:auto}.atomic-title{font-size:17px}.empty{padding:30px;color:#64725f}#summary{font-size:13px}details{margin-top:14px}summary{cursor:pointer;font-weight:600}blockquote{margin:12px 0;padding-left:14px;border-left:2px solid #bdc6b3;color:#5e6858;line-height:1.6}@media(max-width:800px){main{display:block}aside{position:static;max-height:none}}
</style><header><h1>Main thesis experiments</h1><p>31 real atomic theses · five approaches · three independent samples</p><p>Research prototype. Main theses are generated interpretations with traceable references, not validated forecasts.</p><div class="controls"><select id="variant" aria-label="Method and sample"></select><button id="heads" class="active">Main theses</button><button id="agent">Agent answers</button><button id="groups">Membership</button></div><p id="summary"></p></header><main><div id="content"></div><aside id="detail" class="panel"><h2>Inspect the support</h2><p>Select an atomic thesis reference to read its actual stored judgement and evidence.</p></aside></main><script id="study-data" type="application/json">__DATA__</script><script>
const data=JSON.parse(document.querySelector('#study-data').textContent);
const select=document.querySelector('#variant');
let mode='heads';
const make=(tag,text,cls)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;};
for(const v of data.variants){const o=make('option',v.name);o.value=v.key;select.append(o);}
select.value=data.variants.find(v=>v.key==='E_argument-first-1')?.key||data.variants[0].key;
function refs(ids){const div=make('div',undefined,'refs');for(const id of ids){const b=make('button',id);b.onclick=()=>detail(id);div.append(b);}return div;}
function list(parent,title,values){if(!values?.length)return;parent.append(make('h3',title));const ul=make('ul');for(const value of values)ul.append(make('li',value));parent.append(ul);}
function detail(id){const t=data.source.theses.find(t=>t.id===id);if(!t)return;const box=document.querySelector('#detail');box.replaceChildren(make('small',`${t.id} · ${t.object}`),make('h2',t.question,'atomic-title'),make('p',`Due: ${t.due_day}`));if(t.assessment){box.append(make('h3',`${t.assessment.label} · ${t.assessment.condition}`),make('p',t.assessment.reasons));}else box.append(make('p','Not assessed at this snapshot.'));for(const e of t.evidence){const d=make('details');d.append(make('summary',`${e.evidence_id} · ${e.original_who||e.tier}`),make('p',e.one_line),make('blockquote',e.quote));box.append(d);}}
function render(){const v=data.variants.find(v=>v.key===select.value);const content=document.querySelector('#content');content.replaceChildren();document.querySelector('#summary').textContent=`${v.heads.length} main-thesis entries · ${v.unused.length} unassigned/unused atomic theses · as of 2026-08-15. Citation validity is a structural check, not a truth score.`;for(const key of ['heads','agent','groups'])document.querySelector('#'+key).classList.toggle('active',mode===key);if(mode==='heads'){for(const h of v.heads){const a=make('article');a.append(make('small',`${h.group_id} · ${h.status}`),make('h2',h.title),make('p',h.thesis));for(const c of h.claims){const row=make('div',undefined,'claim');row.append(make('span',c.relation,'pill'),make('span',c.text),refs(c.view_ids));a.append(row);}list(a,'Limitations',h.limitations);list(a,'What would change the view?',h.watch_questions);content.append(a);}}else if(mode==='agent'){if(!v.checks.valid){const warning=make('article');warning.append(make('h2','Reference validation failed'),make('p',v.checks.errors.join('; ')));content.append(warning);}for(const answer of v.probe.answers){const a=make('article');a.append(make('h2',answer.question_id),make('p',answer.answer),refs(answer.drill_down_ids));list(a,'Limitations',answer.limitations);content.append(a);}}else{if(v.partition){for(const g of v.partition.groups){const a=make('article');a.append(make('h2',g.title),make('p',g.scope),refs(g.members));content.append(a);}}else{content.append(make('p','Argument-first output allows shared support. There is no exclusive partition.','empty'));for(const h of v.heads){const a=make('article');a.append(make('h2',h.title),refs([...new Set(h.claims.flatMap(c=>c.view_ids))]));content.append(a);}}const a=make('article');a.append(make('h2','Unassigned / unused'),refs(v.unused));content.append(a);}}
select.onchange=render;for(const key of ['heads','agent','groups'])document.querySelector('#'+key).onclick=()=>{mode=key;render();};render();
</script></html>'''.replace('__DATA__', payload)
    (root / 'index.html').write_text(page)
    print(f'Wrote {len(variants)} experiment views to {root / "index.html"}')


if __name__ == '__main__':
    main()
