// D397 on the page (D569; not-judged-display/DESIGN.md): the parts a question does not judge travel from the bundle's
// `not_judged` to the dataset's `notJudged` through the one adapter, are filtered by date in the one snapshot, and the closed
// contract accepts a list, null, or an older bundle without the key.
import test from 'node:test';
import assert from 'node:assert/strict';
import { fromBundles, fromIdeaResponse } from '../src/adapters/bundle.js';
import { snapshotThesis } from '../src/model/thesis.js';
import { live, sequenceDays } from './fixtures.js';

const PARTS = [
  {
    part: 'Whether MIIT caps the quantities approved',
    why: 'The tracked event is formal approval of purchases.',
  },
  {
    part: '<b>Whether shipments follow</b>',
    why: 'A downstream effect & not the decision judged.',
  },
];
const withParts = (parts) => ({
  ...live,
  views: live.views.map((v, i) => (i === 0 ? { ...v, not_judged: parts } : { ...v })),
});

test('D397: a list, an empty list and null pass the closed contract; a bundle without the key gives null', () => {
  assert.deepEqual(fromBundles(withParts(PARTS), { sequenceDays }).theses[0].notJudged, PARTS);
  assert.deepEqual(fromBundles(withParts([]), { sequenceDays }).theses[0].notJudged, []);
  assert.equal(fromBundles(withParts(null), { sequenceDays }).theses[0].notJudged, null);
  assert.equal(fromBundles(live, { sequenceDays }).theses[0].notJudged, null);
});

test('D397: the Idea response carries the parts through the same adapter', () => {
  const response = {
    idea: { as_of: live.as_of },
    days: live.days,
    views: withParts(PARTS).views.slice(0, 1),
  };
  assert.deepEqual(fromIdeaResponse(response).theses[0].notJudged, PARTS);
});

test('D397: a part with no text or an unknown field is refused by the closed contract', () => {
  assert.throws(() => fromBundles(withParts([{ part: '', why: 'x' }]), { sequenceDays }));
  assert.throws(() =>
    fromBundles(withParts([{ part: 'a', why: 'b', extra: 1 }]), { sequenceDays }),
  );
});

test('D397: the snapshot shows the parts from the opening day on and none before it', () => {
  const thesis = fromBundles(withParts(PARTS), { sequenceDays }).theses[0];
  const before = new Date(Date.parse(thesis.created_day) - 86400000).toISOString().slice(0, 10);
  assert.equal(snapshotThesis(thesis, before).notJudged, null);
  assert.deepEqual(snapshotThesis(thesis, thesis.created_day).notJudged, PARTS);
});

// page-contract/DESIGN.md: the new system's answer shapes read without an invented direction.
import { stateWords, stateTone, laneOf, scoreTitle, undirected } from '../src/model/thesis.js';
import { prepareIdeaComposite, CompositeUnavailable } from '../src/idea/composite.js';

const EVENT = [
  { position: 1, label: 'Yes', condition: 'MIIT formally approves the purchases by 2027-01-31.' },
  { position: 2, label: 'Ruled out', condition: 'MIIT formally rejects the purchase plans.' },
  { position: 3, label: 'Still open', condition: 'Neither holds on 2027-01-31.' },
];
const shaped = (patch) => ({
  ...live,
  views: live.views.map((v, i) => (i === 0 ? { ...v, ...patch } : { ...v })),
});
const eventView = (labels = EVENT) =>
  shaped({ rungs: labels, judgements: [], answer_shape: 'event', favourable_end: null });

test('an event of three outcomes passes the contract with its outcome names as scores, neutral, in its stored lanes', () => {
  const thesis = fromBundles(eventView(), { sequenceDays }).theses[0];
  assert.deepEqual(
    thesis.rungs.map((r) => r.score),
    ['Yes', 'Ruled out', 'Still open'],
  );
  assert.equal(thesis.answerShape, 'event');
  assert.equal(undirected(thesis), true);
  assert.deepEqual(
    [1, 2, 3].map((p) => laneOf(thesis, p)),
    [0, 1, 2],
  );
  assert.deepEqual(stateWords(thesis, 2), { main: 'Ruled out', label: '' });
  assert.equal(stateTone('Yes', thesis), 'state--neutral');
  assert.equal(scoreTitle(thesis), 'Current outcome');
  assert.deepEqual(
    [1, 2, 3].map((p) => axisMark(thesis, p)),
    ['1', '2', '3'],
  ); // marks are positions; the outcome is named in the table
});

