import test from 'node:test';
import assert from 'node:assert/strict';
import { fromBundles, fromIdeaResponse } from '../src/adapters/bundle.js';
import { parseDataset, ContractError } from '../src/model/contract.js';
import { english, original, live, sequenceDays } from './fixtures.js';

const data = fromBundles(english, { sequenceDays });
test('D130: both stored languages and every live bundle satisfy the same closed UI contract', () => {
  for (const source of [english, original, live]) {
    const before = JSON.stringify(source);
    const result = fromBundles(source, { sequenceDays });
    assert.equal(result.theses.length, source.views.length);
    assert.equal(
      result.theses.reduce((n, t) => n + t.evidence.length, 0),
      source.views.reduce((n, t) => n + t.evidence.length, 0),
    );
    assert.equal(JSON.stringify(source), before);
    assert(Object.isFrozen(result.theses[0].rungs));
  }
  console.log(
    `Validated ${english.views.length} English, ${original.views.length} original-language and ${live.views.length} live theses.`,
  );
});
test('D112/D130: the idea response uses the exact same thesis adapter', () => {
  const response = { idea: { as_of: live.as_of }, days: live.days, views: live.views.slice(0, 2) };
  assert.deepEqual(fromIdeaResponse(response), fromBundles(response, { asOf: live.as_of }));
});
test('D130: unknown fields, duplicate IDs, invalid dates and state positions fail with a field path', () => {
  const mutations = [
    (d) => {
      d.theses[0].model_html = '<script>bad</script>';
    },
    (d) => {
      d.theses[1].id = d.theses[0].id;
    },
    (d) => {
      d.theses[0].due_day = '2026-02-30';
    },
    (d) => {
      d.theses[0].judgements[0].rung = 5 + d.theses[0].rungs.length;
    },
    (d) => {
      d.theses[0].rungs[0].score = 'Bullish';
    },
    (d) => {
      d.theses[0].judgements[0].cited = ['does-not-exist'];
    },
  ];
  for (const mutate of mutations) {
    const invalid = structuredClone(data);
    mutate(invalid);
    assert.throws(
      () => parseDataset(invalid),
      (error) => error instanceof ContractError && error.path.startsWith('/theses/'),
    );
  }
});
test('D130: live bundles have explicit event dates and stable assessment IDs', () => {
  assert(live.views.length > 0);
  for (const v of live.views) {
    for (const s of v.switches) assert.match(s.day, /^\d{4}-\d{2}-\d{2}$/);
    for (const d of v.dependencies) assert.match(d.day, /^\d{4}-\d{2}-\d{2}$/);
    for (const e of v.evidence) assert.match(e.arrival_day, /^\d{4}-\d{2}-\d{2}$/);
    for (const j of v.judgements) assert(j.id);
  }
});
test('D130: missing event dates refuse incomplete agent payloads instead of guessing', () => {
  const incomplete = structuredClone(english);
  assert.throws(() => fromBundles(incomplete), /missing event date/);
  incomplete.views[0].rungs = null;
  assert.throws(() => fromBundles(incomplete), /\/views\/0\/rungs/);
});
