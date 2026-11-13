"""A three-arm probe of the ladder step's request on stored theses: first answers only, no code check, no resend for a fault.

Arms (files `<arm>-system.txt`, `<arm>-closing.txt`, `<arm>-schema.json` beside this script):
  old        the request as the second Stage A sent it
  reference  the working request, with the reference's kind and range (D411)
  unclear    the working request with a third value, unclear, for a company figure's favourable end (an option, not decided)

Every (arm, draw) has its own model archive, so the same request is a fresh sample each time. What the probe decides and the
numbers that decide it are in REGISTERED.md, written before the send.

  python3 clean-arch/step4-2026-11-10/probe-direction-2026-11-10/probe.py check          # $0: the old arm rebuilds a stored request
  python3 clean-arch/step4-2026-11-10/probe-direction-2026-11-10/probe.py send <new folder>
"""
import concurrent.futures
import hashlib
import json
import sqlite3
import sys
import threading
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch' / 'e2e-2026-11-09'), str(STEP / 'ladder'), str(STEP / 'stage_a')]
import ladder_step  # noqa: E402
import model_calls  # noqa: E402
import stage_a  # noqa: E402
from hivemind import model, universe  # noqa: E402

CAP_USD = 0.20
DRAWS = (1, 2, 3)
DIRECTION_THESES = ['u3/clean-8', 'acc/clean-1', 'acc/clean-7', 'u1/clean-7', 'u2/clean-6', 'u1/clean-1', 'acc/clean-3', 'acc/clean-5']
EVENT_THESES = ['u1/clean-3', 'u1/clean-12', 'u2/clean-3', 'u1/clean-11']
THESES_OF_ARM = {'old': DIRECTION_THESES + EVENT_THESES, 'reference': DIRECTION_THESES + EVENT_THESES, 'unclear': DIRECTION_THESES}
SECOND_RUN = ROOT / 'poc' / 'data' / 'clean-ladder-stage-a-2026-11-10' / 'run-2'


def texts_of(arm):
    return {'system': (HERE / f'{arm}-system.txt').read_text(), 'closing': (HERE / f'{arm}-closing.txt').read_text().strip(),
            'schema': json.loads((HERE / f'{arm}-schema.json').read_text())}


def request_identity_of(arm, case, research_list):
    texts = texts_of(arm)
    request = model.build_request(stage_a.SETTING, texts['system'], ladder_step.user_text(stage_a.payload_for(case, research_list), texts['closing']),
                                  texts['schema'], 'clean_ladder', 'openai')
    return model.request_identity(request)[1]


def check(cases, research_list):
    """The old arm's request for every probed thesis has the identity of the request the second run sent for it."""
    same = 0
    for name in THESES_OF_ARM['old']:
        row = [row for line in (SECOND_RUN / 'send-1' / 'outcomes.jsonl').read_text().splitlines() for row in [json.loads(line)] if row['case'] == name][0]
        rebuilt = request_identity_of('old', cases[name], research_list)
        same += rebuilt == row['requests'][0]['request_sha256']
        if rebuilt != row['requests'][0]['request_sha256']:
            print(f'  {name}: the old arm does not rebuild the stored request')
    print(f"the old arm rebuilds the second run's first request for {same} of {len(THESES_OF_ARM['old'])} theses")
    if same != len(THESES_OF_ARM['old']):
        raise SystemExit(1)


def send(cases, research_list, folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=False)
    limit = stage_a.StageALimit(CAP_USD, folder / 'spend.jsonl')
    write_lock = threading.Lock()
    archives, call_configs = {}, {}
    for arm in THESES_OF_ARM:
        texts = texts_of(arm)
        checksum = hashlib.sha256(json.dumps([texts['system'], texts['closing'], texts['schema']], ensure_ascii=False).encode()).hexdigest()[:16]
        call_configs[arm] = SimpleNamespace(provider='openai', version=f'clean-ladder-probe-{arm}', checksum=checksum)
        for draw in DRAWS:
            (folder / f'{arm}-{draw}').mkdir()
            archives[(arm, draw)] = model.Archive(str(folder / f'{arm}-{draw}' / 'archive.sqlite'))

    def work(job):
        arm, draw, name = job
        texts = texts_of(arm)
        labelled = SimpleNamespace(send=lambda provider, request: limit.send_labelled(f'{arm}|{draw}|{name}', provider, request))
        call_model = model_calls.model_caller(model, archives[(arm, draw)], call_configs[arm], stage_a.SETTING, labelled)
        try:
            sent = call_model(texts['system'], ladder_step.user_text(stage_a.payload_for(cases[name], research_list), texts['closing']), texts['schema'])
        except Exception as error:                       # a transport fault or the cap: stop every worker
            limit.stop(f'{arm} draw {draw} {name}: {type(error).__name__}: {error}')
            return
        row = {'arm': arm, 'draw': draw, 'case': name, 'answer_text': sent['answer_text'], 'error': sent['error'], 'cached': sent['cached'],
               'request_sha256': sent['request_sha256'], 'input_tokens': sent['input_tokens'], 'output_tokens': sent['output_tokens']}
        with write_lock:
            with (folder / 'answers.jsonl').open('a') as handle:
                handle.write(json.dumps(row, ensure_ascii=False) + '\n')

    jobs = [(arm, draw, name) for draw in DRAWS for name in DIRECTION_THESES + EVENT_THESES for arm, names in THESES_OF_ARM.items() if name in names]      # the arms alternate
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(work, jobs))
    known, in_full, _ = stage_a.ledger_total(folder / 'spend.jsonl')
    written = len((folder / 'answers.jsonl').read_text().splitlines()) if (folder / 'answers.jsonl').exists() else 0
    print(f'{written} of {len(jobs)} first answers stored; spent ${known + in_full:.4f} (cap ${CAP_USD:.2f})')
    if limit.stopped or written != len(jobs):
        raise SystemExit(f'STOPPED: {limit.stop_reason}')


def main():
    cases = {case['case']: case for case in json.loads((STEP / 'stage_a' / 'cases.json').read_text())}
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    if sys.argv[1:] == ['check']:
        check(cases, research_list)
    elif len(sys.argv) == 3 and sys.argv[1] == 'send':
        check(cases, research_list)
        send(cases, research_list, sys.argv[2])
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
