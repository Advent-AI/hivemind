/** Exercise page navigation with real DOM and a controlled, stored-response service. */
import fs from 'node:fs/promises';
import { current } from './test/fixtures.js';

const sourcePage = await fs.readFile(new URL('../mock/index.html', import.meta.url), 'utf8');
if (!sourcePage.includes('<body class="hm-ui demo">')) throw new Error('Fixture shell changed');
const page = sourcePage
  .replace('<head>', '<head><base href="../../mock/">')
  .replace(
    '<body class="hm-ui demo">',
    '<body class="hm-ui demo" data-api="http://127.0.0.1:8002">',
  );
const card = await fs.readFile(
  new URL('./test/fixtures/idea-composite-default.json', import.meta.url),
  'utf8',
);
const fixture = `<div id="navigation-checks" style="position:fixed;top:60px;right:12px;z-index:40;background:white;padding:10px;border-radius:8px;font:12px sans-serif"><button id="check-navigation">Run navigation checks</button><button id="fixture-progress">Progress request</button><button id="fixture-finish">Finish request</button><button id="fixture-fail">Fail request</button><div id="navigation-result" role="status">Ready</div><pre id="fixture-network"></pre></div>
<script>
const fixtureData=${JSON.stringify(current).replaceAll('<', '\\u003c')};
const fixtureCard=${card.replaceAll('<', '\\u003c')};
let fixtureRequest=null,fixturePosts=0,fixtureAborts=0;
const fixtureEncoder=new TextEncoder();
const networkStatus=()=>document.querySelector('#fixture-network').textContent=JSON.stringify({posts:fixturePosts,aborts:fixtureAborts,pending:!!fixtureRequest});
const emit=(request,event)=>request.controller.enqueue(fixtureEncoder.encode(JSON.stringify(event)+String.fromCharCode(10)));
window.fetch=async(url,options={})=>{
 const path=new URL(url,location.href).pathname;
 if(path==='/library'||path==='/thesis-bundles')return new Response(JSON.stringify(fixtureData),{headers:{'Content-Type':'application/json'}});
 if(path!=='/ideas'||options.method!=='POST')throw new Error('Unexpected fixture request '+path);
 const request={text:JSON.parse(options.body).text,controller:null};
 fixtureRequest=request;fixturePosts++;
 const stream=new ReadableStream({start(controller){request.controller=controller;emit(request,{type:'progress',stage:'search'});}});
 options.signal.addEventListener('abort',()=>{if(fixtureRequest!==request)return;fixtureAborts++;fixtureRequest=null;request.controller.error(new DOMException('Aborted','AbortError'));networkStatus();},{once:true});
 networkStatus();return new Response(stream,{headers:{'Content-Type':'application/x-ndjson'}});
};
document.querySelector('#fixture-progress').onclick=()=>{for(const stage of ['decompose','retrieve','map'])emit(fixtureRequest,{type:'progress',stage});};
document.querySelector('#fixture-finish').onclick=()=>{const r=fixtureRequest;emit(r,{type:'result',data:{...fixtureCard,idea:{...fixtureCard.idea,text:r.text}}});r.controller.close();fixtureRequest=null;networkStatus();};
document.querySelector('#fixture-fail').onclick=()=>{const r=fixtureRequest;emit(r,{type:'error',status:502,message:'Fixture unavailable'});r.controller.close();fixtureRequest=null;networkStatus();};
networkStatus();
</script>`;
const checks = `<script>
const navFrame=()=>new Promise(resolve=>requestAnimationFrame(resolve));
const navAssert=(ok,message)=>{if(!ok)throw new Error(message)};
const navUntil=async(test)=>{const start=performance.now();while(!test()){navAssert(performance.now()-start<3000,'Timed out');await navFrame();}};
const navClick=id=>document.getElementById(id).click();
const navRoot=()=>document.querySelector('#explorer');
const navTitle=()=>navRoot().querySelector('.card--idea .card__q')?.textContent;
function navSubmit(text){if(document.querySelector('#idea-form').hidden)navClick('idea-launcher');const input=document.querySelector('#ask');input.value=text;input.dispatchEvent(new Event('input',{bubbles:true}));document.querySelector('#idea-form').requestSubmit();}
function navSnapshot(){return JSON.stringify({title:navTitle(),camera:navRoot().querySelector('.world').style.transform,canvas:navRoot().querySelector('marker').id,day:navRoot().querySelector('.replay [data-day]').textContent,slider:navRoot().querySelector('.replay input').value,range:navRoot().querySelector('.ranges [aria-pressed="true"]').textContent,allocation:navRoot().querySelector('.action__allocation input')?.value??null,marketRange:navRoot().querySelector('[data-market-range][aria-pressed="true"]')?.textContent??null,threshold:navRoot().querySelector('.trigger__threshold input')?.value??null,cards:[...navRoot().querySelectorAll('.card')].map(n=>n.dataset.id),edges:[...navRoot().querySelectorAll('.edge')].map(n=>n.getAttribute('d'))});}
document.querySelector('#check-navigation').onclick=async()=>{
 const status=document.querySelector('#navigation-result');status.textContent='Running';
 try{
  navClick('show-idea');navSubmit('First retained idea');
  await navUntil(()=>!!fixtureRequest);navClick('show-library');
  navAssert(fixtureAborts===0,'Navigation aborted the pending request');
  navAssert(navTitle()==='First retained idea','Navigation removed the pending card');
  navClick('fixture-progress');await navFrame();await navFrame();
  navClick('show-idea');
  await navUntil(()=>navRoot().querySelectorAll('.idea-progress__step').length===4);
  navAssert(fixturePosts===1&&fixtureAborts===0,'Returning changed the request');
  navClick('show-library');navClick('fixture-finish');
  await navUntil(()=>document.querySelector('#idea-form').getAttribute('aria-busy')==='false');
  navAssert(navRoot().hidden,'Background result changed navigation');
  navClick('show-idea');
  await navUntil(()=>navRoot().querySelectorAll('.card').length===6);
  navRoot().querySelector('[data-zoom="2"]').click();await navFrame();await navFrame();
  for(const path of navRoot().querySelectorAll('.edge')){
   const source=navRoot().querySelector('.card[data-id="'+path.dataset.source+'"]'),target=navRoot().querySelector('.card[data-id="'+path.dataset.target+'"]');
   const start=path.getPointAtLength(0),end=path.getPointAtLength(path.getTotalLength());
   navAssert(Math.abs(start.x-source.offsetLeft-source.offsetWidth)<1&&Math.abs(end.x-target.offsetLeft)<1,'Hidden result created detached connectors');
  }
  navRoot().querySelector('[data-range="30d"]').click();
  const slider=navRoot().querySelector('.replay input');slider.value=String(Math.floor(Number(slider.max)/2));slider.dispatchEvent(new Event('input',{bubbles:true}));
  navRoot().querySelector('[data-zoom="0"]').click();await navFrame();await navFrame();
  const saved=navSnapshot();
  for(let i=0;i<3;i++){navClick('show-library');navClick('show-idea');navAssert(navSnapshot()===saved,'Completed view changed across navigation');navAssert(!navRoot().querySelector('.is-revealing'),'Navigation restarted the reveal');}
  navAssert(fixturePosts===1&&fixtureAborts===0,'Navigation sent or aborted a request');
  navSubmit('Retained failure');await navUntil(()=>!!fixtureRequest);navClick('show-library');navClick('fixture-fail');
  await navUntil(()=>document.querySelector('#idea-form').getAttribute('aria-busy')==='false');navClick('show-idea');await navFrame();
  navAssert(navTitle()==='Retained failure'&&navRoot().textContent.includes('Fixture unavailable'),'Background error was not retained');
  const failed=navSnapshot();navClick('show-library');navClick('show-idea');navAssert(navSnapshot()===failed,'Error view was cleared');
  navSubmit('Replacement idea');await navUntil(()=>!!fixtureRequest);navClick('fixture-finish');
  await navUntil(()=>navRoot().querySelectorAll('.card').length===6);navRoot().querySelector('[data-zoom="2"]').click();
  navAssert(navTitle()==='Replacement idea','New query did not replace the old one');
  navAssert(fixturePosts===3&&fixtureAborts===0,'Unexpected request count');
  status.textContent='Passed: navigation retention; 3 queries, 0 aborts';
 }catch(error){status.textContent='FAILED: '+error.message;throw error;}
};
</script>`;
const start = page.lastIndexOf('<script>');
const html = (page.slice(0, start) + fixture + page.slice(start)).replace(
  '</body>',
  () => checks + '</body>',
);
await fs.mkdir(new URL('./dist/', import.meta.url), { recursive: true });
await fs.writeFile(new URL('./dist/navigation-check.html', import.meta.url), html);
console.log('Wrote poc/ui/dist/navigation-check.html');
