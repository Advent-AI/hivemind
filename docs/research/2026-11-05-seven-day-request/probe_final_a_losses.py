"""Items where the first split-v2 run opened a question and the final run opened none: the final run's stored A request re-sent twice
(sampler or systematic?), and the stored final conversation continued once on two items for the model's account."""
import concurrent.futures, json, sqlite3, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, model

RUN = ROOT / 'poc/data/split-v2-final-first100-2026-11-05'
OUT = ROOT / 'poc/data/split-v2-final-losses-2026-11-05'
SEQS = [1228, 1241, 1246, 1252, 1254, 1268, 1271]
ACCOUNT = {1252: 'The article reports NVIDIA sold $89 billion of data center silicon last quarter, up 117% year over year.',
           1268: "The article reports Alphabet's second-quarter 2026 advertising revenue of $81.6 billion, up 14%."}

def main():
    OUT.mkdir(exist_ok=False)
    cfg = config.load(str(ROOT / 'poc/config/poc-split-v2.json'))
    jobs = []
    for seq in SEQS:
        request = json.loads((RUN / 'items' / str(seq) / 'a-request.json').read_text())
        for draw in (1, 2):
            jobs.append(('resend', seq, draw, request))
    for seq, fact in ACCOUNT.items():
        request = json.loads((RUN / 'items' / str(seq) / 'a-request.json').read_text())
        answer = (RUN / 'items' / str(seq) / 'a-answer.json').read_text()
        follow = dict(request); follow.pop('response_format')
        follow['messages'] = request['messages'] + [{'role': 'assistant', 'content': answer}, {'role': 'user', 'content': fact + ' You proposed no new question. Quote the exact sentence of your instructions, or the existing question by id, that led you not to propose one about this, and say whether on reflection it should have been proposed.'}]
        jobs.append(('account', seq, 1, follow))
    def send(job):
        kind, seq, draw, request = job
        response = model.openai_transport(cfg.provider, request)
        content = response['choices'][0]['message']['content']
        (OUT / f'{kind}-{seq}-{draw}.json').write_text(json.dumps({'request': request, 'response': response}, ensure_ascii=False))
        if kind == 'resend':
            return kind, seq, draw, [q['question'][:90] for q in json.loads(content)['questions']] or ['(none)']
        return kind, seq, draw, [content[:1400]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(send, jobs))
    (OUT / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=1) + '\n')
    for kind, seq, draw, rows in sorted(results, key=lambda r: (r[0] != 'resend', r[1], r[2])):
        print(kind, seq, draw, ' | '.join(rows))

if __name__ == '__main__':
    main()
