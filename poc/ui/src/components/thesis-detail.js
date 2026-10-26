import { element, esc, SEP, ICON } from './dom.js';
import { longDay } from '../model/dates.js';
import { lastOf, score, rungLabel, statusAt, snapshotThesis } from '../model/thesis.js';
import { ladderChart, bindHistoryChart } from './thesis-chart.js';
import { badgeHtml } from './primitives.js';
import { assessmentHtml, assessmentText, evidenceHtml } from './evidence.js';
import { createDisclosures } from './disclosure.js';
import { createSelect } from './select.js';
import { createDrawerMotion } from './drawer-motion.js';
import { createDetailTabs } from './detail-tabs.js';
import { relationsHtml, identityHtml } from './relations.js';

let instanceCount = 0;
export function createThesisDetail({ root, dataset, onOpen = () => {} }) {
  let data = dataset;
  let thesisById = Object.fromEntries(data.theses.map((t) => [t.id, t]));
  let detail = null;
  let chartController = null;
  let selectControl = null;
  let returnFocus = null;
  const prefix = `thesis-detail-${++instanceCount}-`;
  const events = new AbortController();
  const sheet = element('div', 'sheet');
  sheet.hidden = true;
  root.append(sheet);
  const scopeSelector = (selector) =>
    selector.replace(/#([\w-]+)/g, (_, id) => `[data-ui-id="${id}"]`);
  const all = (selector) => sheet.querySelectorAll(scopeSelector(selector));
  const find = (id) => sheet.querySelector(`[data-ui-id="${id}"]`);
  function setHTML(node, html) {
    node.innerHTML = html
      .replace(/\sid="([^"]+)"/g, (_, id) => ` id="${prefix}${id}" data-ui-id="${id}"`)
      .replace(
        /\b(aria-controls|aria-labelledby)="([^"]+)"/g,
        (_, attr, value) =>
          `${attr}="${value
            .split(' ')
            .map((id) => prefix + id)
            .join(' ')}"`,
      )
      .replace(/url\(#([^)]+)\)/g, (_, id) => `url(#${prefix}${id})`);
  }
  setHTML(
    sheet,
    `<div class="sheet__scrim" id="sheetScrim"></div><aside class="sheet__panel" id="sheetPanel" role="dialog" aria-modal="true" aria-labelledby="detailTitle"><div class="sheet__top"><span class="card__kind" id="sheetKicker"></span><button class="sheet-close" id="sheetClose" type="button" aria-label="Close thesis details"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg></button></div><div class="sheet__body" id="sheetBody"></div></aside>`,
  );
  const disclosures = createDisclosures(find('sheetBody'));
  const tabs = createDetailTabs(sheet, {
    beforeSelect() {
      disclosures.cancel();
      closeEvidenceType();
    },
    onSelect(tab) {
      const panel = find(`panel-${tab}`);
      if (tab === 'evidence' && !panel.dataset.ready) renderEvidence();
      if (tab === 'history' && !panel.dataset.ready) renderHistory();
    },
  });
  const motion = createDrawerMotion({
    sheet,
    panel: find('sheetPanel'),
    scrim: find('sheetScrim'),
    onClosed: () => returnFocus?.focus({ preventScroll: true }),
  });
  function close() {
    disclosures.cancel();
    selectControl?.close();
    motion.close();
  }
  find('sheetClose').addEventListener('click', close, { signal: events.signal });
  find('sheetScrim').addEventListener('click', close, { signal: events.signal });
  sheet.addEventListener(
    'click',
    (event) => {
      const citation = event.target.closest('[data-citation]');
      if (!citation || !detail) return;
      const evidence = detail.thesis.evidence.find((e) => e.id === citation.dataset.citation);
      if (!evidence) return;
      const historical = citation.closest('[role="tabpanel"]')?.dataset.uiId === 'panel-history';
      if (historical) {
        const row = find('historyAssessment').querySelector(`[data-evidence-id="${evidence.id}"]`);
        if (row) {
          row.open = true;
          row.parentElement.closest('details').open = true;
          row.scrollIntoView({ block: 'nearest' });
        }
        return;
      }
      detail.query = evidence.one_line;
      detail.tier = '';
      selectControl?.destroy();
      selectControl = null;
      delete find('panel-evidence').dataset.ready;
      tabs.select('evidence');
      find('evidenceSearch').value = detail.query;
      const row = sheet.querySelector(`[data-evidence-id="${evidence.id}"]`);
      if (row) {
        row.open = true;
        row.scrollIntoView({ block: 'nearest' });
      }
    },
    { signal: events.signal },
  );
  document.addEventListener(
    'keydown',
    (event) => {
      if (sheet.hidden || !sheet.contains(document.activeElement)) return;
      if (event.key === 'Escape') {
        event.preventDefault();
        if (!closeEvidenceType(true)) close();
      }
      if (event.key === 'Tab') {
        const items = [
          ...sheet.querySelectorAll('button:not([disabled]),input,a[href],[tabindex="0"]'),
        ].filter((e) => e.getClientRects().length);
        if (event.shiftKey && document.activeElement === items[0]) {
          event.preventDefault();
          items.at(-1)?.focus();
        } else if (!event.shiftKey && document.activeElement === items.at(-1)) {
          event.preventDefault();
          items[0]?.focus();
        }
      }
    },
    { signal: events.signal },
  );
  function open(id, day = data.as_of) {
    const thesis = thesisById[id];
    if (!thesis) throw new Error(`Unknown thesis: ${id}`);
    if (day > data.as_of || day < (data.days[0] || data.as_of))
      throw new Error(`Date outside loaded history: ${day}`);
    onOpen(id);
    selectControl?.destroy();
    selectControl = null;
    chartController?.destroy();
    chartController = null;
    disclosures.cancel();
    if (sheet.hidden || !sheet.contains(document.activeElement))
      returnFocus = document.activeElement;
    const snapshot = snapshotThesis(thesis, day);
    detail = {
      thesis: snapshot,
      day,
      selected: snapshot.judgements.length - 1,
      evidenceLimit: 20,
      query: '',
      tier: '',
    };
    setHTML(find('sheetKicker'), `${ICON.thesis}<span>Thesis</span>`);
    renderPanel();
    motion.open();
    find('sheetClose').focus({ preventScroll: true });
  }
  function renderPanel() {
    const v = detail.thesis,
      latest = lastOf(v.judgements);
    const citations = latest ? new Set(latest.cited) : new Set();
    const keyEvidence = v.evidence
      .filter((e) => citations.has(e.id))
      .sort((a, b) => b.day.localeCompare(a.day) || b.seq - a.seq)
      .slice(0, 3);
    setHTML(
      find('sheetBody'),
      `
    <div class="detail-hero"><h2 class="panel__title" id="detailTitle">${esc(v.question)}</h2><div class="detail-meta">${latest ? badgeHtml(v, latest) : '<span class="chip">Not assessed yet</span>'}<span class="detail-meta-item">${SEP}<span>${latest ? `Last updated: ${esc(longDay(latest.day))}` : `Opens ${esc(longDay(v.created_day))}`}</span></span><span class="detail-meta-item">${SEP}<span>Due: ${esc(longDay(v.due_day))}</span></span></div></div>
    <nav class="detail-tabs" role="tablist" aria-label="Thesis details">${[
      ['overview', 'Overview'],
      ['evidence', 'Evidence'],
      ['history', 'History'],
    ]
      .map(
        ([id, label]) =>
          `<button type="button" class="detail-tab" id="tab-${id}" role="tab" data-tab="${id}" aria-selected="${id === 'overview'}" aria-controls="panel-${id}" tabindex="${id === 'overview' ? 0 : -1}">${label}</button>`,
      )
      .join('')}</nav>
    <div class="detail-content"><section id="panel-overview" role="tabpanel" aria-labelledby="tab-overview">
      ${
        latest
          ? `<div class="detail-section"><h3 class="detail-heading">Current assessment</h3><blockquote class="detail-copy assessment-conclusion">${esc(v.rungs[latest.rung - 1].condition)}</blockquote>${assessmentHtml(v, latest)}</div>
      <details class="detail-disclosure"><summary>Recent evidence</summary><div class="detail-disclosure-body">${keyEvidence.length ? keyEvidence.map((e) => evidenceHtml(e, detail.day)).join('') : '<p class="detail-muted">No evidence cited in this assessment.</p>'}</div></details>`
          : '<p class="detail-copy">There is no assessment for this thesis at the selected date.</p>'
      }
      ${relationsHtml(v, data, detail.day)}
      <details class="detail-disclosure"><summary>About this thesis</summary><dl class="detail-definitions">${identityHtml(v)}<dt>First seen</dt><dd>${esc(longDay(v.created_day))}</dd><dt>Original source</dt><dd>${esc(v.created_from.title)}</dd><dt>Status</dt><dd><span class="chip chip--line">${statusAt(v, detail.day)}</span></dd></dl></details>
    </section><section id="panel-evidence" role="tabpanel" aria-labelledby="tab-evidence" hidden></section><section id="panel-history" role="tabpanel" aria-labelledby="tab-history" hidden></section></div>`,
    );
    all('[data-thesis]').forEach(
      (button) => (button.onclick = () => open(button.dataset.thesis, detail.day)),
    );
  }
  function renderEvidence() {
    const panel = find('panel-evidence');
    panel.dataset.ready = 'true';
    const tiers = [...new Set(detail.thesis.evidence.map((e) => e.tier))];
    setHTML(
      panel,
      `<div class="evidence-tools"><input class="detail-input" id="evidenceSearch" type="search" placeholder="Find evidence…" aria-label="Find evidence"><div id="evidenceTypeFilter"></div></div><div id="evidenceResults"></div>`,
    );
    find('evidenceSearch').oninput = (event) => {
      detail.query = event.target.value;
      detail.evidenceLimit = 20;
      drawEvidence();
    };
    selectControl = createSelect(find('evidenceTypeFilter'), {
      options: ['', ...tiers].map((tier) => ({ value: tier, label: tier || 'All types' })),
      value: detail.tier,
      label: 'Evidence type',
      onChange(tier) {
        detail.tier = tier;
        detail.evidenceLimit = 20;
        drawEvidence();
      },
    });
    drawEvidence();
  }
  function closeEvidenceType(restoreFocus = false) {
    return selectControl?.close(restoreFocus) || false;
  }
  function drawEvidence() {
    const query = detail.query.trim().toLowerCase();
    const rows = detail.thesis.evidence
      .filter(
        (e) =>
          (!detail.tier || e.tier === detail.tier) &&
          (!query ||
            `${e.one_line} ${e.quote} ${e.speaker} ${e.source.publisher} ${e.source.title}`
              .toLowerCase()
              .includes(query)),
      )
      .sort((a, b) => b.day.localeCompare(a.day) || b.seq - a.seq);
    setHTML(
      find('evidenceResults'),
      rows.length
        ? rows
            .slice(0, detail.evidenceLimit)
            .map((e) => evidenceHtml(e, detail.day))
            .join('') +
            (rows.length > detail.evidenceLimit
              ? '<button type="button" class="detail-link detail-more" id="moreEvidence">Show more</button>'
              : '')
        : '<p class="detail-muted">No evidence matches.</p>',
    );
    find('moreEvidence')?.addEventListener('click', () => {
      detail.evidenceLimit += 20;
      drawEvidence();
    });
  }
  function selectAssessment(index, anchorDay) {
    disclosures.cancel();
    const v = detail.thesis;
    detail.selected = index;
    const j = v.judgements[index];
    detail.historyAnchorDay =
      anchorDay === null ? null : j?.day || anchorDay || data.days[0] || data.as_of;
    all('#historyChart .node').forEach((node) =>
      node.classList.toggle('node--now', Boolean(j && v.judgements[+node.dataset.i].day === j.day)),
    );

    if (!j) {
      setHTML(
        find('historyAssessment'),
        `<div class="history-head"><h3 class="detail-heading">${esc(longDay(anchorDay))}</h3></div><p class="detail-copy">No assessment existed on this date.</p>`,
      );
      return;
    }
    const ids = new Set(j.cited);
    setHTML(
      find('historyAssessment'),
      `<div class="history-head"><h3 class="detail-heading">${esc(longDay(j.day))}</h3>${badgeHtml(v, j)}</div>${assessmentHtml(v, j, 'history')}
    ${j.changed && j.why_changed ? `<details class="detail-disclosure"><summary>Score change</summary><p class="detail-copy">${assessmentText(v, j.why_changed)}</p></details>` : ''}
    <details class="detail-disclosure"><summary>Cited evidence</summary>${
      v.evidence
        .filter((e) => ids.has(e.id))
        .map((e) => evidenceHtml(e, j.day))
        .join('') || '<p class="detail-muted">No evidence cited.</p>'
    }</details>`,
    );
  }
  function renderHistory() {
    const panel = find('panel-history');
    panel.dataset.ready = 'true';
    const v = detail.thesis;
    if (!v.judgements.length) {
      setHTML(panel, '<p class="detail-muted">No assessments at the selected date.</p>');
      return;
    }
    const hasStateLabels = v.rungs.some((r, i) => rungLabel(v, i + 1));
    const definitions = `<div class="score-table"><table aria-label="Score definitions"><colgroup><col class="score-column">${hasStateLabels ? '<col class="state-column">' : ''}<col></colgroup><thead><tr><th scope="col">Score</th>${hasStateLabels ? '<th scope="col">State</th>' : ''}<th scope="col">Definition</th></tr></thead><tbody>${v.rungs.map((r, i) => `<tr><th scope="row">${esc(score(v, i + 1))}</th>${hasStateLabels ? `<td>${esc(rungLabel(v, i + 1))}</td>` : ''}<td>${esc(r.condition)}</td></tr>`).join('')}</tbody></table></div>`;
    setHTML(
      panel,
      `<div class="history-chart" id="historyChart"></div><div id="historyAssessment"></div><details class="detail-disclosure"><summary>Score definitions</summary>${definitions}</details>`,
    );
    const chart = find('historyChart');
    setHTML(
      chart,
      ladderChart(v, {
        width: Math.max(280, panel.clientWidth),
        start: data.days[0] || data.as_of,
        end: detail.day,
        day: detail.day,
        scope: 'detail',
        interactive: true,
      }),
    );
    chartController = bindHistoryChart(chart, {
      thesis: v,
      start: data.days[0] || data.as_of,
      end: detail.day,
      onSelect: selectAssessment,
    });
    selectAssessment(detail.selected, null);
  }

  return {
    open,
    close,
    setDataset(next) {
      disclosures.cancel();
      motion.close({ immediate: true });
      chartController?.destroy();
      selectControl?.destroy();
      selectControl = null;
      chartController = null;
      data = next;
      thesisById = Object.fromEntries(next.theses.map((t) => [t.id, t]));
      detail = null;
    },
    destroy() {
      motion.destroy();
      chartController?.destroy();
      disclosures.destroy();
      tabs.destroy();
      selectControl?.destroy();
      events.abort();
      sheet.remove();
    },
  };
}
