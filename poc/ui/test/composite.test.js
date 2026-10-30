import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { current } from './fixtures.js';
import { fromBundles } from '../src/adapters/bundle.js';
import {
  prepareIdeaComposite,
  prepareCompositeTrial,
  compositeAt,
  confidenceFromScore,
  confidenceHistory,
  formatConfidence,
} from '../src/idea/composite.js';
import { scoreHistoryChart } from '../src/components/thesis-chart.js';
import { laneOf, stateText } from '../src/model/thesis.js';
import { badgeHtml } from '../src/components/primitives.js';
import { ideaAnalysisHtml, ideaDetailMetaHtml } from '../src/idea/analysis.js';
import { graphOf } from '../src/idea/idea.js';

const data = fromBundles(current);
const card = JSON.parse(
  fs.readFileSync(new URL('./fixtures/idea-composite-trial.json', import.meta.url), 'utf8'),
);
const plans = JSON.parse(
  fs.readFileSync(
    new URL('../../config/idea-composite-trial-2026-10-26.json', import.meta.url),
    'utf8',
  ),
);
const defaultCard = JSON.parse(
  fs.readFileSync(new URL('./fixtures/idea-composite-default.json', import.meta.url), 'utf8'),
);

function weightedCard() {
  const card = structuredClone(defaultCard);
  const plan = card.reading.composite;
  plan.version = 'idea-composite/3';
  plan.method = 'weighted';
  for (const driver of plan.drivers) {
    driver.weight_percent = driver.thesis_id === 'v3' ? 70 : 30;
    driver.weight_reason = 'Relative importance to the revenue outcome.';
  }
  for (const entry of plan.excluded) entry.weight_percent = 0;
  return card;
}

test('D197: confidence maps the entire score scale to percent and preserves missing values', () => {
  assert.deepEqual([-2, -1, 0, 1, 2].map(confidenceFromScore), [0, 25, 50, 75, 100]);
  assert.equal(confidenceFromScore(null), null);
  assert.equal(formatConfidence(null), '—');
  assert.equal(formatConfidence(confidenceFromScore(0.45)), '61%');
  assert.equal(formatConfidence(confidenceFromScore(0.45), 2), '61.25%');
  assert.equal(confidenceFromScore(0.45) + confidenceFromScore(-0.45), 100);
  assert.throws(() => confidenceFromScore(NaN), TypeError);
});

test('D197: Idea history and detail show confidence percentages instead of a signed composite', () => {
  const card = weightedCard();
  const composite = prepareIdeaComposite(card, data);
  const series = confidenceHistory(composite);
  assert.equal(series.at(-1).value, 57.5);
  assert.deepEqual(
    series.map((p) => p.day),
    composite.series.map((p) => p.day),
  );
  const chart = scoreHistoryChart(series, {
    start: composite.start,
    end: composite.as_of,
    day: composite.as_of,
    scale: 'confidence',
    scoreLabel: '58%',
  });
  for (const mark of ['0%', '25%', '50%', '75%', '100%']) assert(chart.includes(`>${mark}</text>`));
  assert(chart.includes('AI confidence history') && !chart.includes('>+2</text>'));
  const html = ideaAnalysisHtml(card, data.theses, composite);
  const metadata = ideaDetailMetaHtml(composite, data.as_of, '2026-10-26');
  assert(
    metadata.includes('AI confidence: 58%') && metadata.includes('Idea created: Oct 26, 2026'),
  );
  assert.equal(
    compositeAt(composite, data.as_of).contributions.reduce(
      (sum, entry) => sum + entry.contribution,
      0,
    ),
    0.3,
  );
  assert(!html.includes('<table') && !html.includes('>+0.30 '));
  assert(html.includes('>Theses</h3>') && !html.includes('About AI confidence'));
  assert(!html.includes('role="tooltip"'));
  assert(!html.includes('57.50%') && !html.includes('2/2 drivers'));
  const missing = confidenceHistory({ series: [{ day: data.as_of, value: null }] });
  assert.equal(missing[0].value, null);
});

