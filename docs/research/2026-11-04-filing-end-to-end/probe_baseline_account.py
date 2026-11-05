"""The model's own account of three kept figures of another quantity in the all-seeds reading (baseline-design.md, round 8 result): the stored
reading request rebuilt by baseline_all.build(), continued with the answer as stored (its fields as the model wrote them) and one question.
About a cent each; sends three requests.

usage: python3 probe_baseline_account.py <reading.json> <out.md>
"""
import json
import sys

ROOT = '/Users/lchingen/hivemind'
sys.path[:0] = [f'{ROOT}/src', f'{ROOT}/docs/research/2026-11-04-filing-end-to-end']
import baseline_all  # noqa: E402
from hivemind import model  # noqa: E402

PR = 'edgar:NVDA:0001045810-26-000051:q1fy27pr.htm'
CFO = 'edgar:NVDA:0001045810-26-000051:q1fy27cfocommentary.htm'
CASES = [('v19', CFO, 0), ('v19', CFO, 1), ('v20', PR, 0)]
FIELDS = ('quote', 'value', 'unit', 'period', 'basis', 'one_line')
QUESTION = ('For each figure you wrote above, which sentence of the instructions led you to write it for this question, and is it this '
            'question\'s quantity itself? Then name two statements of the report you considered for this question and did not write, and why. '
            'Answer in plain sentences, at most six.')


def main():
    reading, out = json.load(open(sys.argv[1])), sys.argv[2]
    cfg, report, texts, requests = baseline_all.build()
    lines = []
    for view_id, input_id, n in CASES:
        body = requests[(view_id, input_id)]
        if model.request_identity(body)[1] != reading['requests'][f'{view_id}|{input_id}']:
            raise SystemExit(f'{view_id} {input_id}: the rebuilt request is not the one sent')
        answer = {'figures': [{k: f[k] for k in FIELDS} for f in reading['results'][view_id][input_id][n]['figures']]}
        probe = {k: v for k, v in body.items() if k not in ('response_format', 'messages')}
        probe['messages'] = list(body['messages']) + [{'role': 'assistant', 'content': json.dumps(answer, ensure_ascii=False)},
                                                      {'role': 'user', 'content': QUESTION}]
        reply = model.openai_transport(cfg.provider, probe, timeout=300)
        text = reply['choices'][0]['message']['content']
        lines.append(f'## {view_id}, {input_id.rsplit(":", 1)[-1]}, send {n}\n\nAnswer as stored: `{json.dumps(answer, ensure_ascii=False)[:600]}`\n\n'
                     f'Question: {QUESTION}\n\nThe model\'s account:\n\n{text}\n')
        print(lines[-1])
    open(out, 'w').write('# The model\'s account of the kept figures of another quantity (all-seeds reading)\n\n' + '\n'.join(lines))


if __name__ == '__main__':
    main()
