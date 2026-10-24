import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { fromIdeaResponse } from '../src/adapters/bundle.js';
import { graphOf, statusOf, fmtUsd } from '../src/idea/idea.js';
import { esc } from '../src/components/dom.js';

// Real answers of POST /ideas on the sealed ledger (2026-10-24), replayed from the service's archive.
const read = (name) =>
  JSON.parse(fs.readFileSync(new URL(`./fixtures/${name}.json`, import.meta.url), 'utf8'));
const v3 = read('idea-card-v3'),
  none = read('idea-card-null'),
  empty = read('idea-card-empty');

test('D138: every chosen thesis is a peer and each related thesis keeps its supplied source', () => {
  const dataset = fromIdeaResponse(v3);
  assert.equal(dataset.as_of, v3.idea.as_of);
  assert.deepEqual(
    dataset.theses.map((t) => t.id),
    [...v3.reading.chosen, ...v3.related].map((c) => c.view_id),
  );
  assert.deepEqual(
    graphOf(v3).rootIds,
    v3.reading.chosen.map((entry) => entry.view_id),
  );
  assert.deepEqual(
    graphOf(v3).branches,
    v3.related.map((entry) => ({ sourceId: entry.via, targetId: entry.view_id })),
  );
  assert.ok(v3.reading.parts.length >= 1 && v3.reading.parts[0].view_ids.includes('v3'));
  assert.ok(Array.isArray(v3.reading.trace) && v3.reading.trace.some((t) => t.tool === 'search'));
  assert.deepEqual(graphOf(empty), {});
  assert.deepEqual(graphOf(none), {});
});

test('the card states the verdict on the number the idea gave, in the ladder score the thesis cards use', () => {
  const status = statusOf(
    v3,
    (position) => ({ 1: '+2', 2: '+1', 3: '0', 4: '-1', 5: '-2' })[position],
  );
  assert.equal(status.badge, 'Holds');
  assert.equal(status.cls, 'chip--ink');
  assert.match(status.line, /Your claim <b>&gt;= \$300B<\/b> at \+1/);
  assert.match(status.line, /Judged <b>\+1<\/b> 看多/);
});

test('no recorded view and an empty choice are told apart, and nothing is invented for them', () => {
  assert.deepEqual(statusOf(none), {
    badge: 'No thesis',
    cls: 'chip--line',
    line: 'No recorded view on anything in this idea.',
    summary: '',
  });
  const status = statusOf(empty);
  assert.equal(status.badge, 'No thesis');
  assert.equal(status.line, '');
  assert.equal(status.summary, esc(empty.reading.summary));
});

test('US dollar amounts read the way an analyst writes them', () => {
  assert.equal(fmtUsd(300e9), '$300B');
  assert.equal(fmtUsd(1.05e12), '$1.05T');
  assert.equal(fmtUsd(54e9), '$54B');
  assert.equal(fmtUsd(2.6), '$2.6');
  assert.equal(fmtUsd(26979000000), '$26.98B');
});
