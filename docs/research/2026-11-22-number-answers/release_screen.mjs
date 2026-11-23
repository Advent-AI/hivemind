/**
 * The $0 screen check of RELEASE-PAGE.md §6: headless Chrome through its DevTools protocol (Node's built-in WebSocket), each page
 * opened from file://, every visible text of each checked card compared with the frozen list in screen-expected.json.
 *
 *   node release_screen.mjs <run folder> <screen-expected.json>
 *
 * The run folder holds old-1/index.html, old-3-0825/index.html, old-1-0828/index.html and escape/index.html. The two negative
 * pages (a restored fetch, an extra visible forecast line) are written into the run folder from old-1's page. Exits 1 when any
 * check fails, including a negative page that passes.
 */
import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const [runFolder, expectedPath, profileParent] = process.argv.slice(2).map((p) => path.resolve(p));   // file:// needs an absolute path
const expectedBytes = fs.readFileSync(expectedPath);
const expected = JSON.parse(expectedBytes);
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const results = { expected_sha256: createHash('sha256').update(expectedBytes).digest('hex'), pages: {}, failures: [] };
const fail = (where, what) => results.failures.push(`${where}: ${what}`);

function cspHash(text) {
  return `'sha256-${createHash('sha256').update(text, 'utf8').digest('base64')}'`;
}

/** A copy of a page with its inline script edited and the CSP script hash recomputed, so the edited script runs. */
function mutate(source, target, edit) {
  const page = fs.readFileSync(source, 'utf8');
  const start = page.lastIndexOf('<script>') + '<script>'.length;
  const end = page.lastIndexOf('</script>');
  const script = page.slice(start, end);
  const changed = edit(script);
  if (changed === script) throw new Error(`mutation of ${source} changed nothing`);
  const out = (page.slice(0, start) + changed + page.slice(end)).replace(cspHash(script), cspHash(changed));
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, out);
}

async function browser() {
  const profile = fs.mkdtempSync(path.join(profileParent || os.tmpdir(), 'release-chrome-'));   // outside the run folder and every package
  const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', `--user-data-dir=${profile}`,
                                '--remote-debugging-port=0', 'about:blank'], { stdio: 'ignore' });
  let port;
  for (let i = 0; i < 200 && !port; i++) {
    await new Promise((r) => setTimeout(r, 50));
    try { port = fs.readFileSync(path.join(profile, 'DevToolsActivePort'), 'utf8').split('\n')[0]; } catch { /* not yet */ }
  }
  if (!port) throw new Error('Chrome did not open its debugging port');
  return { chrome, port };
}

async function session(port) {
  const target = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: 'PUT' })).json();
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener('open', r));
  let id = 0;
  const pending = new Map();
  const events = [];
  ws.addEventListener('message', (m) => {
    const d = JSON.parse(m.data);
    if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); } else events.push(d);
  });
  const send = (method, params = {}) => new Promise((r) => { const n = ++id; pending.set(n, r); ws.send(JSON.stringify({ id: n, method, params })); });
  const evaluate = async (expression) => {
    const answer = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    if (answer.result?.exceptionDetails) throw new Error(`page evaluation failed: ${answer.result.exceptionDetails.text}`);
    return answer.result.result.value;
  };
  for (const domain of ['Network', 'Log', 'Runtime', 'Page']) await send(`${domain}.enable`);
  return { ws, send, evaluate, events };
}

const VISIBLE = `((e) => e.checkVisibility({ opacityProperty: true, visibilityProperty: true, contentVisibilityAuto: true })
  && e.getBoundingClientRect().width > 0 && e.getBoundingClientRect().height > 0)`;
