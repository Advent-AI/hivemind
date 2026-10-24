import { createThesisExplorer } from './index.js';
import { fromBundles } from './adapters/bundle.js';
import { readIdea, readBundles, idsOf, graphOf, ideaCard } from './idea/idea.js';
import { score } from './model/thesis.js';
export * from './index.js';

const EXAMPLES = [
  "Can NVIDIA's data center revenue top $300B this year?",
  'The AI capex bubble is about to pop',
  'Vera Rubin volume shipments will slip past H2',
  "NVIDIA can't hold a 75% gross margin",
];
// The service that reads ideas (docs/poc/idea-card.md). The page is static; a host may point it elsewhere with
// <body data-api="…">. The key lives in the service, never here.
const API = document.body.dataset.api || 'http://127.0.0.1:8788';
const input = document.getElementById('ask'),
  root = document.getElementById('explorer');
if (input && root) {
  try {
    const inputData = JSON.parse(document.getElementById('data').textContent);
    const dataset = inputData.schema_version ? inputData : fromBundles(inputData);
    const app = createThesisExplorer(root, { dataset });
    // One request in flight at a time: a new idea cancels the previous one, and a late answer is ignored.
    let inFlight = null,
      serial = 0;
    const idea = { text: '', state: 'idle', card: null, error: null };
    const scoreOf = (position) => {
      const thesis = app
        .getDataset()
        .theses.find((t) => t.id === idea.card?.reading?.chosen[0]?.view_id);
      return thesis ? score(thesis, position) : `position ${position}`;
    };
    const leadingCard = () => ideaCard({ ...idea, scoreOf });
    async function run() {
      const text = input.value.trim();
      if (!text) {
        app.showGraph({});
        return;
      }
      if (inFlight) inFlight.abort();
      inFlight = new AbortController();
      const mine = ++serial;
      Object.assign(idea, { text, state: 'pending', card: null, error: null });
      app.showGraph({ leadingCard });
      try {
        const card = await readIdea(API, text, { signal: inFlight.signal });
        if (mine !== serial) return;
        idea.card = card;
        idea.state = 'answered';
        app.showGraph({ leadingCard }); // the idea card first: verdict, reading, parts
        const bundles = await readBundles(API, idsOf(card), card.idea.as_of, {
          signal: inFlight.signal,
        });
        if (mine !== serial) return;
        if (bundles) app.setDataset(fromBundles(bundles)); // validated before anything is drawn
        app.showGraph({ ...graphOf(card), leadingCard });
      } catch (error) {
        if (error.name === 'AbortError' || mine !== serial) return;
        Object.assign(idea, { state: 'failed', error });
        app.showGraph({ leadingCard });
      } finally {
        if (mine === serial) inFlight = null;
      }
    }
    input.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        run();
        input.blur();
      }
    });
    const examples = document.getElementById('examples');
    EXAMPLES.forEach((text) => {
      const button = document.createElement('button');
      button.className = 'filter';
      button.type = 'button';
      button.textContent = text.length > 26 ? text.slice(0, 25) + '…' : text;
      button.addEventListener('click', () => {
        input.value = text;
        run();
      });
      examples.append(button);
    });
  } catch (error) {
    const message = document.createElement('p');
    message.className = 'ui-error';
    message.setAttribute('role', 'alert');
    message.textContent = `Cannot load the thesis data: ${error.message}`;
    root.append(message);
  }
}
