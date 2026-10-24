import fs from 'node:fs/promises';
import Ajv from 'ajv/dist/2020.js';
import standaloneCode from 'ajv/dist/standalone/index.js';
import { build } from 'esbuild';
import { fileURLToPath } from 'node:url';

const schema = JSON.parse(
  await fs.readFile(new URL('./src/model/thesis.schema.json', import.meta.url), 'utf8'),
);
const ajv = new Ajv({ allErrors: true, code: { source: true, esm: true }, strict: true });
const validate = ajv.compile(schema);
const generated = await build({
  stdin: {
    contents: standaloneCode(ajv, validate),
    resolveDir: fileURLToPath(new URL('.', import.meta.url)),
  },
  bundle: true,
  write: false,
  format: 'esm',
  platform: 'browser',
  logLevel: 'silent',
});
await fs.writeFile(
  new URL('./src/model/validate.generated.js', import.meta.url),
  '// Generated from thesis.schema.json by build-validator.mjs.\n' + generated.outputFiles[0].text,
);