test('D196: graph and score use only the positive selected set, with no excluded cards', () => {
  const card = weightedCard();
  const plan = card.reading.composite;
  plan.version = 'idea-composite/4';
  delete plan.excluded;
  const ids = plan.drivers.map((d) => d.thesis_id);
  card.reading.chosen = card.reading.chosen.filter((c) => ids.includes(c.view_id));
  card.related = [];
  const composite = prepareIdeaComposite(card, data);
  assert.equal(compositeAt(composite, data.as_of).value, 0.3);
  assert.deepEqual(graphOf(card).rootIds.sort(), ids.sort());
  assert.deepEqual(graphOf(card).branches, []);
  const html = ideaAnalysisHtml(card, data.theses, composite);
  assert(!html.includes('Not separately weighted'));
  const invalid = structuredClone(card);
  invalid.reading.chosen.push({ view_id: 'v9' });
  assert.throws(() => prepareIdeaComposite(invalid, data), /Every connected thesis/);
  const zero = structuredClone(card);
  zero.reading.composite.drivers[0].weight_percent = 0;
  assert.throws(() => prepareIdeaComposite(zero, data), /impact percent/);
});

test('D194/D205: explicit unequal impact weights drive the same dated chart and weight pills', () => {
  const card = weightedCard();
  const plan = prepareIdeaComposite(card, data);
  const point = compositeAt(plan, data.as_of);
  assert.equal(point.value, 0.3);
  assert.equal(
    point.contributions.reduce((sum, entry) => sum + entry.contribution, 0),
    point.value,
  );
  const html = ideaAnalysisHtml(card, data.theses, plan);
  assert(
    html.includes('aria-label="Impact weight: 70%"') &&
      html.includes('aria-label="Impact weight: 30%"'),
  );
  assert(html.includes('0% | ') && html.includes('Relative importance to the revenue outcome.'));
  assert(!html.includes('Equal weight'));
  card.reading.composite.drivers.forEach((d) => {
    d.supporting_end = d.supporting_end === 'first' ? 'last' : 'first';
  });
  assert.equal(compositeAt(prepareIdeaComposite(card, data), data.as_of).value, -0.3);
});

test('D194: missing weighted assessments stay unavailable without reallocating impact', () => {
  const copy = structuredClone(data);
  copy.theses.find((t) => t.id === 'v3').judgements = [];
  const point = compositeAt(prepareIdeaComposite(weightedCard(), copy), data.as_of);
  assert.equal(point.value, null);
  assert.equal(point.contributions.find((c) => c.thesis_id === 'v1').contribution, 0.3);
  const future = structuredClone(data);
  const thesis = future.theses.find((t) => t.id === 'v1');
  thesis.judgements.push({ ...thesis.judgements.at(-1), day: '2026-08-16', rung: 1 });
  assert.deepEqual(
    prepareIdeaComposite(weightedCard(), future).series,
    prepareIdeaComposite(weightedCard(), data).series,
  );
});

test('D194: explicit percentages total 100 or the plan is rejected', () => {
  for (const value of [0, -1, 69, 101, true, 70.5]) {
    const card = weightedCard();
    card.reading.composite.drivers.find((d) => d.thesis_id === 'v3').weight_percent = value;
    assert.throws(() => prepareIdeaComposite(card, data), TypeError);
  }
  const bad = weightedCard();
  bad.reading.composite.excluded[0].weight_percent = 1;
  assert.throws(() => prepareIdeaComposite(bad, data), TypeError);
  const empty = weightedCard();
  empty.reading.composite.excluded.push(
    ...empty.reading.composite.drivers.map((d) => ({
      thesis_id: d.thesis_id,
      question: d.question,
      reason: 'No relevant driver.',
      weight_percent: 0,
    })),
  );
  empty.reading.composite.drivers = [];
  assert.equal(compositeAt(prepareIdeaComposite(empty, data), data.as_of).value, null);
});

test('D188: the current three-thesis Idea gets a default chart without matching a query string', () => {
  const composite = prepareIdeaComposite(defaultCard, data);
  assert.equal(compositeAt(composite, '2026-08-15').value, 0.5);
  assert.equal(composite.drivers.find((d) => d.thesis_id === 'v1').direction, 1);
  assert.equal(composite.drivers.length, 2);
  assert.equal(composite.excluded.length, 1);
  const rephrased = structuredClone(defaultCard);
  rephrased.idea.text = 'A completely different wording of the same claim';
  assert.deepEqual(prepareIdeaComposite(rephrased, data).series, composite.series);
  rephrased.reading.composite.drivers.forEach((d) => {
    d.supporting_end = d.supporting_end === 'first' ? 'last' : 'first';
  });
  assert.equal(compositeAt(prepareIdeaComposite(rephrased, data), '2026-08-15').value, -0.5);
});

