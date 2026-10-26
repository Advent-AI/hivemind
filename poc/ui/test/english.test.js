import test from 'node:test';
import assert from 'node:assert/strict';
import { fromBundles } from '../src/adapters/bundle.js';

// D163: a bundle from the English library carries canonical kinds and tiers and numeric rung bounds, no condition_zh.
function thesis(overrides = {}) {
  return {
    view_id: 'v1',
    object: 'ai-capex',
    kind: 'theme',
    looks_at: '2026 hyperscaler capital spending, USD',
    question: 'Can AI infrastructure investment lift 2026 hyperscaler capex into these ranges?',
    due_day: '2027-02-25',
    created_seq: 1,
    created_day: '2026-02-25',
    created_from: { title: 'call', publisher: 'NVIDIA', category: 'T4' },
    rungs: [
      {
        position: 1,
        label: 'below $500 billion',
        condition: 'Capex below $500 billion',
        lo: null,
        hi: 5e11,
      },
      {
        position: 2,
        label: '$500 billion to below $600 billion',
        condition: 'Capex from $500 billion to below $600 billion',
        lo: 5e11,
        hi: 6e11,
      },
      {
        position: 3,
        label: '$600 billion to below $800 billion',
        condition: 'Capex from $600 billion to below $800 billion',
        lo: 6e11,
        hi: 8e11,
      },
      {
        position: 4,
        label: '$800 billion to below $1 trillion',
        condition: 'Capex from $800 billion to below $1 trillion',
        lo: 8e11,
        hi: 1e12,
      },
      {
        position: 5,
        label: '$1 trillion or more',
        condition: 'Capex at or above $1 trillion',
        lo: 1e12,
        hi: null,
      },
    ],
    judgements: [],
    evidence: [
      {
        id: 'e1',
        one_line: 'Analysts expect about $700 billion',
        quote: 'about $700 billion',
        tier: 'third_party_view',
        speaker: 'analysts',
        original_who: 'analysts',
        day: '2026-02-25',
        arrival_day: '2026-02-25',
        seq: 1,
        source: {
          title: 'call',
          publisher: 'NVIDIA',
          category: 'T4',
          uri: null,
          publication_day: '2026-02-25',
        },
        outlets: 1,
        replaced_by: null,
        replaces: null,
      },
    ],
    dependencies: [],
    switches: [{ open: 1, reason: 'created', after_seq: 1, day: '2026-02-25' }],
    ...overrides,
  };
}

test('D163: an English-only theme ladder is oriented from its numeric bounds, without condition_zh', () => {
  const data = fromBundles({ views: [thesis()], days: ['2026-02-25'] });
  const view = data.theses[0];
  assert.equal(view.kind, 'Theme thesis');
  assert.equal(view.evidence[0].tier, 'Third-party view');
  // values rise from rung 1 to rung 5, so rung 5 is the top score, as the legacy magnitudes decided for Chinese conditions
  assert.deepEqual(
    view.rungs.map((r) => r.score),
    ['−2', '−1', '0', '+1', '+2'],
  );
  assert.deepEqual(
    view.rungs.map((r) => [r.lo, r.hi]),
    [
      [undefined, 5e11],
      [5e11, 6e11],
      [6e11, 8e11],
      [8e11, 1e12],
      [1e12, undefined],
    ],
  );
});

test('D163: a falling English ladder keeps the default order, and an asset thesis is never reoriented', () => {
  const falling = thesis({
    rungs: thesis()
      .rungs.slice()
      .reverse()
      .map((r, i) => ({ ...r, position: i + 1 })),
  });
  assert.deepEqual(
    fromBundles({ views: [falling], days: ['2026-02-25'] }).theses[0].rungs.map((r) => r.score),
    ['+2', '+1', '0', '−1', '−2'],
  );
  const asset = thesis({
    object: 'NVDA',
    kind: 'asset',
    rungs: thesis().rungs.map((r, i) => ({
      ...r,
      label: ['Strongly bullish', 'Bullish', 'Neutral', 'Bearish', 'Strongly bearish'][i],
    })),
  });
  const view = fromBundles({ views: [asset], days: ['2026-02-25'] }).theses[0];
  assert.equal(view.kind, 'Company thesis');
  assert.deepEqual(
    view.rungs.map((r) => r.score),
    ['+2', '+1', '0', '−1', '−2'],
  );
});

test('D163: an English ladder without bounds or condition_zh cannot be oriented and keeps the default order', () => {
  const prose = thesis({ rungs: thesis().rungs.map(({ lo: _lo, hi: _hi, ...rest }) => rest) });
  assert.deepEqual(
    fromBundles({ views: [prose], days: ['2026-02-25'] }).theses[0].rungs.map((r) => r.score),
    ['+2', '+1', '0', '−1', '−2'],
  );
});
