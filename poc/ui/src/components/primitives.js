import { esc, ICON } from './dom.js';
import { score, stateTone, stateWords } from '../model/thesis.js';

export function cardHeaderHtml(kind, badge = '') {
  const icon = { Idea: ICON.idea, Thesis: ICON.thesis, Trigger: ICON.trigger, Action: ICON.action }[
    kind
  ];
  if (!icon) throw new TypeError(`Unknown card kind: ${kind}`);
  return `<div class="card__head"><span class="card__kind">${icon}<span>${kind}</span></span><span class="card__spacer"></span>${badge}</div>`;
}

export function weightBadgeHtml(weightPercent) {
  if (weightPercent === undefined) return '';
  if (!Number.isInteger(weightPercent) || weightPercent < 0 || weightPercent > 100)
    throw new TypeError('Impact weight must be an integer percentage');
  return `<span class="chip chip--line card__weight" aria-label="Impact weight: ${weightPercent}%"><span class="card__weight-icon" aria-hidden="true">${ICON.scale}</span><span class="card__weight-value">${weightPercent}%</span></span>`;
}

export function badgeHtml(thesis, judgement) {
  if (!judgement) return '<span class="chip">Not assessed yet</span>';
  const { main, label } = stateWords(thesis, judgement.rung);
  return `<span class="chip chip--state ${stateTone(score(thesis, judgement.rung))}"><b>${esc(main)}</b>${label ? `<span class="state-label">${esc(label)}</span>` : ''}</span>`;
}
export function axisScore(thesis, position, x, y, current) {
  return `<g class="axis-score ${stateTone(score(thesis, position))}${position === current ? ' is-current' : ''}" data-pos="${position}" transform="translate(${x} ${y})"><rect x="-13" y="-9" width="26" height="18" rx="5"/><text>${esc(score(thesis, position))}</text></g>`;
}