test('D188: empty and unassessed baskets have no invented zero; every chosen thesis is accounted for', () => {
  const unassessed = structuredClone(data);
  for (const thesis of unassessed.theses) thesis.judgements = [];
  assert.equal(compositeAt(prepareIdeaComposite(defaultCard, unassessed), data.as_of).value, null);
  const empty = structuredClone(defaultCard);
  empty.reading.composite.excluded.push(
    ...empty.reading.composite.drivers.map(({ thesis_id, question, reason }) => ({
      thesis_id,
      question,
      reason,
    })),
  );
  empty.reading.composite.drivers = [];
  assert.equal(compositeAt(prepareIdeaComposite(empty, data), data.as_of).value, null);
  for (const change of [
    (plan) => plan.excluded.pop(),
    (plan) => plan.drivers.push(plan.drivers[0]),
    (plan) => {
      plan.drivers[0].question = 'Different identity';
    },
    (plan) => {
      plan.as_of = '2026-08-14';
    },
  ]) {
    const invalid = structuredClone(defaultCard);
    change(invalid.reading.composite);
    assert.throws(() => prepareIdeaComposite(invalid, data), TypeError);
  }
  assert.equal(prepareIdeaComposite(card, data), null);
});

test('D188: binary representatives preserve the same two endpoint scores', () => {
  const thesis = data.theses.find((entry) => entry.rungs.length === 2 && entry.judgements.length);
  assert(thesis);
  const binary = structuredClone(defaultCard);
  binary.reading.chosen = [{ view_id: thesis.id }];
  binary.reading.composite = {
    version: 'idea-composite/2',
    method: 'equal_weight',
    as_of: data.as_of,
    drivers: [
      {
        thesis_id: thesis.id,
        question: thesis.question,
        label: 'Event outcome',
        supporting_end: 'first',
        reason: 'This outcome supports the idea.',
      },
    ],
    excluded: [],
  };
  const first = compositeAt(prepareIdeaComposite(binary, data), data.as_of).value;
  assert.equal(Math.abs(first), 2);
  binary.reading.composite.drivers[0].supporting_end = 'last';
  assert.equal(compositeAt(prepareIdeaComposite(binary, data), data.as_of).value, -first);
});

test('D258: a No-first yes/no thesis shows its own outcome and keeps the same composite value', () => {
  const source = current.views.find(
    (view) => view.rungs.length === 2 && view.rungs[0].label === 'Yes' && view.judgements.length,
  );
  assert(source);
  const flipped = structuredClone(source);
  flipped.view_id = `${source.view_id}-no-first`;
  flipped.rungs = source.rungs
    .slice()
    .reverse()
    .map((rung, index) => ({ ...rung, position: index + 1 }));
  for (const judgement of flipped.judgements) judgement.rung = 3 - judgement.rung;
  const both = fromBundles({ ...current, views: [...current.views, flipped] });
  const original = both.theses.find((thesis) => thesis.id === source.view_id);
  const reversed = both.theses.find((thesis) => thesis.id === flipped.view_id);
  assert.deepEqual(
    reversed.rungs.map((rung) => [rung.label, rung.score]),
    [
      ['No', 'No'],
      ['Yes', 'Yes'],
    ],
  );
  const latest = reversed.judgements.at(-1).rung;
  assert.equal(stateText(reversed, latest), stateText(original, 3 - latest));
  assert.equal(laneOf(reversed, 2), 0);
  const valueOf = (thesis, supportingEnd) => {
    const binary = structuredClone(defaultCard);
    binary.reading.chosen = [{ view_id: thesis.id }];
    binary.reading.composite = {
      version: 'idea-composite/2',
      method: 'equal_weight',
      as_of: both.as_of,
      drivers: [
        {
          thesis_id: thesis.id,
          question: thesis.question,
          label: 'Event outcome',
          supporting_end: supportingEnd,
          reason: 'The Yes outcome supports the idea.',
        },
      ],
      excluded: [],
    };
    return compositeAt(prepareIdeaComposite(binary, both), both.as_of).value;
  };
  assert.equal(valueOf(reversed, 'last'), valueOf(original, 'first'));
});

test('D259: a yes/no ladder with named outcomes shows its own outcome once', () => {
  const source = current.views.find(
    (view) => view.rungs.length === 2 && view.rungs[0].label === 'Yes' && view.judgements.length,
  );
  const named = structuredClone(source);
  named.view_id = `${source.view_id}-named`;
  named.rungs[0].label = 'Restriction adopted';
  named.rungs[1].label = 'No restriction adopted';
  const both = fromBundles({ ...current, views: [...current.views, named] });
  const thesis = both.theses.find((entry) => entry.id === named.view_id);
  const plain = both.theses.find((entry) => entry.id === source.view_id);
  const judgement = { ...thesis.judgements.at(-1), rung: 2 };
  assert.equal(stateText(thesis, 2), 'No restriction adopted');
  assert.equal(
    badgeHtml(thesis, judgement),
    '<span class="chip chip--state state--negative"><b>No restriction adopted</b></span>',
  );
  assert.equal(stateText(plain, 1), 'Yes');
  const ordinal = both.theses.find((entry) => entry.rungs.length === 5 && entry.rungs[1].label);
  assert.equal(stateText(ordinal, 2), `${ordinal.rungs[1].score} ${ordinal.rungs[1].label}`);
});