const TOGGLE = `(async (id, open) => {
  const card = [...document.querySelectorAll('article.question')].find((a) => a.dataset.id === id);
  const details = card && card.querySelector('details');
  if (details && details.open !== open) { details.open = open; await new Promise((r) => setTimeout(r, 50)); }
  return Boolean(card);
})`;
const READ_PAGE = `(() => {
  const visible = ${VISIBLE};
  const page = { header: [], cards: [], other: [], clipped: [], unreadable: [] };
  const rgb = (c) => { const m = c.match(/rgba?\\(([^)]+)\\)/); if (!m) return null; const v = m[1].split(',').map((x) => parseFloat(x)); return { r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1 }; };
  const lum = ({ r, g, b }) => { const f = (x) => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const background = (e) => { for (let a = e; a; a = a.parentElement) { const c = rgb(getComputedStyle(a).backgroundColor); if (c && c.a > 0) return c; } return rgb(getComputedStyle(document.documentElement).backgroundColor) || { r: 255, g: 255, b: 255, a: 1 }; };
  const contrast = (e) => { const f = lum(rgb(getComputedStyle(e).color)), b = lum(background(e)); return (Math.max(f, b) + 0.05) / (Math.min(f, b) + 0.05); };
  const clippingAncestor = (e) => { for (let a = e.parentElement; a && a !== document.body; a = a.parentElement) { const s = getComputedStyle(a);
    if (s.overflowX !== 'visible' || s.overflowY !== 'visible' || /paint|strict|content/.test(s.contain) || s.clipPath !== 'none') return true; } return false; };
  const byId = new Map();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const text = n.textContent.trim();
    const owner = n.parentElement;
    if (!text || !owner || owner.closest('script') || !visible(owner)) continue;
    if ((getComputedStyle(owner).display !== 'inline' && (owner.scrollWidth > owner.clientWidth + 1 || owner.scrollHeight > owner.clientHeight + 1)) || clippingAncestor(owner)) {
      page.clipped.push(text.slice(0, 80));
    }
    if (contrast(owner) < 4.5) page.unreadable.push(text.slice(0, 80));
    const card = owner.closest('article.question');
    if (owner.closest('header.release-header')) { page.header.push(text); continue; }
    if (!card) { page.other.push(text); continue; }
    let entry = byId.get(card.dataset.id);
    if (!entry) { entry = { id: card.dataset.id, top: [], groups: [] }; byId.set(card.dataset.id, entry); page.cards.push(entry); }
    const item = owner.closest('li.evidence-item');
    if (!item) { entry.top.push(text); continue; }
    const index = [...card.querySelectorAll('li.evidence-item')].indexOf(item);
    while (entry.groups.length <= index) entry.groups.push([]);
    entry.groups[index].push(text);
  }
  for (const entry of page.cards) entry.groups = entry.groups.filter((g) => g.length);
  return page;
})()`;

const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);

async function open(port, file, count, { media, metrics } = {}) {
  const s = await session(port);
  if (metrics) await s.send('Emulation.setDeviceMetricsOverride', metrics);
  if (media) await s.send('Emulation.setEmulatedMedia', { features: media });
  const started = performance.now();
  await s.send('Page.navigate', { url: `file://${file}` });
  let seconds = null;
  for (let i = 0; i < 160; i++) {
    const ready = await s.evaluate(`(() => { const visible = ${VISIBLE}; const cards = [...document.querySelectorAll('article.question')];
      return document.getElementById('fallback') === null && cards.length === ${count} && cards.every(visible); })()`).catch(() => false);
    if (ready) { seconds = (performance.now() - started) / 1000; break; }
    await new Promise((r) => setTimeout(r, 25));
  }
  return { ...s, seconds };
}

function clean(where, s, file) {
  const sig = signals(s.events);
  const own = `file://${file}`;
  if (sig.requests.length !== 1 || sig.requests[0] !== own) fail(where, `requests ${sig.requests.map((u) => u.slice(0, 120))}`);
  if (sig.errors.length) fail(where, `errors ${sig.errors}`);
  return sig;
}

function signals(events) {
  const requests = events.filter((e) => e.method === 'Network.requestWillBeSent').map((e) => e.params.request.url);
  const errors = events.filter((e) => (e.method === 'Log.entryAdded' && e.params.entry.level === 'error')
    || e.method === 'Runtime.exceptionThrown' || (e.method === 'Runtime.consoleAPICalled' && e.params.type === 'error'))
    .map((e) => e.params.entry ? `${e.params.entry.source}: ${e.params.entry.text}` : e.method);
  return { requests, errors };
}

