/** Build a browser check of atomic snapshots and instance ownership with real library data. */
import fs from 'node:fs/promises';
import { fromBundles } from './src/adapters/bundle.js';
import { snapshotThesis } from './src/model/thesis.js';
import { current } from './test/fixtures.js';
const data = fromBundles(current);
const day = '2026-07-23';
const narrow = {
  ...data,
  as_of: day,
  days: data.days.filter((d) => d <= day),
  theses: data.theses.filter((t) => t.created_day <= day).map((t) => snapshotThesis(t, day)),
  groups: data.groups
    .filter((g) => g.created_day <= day)
    .map((g) => ({ ...g, members: g.members.filter((m) => m.day <= day) })),
};
const page = await fs.readFile(new URL('../mock/index.html', import.meta.url), 'utf8');
const css = page.match(/<style>([\s\S]*?)<\/style>/)[1];
const script = page.slice(page.lastIndexOf('<script>') + 8, page.lastIndexOf('</script>'));
const encode = (value) => JSON.stringify(value).replaceAll('<', '\\u003c');
await fs.mkdir(new URL('./dist/', import.meta.url), { recursive: true });
await fs.writeFile(
  new URL('./dist/library-check.html', import.meta.url),
  `<!doctype html><html><head><meta charset="utf-8"><style>${css}body{margin:0}.checks{padding:16px}#host{height:650px}#canvas{height:300px}</style></head><body><div class="checks"><button id="check">Check library lifecycle</button><p id="result" role="status">Ready</p></div><div id="host"></div><div id="canvas"></div><script>${script}</script><script>
const data=${encode(data)}, narrow=${encode(narrow)};
const host=document.getElementById('host'), canvas=document.getElementById('canvas'), result=document.getElementById('result');
const start=performance.now();
const library=Hivemind.createLibrary(host,{dataset:data});
const renderMs=performance.now()-start;
document.getElementById('check').onclick=()=>{
 let count=0;const check=(ok,label)=>{if(!ok)throw new Error(label);count++};
 try{
  check(getComputedStyle(host.querySelector('.library')).display==='grid','standalone host receives library styling');
  check(!host.querySelector('.library-date,.library-results')&&!/[·•]/.test(host.textContent)&&host.textContent.includes('Research groups')&&!host.textContent.includes('RESEARCH GROUPS'),'presentation rules hold');
  const invalid=structuredClone(data);invalid.groups[0].members[0].thesis_id='missing';
  let refused=false;try{library.setDataset(invalid)}catch{refused=true}
  check(refused&&host.querySelector('[data-group=""] .library-count').textContent==='90','invalid update retains old library');
  library.setDataset(narrow);check(library.getDay()==='2026-07-23','library day clamps before replacement');
  const explorer=Hivemind.createThesisExplorer(canvas,{dataset:data});explorer.showGraph({primaryId:'v7',day:data.as_of});explorer.setDataset(narrow);
  check(explorer.getDataset().as_of==='2026-07-23','canvas accepts narrower date span');
  explorer.destroy();check(!canvas.children.length,'canvas teardown removes all DOM');
  library.setDataset({...data,theses:[],groups:[],days:[]});check(host.textContent.includes('No theses to show'),'empty library renders');
  library.setDataset(data);check(host.querySelector('[data-group=""] .library-count').textContent==='90','library restores');
  const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);check(ids.length===new Set(ids).size,'DOM IDs remain unique');
  result.textContent='Passed '+count+' lifecycle checks. Initial library render '+renderMs.toFixed(1)+' ms.';
 }catch(error){result.textContent='FAILED: '+error.message}
};
</script></body></html>`,
);
console.log('Wrote poc/ui/dist/library-check.html');
