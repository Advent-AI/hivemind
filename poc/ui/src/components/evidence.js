import { esc, safeLink } from './dom.js';
import { longDay, isCalendarDay } from '../model/dates.js';
import { humanise, isSuperseded } from '../model/thesis.js';

export function assessmentHtml(v, j, context = 'overview') {
  const text = assessmentText(v, j.reasons || j.why_changed || 'No assessment recorded.');
  const id = `${context}-assessment-${v.id}`;
  return `<div class="assessment"><p class="detail-copy assessment-copy" id="${id}">${text}</p><button type="button" class="assessment-toggle" data-assessment-toggle aria-expanded="false" aria-controls="${id}"><span class="assessment-toggle-label">Read more</span><svg viewBox="0 0 16 16" aria-hidden="true"><path d="m4 6 4 4 4-4"/></svg></button></div>`;
}
export function assessmentText(thesis, text) {
  const references = new Map();
  const evidenceById = new Map(thesis.evidence.map((e) => [e.id, e]));
  const normalized = humanise(thesis, text).replace(
    /\[\s*e\d+(?:\s*[,–-]\s*e\d+)*\s*\]|\(\s*e\d+(?:\s*[,–-]\s*e\d+)*\s*\)/g,
    (group) =>
      group.match(/e\d+/g).every((id) => evidenceById.has(id)) ? group.slice(1, -1) : group,
  );
  return esc(normalized).replace(/\be\d+\b/g, (id) => {
    const evidence = evidenceById.get(id);
    if (!evidence) return id;
    if (!references.has(id)) references.set(id, references.size + 1);
    return `<button type="button" class="evidence-citation" data-citation="${id}" aria-label="Show evidence: ${esc(evidence.one_line)}">[${references.get(id)}]</button>`;
  });
}
export function evidenceHtml(e, day) {
  const publisher = e.source.publisher || e.speaker || e.source.title || 'Source unavailable';
  const replaced = isSuperseded(e, day);
  const title = e.source.title || publisher;
  const sourceLink = safeLink(e.source.uri, title, 'evidence-source');
  const attribution = e.original_who || e.speaker || publisher;
  const original = attribution !== publisher ? attribution : '';
  const typeAndDate = `${esc(e.tier)} | ${esc(longDay(e.day))}${replaced ? ' | Superseded' : ''}`;
  const metadata = `<span class="evidence-meta">${esc(original || publisher)} | ${typeAndDate}</span>`;
  const sourceMetadata = `<span class="source-meta"> | ${typeAndDate}</span>`;
  const sources = e.sources.filter((s) => s.arrival_day <= day);
  const sourceList = sources.length
    ? sources
        .map(
          (s) =>
            `<div class="source-record"><span class="source-publisher">${esc(s.source.publisher || 'Source')} | ${esc(longDay(s.day))}</span>${safeLink(s.source.uri, s.source.title || s.input_id, 'evidence-source')}</div>`,
        )
        .join('')
    : `<span class="source-publisher">${esc(publisher)}${original ? '' : sourceMetadata}</span>${sourceLink}`;
  return `<details class="evidence-row" data-evidence-id="${esc(e.id)}"><summary><span class="evidence-line">${esc(e.one_line)}</span>${metadata}</summary>
    <div class="evidence-expanded"><blockquote class="evidence-quote">“${esc(e.quote || e.one_line)}”</blockquote><dl class="evidence-provenance"><dt>Source${sources.length > 1 ? ` documents (${sources.length})` : ' document'}</dt><dd>${sourceList}</dd>
    ${original ? `<dt>${e.original_who ? 'Original source' : 'Speaker'}</dt><dd>${esc(original)} | ${esc(e.tier)}${e.original_date ? ` | ${esc(isCalendarDay(e.original_date) ? longDay(e.original_date) : e.original_date)}` : ''}</dd>` : ''}
    ${e.event_time ? `<dt>Event / period</dt><dd>${esc(e.event_time)}</dd>` : ''}</dl></div></details>`;
}
