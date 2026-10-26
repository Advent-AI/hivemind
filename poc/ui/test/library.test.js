import test from 'node:test';
import assert from 'node:assert/strict';
import { fromBundles } from '../src/adapters/bundle.js';
import { parseDataset } from '../src/model/contract.js';
import { librarySelection, libraryCounts } from '../src/model/library.js';
import { groupsFor, isSuperseded, dependenciesAt, snapshotThesis } from '../src/model/thesis.js';
import { evidenceHtml, assessmentText } from '../src/components/evidence.js';
import { relationsHtml } from '../src/components/relations.js';
import { addDays } from '../src/model/dates.js';

import { current as wire } from './fixtures.js';

const data = fromBundles(wire);

test('D181: the whole collected library retains exact groups, identity and source records', () => {
  assert.deepEqual(libraryCounts(data), { theses: 90, groups: 18, evidence: 519 });
  assert.equal(data.theses.filter((t) => t.identity).length, 90);
  assert.equal(librarySelection(data, { group: 'ungrouped' }).length, 50);
  assert.deepEqual(
    librarySelection(data, { group: 'g1' })
      .map((t) => t.id)
      .sort(),
    wire.groups
      .find((g) => g.id === 'g1')
      .members.map((m) => m.thesis_id)
      .sort(),
  );
  for (const t of data.theses) {
    const original = wire.views.find((v) => v.view_id === t.id);
    assert.deepEqual(t.identity, original.identity);
    for (const e of t.evidence)
      assert.equal(e.sources.length, original.evidence.find((r) => r.id === e.id).sources.length);
  }
  assert.equal(librarySelection(data, { object: 'NVDA' }).length, 22);
  assert.equal(librarySelection(data, { query: 'not-a-recorded-question' }).length, 0);
  console.log(
    'Checked 90 identities, 18 groups, 51 memberships and 716 evidence-link source lists.',
  );
});

test('D181: group membership is dated and never presented as a dependency', () => {
  for (const g of data.groups)
    for (const m of g.members) {
      assert(!groupsFor(data, m.thesis_id, addDays(m.day, -1)).some((x) => x.id === g.id));
      assert(groupsFor(data, m.thesis_id, m.day).some((x) => x.id === g.id));
    }
  const thesis = data.theses.find((t) => t.id === 'v7');
  const html = relationsHtml(thesis, data, data.as_of);
  assert(html.includes('Vera Rubin platform rollout'));
  assert(!html.includes('>Dependencies<'));
  const invalid = structuredClone(data);
  invalid.groups[0].members[0].thesis_id = 'missing';
  assert.throws(() => parseDataset(invalid), /missing thesis/);
});

test('D181: prior assessments use prior replacement status and prior source arrivals', () => {
  let judged = 0;
  for (const t of data.theses)
    for (const j of t.judgements)
      for (const id of j.cited) {
        const e = t.evidence.find((e) => e.id === id);
        if (!e.replaced_by || j.day >= e.replaced_by.day) continue;
        assert(!isSuperseded(e, j.day));
        assert(!evidenceHtml(e, j.day).includes(' | Superseded'));
        assert(isSuperseded(e, data.as_of));
        const snapshot = snapshotThesis(t, j.day).evidence.find((e) => e.id === id);
        assert.equal(snapshot.replaced_by, null);
        assert(snapshot.sources.every((s) => s.arrival_day <= j.day));
        judged++;
      }
  assert.equal(judged, 25);
  console.log(`Checked ${judged} historical citations before a recorded replacement.`);
});

test('D181: waiting dependencies resolve only from the recorded date', () => {
  const thesis = structuredClone(data.theses[0]);
  thesis.dependencies = [
    {
      depends_on: null,
      direction: 'same',
      wait_chain_view_id: 'v2',
      wait_year: '2027',
      day: '2026-07-24',
      resolutions: [{ target: 'v3', day: '2026-07-26', seq: 3 }],
    },
  ];
  assert.equal(dependenciesAt(thesis, '2026-07-25')[0].depends_on, null);
  assert.equal(dependenciesAt(thesis, '2026-07-26')[0].depends_on, 'v3');
});

test('D181/D190: references are clickable with one bracket pair and source text stays escaped', () => {
  const t = data.theses.find((t) => t.evidence.length);
  const e = t.evidence[0];
  const html = assessmentText(t, `Supported by [${e.id}] (${e.id}). <script>bad</script>`);
  assert(html.includes(`data-citation="${e.id}"`));
  assert(!html.includes('[<button'));
  assert(!html.includes('(<button'));
  assert.equal((html.match(/>\[1\]<\/button>/g) || []).length, 2);
  assert.equal(assessmentText(t, '(e999999)'), '(e999999)');
  assert(html.includes('&lt;script&gt;'));
  assert(!html.includes('<script>'));
});
