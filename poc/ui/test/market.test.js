import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {
  readMarketSnapshot,
  readActionSettings,
  marketWindow,
  priceGeometry,
} from '../src/model/market.js';
import { layoutGraph } from '../src/model/graph.js';

const stored = JSON.parse(
  fs.readFileSync(new URL('../data/nvda-2026-10-27.json', import.meta.url)),
);

test('D235: the real snapshot keeps all completed USD observations and their source cutoff', () => {
  const data = readMarketSnapshot(stored);
  assert.equal(data.hourly.length, 248);
  assert.equal(data.daily.length, 371);
  assert.deepEqual(data.hourly.at(-1), [Date.parse('2026-10-26T15:59:59.999Z'), 215.3794]);
  assert.notEqual(data.hourly, stored.hourly);
  for (const mutate of [
    (data) => {
      data.currency = 'USDT';
    },
    (data) => {
      data.assetClass = 'perp';
    },
    (data) => {
      data.source = 'Hyperliquid';
    },
    (data) => {
      data.hourly[0][1] = 0;
    },
    (data) => {
      data.hourly[0][1] = null;
    },
    (data) => {
      data.hourly[1][0] = data.hourly[0][0];
    },
    (data) => {
      data.hourly.reverse();
    },
    (data) => {
      data.hourly.at(-1)[0] = Date.parse(data.asOf) + 1;
    },
    (data) => {
      data.daily = [];
    },
    (data) => {
      data.unexpected = true;
    },
  ]) {
    const candidate = structuredClone(stored);
    mutate(candidate);
    assert.throws(() => readMarketSnapshot(candidate), TypeError);
  }
  console.log('Judged 619 real price observations and 10 malformed snapshots.');
});

test('D235: ranges use the newest real observation and preserve intraday time gaps', () => {
  const data = readMarketSnapshot(stored);
  for (const range of ['1D', '1W', '1M', '1Y']) {
    const points = marketWindow(data, range);
    assert(points.length > 1);
    assert.deepEqual(points.at(-1), data.hourly.at(-1), range);
    if (range !== '1D')
      assert(points[0][0] >= points.at(-1)[0] - { '1W': 7, '1M': 30, '1Y': 365 }[range] * 86400000);
    const plot = priceGeometry(points);
    for (const point of plot.mapped)
      assert(
        point.x >= plot.left &&
          point.x <= plot.right &&
          point.y > plot.top &&
          point.y < plot.bottom,
      );
  }
  const day = marketWindow(data, '1D');
  assert(
    day.every(
      ([time]) =>
        new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York' }).format(time) ===
        '2026-10-26',
    ),
  );
  const spaced = priceGeometry([
    [10, 20],
    [20, 25],
    [110, 22],
  ]);
  assert.equal(spaced.mapped[1].x, spaced.left + (spaced.right - spaced.left) / 10);
  assert(
    priceGeometry([
      [10, 20],
      [20, 20],
    ]).mapped.every((point) => Number.isFinite(point.y)),
  );
  assert.equal(priceGeometry([]), null);
  assert.throws(() => marketWindow(data, 'ALL'), TypeError);
});

test('D235: investment settings admit only the displayed tenths and four chart ranges', () => {
  assert.deepEqual(readActionSettings(), { allocation: 5, range: '1Y' });
  for (const allocation of [0, 5, 5.1, 100])
    assert.equal(readActionSettings({ allocation, range: '1M' }).allocation, allocation);
  for (const allocation of [-1, 100.1, 5.01, '5', NaN])
    assert.throws(() => readActionSettings({ allocation, range: '1M' }), TypeError);
  assert.throws(() => readActionSettings({ allocation: 5, range: 'ALL' }), TypeError);
  assert.throws(() => readActionSettings({ allocation: 5, range: '1M', execute: true }), TypeError);
});

test('D235: Action, Trigger, Idea and thesis occupy ordered separate columns', () => {
  for (const rootIds of [[], ['a'], ['a', 'b', 'c']]) {
    const graph = { rootIds, branches: [] };
    const plan = layoutGraph(graph, true, true, true);
    assert.equal(plan.trigger.left - plan.action.left - plan.action.width, 180);
    assert.equal(plan.leading.left - plan.trigger.left - plan.trigger.width, 180);
    assert.equal(
      plan.action.top + plan.action.height / 2,
      plan.leading.top + plan.leading.height / 2,
    );
    assert.deepEqual(
      plan.edges.filter((edge) => edge.sourceId === 'action'),
      [{ sourceId: 'action', targetId: 'trigger' }],
    );
    assert.deepEqual(
      plan.edges.filter((edge) => edge.sourceId === 'idea').map((edge) => edge.targetId),
      rootIds,
    );
    assert.equal(layoutGraph(graph, true, true).action, null);
  }
  assert.throws(
    () => layoutGraph({ rootIds: [], branches: [] }, true, false, true),
    /needs a Trigger/,
  );
});
