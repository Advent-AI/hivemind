import fs from 'node:fs';
import { performance } from 'node:perf_hooks';
import { fromBundles } from './src/adapters/bundle.js';
import { parseDataset } from './src/model/contract.js';

const source = JSON.parse(fs.readFileSync(0, 'utf8'));
const start = performance.now();
const dataset = source.schema_version ? parseDataset(source) : fromBundles(source);
process.stderr.write(
  `Validated ${dataset.theses.length} theses in ${(performance.now() - start).toFixed(1)}ms\n`,
);
process.stdout.write(JSON.stringify(dataset));
