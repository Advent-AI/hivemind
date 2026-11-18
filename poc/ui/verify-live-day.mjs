/** Proof 2f (live-service OPERATING-CONTRACT.md, row 3): the Idea call carries the page's day. A: the live library read succeeds, so the
 * Idea and its question bundles are asked as of the served day and the answer is shown. B: the live read fails, so the page keeps its
 * embedded day, later than the store's last completed day; the service refuses that day (409, as the API answers it) and the page shows
 * the Idea error while the library stays usable and a second sentence is sent again. Real stored data: the library and bundles come
 * from the ledger the stored card was made from (`english-v23-jev-2026-10-25`, last completed day 2026-08-15, the card's day) through
 * the product's own `bundle` functions; the sealed run's store does not hold the card's composite questions. Writes dist/live-day-check-a.html and -b.html, which run
 * their checks on load and write the outcome into #live-day-result. */
import fs from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { root } from './test/fixtures.js';

const sourcePage = await fs.readFile(new URL('../mock/index.html', import.meta.url), 'utf8');
if (!sourcePage.includes('<body class="hm-ui demo">')) throw new Error('Fixture shell changed');
const embeddedDays = [
  ...new Set([...sourcePage.matchAll(/"as_of":\s*"(\d{4}-\d{2}-\d{2})"/g)].map((m) => m[1])),
];
if (embeddedDays.length !== 1)
  throw new Error(`The shell embeds ${embeddedDays.length} days, not one`);
const embeddedDay = embeddedDays[0];
const card = JSON.parse(
  await fs.readFile(
    new URL('./test/fixtures/idea-composite-default.json', import.meta.url),
    'utf8',
  ),
);
const ids = [
  ...(card.reading?.chosen || []).map((c) => c.view_id),
  ...(card.related || []).map((r) => r.view_id),
];
const served = JSON.parse(
  execFileSync(
    'python3',
    [
      '-c',
      `
import json,sys
from pathlib import Path
root=Path(sys.argv[1]);sys.path.insert(0,str(root/'src'))
from hivemind import bundle,service
from hivemind.views import store
ledger=service.open_ledger(str(root/'poc/data/english-v23-jev-2026-10-25/views.sqlite'))
items=store.open_read_only(str(root/'poc/data/items-window-tags2-2026-10-24.sqlite'))
library=bundle.library(ledger,items,None)
print(json.dumps({'library':library,'bundles':bundle.thesis_bundles(ledger,items,sys.argv[2].split(','),library['as_of'])},ensure_ascii=False))
`,
      root,
      ids.join(','),
    ],
    { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 },
  ),
);
const servedDay = served.library.as_of;
if (!(servedDay < embeddedDay))
  throw new Error(`The served day ${servedDay} is not earlier than the embedded ${embeddedDay}`);
if (card.idea.as_of !== servedDay)
  throw new Error('The stored card is not dated on the served day');

const page = sourcePage
  .replace('<head>', '<head><base href="../../mock/">')
  .replace(
    '<body class="hm-ui demo">',
    '<body class="hm-ui demo" data-api="http://127.0.0.1:8002">',
  );
const escape = (value) => JSON.stringify(value).replaceAll('<', '\\u003c');

function fixture(liveDayCase) {
  return `<div id="live-day-checks" style="position:fixed;top:60px;right:12px;z-index:40;background:white;padding:10px;font:12px sans-serif"><button id="check-live-day">Run live-day checks (${liveDayCase})</button><pre id="live-day-result">Ready</pre></div>
<script>
const liveDayCase=${escape(liveDayCase)},servedDay=${escape(servedDay)},embeddedDay=${escape(embeddedDay)};
const servedLibrary=${escape(served.library)},servedBundles=${escape(served.bundles)},storedCard=${escape(card)};
const liveDaySeen={library:0,ideas:[],bundles:[],errors:[]};
window.addEventListener('error',(event)=>liveDaySeen.errors.push(String(event.message)));
window.addEventListener('unhandledrejection',(event)=>liveDaySeen.errors.push(String(event.reason)));
const liveDayJson=(body,status=200)=>new Response(JSON.stringify(body),{status,headers:{'Content-Type':'application/json'}});
window.fetch=async(url,options={})=>{
 const address=new URL(url,location.href);
 if(address.pathname==='/library'){liveDaySeen.library++;return liveDayCase==='A'?liveDayJson(servedLibrary):liveDayJson({error:'the service is unavailable (test)'},503);}
 if(address.pathname==='/ideas'&&options.method==='POST'){
  const body=JSON.parse(options.body);liveDaySeen.ideas.push(body.as_of??null);
  if(liveDayCase==='B'||body.as_of!==servedDay)return liveDayJson({error:'day not completed',requested:body.as_of??null,last_completed_day:servedDay},409);
  const encoder=new TextEncoder();
  const stream=new ReadableStream({start(controller){controller.enqueue(encoder.encode(JSON.stringify({type:'result',data:{...storedCard,idea:{...storedCard.idea,text:body.text}}})+String.fromCharCode(10)));controller.close();}});
  return new Response(stream,{headers:{'Content-Type':'application/x-ndjson'}});
 }
 if(address.pathname==='/thesis-bundles'){liveDaySeen.bundles.push(address.searchParams.get('as_of'));return liveDayJson(servedBundles);}
 throw new Error('Unexpected fixture request '+address.pathname);
};
</script>`;
}

