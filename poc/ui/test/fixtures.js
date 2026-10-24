import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

export const root = fileURLToPath(new URL('../../../', import.meta.url));
const records = JSON.parse(
  execFileSync(
    'python3',
    [
      '-c',
      `
import json,sys
from pathlib import Path
root=Path(sys.argv[1]);sys.path.insert(0,str(root/'src'))
from hivemind import bundle,service
from hivemind.views import store
ledger=service.open_ledger(str(root/'poc/data/sealed-2026-10-24-run3-through-0815/views.sqlite'))
items=store.open_read_only(str(root/'poc/data/items-window.sqlite'))
as_of=service.default_as_of(ledger)
ids=[r[0] for r in ledger.execute('select view_id from views order by created_seq')]
lookup=bundle.item_lookup(items)
print(json.dumps({'sequence_days':service.seq_day_map(ledger),'live':{'as_of':as_of,'days':bundle.days(ledger,as_of),'views':[bundle.view_bundle(ledger,lookup,id,as_of) for id in ids]}},ensure_ascii=False))
`,
      root,
    ],
    { encoding: 'utf8', maxBuffer: 32 * 1024 * 1024 },
  ),
);
export const live = records.live;
export const sequenceDays = records.sequence_days;
export const english = JSON.parse(
  fs.readFileSync(path.join(root, 'poc/mock/data.en.json'), 'utf8'),
);
export const original = JSON.parse(fs.readFileSync(path.join(root, 'poc/mock/data.json'), 'utf8'));
