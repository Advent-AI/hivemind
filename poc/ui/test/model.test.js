import test from 'node:test';
import assert from 'node:assert/strict';
import { fromBundles } from '../src/adapters/bundle.js';
import {
  assessmentAt,
  statusAt,
  snapshotThesis,
  historyIndexAt,
  relatedTheses,
  dayRounds,
} from '../src/model/thesis.js';
import { addDays } from '../src/model/dates.js';
import { ladderChart } from '../src/components/thesis-chart.js';
import { safeLink } from '../src/components/dom.js';
import { evidenceHtml } from '../src/components/evidence.js';
import { english, live, sequenceDays } from './fixtures.js';

const data = fromBundles(english, { sequenceDays });
test('D130/D122: every real judgement date resolves to its last known assessment, never a future state', () => {
  let checked = 0;
  for (const thesis of data.theses) {
    if (!thesis.judgements.length) continue;
    const days = [addDays(thesis.judgements[0].day, -1), ...thesis.judgements.map((j) => j.day)];
    for (const day of days) {
      const expected = thesis.judgements.filter((j) => j.day <= day).at(-1) || null;
      assert.equal(assessmentAt(thesis, day), expected);
      assert.equal(thesis.judgements[historyIndexAt(thesis, day)] || null, expected);
      checked++;
    }
  }
  assert(checked > 0);
  console.log(`${checked} real history selections checked.`);
});
test('D130: snapshot uses evidence arrival day, status switch day and relationship day', () => {
  const late = data.theses
    .flatMap((t) => t.evidence.map((e) => ({ t, e })))
    .find(({ e }) => e.arrival_day > e.day);
  assert(late, 'real late-linked evidence is required');
  assert(!snapshotThesis(late.t, late.e.day).evidence.some((e) => e.id === late.e.id));
  assert(snapshotThesis(late.t, late.e.arrival_day).evidence.some((e) => e.id === late.e.id));
  const closed = data.theses.find((t) => t.switches.some((s) => !s.open));
  assert(closed);
  const closing = closed.switches.find((s) => !s.open);
  assert.equal(statusAt(closed, addDays(closing.day, -1)), 'Open');
  assert.equal(statusAt(closed, closing.day), 'Closed');
  assert.equal(statusAt(closed, addDays(closed.created_day, -1)), 'Not open yet');
  const fullData = fromBundles(live);
  const relation = fullData.theses
    .flatMap((t) =>
      t.dependencies.map((d) => ({
        t,
        d,
        target: fullData.theses.find((other) => other.id === d.depends_on),
      })),
    )
    .find(({ d, target }) => target && d.day > target.created_day);
  assert(relation);
  assert(
    !snapshotThesis(relation.t, addDays(relation.d.day, -1)).dependencies.includes(relation.d),
  );
  assert(
    !relatedTheses(relation.target, fullData, addDays(relation.d.day, -1)).includes(relation.t),
  );
  assert(relatedTheses(relation.target, fullData, relation.d.day).includes(relation.t));
});
test('D130: related theses respect the same dated dependency graph in both directions', () => {
  for (const thesis of data.theses) {
    const related = relatedTheses(thesis, data, data.as_of);
    for (const other of related)
      assert(
        thesis.dependencies.some((d) => d.depends_on === other.id) ||
          other.dependencies.some((d) => d.depends_on === thesis.id),
      );
  }
});
test('D130: end-of-day plot points agree with the last assessment on repeated dates', () => {
  const thesis = data.theses.find((t) =>
    t.judgements.some((j, i) => i && j.day === t.judgements[i - 1].day),
  );
  assert(thesis);
  for (const { j } of dayRounds(thesis.judgements)) assert.equal(j, assessmentAt(thesis, j.day));
});
test('D130: unassessed cards render an empty score chart; model text cannot become HTML or a script URL', () => {
  const thesis = { ...data.theses[0], judgements: [], evidence: [] };
  const svg = ladderChart(thesis, { start: data.days[0], end: data.as_of, day: data.as_of });
  assert(!svg.includes('NaN'));
  assert(!svg.includes('undefined'));
  assert(svg.includes('AI score'));
  assert.equal(safeLink('javascript:alert(1)', '<img onerror=bad>'), '&lt;img onerror=bad&gt;');
  assert(safeLink('https://example.com', 'Source').includes('rel="noopener noreferrer"'));
  assert.throws(
    () =>
      ladderChart(thesis, { start: data.days[0], end: data.as_of, day: data.as_of, width: NaN }),
    /width/,
  );
  const piece = structuredClone(data.theses[0].evidence[0]);
  piece.one_line = '<script>alert(1)</script>';
  piece.source.uri = 'javascript:alert(1)';
  const html = evidenceHtml(piece, data.as_of);
  assert(!html.includes('<script>'));
  assert(!html.includes('href="javascript:'));
});
