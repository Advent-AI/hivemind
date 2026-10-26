/** The Idea card: the user's sentence read by the service (POST /ideas, docs/poc/idea-card.md, D112).
 * This module posts the idea, connects every chosen thesis to it, and renders the card: the sentence,
 * the service's reading, and the verdict on a number the idea
 * states. It never chooses theses itself and never reads the clock; the day is the answer's as_of. */
import { element, esc, SEP } from '../components/dom.js';
import { cardHeaderHtml } from '../components/primitives.js';
import { scoreHistoryChart } from '../components/thesis-chart.js';
import {
  compositeAt,
  confidenceFromScore,
  confidenceHistory,
  formatConfidence,
  byImpactWeight,
} from './composite.js';
import { ideaProgressHtml } from './progress.js';
import { CARD_WIDTH } from '../model/graph.js';

export class IdeaError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

/** POST the idea; resolves to the card the service returns, rejects with IdeaError on any non-200 answer. */
export async function readIdea(api, text, { signal, asOf, onProgress = () => {} } = {}) {
  try {
    const response = await fetch(`${api}/ideas`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/x-ndjson' },
      body: JSON.stringify({ text, bundles: false, ...(asOf ? { as_of: asOf } : {}) }),
      signal,
    });
    if (response.ok && response.headers.get('Content-Type')?.includes('application/x-ndjson'))
      return await readIdeaEvents(response, onProgress);
    const body = await response.json().catch(() => ({}));
    if (!response.ok) throw new IdeaError(response.status, body.error || response.statusText);
    return body;
  } catch (error) {
    if (error.name === 'AbortError' || error instanceof IdeaError) throw error;
    throw new IdeaError(0, `Cannot reach the service at ${api}`);
  }
}

/** Decode newline records across arbitrary network and UTF-8 chunk boundaries. */
export async function readIdeaEvents(response, onProgress) {
  if (!response.body) throw new IdeaError(502, 'The service returned no analysis stream');
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let pending = '',
    result,
    completed = false;
  const consume = (line) => {
    if (!line.trim()) return;
    let event;
    try {
      event = JSON.parse(line);
    } catch {
      throw new IdeaError(502, 'The service returned an invalid analysis update');
    }
    if (event.type === 'progress') onProgress(event.stage);
    else if (event.type === 'result') {
      result = event.data;
      completed = true;
    } else if (event.type === 'error') throw new IdeaError(event.status, event.message);
    else throw new IdeaError(502, 'The service returned an unknown analysis update');
  };
  try {
    while (true) {
      const { value, done } = await reader.read();
      pending += decoder.decode(value, { stream: !done });
      const lines = pending.split('\n');
      pending = lines.pop();
      for (const line of lines) consume(line);
      if (done) break;
    }
    consume(pending);
    if (!completed) throw new IdeaError(502, 'The service stopped before returning the analysis');
    return result;
  } finally {
    await reader.cancel().catch(() => {});
    reader.releaseLock();
  }
}

/** Chosen theses are peers; related theses attach to their explicit source. */
export function graphOf(card) {
  const weights = new Map(
    (card.reading?.composite?.drivers || []).map((entry) => [
      entry.thesis_id,
      entry.weight_percent,
    ]),
  );
  const chosen = byImpactWeight(card.reading?.chosen || [], (entry) => weights.get(entry.view_id));
  return chosen.length
    ? {
        rootIds: [...new Set(chosen.map((entry) => entry.view_id))],
        branches: (card.related || []).map((entry) => ({
          sourceId: entry.via,
          targetId: entry.view_id,
        })),
      }
    : {};
}

const VERDICT = { holds: 'Holds', not_yet: 'Not yet', borderline: 'Borderline' };

export function fmtUsd(value) {
  const units = [
    [1e12, 'T'],
    [1e9, 'B'],
    [1e6, 'M'],
  ];
  for (const [size, suffix] of units) {
    if (Math.abs(value) >= size) {
      const n = value / size;
      return `$${Number.isInteger(n) ? n : n.toFixed(2).replace(/\.?0+$/, '')}${suffix}`;
    }
  }
  return `$${value}`;
}

/** What the card's chip and status line say, from the service's answer alone (no DOM). `scoreOf(position)`
 * renders a ladder position the way the thesis cards do (+2 … −2) when the thesis is loaded. */
