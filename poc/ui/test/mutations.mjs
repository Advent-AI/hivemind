/** Scratch-copy mutation checks against real stored records; no source or data is modified. */
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { fromBundles } from '../src/adapters/bundle.js';
import { english, sequenceDays, current } from './fixtures.js';

const data = fromBundles(english, { sequenceDays });
const currentData = fromBundles(current);
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
  {
    name: 'future group membership',
    old: 'm.day <= day',
    replacement: 'true',
    current: true,
    check: `let judged=0;for(const g of data.groups)for(const m of g.members){if(m.day<=g.created_day)continue;assert(!model.groupsFor(data,m.thesis_id,addDays(m.day,-1)).some(x=>x.id===g.id));judged++;}assert(judged>0);`,
  },
  {
    name: 'replacement leaks into the past',
    old: 'evidence.replaced_by.day <= day',
    replacement: 'true',
    current: true,
    check: `let judged=0;for(const t of data.theses)for(const e of t.evidence){if(!e.replaced_by?.day)continue;assert(!model.isSuperseded(e,addDays(e.replaced_by.day,-1)));judged++;}assert(judged>0);`,
  },
  {
    name: 'future source arrival',
    old: 's.arrival_day <= day',
    replacement: 'true',
    current: true,
    check: `let judged=0;for(const t of data.theses)for(const e of t.evidence){const day=e.arrival_day;if(!e.sources.some(s=>s.arrival_day>day))continue;const at=model.snapshotThesis(t,day).evidence.find(x=>x.id===e.id);assert(at.sources.every(s=>s.arrival_day<=day));judged++;}assert(judged>0);`,
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
    await fs.writeFile(
      path.join(folder, 'data.json'),
      JSON.stringify(entry.current ? currentData : data),
    );
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
  await fs.writeFile(ideaPath, ideaSource);
  await fs.copyFile(
    new URL('./idea-analysis.test.js', import.meta.url),
    path.join(folder, 'test/idea-analysis.test.js'),
  );
  const analysisPath = path.join(folder, 'src/idea/analysis.js');
  const analysisSource = await fs.readFile(analysisPath, 'utf8');
  const runAnalysis = () =>
    execFileSync(process.execPath, ['--test', path.join(folder, 'test/idea-analysis.test.js')], {
      stdio: 'pipe',
    });
  runAnalysis();
  assert(analysisSource.includes('esc(summary)'));
  await fs.writeFile(
    analysisPath,
    analysisSource.replace('esc(summary)', 'esc(summary.slice(0, 50))'),
  );
  let caught = false;
  try {
    runAnalysis();
  } catch (error) {
    assert(error.stdout.toString().includes('ERR_ASSERTION'), error.stdout.toString());
    caught = true;
  }
  assert(caught, 'truncated Idea summary escaped the full-analysis check');
  console.log('Rejected mutant: truncated Idea analysis');
  const compositePath = path.join(folder, 'src/idea/composite.js');
  const compositeSource = await fs.readFile(compositePath, 'utf8');
  const plans = JSON.parse(
    await fs.readFile(
      new URL('../../config/idea-composite-trial-2026-10-26.json', import.meta.url),
      'utf8',
    ),
  );
  const card = JSON.parse(
    await fs.readFile(new URL('./fixtures/idea-composite-trial.json', import.meta.url), 'utf8'),
  );
  const compositeCheck = path.join(folder, 'check-composite.mjs');
  await fs.writeFile(
    compositeCheck,
    `import assert from 'node:assert/strict';import {prepareCompositeTrial,compositeAt} from './src/idea/composite.js';const trial=prepareCompositeTrial(${JSON.stringify(plans)},${JSON.stringify(card)},${JSON.stringify(currentData)});assert.equal(compositeAt(trial,'2026-07-29').value,0.5);`,
  );
  execFileSync(process.execPath, [compositeCheck], { stdio: 'pipe' });
  assert(compositeSource.includes('sum / active.length'));
  await fs.writeFile(compositePath, compositeSource.replace('sum / active.length', 'sum'));
  caught = false;
  try {
    execFileSync(process.execPath, [compositeCheck], { stdio: 'pipe' });
  } catch (error) {
    assert(error.stderr.toString().includes('AssertionError'), error.stderr.toString());
    caught = true;
  }
  assert(caught, 'unnormalised composite escaped the average check');
  console.log('Rejected mutant: composite sum instead of average');
  await fs.writeFile(compositePath, compositeSource);
  await fs.writeFile(analysisPath, analysisSource);
  await fs.copyFile(
    new URL('./idea-progress.test.js', import.meta.url),
    path.join(folder, 'test/idea-progress.test.js'),
  );
  const progressPath = path.join(folder, 'src/idea/progress.js');
  const progressSource = await fs.readFile(progressPath, 'utf8');
  const runProgress = () =>
    execFileSync(process.execPath, ['--test', path.join(folder, 'test/idea-progress.test.js')], {
      stdio: 'pipe',
    });
  runProgress();
  for (const entry of [
    {
      name: 'every progress node is current',
      path: progressPath,
      source: progressSource,
      old: 'index === stages.length - 1',
      replacement: 'true',
    },
    {
      name: 'stream drops progress events',
      path: ideaPath,
      source: ideaSource,
      old: 'onProgress(event.stage)',
      replacement: 'void event.stage',
    },
  ]) {
    assert(entry.source.includes(entry.old));
    await fs.writeFile(entry.path, entry.source.replaceAll(entry.old, entry.replacement));
    caught = false;
    try {
      runProgress();
    } catch (error) {
      assert(error.stdout.toString().includes('ERR_ASSERTION'), error.stdout.toString());
      caught = true;
    }
    assert(caught, `mutant escaped: ${entry.name}`);
    console.log(`Rejected mutant: ${entry.name}`);
    await fs.writeFile(entry.path, entry.source);
  }
  const defaultCard = JSON.parse(
    await fs.readFile(new URL('./fixtures/idea-composite-default.json', import.meta.url), 'utf8'),
  );
  const defaultCheck = path.join(folder, 'check-default-composite.mjs');
  await fs.writeFile(
    defaultCheck,
    `import assert from 'node:assert/strict';import {prepareIdeaComposite,compositeAt} from './src/idea/composite.js';const model=prepareIdeaComposite(${JSON.stringify(defaultCard)},${JSON.stringify(currentData)});assert.equal(compositeAt(model,'2026-08-15').value,0.5);`,
  );
  execFileSync(process.execPath, [defaultCheck], { stdio: 'pipe' });
  assert(compositeSource.includes('Math.sign(first) *'));
  await fs.writeFile(compositePath, compositeSource.replace('Math.sign(first) *', '1 *'));
  caught = false;
  try {
    execFileSync(process.execPath, [defaultCheck], { stdio: 'pipe' });
  } catch (error) {
    assert(error.stderr.toString().includes('AssertionError'), error.stderr.toString());
    caught = true;
  }
  assert(caught, 'theme endpoint inversion escaped the default-composite check');
  console.log('Rejected mutant: ignores displayed theme orientation');
} finally {
  await fs.rm(folder, { recursive: true, force: true });
}