test('D185: the real reviewed basket calculates 0, +0.5, then 0 using historical states', () => {
  const trial = prepareCompositeTrial(plans, card, data);
  assert.equal(compositeAt(trial, '2026-07-28').value, 0);
  assert.equal(compositeAt(trial, '2026-07-29').value, 0.5);
  assert.equal(compositeAt(trial, '2026-08-09').value, 0.5);
  assert.equal(compositeAt(trial, '2026-08-10').value, 0);
  assert.equal(compositeAt(trial, card.idea.as_of).scored, 2);
  assert.equal(trial.excluded.length, 8);
  const future = structuredClone(data);
  const revenue = future.theses.find((t) => t.id === 'v2');
  revenue.judgements.push({ ...revenue.judgements.at(-1), day: '2026-08-16', rung: 1 });
  assert.equal(compositeAt(prepareCompositeTrial(plans, card, future), '2026-08-15').value, 0);
  const inverted = structuredClone(plans);
  inverted[0].drivers.forEach((driver) => {
    driver.direction = -1;
  });
  assert.equal(compositeAt(prepareCompositeTrial(inverted, card, data), '2026-07-29').value, -0.5);
});

test('D185: missing judgements stay missing and repeated connections do not gain weight', () => {
  const missing = structuredClone(data);
  missing.theses.find((t) => t.id === 'v1').judgements = [];
  let point = compositeAt(prepareCompositeTrial(plans, card, missing), '2026-08-15');
  assert.equal(point.value, -1);
  assert.equal(point.scored, 1);
  missing.theses.find((t) => t.id === 'v2').judgements = [];
  point = compositeAt(prepareCompositeTrial(plans, card, missing), '2026-08-15');
  assert.equal(point.value, null);
  assert.equal(point.scored, 0);
  const repeated = structuredClone(card);
  repeated.reading.chosen.push(repeated.reading.chosen[0]);
  assert.equal(compositeAt(prepareCompositeTrial(plans, repeated, data), '2026-07-29').value, 0.5);
});

test('D185: trial identity, unique representatives and explicit directions are required', () => {
  assert.equal(
    prepareCompositeTrial(plans, { ...card, reading: { ...card.reading, chosen: [] } }, data),
    null,
  );
  assert.equal(
    prepareCompositeTrial(
      plans,
      { ...card, idea: { ...card.idea, text: 'A different idea' } },
      data,
    ),
    null,
  );
  for (const change of [
    (plan) => plan.drivers.push(plan.drivers[0]),
    (plan) => {
      plan.drivers[0].question = 'A different thesis';
    },
    (plan) => {
      plan.drivers[0].direction = 0;
    },
    (plan) => {
      plan.drivers[0].weight = 10;
    },
  ]) {
    const changed = structuredClone(plans);
    change(changed[0]);
    assert.throws(() => prepareCompositeTrial(changed, card, data), TypeError);
  }
});

test('D185: fractional plot uses the selected history cutoff and keeps its last dot inside the margin', () => {
  const trial = prepareCompositeTrial(plans, card, data);
  const html = scoreHistoryChart(trial.series, {
    start: trial.start,
    end: trial.as_of,
    day: '2026-07-29',
  });
  assert(html.includes('>+1</text>') && html.includes('>0</text>'));
  assert(!html.includes('history-guide'));
  const dot = html.match(/class="now-dot" cx="([\d.]+)"/);
  assert(dot && Number(dot[1]) < 406 - 3.5);
  const empty = scoreHistoryChart([{ day: trial.start, value: null }], {
    start: trial.start,
    end: trial.as_of,
    day: trial.as_of,
  });
  assert(!empty.includes('class="now-dot"') && !empty.includes('class="ribbon"'));
  assert.throws(
    () =>
      scoreHistoryChart(trial.series, {
        start: trial.start,
        end: trial.as_of,
        day: trial.as_of,
        width: 'invalid',
      }),
    TypeError,
  );
});
