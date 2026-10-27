import { createThesisExplorer, createLibrary } from './index.js';
import { fromBundles } from './adapters/bundle.js';
import { parseDataset } from './model/contract.js';
import { readIdea, readBundles, idsOf, graphOf, ideaCard } from './idea/idea.js';
import { score } from './model/thesis.js';
import { createIdeaDetail } from './idea/analysis.js';
import {
  prepareCompositeTrial,
  prepareIdeaComposite,
  compositeAt,
  confidenceFromScore,
} from './idea/composite.js';
import { DEFAULT_TRIGGER_CONDITION } from './model/trigger.js';
import { advanceIdeaProgress } from './idea/progress.js';
import { createIdeaComposer } from './components/idea-composer.js';
import { DEFAULT_ACTION_SETTINGS } from './model/market.js';
export * from './index.js';

const API = document.body.dataset.api || 'http://127.0.0.1:8788';
const input = document.getElementById('ask');
const root = document.getElementById('explorer');
const libraryRoot = document.getElementById('library');
if (input && root && libraryRoot) {
  try {
    const initial = JSON.parse(document.getElementById('data').textContent);
    let data = initial.schema_version ? parseDataset(initial) : fromBundles(initial);
    const compositeTrials = JSON.parse(
      document.getElementById('composite-trials')?.textContent || '[]',
    );
    // Explicit old exports remain usable for standalone component previews.
    const library = createLibrary(libraryRoot, { dataset: data });
    let app = null;
    let inFlight = null;
    let requestNumber = 0;
    let deferredPresentation = null;
    let leadingDirty = false;
    const libraryRequest = new AbortController();
    const form = document.getElementById('idea-form');
    const send = document.getElementById('idea-send');
    const composer = createIdeaComposer({
      root,
      form,
      input,
      launcher: document.getElementById('idea-launcher'),
    });
    const libraryButton = document.getElementById('show-library');
    const ideaButton = document.getElementById('show-idea');
    const idea = { text: '', state: 'idle', card: null, error: null };
    let market = null;
    try {
      market = JSON.parse(document.getElementById('market-data')?.textContent || 'null');
    } catch {
      /* The card renders unavailable prices. */
    }
    const action = {
      market,
      settings: { ...DEFAULT_ACTION_SETTINGS },
      onChange: (settings) => {
        action.settings = settings;
      },
    };
    const trigger = {
      condition: { ...DEFAULT_TRIGGER_CONDITION },
      getConfidence: () =>
        idea.composite
          ? confidenceFromScore(compositeAt(idea.composite, idea.day)?.value ?? null)
          : null,
      onChange: (condition) => {
        trigger.condition = condition;
      },
    };
    const ideaDetail = createIdeaDetail({ root: document.body });
    function updateSendState() {
      send.disabled = !input.value.trim() || Boolean(inFlight);
      form.setAttribute('aria-busy', String(Boolean(inFlight)));
    }
    function cancelIdea() {
      inFlight?.abort();
      inFlight = null;
      requestNumber++;
      updateSendState();
    }
    function showLibrary() {
      ideaDetail.close();
      app?.pause();
      root.hidden = true;
      libraryRoot.hidden = false;
      libraryButton.setAttribute('aria-pressed', 'true');
      ideaButton.setAttribute('aria-pressed', 'false');
    }
    function showIdea() {
      library.close();
      libraryRoot.hidden = true;
      root.hidden = false;
      libraryButton.setAttribute('aria-pressed', 'false');
      ideaButton.setAttribute('aria-pressed', 'true');
      const firstVisit = !app;
      if (firstVisit) {
        app = createThesisExplorer(root, {
          dataset: data,
          onDayChange: (day, range) => {
            idea.day = day;
            idea.chartStart = range?.start;
          },
        });
        app.showGraph({ day: library.getDay() });
      }
      if (deferredPresentation) {
        const { spec, dataset } = deferredPresentation;
        present(spec, dataset);
      } else if (leadingDirty) {
        app.updateLeading();
        leadingDirty = false;
      }
      if (firstVisit) composer.open();
      updateSendState();
    }
    function present(spec, dataset = null) {
      if (root.hidden) {
        deferredPresentation = { spec, dataset };
        return;
      }
      if (dataset) app.setDataset(dataset);
      app.showGraph({ ...spec, ...(idea.state === 'answered' ? { trigger, action } : {}) });
      deferredPresentation = null;
      leadingDirty = false;
    }
    const leadingCard = (layout = {}) =>
      ideaCard({
        ...idea,
        ...layout,
        onOpen: () =>
          ideaDetail.open(idea.card, data.theses, idea.composite, idea.day, idea.createdDay),
        scoreOf: (position) => {
          const thesis = app
            ?.getDataset()
            .theses.find((t) => t.id === idea.card?.reading?.chosen[0]?.view_id);
          return thesis ? score(thesis, position) : `position ${position}`;
        },
      });
    async function run(event) {
      event.preventDefault();
      const text = input.value.trim();
      if (!text || inFlight) return;
      deferredPresentation = null;
      leadingDirty = false;
      trigger.condition = { ...DEFAULT_TRIGGER_CONDITION };
      action.settings = { ...DEFAULT_ACTION_SETTINGS };
      composer.close();
      input.value = '';
      ideaDetail.close();
      cancelIdea();
      const mine = ++requestNumber;
      inFlight = new AbortController();
      updateSendState();
      const signal = inFlight.signal;
      const submitted = new Date();
      const createdDay = [
        submitted.getFullYear(),
        String(submitted.getMonth() + 1).padStart(2, '0'),
        String(submitted.getDate()).padStart(2, '0'),
      ].join('-');
      Object.assign(idea, {
        text,
        createdDay,
        state: 'pending',
        card: null,
        error: null,
        composite: null,
        day: library.getDay(),
        chartStart: undefined,
        progress: ['search'],
      });
      app.showGraph({
        day: library.getDay(),
        leadingCard,
        centerOn: 'tree',
        center: true,
      });
      try {
        const updateProgress = (stage) => {
          if (mine !== requestNumber || signal.aborted) return;
          const progress = advanceIdeaProgress(idea.progress, stage);
          if (progress === idea.progress) return;
          idea.progress = progress;
          if (root.hidden) leadingDirty = true;
          else app.updateLeading();
        };
        const card = await readIdea(API, text, {
          signal,
          asOf: library.getDay(),
          onProgress: updateProgress,
        });
        if (mine !== requestNumber) return;
        updateProgress('cards');
        const bundles = await readBundles(API, idsOf(card), card.idea.as_of, { signal });
        if (mine !== requestNumber) return;
        const next = bundles ? fromBundles(bundles) : null;
        const chartData = next || { as_of: card.idea.as_of, days: card.days, theses: [] };
        Object.assign(idea, {
          card,
          state: 'answered',
          day: card.idea.as_of,
          composite:
            prepareIdeaComposite(card, chartData) ||
            (next ? prepareCompositeTrial(compositeTrials, card, next) : null),
        });
        const weightPercents = ['idea-composite/3', 'idea-composite/4'].includes(
          idea.composite?.version,
        )
          ? Object.fromEntries(
              [...idea.composite.drivers, ...idea.composite.excluded].map((entry) => [
                entry.thesis_id,
                entry.weight_percent,
              ]),
            )
          : undefined;
        present(
          {
            ...graphOf(card),
            day: card.idea.as_of,
            leadingCard,
            weightPercents,
            centerOn: 'tree',
            center: true,
            reveal: true,
          },
          next,
        );
      } catch (error) {
        if (error.name === 'AbortError' || mine !== requestNumber) return;
        Object.assign(idea, { state: 'failed', error });
        present({ leadingCard, centerOn: 'tree', center: true });
      } finally {
        if (mine === requestNumber) {
          inFlight = null;
          updateSendState();
        }
      }
    }
    async function loadLibrary() {
      try {
        const response = await fetch(`${API}/library`, { signal: libraryRequest.signal });
        if (!response.ok) throw new Error(`Service returned ${response.status}`);
        const next = fromBundles(await response.json());
        if (next.coverage !== 'library')
          throw new Error('The service did not return a complete library');
        if (libraryRequest.signal.aborted) return;
        library.setDataset(next);
        data = next;
      } catch {
        // Keep the displayed snapshot when the optional live read is unavailable.
      }
    }
    form.addEventListener('submit', run);
    input.addEventListener('input', updateSendState);
    libraryButton.addEventListener('click', showLibrary);
    ideaButton.addEventListener('click', showIdea);
    window.addEventListener(
      'pagehide',
      () => {
        cancelIdea();
        libraryRequest.abort();
        library.destroy();
        app?.destroy();
        ideaDetail.destroy();
        composer.destroy();
      },
      { once: true },
    );
    showLibrary();
    updateSendState();
    loadLibrary();
  } catch (error) {
    const message = document.createElement('p');
    message.className = 'ui-error';
    message.setAttribute('role', 'alert');
    message.textContent = `Cannot load the thesis data: ${error.message}`;
    libraryRoot.append(message);
  }
}
