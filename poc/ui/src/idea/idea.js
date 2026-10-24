/** The Idea card: the user's sentence read by the service (POST /ideas, docs/poc/idea-card.md, D112).
 * This module posts the idea, connects every chosen thesis to it, and renders the card: the sentence,
 * the service's reading, and the verdict on a number the idea
 * states. It never chooses theses itself and never reads the clock; the day is the answer's as_of. */
import { element, esc, SEP } from '../components/dom.js';
import { cardHeaderHtml } from '../components/primitives.js';

export class IdeaError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

/** POST the idea; resolves to the card the service returns, rejects with IdeaError on any non-200 answer. */
export async function readIdea(api, text, { signal } = {}) {
  let response;
  try {
    response = await fetch(`${api}/ideas`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, bundles: false }),
      signal,
    });
  } catch (error) {
    if (error.name === 'AbortError') throw error;
    throw new IdeaError(0, `Cannot reach the service at ${api}`);
  }
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new IdeaError(response.status, body.error || response.statusText);
  return body;
}

/** Chosen theses are peers; related theses attach to their explicit source. */
export function graphOf(card) {
  const chosen = card.reading?.chosen || [];
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
export function ideaCard({ text, state, card, error, scoreOf }) {
  let chip,
    line,
    summary = '';
  if (state === 'pending') {
    chip = { badge: 'Reading…', cls: 'chip--line' };
    line = 'Searching the library and reading the candidates';
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
  const html = `${cardHeaderHtml('Idea', `<span class="chip ${chip.cls}">${esc(chip.badge)}</span>`)}
    <div class="card__body"><div class="card__q card__q--two">${esc(text)}</div>
    ${line ? `<div class="card__status">${line}</div>` : ''}${summary ? `<div class="card__summary">${summary}</div>` : ''}</div>`;
  return element('div', 'card card--idea', html);
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
