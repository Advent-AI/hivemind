"""Ask the v79 extraction model for its own account of a newness label (AGENTS §1: "for a choice the model made, the model's own account"):
rebuild the request as resend_targets.py sends it, take the saved answer of the send that wrote the statement (sends/<name>.json), continue
the conversation with one question about that one label, free text, no schema. About a cent a case. Writes nothing.

    python3 probe_fields.py <config json> <base run folder> <saved sends json> <title fragment> <quote fragment>
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / 'docs/research/2026-10-31-reference-context'), str(ROOT / 'src')]
import score_ref as sr  # noqa: E402
from hivemind import config, extraction, model, testdb, universe  # noqa: E402
from hivemind.views import store  # noqa: E402

cfg_path, base, saved_path, title, fragment = sys.argv[1:6]
cfg = config.load(cfg_path); uni = universe.load(str(ROOT / 'poc/universe.json'))
saved = json.loads(Path(saved_path).read_text(encoding='utf-8'))['answers']
article = next(a for a in sr.articles if title.lower() in a['title'].lower() and a['input_id'] in saved)
iid = article['input_id']
item = next(it for it in testdb.feed(testdb.open_db(str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite')), '2026-07-01', '2026-07-14') if it['input_id'] == iid)
scratch = Path(tempfile.mkdtemp(prefix='probe-fields-')); shutil.copy(Path(base) / 'views.sqlite', scratch / 'views.sqlite')
ledger = store.open_db(str(scratch / 'views.sqlite'))
objects = [o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])]
shown = extraction.shown_views(ledger, cfg, item, objects)
setting, system, user, schema = extraction.request_for(cfg, item, item['text'], shown, uni)
body = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
answer, hit = next(((ans, e) for ans in saved[iid] for e in ans.get('evidence', []) if fragment.lower()[:40] in (e.get('quote') or '').lower()), (None, None))
if answer is None:
    print(f'## {title} | {fragment[:50]!r}: no saved send wrote it'); sys.exit(0)
question = (f"About your answer: for the evidence item whose quote begins {hit['quote'][:120]!r} you answered new={hit['new']!r}, kind={hit['kind']!r}, "
            f"party={hit['party']!r}. Answer in three or four sentences, quoting the exact words of the field definition you applied: (1) Which case in the "
            f"'new' field's definition did you match it to? (2) Which case on the other side of that definition did you consider and reject, and why? "
            f"(3) As the analyst following the company, is this something you knew before reading this item, or new to you?")
body.pop('response_format', None)
body['messages'] = body['messages'] + [{'role': 'assistant', 'content': json.dumps(answer, ensure_ascii=False)}, {'role': 'user', 'content': question}]
print(f"## {article['title'][:70]} | {fragment[:50]!r} | labelled {hit['new']}/{hit['kind']}/{hit['party']}\n")
print(model.openai_transport(cfg.provider, body)['choices'][0]['message']['content'])
