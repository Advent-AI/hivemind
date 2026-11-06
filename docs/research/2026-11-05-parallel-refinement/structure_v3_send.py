"""One saved-request read diagnostic; no production writes or automatic link send."""
import hashlib
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import structure_v3_poc as poc
from hivemind import model

PREVIEW = Path('/Users/lchingen/hivemind-no-preseed-evidence-review/poc/data/parallel-structure-v3-preview-2026-11-05-v7/preview.json')


def wire(request):
    return hashlib.sha256(json.dumps(request).encode()).hexdigest()


def main():
    if len(sys.argv) != 2:
        raise SystemExit('usage: structure_v3_send.py absolute-new-directory')
    out = Path(sys.argv[1])
    if not out.is_absolute() or out.exists():
        raise ValueError('directory must be absolute and new')
    cfg, uni, base, questions, system, user, schema, request, link_rule = poc.prepare()
    saved = json.loads(PREVIEW.read_text())['read_request']
    if json.dumps(saved) != json.dumps(request):
        raise ValueError('read wire differs from reviewed preview')
    files = [HERE / 'structure_v3_poc.py', HERE / 'structure-v3-read.txt', HERE / 'structure-v3-link.txt',
             HERE / 'structure-v3-design.zh.md', Path(__file__), PREVIEW]
    frozen = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    out.mkdir(parents=True)
    (out / 'request.json').write_text(json.dumps(request, ensure_ascii=False, indent=2) + '\n')
    (out / 'manifest.json').write_text(json.dumps({'files': frozen, 'article': poc.ARTICLE,
        'article_sha256': poc.digest(base['item']['text']), 'questions_sha256': poc.digest(questions),
        'wire_sha256': wire(request)}, indent=2) + '\n')
    archive = model.Archive(str(out / 'archive.sqlite'))
    def transport(provider, actual):
        if provider != cfg.provider or json.dumps(actual) != json.dumps(request):
            raise ValueError('sent wire does not match reviewed request')
        response = model.openai_transport(provider, actual)
        (out / 'response.json').write_text(json.dumps(response, ensure_ascii=False, indent=2) + '\n')
        return response
    started = time.monotonic()
    try:
        answer = model.call(archive, cfg, base['setting'], system, user, schema, 'extraction', 'extract', transport=transport)
        result = {'status': 'read_complete', 'answer': answer.data, 'request_sha256': answer.request_sha256,
                  'input_tokens': answer.input_tokens, 'output_tokens': answer.output_tokens,
                  'seconds': round(time.monotonic() - started, 2)}
    except Exception as exc:
        result = {'status': 'failed', 'error': repr(exc)}
    finally:
        archive.conn.close()
    (out / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(result['status'], flush=True)


if __name__ == '__main__':
    main()
