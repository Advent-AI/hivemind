"""The model's own account of a stored judgement (AGENTS §1: "which instruction led you here, and which two statements did you
reject"), a cent or two a case. It continues the stored conversation exactly as sent (system, user, the stored answer as the assistant's
turn) with one question, without a response schema, and writes the answers beside this script.

usage: python3 probe_account.py <run folder> <out.md> <view_id:day> [<view_id:day> ...]
"""
import json
import sqlite3
import sys

sys.path.insert(0, '/Users/lchingen/hivemind/src')
from hivemind import config, model  # noqa: E402

QUESTION = ('Look back at the answer you just gave. Which sentence of the instructions, or of the material shown, led you to the implied '
            'outcome and the rung you chose? Name the two statements in the material that pointed elsewhere and say why you set them aside. '
            'Quote the instruction and the statements word for word, and answer in a few short paragraphs.')


def main():
    run, out, *cases = sys.argv[1:]
    cfg = config.load('/Users/lchingen/hivemind/poc/config/poc-v109.json')
    views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
    archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    lines = [f'# The model\'s own account ({run})', '', f'Question asked: "{QUESTION}"', '']
    for case in cases:
        view_id, day = case.split(':')
        sha, rung = views.execute('select request_sha256, rung from judgements where view_id=? and publication_day=?', (view_id, day)).fetchone()
        request_json, answer_json = archive.execute('select request_json, answer_json from model_calls where request_sha256=?', (sha,)).fetchone()
        request = json.loads(request_json)
        request.pop('response_format', None)
        request['messages'] = request['messages'] + [{'role': 'assistant', 'content': answer_json}, {'role': 'user', 'content': QUESTION}]
        response = model.openai_transport(cfg.provider, request)
        text = response['choices'][0]['message']['content']
        usage = response.get('usage') or {}
        lines += [f'## {view_id} on {day} (rung {rung})', '', text.strip(), '',
                  f'(tokens in {usage.get("prompt_tokens")}, out {usage.get("completion_tokens")})', '']
        print(f'{view_id} {day}: answered, {usage.get("prompt_tokens")} in / {usage.get("completion_tokens")} out')
    open(out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