/** The whole read page, collapsed, with the card expanded, and after closing and reopening it, against the frozen pages. */
async function checkPage(s, where, id, frozen) {
  const initiallyClosed = await s.evaluate(`(() => { const c = [...document.querySelectorAll('article.question')].find((a) => a.dataset.id === ${JSON.stringify(id)});
    const d = c && c.querySelector('details'); return Boolean(c) && (!d || !d.open); })()`);
  if (!initiallyClosed) fail(where, `${id} is not closed as first rendered`);
  const collapsed = await s.evaluate(READ_PAGE);                // the page as the reader first sees it, before any toggle
  await s.evaluate(`${TOGGLE}(${JSON.stringify(id)}, true)`);
  const expanded = await s.evaluate(READ_PAGE);
  await s.evaluate(`${TOGGLE}(${JSON.stringify(id)}, false)`);
  await s.evaluate(`${TOGGLE}(${JSON.stringify(id)}, true)`);
  const reopened = await s.evaluate(READ_PAGE);
  const outcome = { collapsed: same(collapsed, frozen.collapsed), expanded: same(expanded, frozen.expanded), reopened: same(reopened, frozen.expanded) };
  for (const [k, v] of Object.entries(outcome)) if (!v) fail(where, `${id} ${k} page differs from the frozen page`);
  const card = expanded.cards.find((c) => c.id === id);
  return { outcome, other: expanded.other, card_top: card ? card.top : null, card_groups: card ? card.groups.length : null };
}

