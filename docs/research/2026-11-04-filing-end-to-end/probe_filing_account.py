"""The extraction model's own account of one filing (AGENTS §1: "which instruction led you here, and which two statements did you reject"),
a cent or two a send. The stored extraction conversation is continued as sent (system, user, the stored answer as the assistant's turn)
without the response schema, so the question quotes the links field's own description from the stored request's schema: the model sees
the rule it applied. Each case is sent `sends` times, since one answer is one draw.

usage: python3 probe_filing_account.py <draw folder> <out.md> <evidence one_line prefix>::<other question ids> [...] [--sends N]
"""
import json
import sqlite3
import sys

sys.path.insert(0, '/Users/lchingen/hivemind/src')
from hivemind import config, model  # noqa: E402


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    sends = int(sys.argv[sys.argv.index('--sends') + 1]) if '--sends' in sys.argv else 2
    folder, out, cases = args[0], args[1], [a for a in args[2:] if '::' in a]
    cfg = config.load('/Users/lchingen/hivemind/poc/config/poc-v108.json')
    archive = sqlite3.connect(f'file:{folder}/archive.sqlite?mode=ro', uri=True)
    lines = [f'# The extraction model\'s account of its filings ({folder})', '']
    for case in cases:
        prefix, others = case.split('::')
        row = None
        for request_json, answer_json in archive.execute("select request_json, answer_json from model_calls where purpose='extract' and answer_json is not null "
                                                          "and request_sha256 not like '%:%' order by call_id"):
            answer = json.loads(answer_json)
            hit = next((ev for ev in answer.get('evidence', []) if ev['one_line'].startswith(prefix)), None)
            if hit:
                row = (json.loads(request_json), answer_json, hit)
        if not row:
            raise SystemExit(f'no stored answer wrote a statement starting {prefix!r}')
        request, answer_json, statement = row
        schema = request['response_format']['json_schema']['schema']
        rule = schema['properties']['evidence']['items']['properties']['links']['description']
        question = (f'You filed the statement "{statement["one_line"]}" under {", ".join(statement["links"]) or "no question"}. '
                    f'The links field\'s instruction was: "{rule}" '
                    f'Which words of that instruction, or of the question list, led you to that filing? Did you consider {others}, and why did you '
                    f'not file it there? Quote the words, and answer in a few short paragraphs.')
        messages = [m for m in request['messages']] + [{'role': 'assistant', 'content': answer_json}, {'role': 'user', 'content': question}]
        probe = {k: v for k, v in request.items() if k not in ('response_format', 'messages')}
        probe['messages'] = messages
        lines += [f'## "{statement["one_line"]}" filed under {statement["links"]}; asked about {others}', '']
        for n in range(sends):
            response = model.openai_transport(cfg.provider, probe)
            lines += [f'### send {n + 1}', '', response['choices'][0]['message']['content'].strip(), '']
            print(f'{prefix[:50]}… send {n + 1}: answered')
    open(out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
