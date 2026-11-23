"""The model's own account of the fresh week's line-3 miss (council round 108): control f1/clean-17 pass 3 wrote its Ruled-out decision
as "The authority formally announces that it will not adopt tighter export controls … by January 31, 2027". Its stored conversation is
continued (the request rebuilt by the production builder from the frozen texts and checked against the stored request's sha256, the
model's own answer text as the assistant turn) with one neutral question. An account is a lead that can rationalize the answer, not
proof of a cause. Asked once; $0.02 ceiling.

  python3 taiwan_account.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import fresh_probe  # noqa: E402

probe = fresh_probe.probe
DATA = Path('/Users/lchingen/hivemind/poc/data/clean-fresh-a2-2026-11-16')
CAP_USD = 0.02
REPLY_TOKEN_CAP = 3000
CASE, PASS = 'f1/clean-17', 3
QUESTION = ('One question about your answer. Your ruled_out decision reads: "formally announces that it will not adopt tighter export '
            'controls on high-end AI processors and servers by January 31, 2027". Which instruction in the request, and which words of '
            'the topic or the item, led you to write that decision? Which other way of writing the ruled-out decision did you consider '
            'and set aside, and why? Quote them. If you cannot identify them, say so. Answer in at most 150 words.')


def main():
    output_path = HERE / 'taiwan-account.json'
    if output_path.exists():
        raise SystemExit(f'{output_path.name} exists: the account is asked once')
    fresh_probe.configure(str(DATA / 'cases/cases.json'), str(DATA / 'population/population.json'))
    research_list = probe.universe.load(str(probe.ROOT / 'poc' / 'universe.json'))
    case = next(case for case in json.loads((DATA / 'cases/cases.json').read_text()) if case['case'] == CASE)
    label = f'control|fresh:{CASE}'
    outcome = next(row for row in map(json.loads, (DATA / 'choices/control' / f'send-{PASS}' / 'outcomes.jsonl').read_text().splitlines())
                   if row['case'] == label)
    if outcome['status'] != 'ladder' or len(outcome['requests']) != 1:
        raise SystemExit(f'{label} pass {PASS}: not a single-request ladder')
    request = probe.built(dict(case, case=label), probe.stage_a.request_texts(), research_list)
    if probe.model.request_identity(request)[1] != outcome['requests'][0]['request_sha256']:
        raise SystemExit(f'{label} pass {PASS}: the rebuilt request is not the one sent')
    follow_up = {key: value for key, value in request.items() if key not in ('response_format', 'max_completion_tokens')}
    follow_up['max_completion_tokens'] = REPLY_TOKEN_CAP
    follow_up['messages'] = request['messages'] + [{'role': 'assistant', 'content': outcome['requests'][0]['answer_text']},
                                                   {'role': 'user', 'content': QUESTION}]
    limit = probe.stage_a.budget.Budget(CAP_USD)
    response = limit.send('openai', follow_up)
    usage = response.get('usage') or {}
    reply = {'case': label, 'pass': PASS, 'question': QUESTION, 'reply': response['choices'][0]['message']['content'],
             'input_tokens': usage.get('prompt_tokens'), 'output_tokens': usage.get('completion_tokens')}
    output_path.write_text(json.dumps(reply, ensure_ascii=False, indent=1) + '\n')
    print(reply['reply'])
    print(f'tokens in {reply["input_tokens"]}, out {reply["output_tokens"]}; spent ${limit.spent_usd:.4f} of ${CAP_USD:.2f}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
