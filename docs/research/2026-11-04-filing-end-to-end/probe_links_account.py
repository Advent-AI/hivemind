"""The extraction model's own account of a choice it made under the tested links rule (AGENTS §1, §7.3: a failed arm is traced to the raw answers
and the model's account), a cent or so a send. The v74l request of one article is rebuilt exactly as the test sent it (`resend_filing.arm_request`)
and continued with the test's stored answer as the assistant's turn (its evidence list; the candidates are not stored in full and are left out),
then one question, without the response schema; the question quotes the links rule, since the schema that carried it is not sent.

usage: python3 probe_links_account.py <out.md> [--sends 2]
"""
import json
import sys

ROOT = '/Users/lchingen/hivemind'
sys.path[:0] = [f'{ROOT}/src', f'{ROOT}/scripts', f'{ROOT}/docs/research/2026-11-04-filing-end-to-end']
import resend_filing as rf  # noqa: E402
from hivemind import config, model  # noqa: E402

HERE = f'{ROOT}/docs/research/2026-11-04-filing-end-to-end'
CASES = [   # (article, send of the test's v74l arm to continue, question template; {rule} is the links rule)
    ('gnews:f66e1689ec2e27e7eab2a2dd', 0,
     'You filed the statement about the Vera Rubin rack costing hyperscale cloud providers around $7.8 million under v4. The links field\'s '
     'instruction was: "{rule}" Which words of that instruction, or of the question list, led you to that filing? Did you consider v20 (How much '
     'revenue will NVIDIA report from Blackwell and Rubin products in FY2027?), and why did you not file it there? Quote the words, and answer in a '
     'few short paragraphs.'),
    ('gnews:3df0bbc8aff2c1d008bc0a32', 1,
     'The item says: "Most strikingly, Micron is now forecasting adjusted gross margins of 86% next quarter". You did not write it as an evidence '
     'item. Which instruction led you to leave it out? Is there an open question it bears on under the links field\'s instruction: "{rule}"? Quote '
     'the words, and answer in a few short paragraphs.'),
]


def main():
    out = sys.argv[1]
    sends = int(sys.argv[sys.argv.index('--sends') + 1]) if '--sends' in sys.argv else 2
    selection = json.load(open(f'{HERE}/selection-test.json'))
    answers = json.load(open(f'{HERE}/answers-links.json'))
    rules = json.load(open(f'{HERE}/links-rules.json'))
    cfg = config.load(f'{ROOT}/poc/config/poc-v108.json')
    items_conn, archive, views = rf.ro(rf.ITEMS), rf.ro(f'{rf.DRAW}/archive.sqlite'), rf.ro(f'{rf.DRAW}/views.sqlite')
    lines = ['# The extraction model\'s account of its choices under v74l (the one test of 2026-11-04)', '']
    for input_id, send, template in CASES:
        meta = selection['articles'][input_id]
        prepared = rf.rebuild(cfg, items_conn, archive, views, input_id, meta['call_id'], meta['request_sha256'])
        body = rf.arm_request(cfg, rules, 'v74l', prepared, input_id)
        stored = answers[input_id]['v74l'][send]
        question = template.format(rule=rules['v74l']['rule'])
        probe = {k: v for k, v in body.items() if k not in ('response_format', 'messages')}
        probe['messages'] = list(body['messages']) + [{'role': 'assistant', 'content': json.dumps({'evidence': stored['raw'], 'candidates': []}, ensure_ascii=False)},
                                                      {'role': 'user', 'content': question}]
        lines += [f'## {input_id}, v74l send {send}', '', f'Question: {question[:400]}…', '']
        for n in range(sends):
            response = model.openai_transport(cfg.provider, probe, timeout=300)
            usage = response.get('usage') or {}
            lines += [f'### send {n + 1} ({usage.get("prompt_tokens", 0)} prompt, {usage.get("completion_tokens", 0)} completion tokens)', '',
                      response['choices'][0]['message']['content'].strip(), '']
            print(f'{input_id} send {n + 1}: answered', flush=True)
    open(out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
