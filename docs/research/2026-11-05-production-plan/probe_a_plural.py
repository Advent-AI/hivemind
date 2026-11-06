"""Does A's singular opening ("find an important new question") suppress a second important question? The confirmation run's stored A
requests on five items where the census found a missed question, re-sent twice as stored and twice with the opening asking for "the
important new questions this item raises" (the production prompt v74i's wording). Nothing else differs."""
import concurrent.futures, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, model

RUN = ROOT / 'poc/data/split-v2-confirm-first100-2026-11-05'
OUT = ROOT / 'poc/data/a-plural-probe-2026-11-05'
SEQS = [1209, 1210, 1228, 1234, 1266]
OLD = 'Your only job is to find an important new question that is not already covered, and bring the article\'s evidence for it.'
NEW = 'Your only job is to find the important new questions this item raises that are not already covered, and bring the article\'s evidence for each.'

def main():
    OUT.mkdir(exist_ok=False)
    cfg = config.load(str(ROOT / 'poc/config/poc-split-v2.json'))
    jobs = []
    for seq in SEQS:
        request = json.loads((RUN / 'items' / str(seq) / 'a-request.json').read_text())
        system = request['messages'][0]['content']
        assert system.count(OLD) == 1
        for arm, text in (('stored', system), ('plural', system.replace(OLD, NEW))):
            for draw in (1, 2):
                jobs.append((seq, arm, draw, dict(request, messages=[{'role': 'system', 'content': text}] + request['messages'][1:])))
    def send(job):
        seq, arm, draw, request = job
        response = model.openai_transport(cfg.provider, request)
        (OUT / f'{seq}-{arm}-{draw}.json').write_text(json.dumps({'request': request, 'response': response}, ensure_ascii=False))
        return seq, arm, draw, [q['question'][:85] for q in json.loads(response['choices'][0]['message']['content'])['questions']] or ['(none)']
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(send, jobs))
    (OUT / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=1) + '\n')
    for seq, arm, draw, rows in sorted(results):
        print(seq, arm, draw, ' | '.join(rows))

if __name__ == '__main__':
    main()
