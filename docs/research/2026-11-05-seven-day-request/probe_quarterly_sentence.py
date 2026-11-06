"""The new-question request with the clarified quarterly sentence, against the final run's stored request (only the system text differs):
seven items where the final run opened nothing although the first run opened an annual question, and four items that must open nothing."""
import concurrent.futures, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, model

RUN = ROOT / 'poc/data/split-v2-final-first100-2026-11-05'
OUT = ROOT / 'poc/data/quarterly-sentence-probe-2026-11-05'
LOST = [1228, 1241, 1246, 1252, 1254, 1268, 1271]
CONTROLS = [1220, 1226, 1231, 1232]

def main():
    OUT.mkdir(exist_ok=False)
    cfg = config.load(str(ROOT / 'poc/config/poc-split-v2.json'))
    system = (ROOT / 'docs/research/2026-11-05-parallel-refinement/split-a-v2-prompt.txt').read_text()
    jobs = []
    for seq in LOST + CONTROLS:
        request = json.loads((RUN / 'items' / str(seq) / 'a-request.json').read_text())
        assert request['messages'][0]['role'] == 'system'
        changed = dict(request, messages=[{'role': 'system', 'content': system}] + request['messages'][1:])
        for draw in (1, 2):
            jobs.append((seq, draw, changed))
    def send(job):
        seq, draw, request = job
        response = model.openai_transport(cfg.provider, request)
        (OUT / f'{seq}-{draw}.json').write_text(json.dumps({'request': request, 'response': response}, ensure_ascii=False))
        questions = json.loads(response['choices'][0]['message']['content'])['questions']
        return seq, draw, [q['question'][:90] for q in questions] or ['(none)']
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(send, jobs))
    (OUT / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=1) + '\n')
    for seq, draw, rows in sorted(results):
        print('lost' if seq in LOST else 'ctrl', seq, draw, ' | '.join(rows))

if __name__ == '__main__':
    main()
