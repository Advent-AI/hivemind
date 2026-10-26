import { esc, SEP } from './dom.js';
import { groupsFor, dependenciesAt } from '../model/thesis.js';

/** Group membership, causal dependencies and period succession stay separate. */
export function relationsHtml(thesis, data, day) {
  const loaded = new Map(data.theses.filter((t) => t.created_day <= day).map((t) => [t.id, t]));
  const button = (id) =>
    loaded.has(id)
      ? `<button class="related-item" type="button" data-thesis="${esc(id)}"><span>${esc(loaded.get(id).question)}</span></button>`
      : '<p class="detail-muted">Related thesis is not loaded.</p>';
  const groups = groupsFor(data, thesis.id, day);
  const membership = groups.length
    ? `<details class="detail-disclosure"><summary>Research groups (${groups.length})</summary><div class="detail-disclosure-body">${groups
        .map(
          (g) =>
            `<div class="thesis-group"><strong>${esc(g.name)}</strong><p>${esc(g.scope)}</p>${g.members
              .filter((m) => m.thesis_id !== thesis.id && m.day <= day)
              .map((m) => button(m.thesis_id))
              .join('')}</div>`,
        )
        .join('')}</div></details>`
    : '';
  const dependencies = dependenciesAt(thesis, day);
  const dependants = [...loaded.values()].filter((t) =>
    dependenciesAt(t, day).some((d) => d.depends_on === thesis.id),
  );
  const links =
    dependencies.length || dependants.length
      ? `<details class="detail-disclosure"><summary>Dependencies</summary><div class="detail-disclosure-body">${dependencies.map((d) => `<p class="detail-muted">Depends on${d.direction ? ` ${SEP} ${esc(d.direction)}` : ''}</p>${d.depends_on ? button(d.depends_on) : `<p class="detail-copy">Waiting for a thesis for ${esc(d.wait_year || 'a future period')}.</p>`}`).join('')}${dependants.length ? '<p class="detail-muted">Used by</p>' + dependants.map((t) => button(t.id)).join('') : ''}</div></details>`
      : '';
  const successions = thesis.successions.filter((s) => s.day <= day);
  const periods = successions.length
    ? `<details class="detail-disclosure"><summary>Other periods</summary><div class="detail-disclosure-body">${successions.map((s) => `<p class="detail-muted">${s.relation === 'previous' ? 'Previous' : 'Next'} period</p>${button(s.thesis_id)}`).join('')}</div></details>`
    : '';
  return membership + links + periods;
}

export function identityHtml(thesis) {
  const identity = thesis.identity;
  const rows = [
    ['Subject', thesis.object],
    ['Period', thesis.year],
  ];
  if (identity)
    rows.push(
      ['Measure', identity.measure.replaceAll('_', ' ')],
      ['Scope', identity.scope],
      ['Period start', identity.period_start],
      ['Period end', identity.period_end],
      ['Basis', identity.basis],
      ['Unit', identity.unit],
    );
  return rows
    .filter(([, value]) => value && value !== 'n/a')
    .map(([label, value]) => `<dt>${label}</dt><dd>${esc(value)}</dd>`)
    .join('');
}
