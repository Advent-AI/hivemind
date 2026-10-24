/** Generate a browser fixture for instance isolation and host-driven updates. */
import fs from 'node:fs/promises';

const page = await fs.readFile(new URL('../mock/index.html', import.meta.url), 'utf8');
const css = page.match(/<style>([\s\S]*?)<\/style>/)[1];
const data = page.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const script = page.slice(page.lastIndexOf('<script>') + 8, page.lastIndexOf('</script>'));
const fixture = `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../../../web/design-system/fonts-embedded.css"><style>${css}
body { margin:20px; background:var(--paper);font-family:var(--sans); } .hosts {display:grid;grid-template-columns:1fr 1fr;gap:16px;} .host {height:540px;border:1px solid var(--rule);margin-top:16px;} .test-actions {display:flex;gap:12px;flex-wrap:wrap;} .test-actions button {padding:10px;}</style></head><body class="hm-ui"><h1>Thesis component verification</h1><div class="test-actions"><button id="open-first">Open first</button><button id="open-second">Open second</button><button id="empty-history">Open before first assessment</button><button id="invalid">Reject invalid update</button><button id="destroy">Destroy first</button><button id="recreate">Recreate first</button></div><p id="result" role="status">Ready</p><div class="hosts"><div class="host" id="first"></div><div class="host" id="second"></div></div><script id="fixture-data" type="application/json">${data}</script><script>${script}</script><script>
const dataset=JSON.parse(document.querySelector('#fixture-data').textContent);
const primary=dataset.theses.find(t=>t.id==='v3') || dataset.theses[0];
let first=Hivemind.createThesisExplorer(document.querySelector('#first'),{dataset});
const second=Hivemind.createThesisExplorer(document.querySelector('#second'),{dataset});
first.showGraph({primaryId:primary.id});second.showGraph({primaryId:dataset.theses[0].id});
const result=document.querySelector('#result');
document.querySelector('#open-first').onclick=()=>first.openThesis(primary.id);
document.querySelector('#open-second').onclick=()=>second.openThesis(dataset.theses[0].id);
document.querySelector('#empty-history').onclick=()=>first.openThesis(dataset.theses.find(t=>t.judgements[0]?.day>dataset.days[0]).id,dataset.days[0]);
document.querySelector('#invalid').onclick=()=>{const bad=structuredClone(dataset);bad.theses[0].id=bad.theses[1].id;try{first.setDataset(bad);result.textContent='ERROR: accepted invalid data';}catch(error){result.textContent='Rejected: '+error.message;}};
document.querySelector('#destroy').onclick=()=>{first.destroy();result.textContent='First destroyed; second remains mounted';};
document.querySelector('#recreate').onclick=()=>{first.destroy();first=Hivemind.createThesisExplorer(document.querySelector('#first'),{dataset});first.showGraph({primaryId:primary.id});result.textContent='First recreated';};
const motionCheck=document.createElement('button');motionCheck.textContent='Check drawer motion';document.querySelector('.test-actions').append(motionCheck);
motionCheck.onclick=async()=>{
  const passed=[];
  const check=(condition,label)=>{if(!condition)throw new Error(label);passed.push(label);};
  const frame=()=>new Promise(resolve=>requestAnimationFrame(resolve));
  const wait=async(ms)=>{const start=performance.now();while(performance.now()-start<ms)await frame();};
  const sheet=()=>document.querySelector('#first .sheet');
  const panel=()=>document.querySelector('#first .sheet__panel');
  const close=()=>document.querySelector('#first .sheet-close').click();
  try{
    motionCheck.focus();first.openThesis(primary.id);await wait(65);
    const entering=panel().getBoundingClientRect();
    check(!sheet().hidden&&entering.right>innerWidth&&entering.left<innerWidth,'opening has an intermediate slide frame');
    await wait(300);check(Math.abs(panel().getBoundingClientRect().right-innerWidth)<1,'opening reaches the screen edge');
    close();await wait(65);check(!sheet().hidden&&panel().getBoundingClientRect().right>innerWidth,'closing remains visible while sliding');
    await wait(300);check(sheet().hidden&&document.activeElement===motionCheck,'closing hides and restores focus after exit');
    first.openThesis(primary.id);await wait(80);close();await wait(60);first.openThesis(primary.id);await wait(350);
    check(!sheet().hidden&&sheet().classList.contains('is-open')&&!sheet().classList.contains('is-transitioning'),'a reversed close finishes open');
    close();first.setDataset(dataset);await wait(320);check(sheet().hidden,'dataset replacement cancels the closing animation');
    first.openThesis(primary.id);await wait(70);first.destroy();await wait(320);check(!document.querySelector('#first .sheet'),'destroy cancels the opening animation');
    first=Hivemind.createThesisExplorer(document.querySelector('#first'),{dataset});first.showGraph({primaryId:primary.id});
    result.textContent='Passed '+passed.length+' drawer checks: '+passed.join('; ');
  }catch(error){result.textContent='FAILED: '+error.message;}
};
</script></body></html>`;
await fs.mkdir(new URL('./dist/', import.meta.url), { recursive: true });
await fs.writeFile(new URL('./dist/verify.html', import.meta.url), fixture);
console.log('Wrote poc/ui/dist/verify.html');

