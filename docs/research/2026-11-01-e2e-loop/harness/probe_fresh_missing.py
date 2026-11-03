"""The model's own account under a configuration that has no stored answers yet (AGENTS §1: "for a choice the model made, the model's own
account"): build the article's extraction request under the configuration from a finished run's day-start snapshot, send it once, then
continue that conversation with one question about one sentence of the item the answer left out (or kept), free text, no schema.
Two calls a case, about two cents. Reads a finished run's ledger copy, writes nothing.

    python3 probe_fresh_missing.py <snapshot run folder> <config json> <title fragment> <sentence fragment>
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, extraction, model, testdb, universe  # noqa: E402
from hivemind.views import store  # noqa: E402

run, cfg_path, title, fragment = sys.argv[1:5]
cfg = config.load(cfg_path)
uni = universe.load(str(ROOT / 'poc/universe.json'))
scratch = Path(tempfile.mkdtemp(prefix='probe-'))
shutil.copy(Path(run) / 'views.sqlite', scratch / 'views.sqlite')
ledger = store.open_db(str(scratch / 'views.sqlite'))
items_db = testdb.open_db(str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'))
item = next(it for it in testdb.feed(items_db, '2026-07-01', '2026-07-14') if title.lower() in (it.get('title') or '').lower())
objects = [o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])]
shown = extraction.shown_views(ledger, cfg, item, objects)
setting, system, user, schema = extraction.request_for(cfg, item, item['text'], shown, uni)
body = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
answer = json.loads(model.openai_transport(cfg.provider, body)['choices'][0]['message']['content'])
text = item['text']; at = text.lower().find(fragment.lower())
sentence = text[max(0, at - 80):at + len(fragment) + 160].replace('\n', ' ') if at >= 0 else fragment
kept = [e for e in answer.get('evidence', []) if fragment.lower()[:40] in (e.get('quote') or '').lower()]
question = (f"About your answer: the item contains the passage {sentence!r}. Your evidence list {'has' if kept else 'does not have'} an item for it. Answer in "
            f"three or four sentences, quoting the exact instruction, check row or takes line you followed: (1) Which sentence of the role text, the closing check or "
            f"the schema led you to leave this statement out (or to keep it as you wrote it)? (2) Does that sentence's own boundary send it back to the check? "
            f"(3) As the senior analyst covering the company, does this statement bear on its demand, supply, input costs, competition or pricing, and under "
            f"which open question would you file it?")
body.pop('response_format', None)
body['messages'] = body['messages'] + [{'role': 'assistant', 'content': json.dumps(answer, ensure_ascii=False)}, {'role': 'user', 'content': question}]
print(f'## {item["title"][:70]} | fragment {fragment[:60]!r} | kept in the fresh answer: {bool(kept)} | statements written {len(answer.get("evidence", []))}\n')
print(model.openai_transport(cfg.provider, body)['choices'][0]['message']['content'])
shutil.rmtree(scratch, ignore_errors=True)
