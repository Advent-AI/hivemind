"""Ask the extraction model for its own account of a link it did not write (AGENTS §1: "for a choice the model made, the model's
own account"): continue the stored extraction conversation (the request as sent, the answer as returned) with one question about
one statement and one candidate, free text, no schema. About a cent a case.

    python3 probe_link.py <run folder> <config json> <title fragment> <statement id> <candidate id>
"""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, model  # noqa: E402

run, cfg_path, title, sid, cid = sys.argv[1:6]
cfg = config.load(cfg_path)
archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
row = archive.execute("select request_json, answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1",
                      (f'%{title}%',)).fetchone()
body, answer = json.loads(row[0]), json.loads(row[1])
statement = next(e for e in answer['evidence'] if e['id'] == sid)
candidate = next(c for c in answer['candidates'] if c['id'] == cid)
question = (f"About your answer: statement {sid} ({statement['quote'][:200]!r}) has links {statement.get('links')}, and candidate {cid} asks "
            f"{candidate.get('question') or candidate.get('title')!r}. Two questions, answer each in two or three sentences, quoting the instruction you followed: "
            f"(1) Which instruction or schema description led you to leave {sid} without a link to {cid}? "
            f"(2) Reading the item, does the matter of {sid} belong to the matter {cid} asks about, and what in the item tells you so?")
body.pop('response_format', None)
body['messages'] = body['messages'] + [{'role': 'assistant', 'content': json.dumps(answer, ensure_ascii=False)}, {'role': 'user', 'content': question}]
print(f'## {title} | {sid} -> {cid}\nQ: {question}\n')
print(model.openai_transport(cfg.provider, body)['choices'][0]['message']['content'])
