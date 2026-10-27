/** Build a real-browser fixture for the default reveal and its cancellation paths. */
import fs from 'node:fs/promises';

const page = await fs.readFile(new URL('../mock/index.html', import.meta.url), 'utf8');
const css = page.match(/<style>([\s\S]*?)<\/style>/)[1];
const data = page.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const market = page.match(
  /<script id="market-data" type="application\/json">([\s\S]*?)<\/script>/,
)[1];
const script = page.slice(page.lastIndexOf('<script>') + 8, page.lastIndexOf('</script>'));
const card = await fs.readFile(
  new URL('./test/fixtures/idea-composite-default.json', import.meta.url),
  'utf8',
);
const empty = await fs.readFile(
  new URL('./test/fixtures/idea-card-empty.json', import.meta.url),
  'utf8',
);
const html = `<!doctype html><html><head><meta charset="utf-8"><title>Tree reveal verification</title>
<link rel="stylesheet" href="../../../web/design-system/fonts-embedded.css"><style>${css}
body{margin:0;height:100vh;display:flex;flex-direction:column;background:var(--paper)}
.controls{padding:12px;display:flex;gap:12px;align-items:center}#fixture{flex:1;min-height:0}
#trace{position:fixed;right:12px;bottom:12px;max-width:420px;max-height:170px;overflow:auto;background:white;font:12px monospace;z-index:9}
</style></head><body class="hm-ui"><div class="controls"><button id="run">Run reveal</button><button id="fit">Cancel with Fit</button><button id="replace">Replace during reveal</button><button id="destroy">Destroy during reveal</button><button id="empty">Empty result</button><span id="result" role="status">Ready</span></div><main id="fixture"></main><pre id="trace"></pre>
<script>${script}</script><script>
const market=${market},data=${data},card=${card.replaceAll('<', '\\u003c')},empty=${empty.replaceAll('<', '\\u003c')};
const root=document.querySelector('#fixture'),result=document.querySelector('#result'),trace=document.querySelector('#trace');
let app=Hivemind.createThesisExplorer(root,{dataset:data});
const composite=Hivemind.prepareIdeaComposite(card,data);
const frame=()=>new Promise(resolve=>requestAnimationFrame(resolve));
const assert=(ok,message)=>{if(!ok)throw new Error(message)};
const stage=()=>root.querySelector('.stage');
const pose=()=>root.querySelector('.world').style.transform;
const camera=()=>new DOMMatrix(root.querySelector('.world').style.transform);
function show(value=card,reveal=true){
 app.showGraph({...Hivemind.graphOf(value),centerOn:'tree',center:true,reveal,
 action:{market},
 trigger:{getConfidence:()=>value===card?Hivemind.confidenceFromScore(Hivemind.compositeAt(composite,data.as_of)?.value??null):null},
 leadingCard:layout=>Hivemind.ideaCard({...layout,text:value.idea.text,state:'answered',card:value,composite:value===card?composite:null})});
}
async function until(test){const start=performance.now();while(!test()){assert(performance.now()-start<15000,'Timed out');await frame();}}
function visible(){return [...root.querySelectorAll('.card')].every(n=>getComputedStyle(n).opacity==='1'&&!n.inert&&!n.hasAttribute('aria-hidden'))&&[...root.querySelectorAll('.edge')].every(p=>!p.style.strokeDashoffset&&!p.style.markerEnd);}
async function run(kind){
 result.textContent='Running '+kind;trace.textContent='';
 try{
  if(!root.querySelector('.stage'))app=Hivemind.createThesisExplorer(root,{dataset:data});
  show(kind==='empty'?empty:card);
  const samples=[],order=[];let partial=false,followed=false,lastPose=pose(),columnX=null,lastScanY=null,scanFrames=0;
  if(kind!=='run'&&kind!=='empty'){
   await until(()=>stage().dataset.revealPhase==='line');
   if(kind==='fit')app.fit();
   if(kind==='replace')show(empty,false);
   if(kind==='destroy')app.destroy();
   const settledPose=kind==='destroy'?null:pose();
   const start=performance.now();while(performance.now()-start<1200)await frame();
   if(kind==='destroy')assert(!root.querySelector('.stage'),'Destroyed canvas came back');
   else{
    assert(!stage().classList.contains('is-revealing'),'Cancellation remained active');
    assert(pose()===settledPose,'Cancelled camera moved later');assert(visible(),'Cancelled cards or paths remained hidden');
    if(kind==='replace')assert(root.querySelectorAll('.card').length===3,'Old cards returned after replacement');
   }
  }else{
   do{
    const phase=stage().dataset.revealPhase,node=stage().dataset.revealNode;
    assert(phase!=='source','Camera returned to a connection source');
    if(phase==='card'&&order.at(-1)!==node)order.push(node);
    const trigger=root.querySelector('.card--trigger'),triggerPath=root.querySelector('.edge[data-source="trigger"]');
    const action=root.querySelector('.card--action');if(node!=='action')assert(getComputedStyle(action).opacity==='0'&&action.inert,'Action appeared before Trigger');
    if(node!=='trigger'&&node!=='action'){
     assert(getComputedStyle(trigger).opacity==='0'&&trigger.inert,'Trigger appeared before the theses finished');
     assert(triggerPath.style.opacity==='0','Trigger connector appeared early');
    }else{
     assert([...root.querySelectorAll('.card--thesis')].every(n=>getComputedStyle(n).opacity==='1'&&!n.inert),'Trigger preceded a thesis');
    }
    if(phase==='card'&&node!=='idea'&&node!=='trigger'&&node!=='action'&&columnX===null){columnX=camera().e;lastScanY=camera().f;}
    if(columnX!==null&&(phase==='line'||phase==='card')&&node!=='idea'&&node!=='trigger'&&node!=='action'){
     const at=camera();assert(Math.abs(at.e-columnX)<0.01,'Camera moved sideways between targets');
     assert(at.f<=lastScanY+0.01,'Camera moved upward between targets');lastScanY=at.f;scanFrames++;
    }
    const offsets=[...root.querySelectorAll('.edge')].map(p=>Number(p.style.strokeDashoffset)||0);
    if(phase==='line'){
     const target=root.querySelector('.card[data-id="'+node+'"]');
     assert(getComputedStyle(target).opacity==='0'&&target.inert,'Target appeared before its line arrived');
     partial ||= offsets.some(n=>n>0);followed ||= pose()!==lastPose;
    }
    if(samples.at(-1)?.phase!==phase||samples.at(-1)?.node!==node)samples.push({phase,node,pose:pose()});
    lastPose=pose();await frame();
   }while(stage().classList.contains('is-revealing'));
   const targets=[...root.querySelectorAll('.card--thesis')].sort((a,b)=>a.offsetTop+a.offsetHeight/2-b.offsetTop-b.offsetHeight/2);
   const expected=['idea',...targets.map(n=>n.dataset.id),'trigger','action'];
   assert(JSON.stringify(order)===JSON.stringify(expected),'Incorrect card sequence '+order);
   assert(visible(),'Final graph remained hidden: '+JSON.stringify([...root.querySelectorAll('.card')].map(n=>({id:n.dataset.id,opacity:getComputedStyle(n).opacity,inert:n.inert,hidden:n.hasAttribute('aria-hidden')}))));
   if(kind==='run'){assert(partial,'No partial line frame');assert(followed,'Camera did not move toward the targets');assert(scanFrames>0,'No vertical scan frames judged');}
   const box=stage().getBoundingClientRect(),nodes=[...root.querySelectorAll('.card')].map(n=>n.getBoundingClientRect());
   const left=Math.min(...nodes.map(n=>n.left)),right=Math.max(...nodes.map(n=>n.right));
   assert(Math.abs((left+right)/2-(box.left+box.right)/2)<1,'Final tree is not centred');
   const cardNodes=[...root.querySelectorAll('.card')];const span=Math.max(...cardNodes.map(n=>n.offsetLeft+n.offsetWidth))-Math.min(...cardNodes.map(n=>n.offsetLeft));const expectedZoom=Math.min(1,(stage().clientWidth-48)/span);assert(Math.abs(camera().a-expectedZoom)<.001,'Final zoom is not a horizontal fit');
  }
  trace.textContent=JSON.stringify({kind,order,partial,followed,scanFrames,samples},null,2);
  result.textContent='Passed: '+kind;
 }catch(error){result.textContent='FAILED: '+error.message;throw error;}
}
for(const kind of ['run','fit','replace','destroy','empty'])document.querySelector('#'+kind).onclick=()=>run(kind);
show(card,false);
</script></body></html>`;
await fs.mkdir(new URL('./dist/', import.meta.url), { recursive: true });
await fs.writeFile(new URL('./dist/reveal-check.html', import.meta.url), html);
console.log('Wrote poc/ui/dist/reveal-check.html');
