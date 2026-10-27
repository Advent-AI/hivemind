import fs from 'node:fs';
import { performance } from 'node:perf_hooks';
import { fromBundles } from './src/adapters/bundle.js';
import { parseDataset } from './src/model/contract.js';
import { readMarketSnapshot } from './src/model/market.js';

const source = JSON.parse(fs.readFileSync(0, 'utf8'));
const start = performance.now();
const market = process.argv.includes('--market');
const dataset = market
  ? readMarketSnapshot(source)
  : source.schema_version
    ? parseDataset(source)
    : fromBundles(source);
process.stderr.write(
  `Validated ${market ? `${dataset.hourly.length + dataset.daily.length} price observations` : `${dataset.theses.length} theses`} in ${(performance.now() - start).toFixed(1)}ms\n`,
);
process.stdout.write(JSON.stringify(dataset));
