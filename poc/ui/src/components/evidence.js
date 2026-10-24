import { esc, safeLink } from './dom.js';
import { longDay } from '../model/dates.js';
import { humanise } from '../model/thesis.js';

export function assessmentHtml(v, j, context = 'overview') {
  const text = esc(humanise(v, j.reasons || j.why_changed || 'No assessment recorded.'));
  const id = `${context}-assessment-${v.id}`;
  return `<div class="assessment"><p class="detail-copy assessment-copy" id="${id}">${text}</p><button type="button" class="assessment-toggle" data-assessment-toggle aria-expanded="false" aria-controls="${id}"><span class="assessment-toggle-label">Read more</span><svg viewBox="0 0 16 16" aria-hidden="true"><path d="m4 6 4 4 4-4"/></svg></button></div>`;
}
export function evidenceHtml(e, day) {
  const publisher = e.source.publisher || e.speaker || e.source.title || 'Source unavailable';
  const replaced = e.replaced_by && e.replaced_by.said_day <= day;
  const title = e.source.title || publisher;
  const sourceLink = safeLink(e.source.uri, title, 'evidence-source');
  const original =
    e.original_who && e.original_who !== e.speaker && e.original_who !== publisher
      ? e.original_who
      : '';
  const typeAndDate = `${esc(e.tier)} | ${esc(longDay(e.day))}${replaced ? ' | Superseded' : ''}`;
  const metadata = `<span class="evidence-meta">${esc(original || publisher)} | ${typeAndDate}</span>`;
  const sourceMetadata = `<span class="source-meta"> | ${typeAndDate}</span>`;
  return `<details class="evidence-row" data-evidence-id="${esc(e.id)}"><summary><span class="evidence-line">${esc(e.one_line)}</span>${metadata}</summary>
    <div class="evidence-expanded"><blockquote class="evidence-quote">“${esc(e.quote || e.one_line)}”</blockquote><dl class="evidence-provenance"><dt>Source document</dt><dd><span class="source-publisher">${esc(publisher)}${original ? '' : sourceMetadata}</span>${sourceLink}</dd>
    ${original ? `<dt>Original source</dt><dd>${esc(original)}${sourceMetadata}</dd>` : ''}</dl></div></details>`;
}