const { chrome, port } = await browser();
const PHONE = { width: 390, height: 844, deviceScaleFactor: 2, mobile: true };
const DARK = [{ name: 'prefers-color-scheme', value: 'dark' }];
const LIGHT = [{ name: 'prefers-color-scheme', value: 'light' }];   // headless Chrome follows the system scheme unless told
try {
  const old1 = path.join(runFolder, 'old-1', 'index.html');
  const v8 = expected.pages['old-1/v8'];
  {
    const s = await open(port, old1, v8.count, { media: LIGHT });
    const page = { seconds: s.seconds, check: await checkPage(s, 'old-1', 'v8', v8) };
    page.links = await s.evaluate(`document.querySelectorAll('a,[href],[src]').length`);
    if (page.links !== 0) fail('old-1', `${page.links} links or sources`);
    page.light_background = await s.evaluate(`getComputedStyle(document.body).backgroundColor`);
    if (page.light_background !== 'rgb(245, 242, 235)') fail('old-1', `light background ${page.light_background}`);
    const top = await s.evaluate(`(() => { const c = [...document.querySelectorAll('article.question')].find((a) => a.dataset.id === 'v8'); return c.getBoundingClientRect().top + window.scrollY; })()`);
    const shot = await s.send('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: Math.max(0, top - 16), width: 900, height: 1100, scale: 1 }, captureBeyondViewport: true });
    if (shot.result?.data) fs.writeFileSync(path.join(runFolder, 'old-1-v8.png'), Buffer.from(shot.result.data, 'base64'));
    page.signals = clean('old-1', s, old1);
    page.size = fs.statSync(old1).size;
    page.data_size = fs.statSync(path.join(runFolder, 'old-1', 'release-data.json')).size;
    if (page.size > page.data_size + 65536) fail('old-1', `page ${page.size} bytes over data ${page.data_size} + 64 KB`);
    if (s.seconds === null || s.seconds > 3) fail('old-1', `rendered in ${s.seconds} s`);
    s.ws.close();
    results.pages['old-1'] = page;
  }
  {
    const s = await open(port, old1, v8.count, { metrics: PHONE, media: DARK });
    const phone = { check: await checkPage(s, 'old-1 phone', 'v8', v8) };
    phone.scroll_width = await s.evaluate(`document.scrollingElement.scrollWidth`);
    phone.dark_background = await s.evaluate(`getComputedStyle(document.body).backgroundColor`);
    phone.morningstar = await s.evaluate(`(() => {
      const quote = [...document.querySelectorAll('.evidence-quote')].find((q) => q.textContent === ${JSON.stringify(expected.morningstar_quote)});
      if (!quote) return null;
      quote.scrollIntoView();
      const range = document.createRange(); range.selectNodeContents(quote);
      const box = quote.getBoundingClientRect();
      return { lines: new Set([...range.getClientRects()].map((r) => Math.round(r.top))).size, left: box.left, right: box.right };
    })()`);
    if (phone.scroll_width > 390) fail('old-1 phone', `scroll width ${phone.scroll_width}`);
    if (phone.dark_background !== 'rgb(15, 20, 13)') fail('old-1 dark', `background ${phone.dark_background}`);
    if (!phone.morningstar || phone.morningstar.lines < 2 || phone.morningstar.left < 0 || phone.morningstar.right > 390) fail('old-1 phone', `Morningstar quote ${JSON.stringify(phone.morningstar)}`);
    phone.signals = clean('old-1 phone dark', s, old1);
    s.ws.close();
    results.pages['old-1 phone dark'] = phone;
  }
  for (const [folder, key, id] of [['old-3-0825', 'old-3/v36@2026-08-25', 'v36'], ['old-1-0828', 'old-1/v10@2026-08-28', 'v10']]) {
    const frozen = expected.pages[key];
    const file = path.join(runFolder, folder, 'index.html');
    const s = await open(port, file, frozen.count);
    const page = { check: await checkPage(s, key, id, frozen) };
    page.signals = clean(key, s, file);
    s.ws.close();
    results.pages[key] = page;
  }
  {
    const file = path.join(runFolder, 'escape', 'index.html');
    const s = await open(port, file, expected.escape.count);
    await s.evaluate(`${TOGGLE}(${JSON.stringify(expected.escape.question)}, true)`);
    const page = {
      quote_visible: await s.evaluate(`(() => { const visible = ${VISIBLE};
        return [...document.querySelectorAll('.evidence-quote')].some((q) => q.textContent === ${JSON.stringify(expected.escape.quote)} && visible(q)); })()`),
      images: await s.evaluate(`document.querySelectorAll('img').length`),
    };
    if (!page.quote_visible) fail('escape', 'the quote is not shown, visibly, as text');
    if (page.images !== 0) fail('escape', `${page.images} img elements`);
    page.signals = clean('escape', s, file);
    s.ws.close();
    results.pages.escape = page;
  }
  // the negative pages: each must be caught for its own reason
  const negative = async (name, edit, options, judge) => {
    const target = path.join(runFolder, `mutant-${name}`, 'index.html');
    mutate(old1, target, edit);
    const s = await open(port, target, v8.count, options);
    const before = results.failures.length;
    const verdict = await judge(s);
    results.failures.splice(before);                  // a negative page's own failures are its expected outcome
    results.pages[`mutant-${name}`] = verdict;
    if (!verdict.caught) fail(`mutant-${name}`, 'not caught');
    s.ws.close();
  };
  const ENTRY = "(function(){'use strict';";
  const FORECAST = "if(q['class']==='number'){card.appendChild(el('p','question-forecast',q.forecast));}";
  await negative('fetch', (x) => x.replace(ENTRY, `${ENTRY}fetch('http://127.0.0.1:59999/library').catch(function(){});`), {}, async (s) => {
    const sig = signals(s.events);
    const named = sig.errors.some((e) => e.startsWith('security:') && e.includes('http://127.0.0.1:59999/library') && e.includes('connect-src'));
    return { caught: s.seconds !== null && named, rendered: s.seconds !== null, named };
  });
  await negative('line-inside', (x) => x.replace(FORECAST, `${FORECAST.slice(0, -1)}if(q.id==='v8'){card.appendChild(el('p','note','Forecast: $361 billion'));}}`), {}, async (s) => {
    const page = await s.evaluate(READ_PAGE);
    const card = page.cards.find((c) => c.id === 'v8');
    const frozenTop = v8.collapsed.cards.find((c) => c.id === 'v8').top;
    const withLine = [...frozenTop.slice(0, 3), 'Forecast: $361 billion', ...frozenTop.slice(3)];
    return { caught: Boolean(card) && same(card.top, withLine) && page.other.length === 0, card_top: card ? card.top : null };   // the mismatch is exactly the added line
  });
  await negative('line-beside', (x) => x.replace("root.appendChild(card);}", "if(q.id==='v8'){root.appendChild(el('p','note','Forecast: $361 billion'));}root.appendChild(card);}"), {}, async (s) => {
    const check = await checkPage(s, 'line-beside', 'v8', v8);
    return { caught: !check.outcome.collapsed && check.other.includes('Forecast: $361 billion'), other: check.other };
  });
  await negative('transparent', (x) => x.replace("var root=document.getElementById('release');", "var root=document.getElementById('release');root.style.opacity='0';"), {}, async (s) => {
    const state = await s.evaluate(`(() => { const visible = ${VISIBLE}; const cards = [...document.querySelectorAll('article.question')];
      return { cards: cards.length, visible: cards.filter(visible).length, fallback: document.getElementById('fallback') !== null }; })()`);
    const sig = signals(s.events);
    return { caught: (s.seconds === null || s.seconds > 3) && state.cards === v8.count && state.visible === 0 && !state.fallback && sig.errors.length === 0,
             seconds: s.seconds, ...state, errors: sig.errors.length };   // every card exists and none is visible: the reason, not a script failure
  });
  await negative('clipped', (x) => x.replace("item.appendChild(el('blockquote','evidence-quote',e.quote));",
    "var bq=el('blockquote','evidence-quote',e.quote);bq.style.whiteSpace='nowrap';bq.style.overflow='hidden';bq.style.textOverflow='ellipsis';item.appendChild(bq);"),
  { metrics: PHONE }, async (s) => {
    await s.evaluate(`${TOGGLE}('v8', true)`);
    const page = await s.evaluate(READ_PAGE);
    return { caught: page.clipped.length > 0, clipped: page.clipped.length };
  });
  await negative('clipping-wrapper', (x) => x.replace("item.appendChild(el('blockquote','evidence-quote',e.quote));",
    "var wrap=el('div','quote-wrap');wrap.style.contain='paint';wrap.style.height='1.5em';wrap.appendChild(el('blockquote','evidence-quote',e.quote));item.appendChild(wrap);"),
  { metrics: PHONE }, async (s) => {
    await s.evaluate(`${TOGGLE}('v8', true)`);
    const page = await s.evaluate(READ_PAGE);
    return { caught: page.clipped.length > 0, clipped: page.clipped.length };
  });
  await negative('own-background', (x) => x.replace(FORECAST, "if(q['class']==='number'){var ob=el('p','question-forecast',q.forecast);ob.style.color='rgb(15, 20, 13)';ob.style.background='rgb(15, 20, 13)';card.appendChild(ob);}"),
  { media: LIGHT }, async (s) => {
    const page = await s.evaluate(READ_PAGE);
    const around = await s.evaluate(`(() => { const c = [...document.querySelectorAll('article.question')].find((a) => a.dataset.id === 'v8');
      return { body: getComputedStyle(document.body).backgroundColor, card: getComputedStyle(c).backgroundColor }; })()`);
    return { caught: page.unreadable.includes('Forecast unavailable') && around.body === 'rgb(245, 242, 235)', unreadable: page.unreadable.length, ...around };   // a light page around the dark marker
  });
  await negative('unreadable-marker', (x) => x.replace(FORECAST, "if(q['class']==='number'){var mk=el('p','question-forecast',q.forecast);mk.style.color='rgb(15, 20, 13)';mk.style.background='rgb(15, 20, 13)';card.appendChild(mk);}"),
  { media: DARK }, async (s) => {
    const page = await s.evaluate(READ_PAGE);
    return { caught: page.unreadable.includes('Forecast unavailable'), unreadable: page.unreadable.length };
  });
} finally {
  chrome.kill();
}
fs.writeFileSync(path.join(runFolder, 'screen-results.json'), JSON.stringify(results, null, 1));
console.log(JSON.stringify({ failures: results.failures, seconds: results.pages['old-1']?.seconds, expected_sha256: results.expected_sha256 }, null, 1));
process.exit(results.failures.length ? 1 : 0);
