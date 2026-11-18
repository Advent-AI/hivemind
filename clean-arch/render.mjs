import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

// Render the same Markdown subset used by the repository's design page.
const root = dirname(fileURLToPath(import.meta.url));
const source = readFileSync(join(root, 'PRD.md'), 'utf8');
const renderer = readFileSync(join(root, '../docs/system-design/markdown.js'), 'utf8');
const sandbox = { window: {} };
vm.runInNewContext(renderer, sandbox);
const escape = (s) => s.replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

let body = sandbox.window.HIVEMIND_MARKDOWN.render(source);
// Derive the readable connection map from the Mermaid source, so its labels and
// arrows cannot drift independently of the PRD.
const graph = source.match(/```mermaid\n([\s\S]*?)\n```/);
if (!graph) throw new Error('PRD system picture is missing');
const labels = new Map();
const edges = [];
const edgePattern = /^\s*([A-Za-z]\w*)(?:\[\((.*?)\)\]|\[(.*?)\])?\s*(?:-->(?:\|([^|]+)\|)?|-\.->|-\.\s*(.*?)\s*\.->)\s*([A-Za-z]\w*)(?:\[\((.*?)\)\]|\[(.*?)\])?\s*$/;
for (const line of graph[1].split('\n').slice(1)) {
  if (!line.trim()) continue;
  const m = line.match(edgePattern);
  if (!m) throw new Error(`Unsupported system picture line: ${line}`);
  if (m[2] || m[3]) labels.set(m[1], m[2] || m[3]);
  if (m[7] || m[8]) labels.set(m[6], m[7] || m[8]);
  edges.push({ from: m[1], to: m[6], description: m[4] || m[5] || '', dotted: line.includes('-.') });
}
const connections = edges.map(({from, to, description}) => {
  if (!labels.has(from) || !labels.has(to)) throw new Error(`Undefined diagram node: ${from} or ${to}`);
  return `<div class="connection"><span>${escape(labels.get(from))}</span><span class="connection-arrow" aria-label="to">→${description ? `<small>${escape(description)}</small>` : ''}</span><span>${escape(labels.get(to))}</span></div>`;
}).join('');
// Place nodes from the PRD graph in a readable layout. Unrecognised nodes fail
// the build so the visual cannot silently omit a future architecture change.
const positions = {H:[130,80],T:[560,80],X:[360,205],N:[820,120],O:[820,205],M:[820,290],P:[360,380],S:[130,500],D:[130,650],C:[360,650],B:[820,500],U:[820,650],K:[820,800],W:[360,875],L:[360,1000],J:[360,1125],Z:[360,1250],Q:[820,1250],G:[1150,130],V:[1150,250],R:[1150,370]};
for (const id of labels.keys()) if (!positions[id]) throw new Error(`Diagram layout needed for ${id}`);
const line = (from, to) => {
  const a = positions[from], b = positions[to];
  if (from === 'W' && to === 'T') return `M 460 865 L 1000 865 L 1000 80 L 660 80`;
  if (from === 'W' && to === 'J') return `M 460 885 L 520 885 L 520 1115 L 460 1115`;
  if (from === 'J' && to === 'Q') return `M 460 1135 L 820 1135 L 820 1216`;
  if (from === 'W' && to === 'D') return `M 260 875 L 20 875 L 20 650 L 30 650`;
  if (from === 'P' && to === 'C') return `M 460 380 L 510 380 L 510 630 L 460 630`;
  if (from === 'T' && to === 'X') return `M 520 114 L 520 140 L 400 140 L 400 171`;
  if (from === 'P' && to === 'S') return `M 260 380 L 245 380 L 245 500 L 230 500`;
  if (from === 'S' && to === 'C') return `M 230 500 L 245 500 L 245 650 L 260 650`;
  if (from === 'D' && to === 'S') return `M 130 616 L 130 534`;
  if (from === 'X' && to === 'V') return `M 460 205 L 620 205 L 620 350 L 1030 350 L 1030 250 L 1050 250`;
  if (from === 'X' && (to === 'N' || to === 'O' || to === 'M')) return `M 460 205 L 600 205 L 600 ${b[1]} L 720 ${b[1]}`;
  if (from === 'C' && (to === 'B' || to === 'K')) return `M 460 650 L 600 650 L 600 ${b[1]} L 720 ${b[1]}`;
  if (a[0] === b[0]) return `M ${a[0]} ${a[1]+34} L ${b[0]} ${b[1]-34}`;
  if (a[1] === b[1]) return `M ${a[0]+(b[0]>a[0]?100:-100)} ${a[1]} L ${b[0]+(b[0]>a[0]?-100:100)} ${b[1]}`;
  return `M ${a[0]} ${a[1]+34} L ${a[0]} ${b[1]} L ${b[0]+(b[0]>a[0]?-100:100)} ${b[1]}`;
};
const paths = edges.map(e => `<path d="${line(e.from,e.to)}"${e.dotted ? ' class="optional"' : ''}/>`).join('');
const nodes = [...labels].map(([id,label]) => {
  const [x,y]=positions[id];
  const words=label.split(' '), lines=[''];
  for (const word of words) {
    const i=lines.length-1;
    if ((lines[i]+' '+word).trim().length > 25 && lines[i]) lines.push(word);
    else lines[i]=(lines[i]+' '+word).trim();
  }
  return `<g><rect x="${x-100}" y="${y-34}" width="200" height="68" rx="10"/><text x="${x}" y="${y-(lines.length-1)*9}">${lines.map((s,i)=>`<tspan x="${x}" dy="${i?18:0}">${escape(s)}</tspan>`).join('')}</text></g>`;
}).join('');
const diagram = `<p class="diagram-hint">Scroll the diagram horizontally to see the evaluation branch.</p><div class="diagram"><svg viewBox="0 0 1300 1310" role="img" aria-label="Architecture flow, with an independent evaluation branch"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#538276"/></marker></defs><g class="arrows">${paths}</g><g class="nodes">${nodes}</g></svg></div><details class="graph-source"><summary>View all connections</summary><div class="flow-map" aria-label="Architecture connections">${connections}</div></details><details class="graph-source"><summary>View diagram source</summary><pre><code>${escape(graph[1])}</code></pre></details>`;
const graphCode = `<pre><code>${escape(graph[1])}</code></pre>`;
if (!body.includes(graphCode)) throw new Error('System picture was not rendered');
body = body.replace(graphCode, diagram);
const toc = [];
body = body.replace(/<h([123])>(.*?)<\/h\1>/g, (_, level, title) => {
  const plain = title.replace(/<[^>]+>/g, '');
  const id = slug(plain);
  if (level === '2' || (level === '3' && ['1.1 The vision: a market world model', '1.2 The problems it answers', '1.3 Why the running pipeline was rebuilt', '1.4 What the new system does differently', '1.5 The gates before it replaces the running pipeline', 'What the model decides', 'Two parts', 'What the ladder step decides', 'Where each step stands', 'What the measurements say', 'System prompt', 'Closing check', 'Structured-output schema', 'Diagram-to-code map'].includes(plain))) toc.push({ id, title: plain, level });
  return `<h${level} id="${id}">${title}</h${level}>`;
});
const nav = toc.map(({ id, title, level }) => `<a${level === '3' ? ' class="subsection"' : ''} href="#${id}">${escape(title)}</a>`).join('\n');
const lunaPrompt = toc.find(({ title }) => title.includes('Step 1 prompt: c8'));
const jevPrompt = toc.find(({ title }) => title.includes('Step 2 prompt: Jev'));
const vision = toc.find(({ title }) => title.startsWith('1. Vision'));
const standing = toc.find(({ title }) => title.startsWith('8. How the system is measured'));
if (!lunaPrompt || !jevPrompt || !vision || !standing) throw new Error('The vision, the measurement section and both prompt sections must be present');
const digest = createHash('sha256').update(source).digest('hex');
const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="source-sha256" content="${digest}"><title>Hivemind | Clean architecture</title>
<style>
:root{color-scheme:light;--ink:#1e2a2d;--muted:#5d6d70;--teal:#145b50;--line:#dbe6e2;--paper:#fff;--bg:#f4f7f5}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);font:16px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink)}
.shell{display:grid;grid-template-columns:260px minmax(0,1fr);max-width:1600px;margin:auto}.side{position:sticky;top:0;height:100vh;overflow:auto;padding:32px 22px;background:#eef4f1;border-right:1px solid var(--line)}
.brand{font-weight:750;letter-spacing:.04em;font-size:13px;color:var(--teal);text-transform:uppercase}.side p{font-size:13px;color:var(--muted);margin:5px 0 22px}.side nav{display:grid;gap:3px;margin-top:22px}.side nav a{font-size:13px;color:#45605b;text-decoration:none;padding:7px 9px;border-radius:6px;line-height:1.35}.side nav a.subsection{padding-left:22px;font-size:12px}.side nav a:hover,.side nav a:focus{background:#dfece5;color:#103e35}
main{min-width:0;padding:52px clamp(24px,6vw,90px) 90px}.content{max-width:900px;margin:auto}h1{font-size:clamp(32px,4vw,48px);line-height:1.15;letter-spacing:-.035em;margin:14px 0 24px}h2{font-size:25px;line-height:1.3;margin:60px 0 16px;padding-top:20px;border-top:1px solid var(--line);scroll-margin-top:20px}h3{font-size:19px;margin:30px 0 12px}p{margin:0 0 18px}a{color:#14695b;text-underline-offset:3px}strong{font-weight:700}ul,ol{padding-left:25px;margin:0 0 22px}li{padding-left:4px;margin:7px 0}.eyebrow{font-size:12px;font-weight:750;letter-spacing:.12em;text-transform:uppercase;color:var(--teal)}
.intro{background:#e6f2ed;border:1px solid #c5ddd3;border-radius:12px;padding:17px 20px;margin:0 0 32px;font-size:14px}.intro p{margin:0}.prompt-links{display:flex;gap:12px;flex-wrap:wrap;margin-top:12px}.prompt-links a{font-weight:700}.prd__table{overflow-x:auto;margin:22px 0 30px;border:1px solid var(--line);border-radius:10px;background:var(--paper)}table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.55}th,td{text-align:left;vertical-align:top;padding:12px 15px;border-bottom:1px solid var(--line)}th{background:#eff5f2;color:#345049}tr:last-child td{border-bottom:0}pre{overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere;background:#183530;color:#e9f5ef;padding:20px;border-radius:10px;font-size:13px;line-height:1.55}code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}p code,li code{background:#e9f0ed;padding:2px 5px;border-radius:4px;font-size:.9em}.diagram{overflow-x:auto;background:white;border:1px solid var(--line);border-radius:12px;margin:22px 0}.diagram svg{display:block;width:100%;min-width:680px;height:auto}.arrows path{fill:none;stroke:#538276;stroke-width:2;marker-end:url(#arrow)}.arrows path.optional{stroke-dasharray:6 4}.nodes rect{fill:#eaf4ef;stroke:#b6d4c7;stroke-width:1.5}.nodes text{fill:#244c43;text-anchor:middle;dominant-baseline:middle;font:600 14px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.flow-map{display:grid;gap:8px;margin:22px 0}.connection{display:grid;grid-template-columns:minmax(0,1fr) 120px minmax(0,1fr);align-items:center;gap:8px;font-size:14px;line-height:1.35}.connection>span:not(.connection-arrow){background:#e7f2ed;border:1px solid #c7ded4;border-radius:8px;padding:10px 12px}.connection-arrow{text-align:center;color:var(--teal);font-size:20px}.connection-arrow small{display:block;font-size:11px;color:var(--muted)}.graph-source summary{cursor:pointer;color:var(--teal);font-size:13px}.reference{margin-top:22px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:15px 18px}.reference summary{cursor:pointer;color:var(--teal);font-weight:700}.reference img{display:block;width:100%;height:auto;margin:16px auto 0}
.replay-frame{height:960px;margin:18px 0;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:white}.replay-frame iframe{display:block;width:100%;height:100%;border:0}
@media(max-width:760px){.shell{display:block}.side{position:static;height:auto;padding:20px 22px;border-right:0;border-bottom:1px solid var(--line)}.side p{margin-bottom:10px}.side nav{display:flex;overflow:auto;gap:5px;padding-bottom:4px}.side nav a{white-space:nowrap;background:#e3eee8}main{padding:32px 20px 70px}h2{margin-top:45px}table{min-width:600px}.connection{grid-template-columns:minmax(0,1fr) 65px minmax(0,1fr);font-size:12px}.connection>span:not(.connection-arrow){padding:8px}}
</style></head><body><div class="shell"><aside class="side"><div class="brand">Hivemind</div><nav aria-label="On this page">${nav}</nav></aside><main><div class="content"><div class="eyebrow">Architecture / working draft</div><div class="intro"><p>This page is generated from <a href="PRD.md">PRD.md</a>. The Markdown is the source of truth; the reading page is checked against it.</p><div class="prompt-links"><a href="#${vision.id}">Read the vision and problems →</a><a href="#${standing.id}">See where each step stands →</a><a href="#${lunaPrompt.id}">Read the adopted Step 1 prompt (c8) →</a><a href="#${jevPrompt.id}">Read the frozen Jev request →</a><a href="PRD-HISTORY.md">Earlier record →</a></div></div>${body}
<details class="reference"><summary>View the original architecture diagram</summary><img src="reference-diagram.png" alt="Original architecture diagram supplied by Alex"></details>
</div></main></div></body></html>\n`;

const output = join(root, 'architecture.html');
if (process.argv.includes('--check')) {
  let actual = '';
  try { actual = readFileSync(output, 'utf8'); } catch {}
  if (actual !== html) {
    console.error('Clean architecture HTML is missing or out of date. Run: node clean-arch/render.mjs');
    process.exit(1);
  }
  console.log('Clean architecture HTML matches PRD.md.');
} else {
  writeFileSync(output, html);
  console.log('Generated clean-arch/architecture.html from PRD.md.');
}