const checks = `<script>
const ldFrame=()=>new Promise(resolve=>setTimeout(resolve,20)); // a timer, not a frame: headless Chrome may not paint frames
const ldAssert=(ok,message)=>{if(!ok)throw new Error(message)};
const ldUntil=async(test,what)=>{const start=performance.now();while(!test()){ldAssert(performance.now()-start<5000,'Timed out waiting for '+what);await ldFrame();}};
const ldClick=id=>document.getElementById(id).click();
const ldRoot=()=>document.querySelector('#explorer');
const ldTitle=()=>ldRoot().querySelector('.card--idea .card__q')?.textContent;
const ldIdle=()=>document.querySelector('#idea-form').getAttribute('aria-busy')==='false';
const ldLibraryCards=()=>[...document.querySelectorAll('#library .library-card .card__q')].map(q=>q.textContent.trim());
const ldLibraryCount=()=>Number(document.querySelector('#library [data-library-stats] b')?.textContent);
function ldSubmit(text){if(document.querySelector('#idea-form').hidden)ldClick('idea-launcher');const input=document.querySelector('#ask');input.value=text;input.dispatchEvent(new Event('input',{bubbles:true}));document.querySelector('#idea-form').requestSubmit();}
document.querySelector('#check-live-day').onclick=async()=>{
 const status=document.querySelector('#live-day-result');status.textContent='Running';
 try{
  await ldUntil(()=>liveDaySeen.library>0,'the live library read');for(let i=0;i<10;i++)await ldFrame();
  const before=ldLibraryCards(),beforeCount=ldLibraryCount();ldAssert(before.length>0,'The library shows no cards');
  if(liveDayCase==='A'){
   const expected=servedLibrary.views.filter(v=>v.created_day<=servedDay).length; // the library pages its cards (24 at a time); its count is the whole
   ldAssert(ldLibraryCount()===expected,'The library does not count the served library ('+ldLibraryCount()+', expected '+expected+')');
   ldClick('show-idea');ldSubmit('Live day idea');
   await ldUntil(()=>liveDaySeen.ideas.length===1&&ldIdle(),'the Idea answer');
   ldAssert(liveDaySeen.ideas[0]===servedDay,'The Idea was not asked as of the served day ('+liveDaySeen.ideas[0]+')');
   ldAssert(liveDaySeen.bundles.length===1&&liveDaySeen.bundles[0]===servedDay,'The question bundles were not asked as of the served day ('+liveDaySeen.bundles+')');
   await ldUntil(()=>ldTitle()==='Live day idea','the Idea card');
   const shown=storedCard.reading.chosen.map(c=>c.view_id);
   const present=()=>[...ldRoot().querySelectorAll('.card')].map(n=>n.dataset.id);
   try{await ldUntil(()=>shown.every(id=>present().includes(id)),'the chosen questions');}catch(error){throw new Error('The chosen questions '+shown+' are not shown; the cards are '+present()+'; the Idea card reads: '+(ldRoot().querySelector('.card--idea')?.textContent||'').replace(/\s+/g,' ').slice(0,400));}
   ldAssert(!ldRoot().textContent.includes('day not completed'),'An error is shown');
   status.textContent='Passed A: the library counts the served '+expected+' questions; Idea and bundles asked as of '+servedDay+'; '+shown.length+' questions shown; '+liveDaySeen.errors.length+' page errors';
  }else{
   ldClick('show-idea');ldSubmit('Late day idea');
   await ldUntil(()=>liveDaySeen.ideas.length===1&&ldIdle(),'the refused Idea');
   ldAssert(liveDaySeen.ideas[0]===embeddedDay,'The Idea was not asked as of the embedded day ('+liveDaySeen.ideas[0]+')');
   await ldUntil(()=>ldTitle()==='Late day idea'&&ldRoot().textContent.includes('day not completed'),'the Idea error');
   ldAssert(liveDaySeen.bundles.length===0,'Bundles were asked after a refused Idea');
   ldClick('show-library');await ldFrame();
   ldAssert(JSON.stringify(ldLibraryCards())===JSON.stringify(before)&&ldLibraryCount()===beforeCount,'The library changed after the refused Idea');
   ldClick('show-idea');ldSubmit('Second late idea');
   await ldUntil(()=>liveDaySeen.ideas.length===2&&ldIdle(),'the second Idea');
   ldAssert(liveDaySeen.ideas[1]===embeddedDay,'The second Idea was not sent as of the embedded day');
   await ldUntil(()=>ldTitle()==='Second late idea'&&ldRoot().textContent.includes('day not completed'),'the second Idea error');
   status.textContent='Passed B: refused as of '+embeddedDay+', error shown twice, library unchanged ('+beforeCount+' questions, '+before.length+' cards on its first page); '+liveDaySeen.errors.length+' page errors';
  }
  ldAssert(liveDaySeen.errors.length===0,'Uncaught page errors: '+liveDaySeen.errors.join(' | '));
 }catch(error){status.textContent='FAILED: '+error.message;}
};
setTimeout(()=>ldClick('check-live-day'),500);
</script>`;

await fs.mkdir(new URL('./dist/', import.meta.url), { recursive: true });
const start = page.lastIndexOf('<script>');
for (const liveDayCase of ['A', 'B']) {
  const html = (page.slice(0, start) + fixture(liveDayCase) + page.slice(start)).replace(
    '</body>',
    () => checks + '</body>',
  );
  await fs.writeFile(
    new URL(`./dist/live-day-check-${liveDayCase.toLowerCase()}.html`, import.meta.url),
    html,
  );
}
console.log(
  `Wrote poc/ui/dist/live-day-check-a.html and -b.html (served ${servedDay}, embedded ${embeddedDay})`,
);
