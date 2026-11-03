"""Ask the extraction model why it left a statement out (AGENTS §1: the model's own account): rebuild the request as resend_targets.py sends
it, take one saved answer of that article (sends/<name>.json, answer index given), continue the conversation with one free-text question
naming the omitted sentence. About a cent a case. Writes nothing.
    python3 probe_omitted.py <config json> <base run folder> <saved sends json> <answer index> <title fragment> <omitted sentence>
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

cfg_path, base, saved_path, index, title, sentence = sys.argv[1:7]
cfg = config.load(cfg_path); uni = universe.load(str(ROOT / 'poc/universe.json'))
saved = json.loads(Path(saved_path).read_text(encoding='utf-8'))['answers']
article = next(a for a in sr.articles if title.lower() in a['title'].lower() and a['input_id'] in saved)
iid = article['input_id']
item = next(it for it in testdb.feed(testdb.open_db(str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite')), '2026-07-01', '2026-07-14') if it['input_id'] == iid)
scratch = Path(tempfile.mkdtemp(prefix='probe-omitted-')); shutil.copy(Path(base) / 'views.sqlite', scratch / 'views.sqlite')
ledger = store.open_db(str(scratch / 'views.sqlite'))
objects = [o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])]
shown = extraction.shown_views(ledger, cfg, item, objects)
setting, system, user, schema = extraction.request_for(cfg, item, item['text'], shown, uni)
body = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
answer = saved[iid][int(index)]
question = (f"About your answer: the item says {sentence!r}, and your evidence list does not include it. In three or four sentences, quoting the "
            f"exact words of the instruction you applied: (1) Which instruction led you to leave it out? (2) As the analyst following the company, "
            f"would you write it in this week's notes?")
body.pop('response_format', None)
body['messages'] = body['messages'] + [{'role': 'assistant', 'content': json.dumps(answer, ensure_ascii=False)}, {'role': 'user', 'content': question}]
print(f"## {article['title'][:70]} | answer {index} | {sentence[:60]!r}\n")
print(model.openai_transport(cfg.provider, body)['choices'][0]['message']['content'])
print()
