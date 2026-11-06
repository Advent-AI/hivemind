"""Continue one saved conversation to ask about a missing candidate; the account is retrospective."""
import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import model

RUN = ROOT / 'poc/data/simple-new-question-run-2026-11-05-v1'
ID = 'gnews:085b1e1a1543437edb9756d6'
QUESTION = ('You proposed a question about the amount of datacenter-lease backstops. Explain how you considered the GPU-capacity revenue backstop programme described in the article and the existing v1 question. Which instructions and source statements guided your decision, and what alternative question or interpretation did you reject? Do not invent a past decision; say when you cannot tell from the saved conversation.')


def wire(request):
    return hashlib.sha256(json.dumps(request).encode()).hexdigest()


def build():
    manifest = json.loads((RUN / 'manifest.json').read_text())
    row = next(r for r in manifest['requests'] if r['id'] == ID)
    request = copy.deepcopy(row['request'])
    if wire(request) != row['wire_sha256']:
        raise ValueError('saved request hash mismatch')
    response = json.loads((RUN / (ID.replace(':', '_')) / 'response.json').read_text())
    answer = response['choices'][0]['message']['content']
    json.loads(answer)
    request['messages'] += [{'role': 'assistant', 'content': answer}, {'role': 'user', 'content': QUESTION}]
    request.pop('response_format', None)
    request['max_completion_tokens'] = 1500
    return request


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ('freeze', 'send'):
        raise SystemExit('usage: freeze|send absolute-directory')
    out = Path(sys.argv[2])
    if not out.is_absolute():
        raise ValueError('absolute directory required')
    request = build()
    if sys.argv[1] == 'freeze':
        if out.exists():
            raise ValueError('directory exists')
        out.mkdir(parents=True)
        (out / 'request.json').write_text(json.dumps({'request': request, 'wire_sha256': wire(request)}, ensure_ascii=False, indent=2) + '\n')
        print('account request frozen', flush=True)
        return
    saved = json.loads((out / 'request.json').read_text())
    if saved['wire_sha256'] != wire(request) or json.dumps(saved['request']) != json.dumps(request):
        raise ValueError('account request changed')
    path = out / 'response.json'
    if path.exists():
        raise ValueError('account already sent')
    response = model.openai_transport('openai', request)
    path.write_text(json.dumps(response, ensure_ascii=False, indent=2) + '\n')
    print(response['choices'][0]['message'].get('content', ''), flush=True)


if __name__ == '__main__':
    main()