test('an event whose choices are not its outcome names is refused, never read by position', () => {
  const other = EVENT.map((r, i) => ({ ...r, label: ['Approved', 'Rejected', 'Pending'][i] }));
  assert.throws(() => fromBundles(eventView(other), { sequenceDays }), /an event's choices/);
});

test('a two-outcome event of the new system is neutral too; a legacy Yes/No keeps its tones', () => {
  const two = EVENT.slice(0, 2).map((r, i) => ({ ...r, label: ['Yes', 'No'][i] }));
  const thesis = fromBundles(eventView(two), { sequenceDays }).theses[0];
  assert.equal(stateTone('Yes', thesis), 'state--neutral');
  assert.equal(stateTone('Yes', null), 'state--positive');
});

test('a theme range with no direction shows its label and no score word; a legacy store is read as before', () => {
  const five = live.views.find((v) => v.rungs.length === 5);
  const index = live.views.indexOf(five);
  const data = {
    ...live,
    views: live.views.map((v, i) =>
      i === index ? { ...v, answer_shape: 'figure', favourable_end: 'n/a' } : { ...v },
    ),
  };
  const thesis = fromBundles(data, { sequenceDays }).theses[index];
  assert.equal(scoreTitle(thesis), 'Current range');
  assert.deepEqual(stateWords(thesis, 1), { main: thesis.rungs[0].label, label: '' });
  const legacy = fromBundles(live, { sequenceDays }).theses[index];
  assert.equal(scoreTitle(legacy), 'AI score');
  assert.equal(legacy.answerShape, null);
});

test('an Idea composite with an undirected driver is not computed and names the driver', () => {
  const data = fromBundles(eventView(), { sequenceDays });
  const id = data.theses[0].id;
  const card = {
    idea: { as_of: data.as_of },
    related: [],
    reading: {
      chosen: [{ view_id: id }],
      composite: {
        version: 'idea-composite/3',
        method: 'weighted',
        as_of: data.as_of,
        excluded: [],
        drivers: [
          {
            thesis_id: id,
            supporting_end: 'first',
            label: 'Yes',
            weight_percent: 100,
            reason: 'test',
          },
        ],
      },
    },
  };
  assert.throws(
    () => prepareIdeaComposite(card, data),
    (error) => error instanceof CompositeUnavailable && error.message.includes(id),
  );
});

// council round 41: undirected ranges and unrecorded shapes carry positions, not scores, on every path.
import { axisMark } from '../src/model/thesis.js';
import { prepareCompositeTrial } from '../src/idea/composite.js';

const themeIndex = live.views.findIndex((v) => v.rungs.length === 5);
const asTheme = () => ({
  ...live,
  views: live.views.map((v, i) =>
    i === themeIndex ? { ...v, answer_shape: 'figure', favourable_end: 'n/a' } : { ...v },
  ),
});

test('a theme range with no direction is read by position: marks, lanes and scores are positions, top to bottom in stored order', () => {
  const thesis = fromBundles(asTheme(), { sequenceDays }).theses[themeIndex];
  assert.deepEqual(
    thesis.rungs.map((r) => r.score),
    ['1', '2', '3', '4', '5'],
  );
  assert.deepEqual(
    [1, 2, 3, 4, 5].map((p) => laneOf(thesis, p)),
    [0, 1, 2, 3, 4],
  );
  assert.deepEqual(
    [1, 5].map((p) => axisMark(thesis, p)),
    ['1', '5'],
  );
});

test('an unrecorded question of three choices with any labels passes the contract by position', () => {
  const labels = ['Approved', 'Rejected', 'Pending'].map((label, i) => ({
    position: i + 1,
    label,
    condition: `${label}.`,
  }));
  const thesis = fromBundles(
    shaped({ rungs: labels, judgements: [], answer_shape: 'unrecorded', favourable_end: null }),
    { sequenceDays },
  ).theses[0];
  assert.deepEqual(
    thesis.rungs.map((r) => r.score),
    ['1', '2', '3'],
  );
  assert.equal(scoreTitle(thesis), 'Current answer');
  assert.equal(stateTone('1', thesis), 'state--neutral');
});

test('the trial composite refuses an undirected driver and names it', () => {
  const data = fromBundles(eventView(), { sequenceDays });
  const t = data.theses[0];
  const card = {
    idea: { text: 'idea', as_of: data.as_of },
    reading: { chosen: [{ view_id: t.id }] },
  };
  const trials = [
    {
      version: 'idea-composite/1',
      idea_text: 'idea',
      as_of: data.as_of,
      note: 'n',
      drivers: [{ thesis_id: t.id, question: t.question, label: 'Yes', direction: 1, reason: 'r' }],
    },
  ];
  assert.throws(
    () => prepareCompositeTrial(trials, card, data),
    (error) => error instanceof CompositeUnavailable && error.message.includes(t.id),
  );
});
