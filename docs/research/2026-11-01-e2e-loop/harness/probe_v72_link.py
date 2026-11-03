"""Ask the v72 extraction model for its own account of a link it wrote to an open question (AGENTS §1: "for a choice the model made, the
model's own account"): continue the stored extraction conversation (the request as sent, the answer as returned) with one question about
one statement, found by a fragment of its quote, free text, no schema. About a cent a case. Reads a finished run's archive, writes nothing.

    python3 probe_v72_link.py <run folder> <config json> <title fragment> <quote fragment>
"""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, model  # noqa: E402

run, cfg_path, title, fragment = sys.argv[1:5]
cfg = config.load(cfg_path)
archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
row = archive.execute("select request_json, answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1",
                      (f'%{title}%',)).fetchone()
body, answer = json.loads(row[0]), json.loads(row[1])
statement = next(e for e in answer['evidence'] if fragment.lower() in (e.get('quote') or '').lower())
question = (f"About your answer: statement {statement['id']} ({statement['quote'][:220]!r}) has links {statement.get('links')}. Answer in three or four "
            f"sentences, quoting the instruction or takes line you followed: (1) Which takes line or instruction led you to file it under each of those "
            f"question ids? (2) The links field says to file under the narrowest covering question only, never a broader one beside it: why more than one, "
            f"or why a company-wide revenue question for this statement? (3) Reading the item again, which single question, if any, does this statement "
            f"make more or less likely, and through which path?")
body.pop('response_format', None)
body['messages'] = body['messages'] + [{'role': 'assistant', 'content': json.dumps(answer, ensure_ascii=False)}, {'role': 'user', 'content': question}]
print(f'## {title} | {statement["id"]} links {statement.get("links")}\nquote: {statement["quote"][:200]}\n')
print(model.openai_transport(cfg.provider, body)['choices'][0]['message']['content'])
