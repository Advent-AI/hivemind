import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const root = dirname(fileURLToPath(import.meta.url));
const source = readFileSync(join(root, 'STEP1-TRACE-REVIEW.md'), 'utf8');
const sandbox = { window: {} };
vm.runInNewContext(readFileSync(join(root, '../docs/system-design/markdown.js'), 'utf8'), sandbox);
const body = sandbox.window.HIVEMIND_MARKDOWN.render(source);
const hash = createHash('sha256').update(source).digest('hex');
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="source-sha256" content="${hash}"><title>Step 1 trace review</title><style>
:root{color-scheme:light}body{margin:0;background:#f4f8f5;color:#24343a;font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1100px;margin:auto;padding:42px 28px 80px;background:white;min-height:100vh}h1{font-size:32px;line-height:1.2}h2{margin-top:50px;border-bottom:1px solid #dce8e1;padding-bottom:9px}h3{margin-top:32px}a{color:#176b58}p{max-width:90ch}li{margin:.45em 0}table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.5}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #dce8e1;padding:11px}th{background:#edf5ef}td:first-child{min-width:230px;width:34%}code{background:#edf5ef;padding:2px 4px;border-radius:4px}@media(max-width:650px){main{padding:24px 14px}table{display:block;overflow-x:auto}}
</style></head><body><main><p><a href="architecture.html">← Architecture</a> · <a href="../poc/data/clean-step1-2026-07-08-09-continuing/review.html">Article replay →</a></p>${body}</main></body></html>\n`;
const output = join(root, 'step1-trace-review.html');
if (process.argv.includes('--check')) {
  if (readFileSync(output, 'utf8') !== html) throw new Error('Step 1 review HTML differs from Markdown');
  console.log('Step 1 review HTML matches Markdown.');
} else {
  writeFileSync(output, html);
  console.log('Generated Step 1 review HTML from Markdown.');
}
