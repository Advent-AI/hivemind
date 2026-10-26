import { esc, element, ICON, SEP } from '../components/dom.js';
import { longDay } from '../model/dates.js';
import { createDrawerMotion } from '../components/drawer-motion.js';
import { createDisclosures } from '../components/disclosure.js';
import { createDetailTabs } from '../components/detail-tabs.js';
import { weightBadgeHtml } from '../components/primitives.js';
import { compositeAt, confidenceFromScore, formatConfidence, byImpactWeight } from './composite.js';

export function ideaDetailMetaHtml(trial, day, createdDay) {
  const value = trial ? confidenceFromScore(compositeAt(trial, day || trial.as_of).value) : null;
  const tone = value === null || value === 50 ? 'neutral' : value > 50 ? 'positive' : 'negative';
  return `<span class="chip chip--state state--${tone}">AI confidence: ${formatConfidence(value)}</span><span class="detail-meta-item">${SEP}<span>Idea created: ${createdDay ? esc(longDay(createdDay)) : 'Not recorded'}</span></span>`;
}

function driverHtml(driver, weighted) {
  const weight = weighted ? weightBadgeHtml(driver.weight_percent) : '';
  const rationale = weighted
    ? `<div class="analysis-driver__reason"><h5>Weight rationale</h5><p class="detail-copy">${esc(driver.weight_reason)}</p></div>`
    : '';
  return `<section class="analysis-driver"><div class="analysis-driver__header">${weight}<h4>${esc(driver.question)}</h4></div><div class="analysis-driver__reason"><h5>Relevance</h5><p class="detail-copy">${esc(driver.reason)}</p></div>${rationale}</section>`;
}

function compositeHtml(trial, day) {
  if (!trial) return '';
  const point = compositeAt(trial, day || trial.as_of);
  const automatic = ['idea-composite/2', 'idea-composite/3', 'idea-composite/4'].includes(
    trial.version,
  );
  const weighted = trial.method === 'weighted';
  const excluded =
    automatic && trial.excluded.length
      ? `<div class="analysis-search"><h4>Not separately weighted</h4><ul class="analysis-theses">${trial.excluded.map((entry) => `<li>${weighted ? '0% | ' : ''}${esc(entry.question)}<p class="detail-muted">${esc(entry.reason)}</p></li>`).join('')}</ul></div>`
      : '';
  const missing =
    weighted && point.scored < point.total
      ? '<p class="detail-muted">The composite is unavailable until every weighted driver has an assessment. Missing weight is not reassigned.</p>'
      : '';
  const drivers = byImpactWeight(trial.drivers)
    .map((driver) => driverHtml(driver, weighted))
    .join('');
  const replayNote =
    trial.version === 'idea-composite/4'
      ? ''
      : `<p class="detail-muted">${weighted ? 'Weights remain fixed during replay.' : 'Equal weight across available drivers.'} ${trial.excluded.length} other ${trial.excluded.length === 1 ? 'connection is' : 'connections are'} not separately weighted.</p>`;
  return `<section class="analysis-section"><h3 class="detail-heading analysis-theses-heading">Theses</h3>${missing}${drivers}${replayNote}${excluded}</section>`;
}

function readingStepHtml(part, index, matches) {
  return `<details class="detail-disclosure analysis-reading-part" open><summary><span class="analysis-reading-summary"><span class="analysis-reading-title">${index + 1}. ${esc(part.looks_for)}</span><span class="analysis-reading-meta">${esc(part.object)} ${SEP} ${esc(part.period)}</span></span></summary><div class="detail-disclosure-body"><p class="detail-copy">${esc(part.why || 'No explanation was returned for this part.')}</p>${matches(part)}</div></details>`;
}

/** Keep each returned explanation and search record in its corresponding detail section. */
export function ideaAnalysisSections(card, theses = [], trial = null, day) {
  const reading = card.reading;
  const names = new Map(theses.map((thesis) => [thesis.id, thesis.question]));
  const title = (id) => esc(names.get(id) || `Thesis ${id} (not loaded)`);
  const list = (ids) =>
    `<ul class="analysis-theses">${ids.map((id) => `<li>${title(id)}</li>`).join('')}</ul>`;
  const matches = (part) =>
    [
      ['Direct match', part.direct || []],
      ['Related drivers', part.driver || []],
      ['Context', part.context || []],
    ]
      .map(([label, ids]) =>
        ids.length
          ? `<div class="analysis-matches"><h4>${label}</h4>${list(ids)}</div>`
          : label === 'Direct match'
            ? '<p class="detail-muted">No direct thesis was selected.</p>'
            : '',
      )
      .join('');
  const summary =
    reading?.summary ||
    (card.no_recorded_view
      ? 'No recorded thesis matches this idea. No analysis was generated.'
      : 'No summary was returned.');
  const parts = reading?.parts || [];
  const response = {
    idea: card.idea,
    search: card.search,
    reading,
    evaluation: card.evaluation,
    related: card.related,
    cost: card.cost,
  };
  const overview = `<section class="analysis-section"><h3 class="detail-heading">Summary</h3><p class="detail-copy">${esc(summary)}</p></section>${compositeHtml(trial, day)}`;
  const readingSteps = parts.length
    ? `<section class="analysis-section"><h3 class="detail-heading">Reading steps</h3>${parts.map((part, index) => readingStepHtml(part, index, matches)).join('')}</section>`
    : '<section class="analysis-section"><h3 class="detail-heading">Reading steps</h3><p class="detail-muted">No reading steps were returned.</p></section>';
  const excluded = reading?.dropped?.length
    ? `<section class="analysis-section"><h3 class="detail-heading">Excluded choices</h3>${reading.dropped.map((choice) => `<div class="analysis-search">${choice.view_id ? `<h4>${title(choice.view_id)}</h4>` : ''}<p class="detail-copy">${esc(choice.why)}</p></div>`).join('')}</section>`
    : '';
  return {
    overview,
    trace: readingSteps + excluded,
    response: `<pre class="analysis-json" aria-label="Idea response">${esc(JSON.stringify(response, null, 2))}</pre>`,
  };
}

