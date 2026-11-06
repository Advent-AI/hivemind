"""The model's own account (AGENTS §1) of record preparation returning no rungs for questions whose article or evidence states a full-period
reference: the stored preparation conversation of the 2026-08-29/30 production-path probe is continued with one question. A cent a case.

    PYTHONPATH=src python3 probe_ladder_account.py <out.json> <seq> [<seq> ...]"""
import json
import sqlite3
import sys

sys.path.insert(0, '/Users/lchingen/hivemind-no-preseed-evidence-review/src')
from hivemind import config, model  # noqa: E402

RUN = '/Users/lchingen/hivemind-no-preseed-evidence-review/poc/data/split-v3-prod-0829-0830-r2-2026-11-06'
QUESTION = ('For each question in your answer whose rungs array is empty, which instruction led you to return no rungs, and which statements in the '
            'article or the evidence did you consider and reject as the neutral comparison? Quote the instruction and the statements.')


def main():
    out, *seqs = sys.argv[1:]
    cfg = config.load('/Users/lchingen/hivemind-no-preseed-evidence-review/poc/config/poc-split-v3.json')
    views = sqlite3.connect(f'file:{RUN}/views.sqlite?mode=ro', uri=True)
    archive = sqlite3.connect(f'file:{RUN}/archive.sqlite?mode=ro', uri=True)
    results = {}
    for seq in seqs:
        input_id = views.execute("select input_id from processing_steps where sequence_no=? and step='dispatched'", (int(seq),)).fetchone()[0]
        title = sqlite3.connect(f'file:{RUN}/items-window.sqlite?mode=ro', uri=True).execute('select title from items where input_id=?', (input_id,)).fetchone()[0]
        rows = [(json.loads(r), a) for r, a in archive.execute("select request_json, answer_json from model_calls where purpose='split_preparation'")]
        question = views.execute('select question from views where created_seq=? order by view_id limit 1', (int(seq),)).fetchone()[0]
        request, answer = next((r, a) for r, a in rows if question[:80] in r['messages'][-1]['content'])
        request['messages'] = request['messages'] + [{'role': 'assistant', 'content': answer}, {'role': 'user', 'content': QUESTION}]
        request.pop('response_format', None)
        response = model.openai_transport(cfg.provider, request)
        results[seq] = {'input_id': input_id, 'account': response['choices'][0]['message']['content'], 'usage': response.get('usage')}
        print(seq, results[seq]['account'][:1500], '\n')
    json.dump(results, open(out, 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
