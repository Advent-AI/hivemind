import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { fanOutGap, routeFanOut } from '../src/components/connectors.js';
import { live } from './fixtures.js';
import { graphOf } from '../src/idea/idea.js';
import { layoutGraph } from '../src/model/graph.js';

function graphBounds(count) {
  const source = {
    left: 480,
    top: 40 + (Math.max(0, count - 1) * 404) / 2,
    width: 440,
    height: 380,
  };
  const targets = Array.from({ length: count }, (_, index) => ({
    left: source.left + source.width + fanOutGap(count),
    top: 40 + index * 404,
    width: 440,
    height: 380,
  }));
  return { source, targets };
}

function segments(points) {
  return points.slice(1).flatMap((end, index) => {
    const start = points[index];
    return start.x === end.x && start.y === end.y ? [] : [[start, end]];
  });
}

function intersects([a, b], [c, d]) {
  return (
    Math.max(Math.min(a.x, b.x), Math.min(c.x, d.x)) <=
      Math.min(Math.max(a.x, b.x), Math.max(c.x, d.x)) &&
    Math.max(Math.min(a.y, b.y), Math.min(c.y, d.y)) <=
      Math.min(Math.max(a.y, b.y), Math.max(c.y, d.y))
  );
}

function checkRoutes(count) {
  const { source, targets } = graphBounds(count);
  const routes = routeFanOut(source, targets);
  assert.equal(routes.length, count);
  for (const route of routes) {
    const start = route.points[0];
    const end = route.points.at(-1);
    const target = targets[route.index];
    assert.equal(start.x, source.left + source.width);
    assert(start.y >= source.top + 24 && start.y <= source.top + source.height - 24);
    assert.deepEqual(end, { x: target.left, y: target.top + target.height / 2 });
    assert(route.path.startsWith(`M${start.x},${start.y} `));
    assert(route.path.endsWith(`H${end.x}`));
    for (const point of route.points) assert(point.x >= start.x && point.x <= end.x);
  }
  for (let i = 0; i < routes.length; i++)
    for (let j = i + 1; j < routes.length; j++)
      assert(
        !segments(routes[i].points).some((a) =>
          segments(routes[j].points).some((b) => intersects(a, b)),
        ),
        `${count} children: routes ${i} and ${j} intersect`,
      );
}

test('D137: stored multi-thesis response routes have no overlapping branches or detached endpoints', () => {
  const card = JSON.parse(
    fs.readFileSync(new URL('./fixtures/idea-card-v3.json', import.meta.url), 'utf8'),
  );
  const ids = new Set([...card.reading.chosen, ...card.related].map((view) => view.view_id));
  assert(ids.size > 4, 'requires the real high-fan-out response');
  checkRoutes(ids.size - 1);
  console.log(`Checked ${ids.size - 1} branches from the stored Idea response.`);
});

test('D137: every fan-out size in the loaded ledger keeps separate routes within card edges', () => {
  assert(live.views.length > 17, 'requires a ledger large enough to exercise port compression');
  for (let count = 0; count < live.views.length; count++) checkRoutes(count);
  console.log(
    `Checked ${live.views.length} fan-out sizes, including empty and single-child graphs.`,
  );
});

test('D138: unequal groups in the real Idea graph preserve separate connector lanes', () => {
  const response = JSON.parse(
    fs.readFileSync(new URL('./fixtures/idea-card-v3.json', import.meta.url), 'utf8'),
  );
  const plan = layoutGraph(graphOf(response), true);
  const nodes = new Map([plan.leading, ...plan.nodes].map((node) => [node.id, node]));
  const routes = [];
  for (const [id, source] of nodes) {
    const targets = plan.edges
      .filter((edge) => edge.sourceId === id)
      .map((edge) => nodes.get(edge.targetId));
    routes.push(...routeFanOut(source, targets));
  }
  assert.equal(routes.length, plan.edges.length);
  for (let i = 0; i < routes.length; i++)
    for (let j = i + 1; j < routes.length; j++)
      assert(
        !segments(routes[i].points).some((a) =>
          segments(routes[j].points).some((b) => intersects(a, b)),
        ),
        `Idea routes ${i} and ${j} intersect`,
      );
  console.log(`Checked ${routes.length} routes across unequal related-thesis groups.`);
});
