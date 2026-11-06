"""The model's own account (AGENTS §1) of the split's evidence call (B) leaving out a statement the frozen extraction kept and the gold keeps: the stored
B conversation of a window draw is continued with one question naming the statement. A cent a case.

    PYTHONPATH=src python3 probe_b_omission_account.py <out.json> <draw> <matter> [<matter> ...]"""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / 'src'))
from hivemind import config, model  # noqa: E402

GOLD = '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json'


def main():
    out, draw, *matters = sys.argv[1:]
    cfg = config.load(str(HERE.parents[3] / 'poc/config/poc-split-v3.json'))
    gold = {a['input_id']: a for a in json.load(open(GOLD))['articles']}
    archive = sqlite3.connect(f'file:{HERE.parent}/runs/split-v3-d{draw}/archive.sqlite?mode=ro', uri=True)
    results = {}
    for matter in matters:
        input_id, index = matter.rsplit('#', 1)
        span = gold[input_id]['items'][int(index)]['span']
        rows = [(json.loads(r), a) for r, a in archive.execute("select request_json, answer_json from model_calls where purpose='split_b'")]
        request, answer = next((r, a) for r, a in rows if f'id {input_id},' in r['messages'][-1]['content'])
        question = (f'The article says: "{span}" Your answer does not include it as evidence. Which instruction led you to leave it out, and which '
                    'instructions did you weigh against that? Quote them, and name the open question you considered for it, if any.')
        request['messages'] = request['messages'] + [{'role': 'assistant', 'content': answer}, {'role': 'user', 'content': question}]
        request.pop('response_format', None)
        response = model.openai_transport(cfg.provider, request)
        results[matter] = {'span': span, 'account': response['choices'][0]['message']['content']}
        print('==', matter, '\n', results[matter]['account'][:1500], '\n')
    json.dump(results, open(out, 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
