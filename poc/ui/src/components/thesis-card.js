import { esc, element } from './dom.js';
import { ladderChart } from './thesis-chart.js';
import { badgeHtml, cardHeaderHtml } from './primitives.js';
import { assessmentAt } from '../model/thesis.js';

export function createThesisCard(thesis, { day, start, end, onOpen, scope = 'canvas' }) {
  const card = element('div', 'card card--thesis');
  card.dataset.id = thesis.id;
  card.innerHTML = `${cardHeaderHtml('Thesis', badgeHtml(thesis, assessmentAt(thesis, day)))}<div class="card__body"><button type="button" class="card__q card__q--two card__open" aria-label="${esc('Open thesis: ' + thesis.question)}">${esc(thesis.question)}</button><div class="ladder__chart">${ladderChart(thesis, { day, start, end, scope })}</div></div>`;
  card.querySelector('.card__open').addEventListener('click', () => onOpen?.(thesis.id));
  return card;
}
