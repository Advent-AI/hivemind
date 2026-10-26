import { esc } from '../components/dom.js';

const LABELS = {
  search: 'Searching the research library',
  decompose: 'Understanding your idea',
  retrieve: 'Finding relevant theses',
  map: 'Comparing the thesis evidence',
  summarize: 'Writing the assessment',
  cards: 'Preparing the cards',
};

/** Keep actual, request-local stages in arrival order; repeated updates do not add nodes. */
export function advanceIdeaProgress(stages, stage) {
  if (!Object.hasOwn(LABELS, stage)) throw new Error(`Unknown Idea progress stage: ${stage}`);
  if (stages.includes(stage)) return stages;
  const order = Object.keys(LABELS);
  if (stages.length && order.indexOf(stage) < order.indexOf(stages.at(-1)))
    throw new Error('Idea progress moved backwards');
  return [...stages, stage];
}

/** A connected activity list; only the current task glimmers. */
export function ideaProgressHtml(stages) {
  return `<ol class="idea-progress" aria-label="Analysis progress">${stages
    .map(
      (stage, index) =>
        `<li class="idea-progress__step ${index === stages.length - 1 ? 'is-current' : 'is-complete'}" data-progress-stage="${esc(stage)}"${index === stages.length - 1 ? ' aria-current="step"' : ''}><span class="idea-progress__dot" aria-hidden="true"></span><span class="idea-progress__label">${esc(LABELS[stage])}</span></li>`,
    )
    .join('')}</ol>`;
}
