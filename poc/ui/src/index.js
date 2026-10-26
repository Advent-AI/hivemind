import { parseDataset } from './model/contract.js';
import { createCanvas } from './components/canvas.js';
import { createThesisDetail } from './components/thesis-detail.js';
import { isCalendarDay } from './model/dates.js';
import { resolveGraph } from './model/graph.js';

export { fromBundles, fromIdeaResponse } from './adapters/bundle.js';
export { parseDataset, ContractError } from './model/contract.js';
export { createThesisCard } from './components/thesis-card.js';
export { createThesisDetail } from './components/thesis-detail.js';
export { ladderChart, bindHistoryChart, scoreHistoryChart } from './components/thesis-chart.js';
export { createCanvas } from './components/canvas.js';
export { createLibrary } from './components/library.js';
export { createSelect } from './components/select.js';
export { ideaCard, graphOf } from './idea/idea.js';
export { createIdeaDetail, ideaAnalysisHtml } from './idea/analysis.js';
export {
  prepareIdeaComposite,
  prepareCompositeTrial,
  compositeAt,
  confidenceFromScore,
  confidenceHistory,
  formatConfidence,
} from './idea/composite.js';

/** Mount a reusable explorer. The host supplies data and chooses the graph; this module never fetches or calls an LLM. */
export function createThesisExplorer(root, { dataset, onDayChange = () => {} }) {
  if (!root || typeof root.append !== 'function')
    throw new TypeError('An explorer needs a root element');
  let data = parseDataset(dataset);
  let graph = null;
  let destroyed = false;
  root.classList.add('hm-ui');
  const canvas = createCanvas({ root, onDayChange, onOpen: (id, day) => details.open(id, day) });
  const details = createThesisDetail({ root, dataset: data, onOpen: () => canvas.stop() });
  canvas.render({ dataset: data });
  function active() {
    if (destroyed) throw new Error('This explorer has been destroyed');
  }
  function showGraph(spec) {
    active();
    if (
      spec.day &&
      (!isCalendarDay(spec.day) || spec.day < (data.days[0] || data.as_of) || spec.day > data.as_of)
    )
      throw new Error('Date outside loaded history');
    const resolved = resolveGraph(spec, data);
    const same =
      JSON.stringify(graph?.rootIds) === JSON.stringify(resolved.rootIds) &&
      JSON.stringify(graph?.branches) === JSON.stringify(resolved.branches);
    graph = { ...spec, ...resolved };
    delete graph.primaryId;
    delete graph.supportingIds;
    canvas.render({ ...graph, dataset: data }, { center: spec.center ?? !same });
  }
  return {
    showGraph,
    openThesis(id, day = data.as_of) {
      active();
      details.open(id, day);
    },
    setDay(day) {
      active();
      if (!isCalendarDay(day) || day < (data.days[0] || data.as_of) || day > data.as_of)
        throw new Error('Date outside loaded history');
      canvas.setDay(day);
    },
    setDataset(input) {
      active();
      const next = parseDataset(input); // Validate before touching the current UI.
      const firstDay = next.days[0] || next.as_of;
      const retainedDay = graph?.day
        ? graph.day < firstDay
          ? firstDay
          : graph.day > next.as_of
            ? next.as_of
            : graph.day
        : next.as_of;
      data = next;
      details.setDataset(next);
      if (graph) {
        const known = new Set(data.theses.map((thesis) => thesis.id));
        const rootIds = graph.rootIds.filter((id) => known.has(id));
        const branches = graph.branches.filter(
          (edge) => rootIds.includes(edge.sourceId) && known.has(edge.targetId),
        );
        showGraph({ ...graph, rootIds, branches, day: retainedDay });
      } else canvas.render({ dataset: data });
    },
    updateLeading() {
      active();
      canvas.updateLeading();
    },
    fit() {
      active();
      canvas.fit();
    },
    getDataset() {
      return data;
    },
    destroy() {
      if (!destroyed) {
        destroyed = true;
        canvas.destroy();
        details.destroy();
      }
    },
  };
}
