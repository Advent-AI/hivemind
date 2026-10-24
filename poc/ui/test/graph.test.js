import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { graphOf } from '../src/idea/idea.js';
import { fromIdeaResponse } from '../src/adapters/bundle.js';
import { layoutGraph, resolveGraph } from '../src/model/graph.js';

const response = JSON.parse(
  fs.readFileSync(new URL('./fixtures/idea-card-v3.json', import.meta.url), 'utf8'),
);
const data = fromIdeaResponse(response);

test('D138: stored Idea layout connects all eight chosen theses directly and reserves their related groups', () => {
  const graph = resolveGraph(graphOf(response), data);
  const plan = layoutGraph(graph, true);
  assert.equal(plan.nodes.length, data.theses.length);
  assert.deepEqual(
    plan.edges.filter((edge) => edge.sourceId === 'idea').map((edge) => edge.targetId),
    graph.rootIds,
  );
  for (const related of response.related) {
    assert(
      plan.edges.some((edge) => edge.sourceId === related.via && edge.targetId === related.view_id),
    );
    const source = plan.nodes.find((node) => node.id === related.via);
    const target = plan.nodes.find((node) => node.id === related.view_id);
    assert(source.left + source.width < target.left);
  }
  for (let i = 0; i < plan.nodes.length; i++)
    for (let j = i + 1; j < plan.nodes.length; j++) {
      const a = plan.nodes[i],
        b = plan.nodes[j];
      assert(
        a.left + a.width <= b.left ||
          b.left + b.width <= a.left ||
          a.top + a.height <= b.top ||
          b.top + b.height <= a.top,
        `${a.id} overlaps ${b.id}`,
      );
    }
  console.log(
    `Checked ${graph.rootIds.length} direct Idea edges and ${graph.branches.length} source-specific related edges.`,
  );
});

test('D138: malformed graphs fail before layout, and standalone thesis callers retain their explicit children', () => {
  const graph = graphOf(response);
  for (const invalid of [
    { rootIds: ['v3', 'v3'] },
    { rootIds: ['missing'] },
    { rootIds: ['v3'], branches: [{ sourceId: 'v2', targetId: 'v48' }] },
    { rootIds: ['v3'], branches: [{ sourceId: 'v3', targetId: 'v3' }] },
    { rootIds: ['v3'], branches: [{ sourceId: 'v3', targetId: 'missing' }] },
    { ...graph, branches: [...graph.branches, graph.branches[0]] },
  ])
    assert.throws(() => resolveGraph(invalid, data));
  assert.deepEqual(resolveGraph({ primaryId: 'v3', supportingIds: ['v1', 'v7'] }, data), {
    rootIds: ['v3'],
    branches: [
      { sourceId: 'v3', targetId: 'v1' },
      { sourceId: 'v3', targetId: 'v7' },
    ],
  });
  const empty = layoutGraph(resolveGraph({}, data), true);
  assert.equal(empty.nodes.length, 0);
  assert.equal(empty.edges.length, 0);
  assert(empty.leading);
});
