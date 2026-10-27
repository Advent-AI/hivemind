import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { graphOf } from '../src/idea/idea.js';
import { revealSequence } from '../src/components/tree-reveal.js';
import { layoutGraph } from '../src/model/graph.js';

test('D223: the stored graph reveals each root and its children before the next root', () => {
  const card = JSON.parse(
    fs.readFileSync(new URL('./fixtures/idea-card-v3.json', import.meta.url)),
  );
  const graph = graphOf(card);
  const edges = [
    ...graph.rootIds.map((targetId) => ({ sourceId: 'idea', targetId })),
    ...graph.branches,
  ];
  const expected = graph.rootIds.flatMap((targetId) => [
    { sourceId: 'idea', targetId },
    ...graph.branches.filter((edge) => edge.sourceId === targetId),
  ]);
  assert.notDeepEqual(edges, expected, 'The stored case must distinguish the two orders');
  assert.deepEqual(revealSequence(edges), expected);
  assert.equal(new Set(revealSequence(edges).map((edge) => edge.targetId)).size, edges.length);
  assert.deepEqual(revealSequence([]), []);
  console.log(`Checked ${edges.length} stored connections in reveal order.`);
});

test('D227/D228: the default thesis column reveals top to bottom after the Idea', () => {
  const card = JSON.parse(
    fs.readFileSync(new URL('./fixtures/idea-composite-default.json', import.meta.url)),
  );
  const layout = layoutGraph(graphOf(card), true, true);
  const nodes = new Map([...layout.nodes, layout.trigger].map((node) => [node.id, node]));
  const targets = revealSequence(layout.edges).map((edge) => nodes.get(edge.targetId));
  assert.equal(targets.length, 3);
  assert.deepEqual(
    targets.map((node) => node.top + node.height / 2),
    targets.map((node) => node.top + node.height / 2).sort((a, b) => a - b),
  );
  assert.equal(new Set(targets.map((node) => node.left)).size, 1);
});
