"""Re-send one probe case several times under the request as first sent and as sent the second time (AGENTS §7.3: a model call is a
sampler; re-send a stored request before calling its answer a defect). The stored requests are sent as they were, byte for byte.

  python3 clean-arch/step4-2026-11-10/probe-2026-11-10/resend_case.py u2/clean-10 3
"""
import concurrent.futures
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
sys.path[:0] = [str(REPOSITORY / 'src'), str(REPOSITORY / 'clean-arch' / 'e2e-2026-11-09')]
import budget  # noqa: E402

CAP_USD = 0.15


def stored_request(archive_name, case_thesis_id):
    """The request of one case as the archive holds it: the one whose payload carries that thesis id."""
    connection = sqlite3.connect(f'file:{HERE / archive_name}?mode=ro', uri=True)
    for (request_json,) in connection.execute('select request_json from model_calls order by rowid'):
        request = json.loads(request_json)
        payload = json.loads(request['messages'][1]['content'].rsplit('\n\n', 1)[0])
        if payload['thesis']['id'] == case_thesis_id:
            return request
    raise SystemExit(f'no request for {case_thesis_id} in {archive_name}')


def main():
    case, sends_each = sys.argv[1], int(sys.argv[2])
    thesis_id = case.split('/')[1]
    output_path = HERE / f"resend-{case.replace('/', '-')}.json"
    if output_path.exists():
        raise SystemExit(f'{output_path} exists')
    limit = budget.Budget(CAP_USD)
    jobs = [(label, number, stored_request(archive_name, thesis_id))
            for label, archive_name in (('first request', 'archive.sqlite'), ('second request', 'archive-round2.sqlite'))
            for number in range(1, sends_each + 1)]

    def send(job):
        label, number, request = job
        response = limit.send('openai', request)
        answer = json.loads(response['choices'][0]['message']['content'])
        ladder = answer.get('ladder')
        shape = 'declined' if answer.get('no_ladder') else next(name for name in ('yes_no', 'states', 'figure') if ladder.get(name))
        return {'request': label, 'send': number, 'shape': shape, 'answer': answer}

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(jobs)) as pool:
        results = list(pool.map(send, jobs))
    output_path.write_text(json.dumps(results, ensure_ascii=False, indent=1) + '\n')
    for result in results:
        answer = result['answer']
        summary = answer['no_ladder'] if answer.get('no_ladder') else answer['ladder']['question']
        print(f"{result['request']:>14} #{result['send']} | {result['shape']:<8} | {summary[:150]}")
    print(f'spent ${limit.spent_usd:.4f} of ${CAP_USD:.2f}')


if __name__ == '__main__':
    main()
