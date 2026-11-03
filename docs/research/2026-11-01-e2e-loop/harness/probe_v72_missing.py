"""Ask the v72 extraction model for its own account of a statement it did not keep (AGENTS §1: "for a choice the model made, the
model's own account"): continue the stored extraction conversation (the request as sent, the answer as returned) with one question about
one sentence of the item, found by a fragment, free text, no schema. About a cent a case. Reads a finished run's archive, writes nothing.

    python3 probe_v72_missing.py <run folder> <config json> <title fragment> <sentence fragment>
"""
import json
import re
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
text = body['messages'][-1]['content']
at = text.lower().find(fragment.lower())
sentence = text[max(0, at - 60):at + len(fragment) + 160].replace('\n', ' ') if at >= 0 else fragment
kept = [e for e in answer['evidence'] if fragment.lower()[:40] in (e.get('quote') or '').lower()]
question = (f"About your answer: the item contains the passage {sentence!r}. Your evidence list {'has' if kept else 'does not have'} an item for it. "
            f"Answer in three or four sentences, quoting the exact instruction or check row you followed: (1) Which row of the closing check, or which "
            f"instruction in the role text, led you to leave this statement out (or to keep it)? (2) Does that row's own boundary ('it does not cover ...') "
            f"send this statement back to the check? (3) As the analyst following the company, would you write it in this week's notes, and under which "
            f"open question, if any?")
body.pop('response_format', None)
body['messages'] = body['messages'] + [{'role': 'assistant', 'content': json.dumps(answer, ensure_ascii=False)}, {'role': 'user', 'content': question}]
print(f'## {title} | fragment {fragment[:60]!r} | kept in the stored answer: {bool(kept)}\n')
print(model.openai_transport(cfg.provider, body)['choices'][0]['message']['content'])
