/** Scratch-copy mutation checks against real stored records; no source or data is modified. */
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { fromBundles } from '../src/adapters/bundle.js';
import { english, sequenceDays } from './fixtures.js';

const data = fromBundles(english, { sequenceDays });
const folder = await fs.mkdtemp(path.join(os.tmpdir(), 'hivemind-ui-mutations-'));
await fs.writeFile(path.join(folder, 'package.json'), ' {"type":"module"}');
await fs.cp(new URL('../src/', import.meta.url), path.join(folder, 'src'), { recursive: true });
const modelPath = path.join(folder, 'src/model/thesis.js');
const source = await fs.readFile(modelPath, 'utf8');
const cases = [
  {
    name: 'future assessment',
    old: 'j.day <= day',
    replacement: 'j.day >= day',
    check: `for(const t of data.theses){if(t.judgements.length){const day=addDays(t.judgements[0].day,-1);assert.equal(model.assessmentAt(t,day),null);}}`,
  },
  {
    name: 'publication date used as arrival',
    old: 'e.arrival_day <= day',
    replacement: 'e.day <= day',
    check: `const pair=data.theses.flatMap(t=>t.evidence.map(e=>({t,e}))).find(({e})=>e.arrival_day>e.day);assert(pair);assert(!model.snapshotThesis(pair.t,pair.e.day).evidence.some(e=>e.id===pair.e.id));`,
  },
  {
    name: 'future status switch',
    old: 's.day <= day',
    replacement: 'true',
    check: `const t=data.theses.find(t=>t.switches.some(s=>!s.open));const closing=t.switches.find(s=>!s.open);assert.equal(model.statusAt(t,addDays(closing.day,-1)),'Open');`,
  },
];
try {
  for (const entry of cases) {
    assert(source.includes(entry.old));
    const run = path.join(folder, 'check.mjs');
    await fs.writeFile(
      run,
      `import assert from 'node:assert/strict';import fs from 'node:fs';import * as model from './src/model/thesis.js';import {addDays} from './src/model/dates.js';const data=JSON.parse(fs.readFileSync(new URL('./data.json',import.meta.url),'utf8'));${entry.check}`,
    );
    await fs.writeFile(path.join(folder, 'data.json'), JSON.stringify(data));
    await fs.writeFile(modelPath, source);
    execFileSync(process.execPath, [run], { stdio: 'pipe' });
    await fs.writeFile(modelPath, source.replace(entry.old, entry.replacement));
    let caught = false;
    try {
      execFileSync(process.execPath, [run], { stdio: 'pipe' });
    } catch (error) {
      const stderr = error.stderr.toString();
      assert(stderr.includes('AssertionError'), stderr);
      caught = true;
    }
    assert(caught, `mutant escaped: ${entry.name}`);
    console.log(`Rejected mutant: ${entry.name}`);
  }
  await fs.writeFile(modelPath, source);
  await fs.mkdir(path.join(folder, 'test'));
  await fs.cp(new URL('./fixtures/', import.meta.url), path.join(folder, 'test/fixtures'), {
    recursive: true,
  });
  await fs.copyFile(
    new URL('./idea.test.js', import.meta.url),
    path.join(folder, 'test/idea.test.js'),
  );
  const ideaPath = path.join(folder, 'src/idea/idea.js');
  const ideaSource = await fs.readFile(ideaPath, 'utf8');
  const runIdea = () =>
    execFileSync(process.execPath, ['--test', path.join(folder, 'test/idea.test.js')], {
      stdio: 'pipe',
    });
  runIdea();
  for (const entry of [
    {
      name: 'only the first chosen thesis is direct',
      old: 'chosen.map((entry) => entry.view_id)',
      replacement: 'chosen.slice(0, 1).map((entry) => entry.view_id)',
    },
    {
      name: 'every related thesis hangs from the first',
      old: 'sourceId: entry.via',
      replacement: 'sourceId: chosen[0].view_id',
    },
  ]) {
    assert(ideaSource.includes(entry.old));
    await fs.writeFile(ideaPath, ideaSource.replace(entry.old, entry.replacement));
    let caught = false;
    try {
      runIdea();
    } catch (error) {
      const output = error.stdout.toString();
      assert(output.includes('ERR_ASSERTION'), output);
      caught = true;
    }
    assert(caught, `mutant escaped: ${entry.name}`);
    console.log(`Rejected mutant: ${entry.name}`);
  }
} finally {
  await fs.rm(folder, { recursive: true, force: true });
}