const IDEA_TABS = [
  ['overview', 'Overview'],
  ['trace', 'Trace'],
  ['response', 'Response'],
];
let detailCount = 0;

export function ideaAnalysisHtml(card, theses = [], trial = null, day, scope = 'idea-detail') {
  const sections = ideaAnalysisSections(card, theses, trial, day);
  return IDEA_TABS.map(
    ([id]) =>
      `<section id="${scope}-panel-${id}" data-idea-panel="${id}" role="tabpanel" aria-labelledby="${scope}-tab-${id}"${id === 'overview' ? '' : ' hidden'}>${sections[id]}</section>`,
  ).join('');
}

/** Read-only Idea detail, using the same motion and disclosure controls as thesis details. */
export function createIdeaDetail({ root }) {
  root.classList.add('hm-ui');
  const scope = `idea-detail-${++detailCount}`;
  const sheet = element('div', 'sheet idea-detail');
  sheet.hidden = true;
  sheet.innerHTML = `<div class="sheet__scrim"></div><aside class="sheet__panel" role="dialog" aria-modal="true" aria-label="Idea analysis"><div class="sheet__top"><span class="card__kind">${ICON.idea}<span>Idea</span></span><button class="sheet-close" type="button" aria-label="Close idea analysis"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg></button></div><div class="detail-hero"><h2 class="panel__title"></h2><div class="detail-meta"></div></div><nav class="detail-tabs" role="tablist" aria-label="Idea details">${IDEA_TABS.map(([id, label]) => `<button class="detail-tab" type="button" role="tab" id="${scope}-tab-${id}" data-tab="${id}" aria-controls="${scope}-panel-${id}" aria-selected="${id === 'overview'}" tabindex="${id === 'overview' ? 0 : -1}">${label}</button>`).join('')}</nav><div class="detail-content"></div></aside>`;
  root.append(sheet);
  const body = sheet.querySelector('.detail-content');
  const button = sheet.querySelector('.sheet-close');
  const events = new AbortController();
  const disclosures = createDisclosures(body);
  let opener = null;
  const motion = createDrawerMotion({
    sheet,
    panel: sheet.querySelector('.sheet__panel'),
    scrim: sheet.querySelector('.sheet__scrim'),
    onClosed: () => opener?.focus({ preventScroll: true }),
  });
  const tabs = createDetailTabs(sheet, { beforeSelect: () => disclosures.cancel() });
  function close() {
    disclosures.cancel();
    motion.close();
  }
  button.addEventListener('click', close, { signal: events.signal });
  sheet.querySelector('.sheet__scrim').addEventListener('click', close, { signal: events.signal });
  sheet.addEventListener(
    'keydown',
    (event) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        close();
      }
      if (event.key === 'Tab') {
        const controls = [
          ...sheet.querySelectorAll('button:not([disabled]):not([tabindex="-1"]),summary,a[href]'),
        ].filter((el) => el.getClientRects().length);
        if (event.shiftKey && document.activeElement === controls[0]) {
          event.preventDefault();
          controls.at(-1)?.focus();
        } else if (!event.shiftKey && document.activeElement === controls.at(-1)) {
          event.preventDefault();
          controls[0]?.focus();
        }
      }
    },
    { signal: events.signal },
  );
  return {
    open(card, theses = [], trial = null, day, createdDay) {
      disclosures.cancel();
      opener = document.activeElement;
      sheet.querySelector('.panel__title').textContent = card.idea?.text || 'Idea analysis';
      sheet.querySelector('.detail-meta').innerHTML = ideaDetailMetaHtml(trial, day, createdDay);
      body.innerHTML = ideaAnalysisHtml(card, theses, trial, day, scope);
      tabs.select('overview');
      motion.open();
      button.focus({ preventScroll: true });
    },
    close,
    destroy() {
      events.abort();
      disclosures.destroy();
      tabs.destroy();
      motion.destroy();
      sheet.remove();
    },
  };
}
