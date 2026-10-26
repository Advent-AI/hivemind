import { parseDataset } from '../model/contract.js';
import { librarySelection, libraryCounts } from '../model/library.js';
import { groupsFor, snapshotThesis, statusAt } from '../model/thesis.js';
import { addDays } from '../model/dates.js';
import { element, esc, SEP } from './dom.js';
import { createSelect } from './select.js';
import { createThesisCard } from './thesis-card.js';
import { createThesisDetail } from './thesis-detail.js';

let nextId = 0;
/** A read-only, dated library. Networking and Idea requests belong to its host. */
export function createLibrary(root, { dataset }) {
  let data = parseDataset(dataset);
  root.classList.add('hm-ui');
  const scope = `library-${++nextId}`;
  const state = {
    day: data.as_of,
    group: '',
    object: '',
    status: '',
    query: '',
    range: 'full',
    limit: 24,
  };
  const events = new AbortController();
  const shell = element('div', 'library');
  shell.innerHTML = `<aside class="library-sidebar" aria-label="Research groups"><div class="sidebar-kicker">Workspace</div><div data-library-nav></div></aside><section class="library-content"><div class="library-heading"><div><h1 data-library-title></h1><p data-library-description></p></div></div><div class="library-stats" data-library-stats></div><div class="library-tools"><input type="search" class="detail-input" aria-label="Search theses" placeholder="Search theses, subjects or groups…"><div data-subject-filter></div><div data-status-filter></div><div class="library-range" role="group" aria-label="Chart range"><button type="button" data-range="full">Full</button><button type="button" data-range="30">Last 30 days</button></div></div><div class="library-grid" data-cards></div><button class="library-more" type="button" data-more hidden>Show more</button></section>`;
  root.append(shell);
  const find = (selector) => shell.querySelector(selector);
  const details = createThesisDetail({ root, dataset: data });
  let filters = [];
  function controls() {
    filters.forEach((f) => f.destroy());
    filters = [
      createSelect(find('[data-subject-filter]'), {
        label: 'Subject',
        value: state.object,
        options: [
          { value: '', label: 'All subjects' },
          ...[...new Set(data.theses.map((t) => t.object))]
            .sort()
            .map((value) => ({ value, label: value })),
        ],
        onChange(value) {
          state.object = value;
          state.limit = 24;
          draw();
        },
      }),
      createSelect(find('[data-status-filter]'), {
        label: 'Status',
        value: state.status,
        options: [
          { value: '', label: 'All statuses' },
          { value: 'Open', label: 'Open' },
          { value: 'Closed', label: 'Closed' },
        ],
        onChange(value) {
          state.status = value;
          state.limit = 24;
          draw();
        },
      }),
    ];
  }
  function draw() {
    const counts = libraryCounts(data, state.day);
    const allLabel = data.coverage === 'library' ? 'All theses' : 'Loaded theses';
    const selected = data.groups.find((g) => g.id === state.group);
    find('[data-library-title]').textContent =
      selected?.name || (state.group === 'ungrouped' ? 'Ungrouped theses' : allLabel);
    find('[data-library-description]').textContent =
      selected?.scope ||
      (data.coverage === 'library'
        ? 'Explore the questions, evidence and assessments in your research library.'
        : 'This selection contains only the supplied theses and their loaded group members.');
    find('[data-library-stats]').innerHTML =
      `<span><b>${counts.theses}</b> ${data.coverage === 'library' ? 'theses' : 'loaded theses'}</span>${SEP}<span><b>${counts.groups}</b> research groups</span>${SEP}<span><b>${counts.evidence}</b> active evidence items</span>`;
    const groups = data.groups
      .filter((g) => g.created_day <= state.day)
      .map((g) => ({ ...g, count: g.members.filter((m) => m.day <= state.day).length }))
      .filter((g) => g.count);
    const nav = (id, name, count) =>
      `<button type="button" class="library-nav${state.group === id ? ' is-selected' : ''}" data-group="${esc(id)}" aria-pressed="${state.group === id}"><span>${esc(name)}</span><span class="library-count">${count}</span></button>`;
    find('[data-library-nav]').innerHTML =
      nav('', allLabel, counts.theses) +
      nav(
        'ungrouped',
        'Ungrouped',
        librarySelection(data, { day: state.day, group: 'ungrouped' }).length,
      ) +
      `<div class="sidebar-kicker sidebar-kicker--groups">Research groups</div>` +
      groups.map((g) => nav(g.id, g.name, g.count)).join('');
    const rows = librarySelection(data, state);
    const cards = find('[data-cards]');
    cards.replaceChildren();
    const start =
      state.range === '30'
        ? [data.days[0] || state.day, addDays(state.day, -29)].sort().at(-1)
        : data.days[0] || state.day;
    for (const thesis of rows.slice(0, state.limit)) {
      const card = createThesisCard(snapshotThesis(thesis, state.day), {
        day: state.day,
        start,
        end: state.day,
        scope,
        onOpen: (id) => details.open(id, state.day),
      });
      card.classList.add('library-card', 'is-on');
      const metadata = element('div', 'library-card-meta');
      metadata.innerHTML = `<span>${esc(thesis.object)}${thesis.year ? ` ${SEP} ${esc(thesis.year)}` : ''}</span><span class="chip chip--line">${statusAt(thesis, state.day)}</span>`;
      card.querySelector('.card__body').prepend(metadata);
      const groups = groupsFor(data, thesis.id, state.day);
      card.setAttribute(
        'aria-label',
        `${thesis.object}: ${thesis.question}${groups.length ? '. ' + groups.map((g) => g.name).join(', ') : ''}`,
      );
      card.addEventListener('click', (event) => {
        if (!event.target.closest('button')) details.open(thesis.id, state.day);
      });
      cards.append(card);
    }
    if (!rows.length)
      cards.innerHTML =
        '<div class="library-empty"><h2>No theses to show</h2><p>Try a different search, group or date.</p><button type="button" class="filter" data-clear>Clear filters</button></div>';
    find('[data-more]').hidden = rows.length <= state.limit;
    shell
      .querySelectorAll('[data-range]')
      .forEach((b) => b.setAttribute('aria-pressed', String(state.range === b.dataset.range)));
  }
  shell.addEventListener(
    'click',
    (event) => {
      const group = event.target.closest('[data-group]');
      if (group) {
        state.group = group.dataset.group;
        state.limit = 24;
        draw();
      }
      const range = event.target.closest('[data-range]');
      if (range) {
        state.range = range.dataset.range;
        draw();
      }
      if (event.target.closest('[data-more]')) {
        state.limit += 24;
        draw();
      }
      if (event.target.closest('[data-clear]')) {
        Object.assign(state, { group: '', object: '', status: '', query: '', limit: 24 });
        find('input[type=search]').value = '';
        controls();
        draw();
      }
    },
    { signal: events.signal },
  );
  find('input[type=search]').addEventListener(
    'input',
    (event) => {
      state.query = event.target.value;
      state.limit = 24;
      draw();
    },
    { signal: events.signal },
  );
  controls();
  draw();
  return {
    getDay: () => state.day,
    openThesis: (id) => details.open(id, state.day),
    close: () => details.close(),
    setDataset(input) {
      const next = parseDataset(input);
      data = next;
      state.day = [data.days[0] || data.as_of, state.day, data.as_of].sort()[1];
      if (!data.groups.some((g) => g.id === state.group) && state.group !== 'ungrouped')
        state.group = '';
      if (!data.theses.some((t) => t.object === state.object)) state.object = '';
      state.limit = 24;
      details.setDataset(data);
      controls();
      draw();
    },
    destroy() {
      events.abort();
      filters.forEach((f) => f.destroy());
      details.destroy();
      shell.remove();
    },
  };
}