const response = await fs.readFile(
  new URL('./test/fixtures/idea-card-v3.json', import.meta.url),
  'utf8',
);
const routing = `<!doctype html><html><head><meta charset="utf-8"><title>Hivemind connector verification</title><link rel="stylesheet" href="../../../web/design-system/fonts-embedded.css"><style>${css}
body{margin:0;height:100vh;display:flex;flex-direction:column}.routing-controls{display:flex;align-items:center;gap:12px;padding:12px 24px;height:56px;flex-shrink:0}.routing-controls button{padding:6px 10px;border:1px solid var(--rule);border-radius:6px;background:white}#routing{flex:1;min-height:0}</style></head><body class="hm-ui"><div class="routing-controls"><b>Hivemind</b><button id="stored">Stored 12-branch graph</button><button id="small">Four branches</button><button id="dense">All loaded theses</button><button id="check">Check attached endpoints</button><span id="result" role="status"></span></div><div id="routing"></div><script>${script}</script><script>
const response=${response.replaceAll('<', '\\u003c')};
const allData=${data};
const stored=Hivemind.fromIdeaResponse(response);
const app=Hivemind.createThesisExplorer(document.querySelector('#routing'),{dataset:stored});
const primaryId=response.reading.chosen[0].view_id;
function show(dataset,limit){app.showGraph({});app.setDataset(dataset);app.showGraph({primaryId,supportingIds:dataset.theses.filter(t=>t.id!==primaryId).slice(0,limit).map(t=>t.id),center:true});document.querySelector('#result').textContent='';}
document.querySelector('#stored').onclick=()=>show(stored,Infinity);
document.querySelector('#small').onclick=()=>show(stored,4);
document.querySelector('#dense').onclick=()=>show(allData,Infinity);
document.querySelector('#check').onclick=()=>{
  const paths=[...document.querySelectorAll('.edge')];let checked=0;
  for(const path of paths){
    const source=document.querySelector('.card[data-id="'+path.dataset.source+'"]').getBoundingClientRect();
    const target=document.querySelector('.card[data-id="'+path.dataset.target+'"]').getBoundingClientRect();
    const matrix=path.getScreenCTM();
    const start=path.getPointAtLength(0).matrixTransform(matrix);
    const end=path.getPointAtLength(path.getTotalLength()).matrixTransform(matrix);
    if(Math.abs(start.x-source.right)>.75||start.y<source.top||start.y>source.bottom||Math.abs(end.x-target.left)>.75||Math.abs(end.y-(target.top+target.height/2))>.75){document.querySelector('#result').textContent='FAILED: detached '+path.dataset.target;return;}
    checked++;
  }
  document.querySelector('#result').textContent=checked?'Passed: '+checked+' attached connectors':'FAILED: no connectors';
};
show(stored,Infinity);
</script></body></html>`;
await fs.writeFile(new URL('./dist/routing.html', import.meta.url), routing);
console.log('Wrote poc/ui/dist/routing.html');

const empty = await fs.readFile(
  new URL('./test/fixtures/idea-card-empty.json', import.meta.url),
  'utf8',
);
const noMatch = await fs.readFile(
  new URL('./test/fixtures/idea-card-null.json', import.meta.url),
  'utf8',
);
const ideaPage = `<!doctype html><html><head><meta charset="utf-8"><title>Hivemind Idea graph</title><link rel="stylesheet" href="../../../web/design-system/fonts-embedded.css"><style>${css}
body{margin:0;height:100vh;display:flex;flex-direction:column}.test-controls{display:flex;align-items:center;gap:12px;padding:12px 24px;height:56px;flex-shrink:0}.test-controls button{padding:6px 10px;border:1px solid var(--rule);border-radius:6px;background:white}#preview{flex:1;min-height:0}</style></head><body class="hm-ui"><div class="test-controls"><b>Hivemind</b><button id="answer">Stored Idea</button><button id="empty">Empty mapping</button><button id="none">No recorded thesis</button><button id="verify">Check graph and headers</button><span id="result" role="status"></span></div><div id="preview"></div><script>${script}</script><script>
const cases={answer:${response.replaceAll('<', '\\u003c')},empty:${empty.replaceAll('<', '\\u003c')},none:${noMatch.replaceAll('<', '\\u003c')}};
let current=cases.answer;
const app=Hivemind.createThesisExplorer(document.querySelector('#preview'),{dataset:Hivemind.fromIdeaResponse(current)});
function show(card){current=card;app.showGraph({});app.setDataset(Hivemind.fromIdeaResponse(card));const dataset=app.getDataset();app.showGraph({...Hivemind.graphOf(card),leadingCard:()=>Hivemind.ideaCard({text:card.idea.text,state:'answered',card,scoreOf:position=>dataset.theses.find(t=>t.id===card.reading?.chosen[0]?.view_id)?.rungs.find(r=>r.position===position)?.score||String(position)}),center:true});document.querySelector('#result').textContent='';}
for(const name of Object.keys(cases))document.querySelector('#'+name).onclick=()=>show(cases[name]);
document.querySelector('#verify').onclick=()=>{
  const expected=[...(current.reading?.chosen||[]).map(c=>['idea',c.view_id]),...(current.related||[]).map(r=>[r.via,r.view_id])];
  const actual=[...document.querySelectorAll('.edge')].map(e=>[e.dataset.source,e.dataset.target]);
  const headers=[...document.querySelectorAll('.card__head')];
  const valid=JSON.stringify(actual)===JSON.stringify(expected)&&headers.every(h=>h.offsetHeight===40)&&!document.querySelector('.idea__parts');
  document.querySelector('#result').textContent=valid?'Passed: '+actual.length+' correct edges; '+headers.length+' matching headers':'FAILED: graph or header mismatch';
};
show(current);
</script></body></html>`;
await fs.writeFile(new URL('./dist/idea.html', import.meta.url), ideaPage);
console.log('Wrote poc/ui/dist/idea.html');