export function statusOf(card, scoreOf = (position) => `position ${position}`) {
  if (card.no_recorded_view)
    return {
      badge: 'No thesis',
      cls: 'chip--line',
      line: 'No recorded view on anything in this idea.',
      summary: '',
    };
  const chosen = card.reading?.chosen || [];
  const summary = esc(card.reading.summary);
  if (!chosen.length) return { badge: 'No thesis', cls: 'chip--line', line: '', summary };
  const e = card.evaluation;
  if (e && e.evaluable !== false && e.verdict && VERDICT[e.verdict]) {
    const claim = `${e.comparator} ${fmtUsd(e.value_usd)}`;
    const at = e.claim_position ? ` at ${scoreOf(e.claim_position)}` : '';
    return {
      badge: VERDICT[e.verdict],
      cls: e.verdict === 'holds' ? 'chip--ink' : 'chip--line',
      line: `Your claim <b>${esc(claim)}</b>${esc(at)} ${SEP} Judged <b>${esc(scoreOf(e.judged_position))}</b> ${esc(e.judged_label || '')}`,
      summary,
    };
  }
  return {
    badge: `${chosen.length} ${chosen.length === 1 ? 'thesis' : 'theses'}`,
    cls: 'chip--line',
    line: '',
    summary,
  };
}

/** The card element the canvas leads with. `state` is one of pending, answered, failed. */
export function ideaCard({
  text,
  state,
  card,
  error,
  scoreOf,
  onOpen,
  composite,
  day,
  chartStart,
  progress = ['search'],
  width = CARD_WIDTH,
}) {
  let chip,
    line,
    summary = '';
  if (state === 'pending') {
    chip = { badge: '', cls: '' };
    line = '';
  } else if (state === 'failed') {
    chip = { badge: 'Error', cls: 'chip--line' };
    line = esc(
      error?.status ? `${error.status}: ${error.message}` : error?.message || 'Unknown error',
    );
  } else {
    const status = statusOf(card, scoreOf);
    chip = status;
    line = status.line;
    summary = status.summary;
  }
  const point = composite ? compositeAt(composite, day || composite.as_of) : null;
  const badge =
    state === 'pending' || composite
      ? ''
      : `<span class="chip ${chip.cls}">${esc(chip.badge)}</span>`;
  const chart = composite
    ? `<div class="idea-composite">${scoreHistoryChart(confidenceHistory(composite), { start: chartStart || composite.start, end: composite.as_of, day: day || composite.as_of, width: width - 34, scoreLabel: formatConfidence(confidenceFromScore(point?.value ?? null)), scale: 'confidence' })}</div>`
    : '';
  const html = `${cardHeaderHtml('Idea', badge)}
    <div class="card__body"><div class="card__q card__q--two">${esc(text)}</div>
    ${state === 'pending' ? ideaProgressHtml(progress) : ''}${line ? `<div class="card__status">${line}</div>` : ''}${summary ? `<div class="card__summary">${summary}</div>` : ''}${chart}</div>`;
  const node = element('div', `card card--idea${composite ? ' has-composite' : ''}`, html);
  if (state === 'pending') node.setAttribute('aria-busy', 'true');
  if (state === 'answered' && onOpen) {
    node.tabIndex = 0;
    node.setAttribute('role', 'button');
    node.setAttribute('aria-label', `View analysis for ${text}`);
    const open = () => {
      node.focus({ preventScroll: true });
      onOpen();
    };
    node.addEventListener('click', open);
    node.addEventListener('keydown', (event) => {
      if (event.target === node && ['Enter', ' '].includes(event.key)) {
        event.preventDefault();
        open();
      }
    });
  }
  return node;
}

/** The theses' full records for the cards the canvas will draw, fetched after the card so the idea shows first. */
export async function readBundles(api, ids, asOf, { signal } = {}) {
  if (!ids.length) return null;
  let response;
  try {
    response = await fetch(
      `${api}/thesis-bundles?ids=${encodeURIComponent(ids.join(','))}&as_of=${encodeURIComponent(asOf)}`,
      { signal },
    );
  } catch (error) {
    if (error.name === 'AbortError') throw error;
    throw new IdeaError(0, `Cannot reach the service at ${api}`);
  }
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new IdeaError(response.status, body.error || response.statusText);
  return body;
}

/** Every thesis id a card wants drawn: the mapped views, then the graph's related views. */
export function idsOf(card) {
  const chosen = (card.reading?.chosen || []).map((c) => c.view_id);
  const related = (card.related || []).map((r) => r.view_id);
  return [...chosen, ...related];
}
