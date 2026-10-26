import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { build } from 'esbuild';
await import('./build-validator.mjs');
const root = fileURLToPath(new URL('.', import.meta.url));
const result = await build({
  absWorkingDir: root,
  entryPoints: ['src/bootstrap.js', 'src/styles/index.css'],
  bundle: true,
  write: false,
  outdir: 'dist',
  format: 'iife',
  globalName: 'Hivemind',
  platform: 'browser',
  target: ['es2022'],
  charset: 'utf8',
  minify: true,
  logLevel: 'silent',
  legalComments: 'none',
});
const script = result.outputFiles.find((file) => file.path.endsWith('.js')).text;
const style = result.outputFiles.find((file) => file.path.endsWith('.css')).text;
if (Buffer.byteLength(script) > 200 * 1024)
  throw new Error('UI bundle exceeds the 200KB script budget');
if (process.argv.includes('--json')) process.stdout.write(JSON.stringify({ script, style }));
else {
  await fs.mkdir(new URL('./dist/', import.meta.url), { recursive: true });
  await fs.writeFile(new URL('./dist/hivemind.js', import.meta.url), script);
  await fs.writeFile(new URL('./dist/hivemind.css', import.meta.url), style);
  console.log(
    `UI built: ${Buffer.byteLength(script)} JS bytes, ${Buffer.byteLength(style)} CSS bytes`,
  );
}
