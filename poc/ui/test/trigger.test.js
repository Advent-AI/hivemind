import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {
  DEFAULT_TRIGGER_CONDITION,
  readTriggerCondition,
  triggerMatches,
} from '../src/model/trigger.js';
import { layoutGraph } from '../src/model/graph.js';
import { graphOf } from '../src/idea/idea.js';

test('D226: all six Trigger operators distinguish below, equal and above the threshold', () => {
  const expected = {
    '>': [false, false, true],
    '>=': [false, true, true],
    '<': [true, false, false],
    '<=': [true, true, false],
    '=': [false, true, false],
    '!=': [true, false, true],
  };
  for (const [operator, result] of Object.entries(expected))
    assert.deepEqual(
      [60, 70, 80].map((confidence) => triggerMatches({ operator, threshold: 70 }, confidence)),
      result,
      operator,
    );
  assert.equal(triggerMatches({ operator: '=', threshold: 61 }, 61.25), true);
  assert.equal(triggerMatches({ operator: '>', threshold: 61 }, 61.49), false);
  assert.equal(triggerMatches({ operator: '>', threshold: 61 }, 61.5), true);
  assert.equal(triggerMatches({ operator: '=', threshold: 0 }, 0), true);
  assert.equal(triggerMatches({ operator: '=', threshold: 100 }, 100), true);
  assert.equal(triggerMatches(DEFAULT_TRIGGER_CONDITION, null), null);
  console.log('Checked 18 operator boundaries, rounding, 0/100 and missing confidence.');
});

test('D226: unsupported comparisons and percentages fail the closed Trigger contract', () => {
  for (const condition of [
    null,
    { operator: '==', threshold: 70 },
    { operator: '>', threshold: -1 },
    { operator: '>', threshold: 101 },
    { operator: '>', threshold: 70.5 },
    { operator: '>', threshold: '70' },
    { operator: '>', threshold: 70, extra: true },
  ])
    assert.throws(() => readTriggerCondition(condition), TypeError);
  for (const confidence of [undefined, NaN, Infinity, -1, 101, '70'])
    assert.throws(() => triggerMatches(DEFAULT_TRIGGER_CONDITION, confidence), TypeError);
});

test('D228: a Trigger reserves a connected column to the left of the stored Idea graph', () => {
  const card = JSON.parse(
    fs.readFileSync(new URL('./fixtures/idea-card-v3.json', import.meta.url), 'utf8'),
  );
  const graph = graphOf(card);
  for (const value of [graph, { rootIds: [], branches: [] }]) {
    const plan = layoutGraph(value, true, true);
    assert.equal(plan.leading.left - plan.trigger.left - plan.trigger.width, 180);
    assert.equal(plan.trigger.width, 320);
    assert.equal(
      plan.trigger.top + plan.trigger.height / 2,
      plan.leading.top + plan.leading.height / 2,
    );
    assert.deepEqual(
      plan.edges.filter((edge) => edge.sourceId === 'trigger'),
      [{ sourceId: 'trigger', targetId: 'idea' }],
    );
    assert.deepEqual(
      plan.edges
        .filter((edge) => edge.sourceId === 'idea' && edge.targetId !== 'trigger')
        .map((edge) => edge.targetId),
      value.rootIds,
    );
    for (const node of plan.nodes)
      assert(
        node.left + node.width <= plan.trigger.left ||
          plan.trigger.left + plan.trigger.width <= node.left ||
          node.top + node.height <= plan.trigger.top ||
          plan.trigger.top + plan.trigger.height <= node.top,
        `${node.id} overlaps the Trigger`,
      );
  }
  assert.equal(layoutGraph(graph, true).trigger, null);
  assert.throws(() => layoutGraph(graph, false, true), /needs an Idea/);
});
