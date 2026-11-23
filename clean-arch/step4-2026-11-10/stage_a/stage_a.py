"""Stage A of the clean ladder step (DESIGN.md §8; D400, D401, D408, D409): the step alone, on 44 stored theses, three sends each.

The run folder is created once and refused if it exists. Each of the three passes has its own model archive, so an identical
request is sent again and never answered from a stored answer. One spending limit covers every request; it stops every worker at
the first refusal of the cap or the first error that is not an answer's own, and a stopped run is not started again. What was
spent is on disk as it happens, in `spend.jsonl`.

  python3 clean-arch/step4-2026-11-10/stage_a/stage_a.py --folder <new folder> --cap 3.00            # the 132 sends
  python3 clean-arch/step4-2026-11-10/stage_a/stage_a.py --folder <new folder> --cap 0.20 --passes 1 --cases u1/clean-3,u1/clean-4
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
import sys
import threading
import time
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch' / 'e2e-2026-11-09'), str(STEP / 'ladder')]
import budget  # noqa: E402
import ladder_step  # noqa: E402
import model_calls  # noqa: E402
from hivemind import config, extraction, model, universe  # noqa: E402

COMPANY = 'NVDA'
SETTING = config.Setting(name='clean_ladder', model='gpt-6-luna', prompt_version='clean-ladder-three-outcomes', reasoning_effort='medium',
                         max_output_tokens=16000)        # the judge's setting (cfg.rejudging): model, effort and output cap


class Stopped(Exception):
    """The run was stopped before this send began."""


class StageALimit(budget.Budget):
    """The adapter's spending limit (the same reserve, charge and retries) with two additions inside the locked step it takes
    before every send, a transport retry included: the stop flag is read, and the ledger's reserve line is written. A send
    either took its reserve before the flag was set, and then runs, finishes and is charged, or it never begins."""

    def __init__(self, cap_usd, ledger_path, attempt=None, sleep=time.sleep, shared=None):
        super().__init__(cap_usd, attempt=attempt, sleep=sleep)
        self.ledger_path = Path(ledger_path)
        self.shared = shared            # a run's shared ledger (WIRING-DESIGN.md §B2, D448): reserved and settled inside each attempt
        self.stopped = False
        self.stop_reason = None

    def stop(self, reason):
        """Set the stop flag, once; no send begins after it. With a shared ledger, the run stops too (every Stage A stop is final)."""
        with self.lock:
            if not self.stopped:
                self.stopped, self.stop_reason = True, reason
        if self.shared is not None:
            self.shared.stop(f'the ladder step: {reason}')

    def _write_line(self, line):
        """One whole JSON object a line, flushed and synced; called under the lock, so lines never interleave."""
        with self.ledger_path.open('a') as handle:
            handle.write(json.dumps(line) + '\n')
            handle.flush()
            os.fsync(handle.fileno())

    def send_labelled(self, label, provider, request):
        """Send one request; `label` names the case, the pass and the request (1, or 2 for the resend)."""
        reserve = budget.worst_cost(request)
        for attempt_number in range(budget.ATTEMPTS):
            attempt_id = f'{label}|{attempt_number + 1}'
            with self.lock:
                if self.stopped:
                    raise Stopped(self.stop_reason)
                if self.spent_usd + self.reserved_usd + reserve > self.cap_usd:
                    self.stopped, self.stop_reason = True, 'the spending cap'
                    if self.shared is not None:
                        self.shared.stop('the ladder step: its local spending cap')
                    raise budget.OverBudget(f'spent ${self.spent_usd:.4f}, ${self.reserved_usd:.4f} in flight; '
                                            f'${reserve:.4f} more would pass the ${self.cap_usd:.2f} cap')
                shared_reserve = self.shared.estimate(request) if self.shared is not None else None
                if self.shared is not None and not self.shared.reserve(shared_reserve):
                    self.stopped, self.stop_reason = True, 'the shared ledger'
                    raise budget.OverBudget('the shared ledger refused the reservation')
                self.reserved_usd += reserve
                self._write_line({'attempt': attempt_id, 'reserve': reserve})
            response, failure = None, None
            try:
                response = self.attempt(provider, request)
            except model.TransportError as error:
                failure = error
            finally:
                with self.lock:
                    self.reserved_usd -= reserve
                    charged = budget.cost(request, response) if response is not None else None
                    self.spent_usd += reserve if charged is None else charged
                    self._write_line({'attempt': attempt_id, 'charge': reserve if charged is None else charged, 'known': charged is not None})
                    if self.shared is not None:
                        self.shared.settle(shared_reserve, charged)       # the ledger settles a missing or zero charge at its reservation
            if response is not None:
                return response
            retried = getattr(failure, 'http_status', None) not in budget.NOT_RETRIED and str(failure) not in budget.UNDECODABLE
            if not retried or attempt_number + 1 == budget.ATTEMPTS:
                raise failure
            self.sleep(5 * (attempt_number + 1))


def ledger_total(ledger_path):
    """What the ledger says was spent: over its attempt ids, the charge where there is one and the reserve where there is none.
    Returns (known charges, reserves counted in full, whether a last line that was not whole was dropped)."""
    reserves, charges, dropped = {}, {}, False
    lines = Path(ledger_path).read_text().split('\n') if Path(ledger_path).exists() else []
    for index, line in enumerate(lines):
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            if index != len(lines) - 1:
                raise
            dropped = True
            continue
        if 'reserve' in entry:
            reserves[entry['attempt']] = entry['reserve']
        else:
            charges[entry['attempt']] = (entry['charge'], entry['known'])
    known = sum(charge for charge, is_known in charges.values() if is_known)
    in_full = sum(charge for charge, is_known in charges.values() if not is_known)
    in_full += sum(reserve for attempt, reserve in reserves.items() if attempt not in charges)
    return known, in_full, dropped


def request_texts():
    """The request the build uses: the system text, the closing check and the schema (the request as first sent, D407, with an
    event answered in three outcomes, D409)."""
    return {'system': (STEP / 'ladder' / 'candidate-system.txt').read_text(),
            'closing': (STEP / 'ladder' / 'candidate-closing.txt').read_text().strip(),
            'schema': json.loads((STEP / 'ladder' / 'candidate-schema.json').read_text())}


def payload_for(case, research_list):
    """The payload of one case, with the keys in the order the design gives."""
    themes = [{'id': theme_id, 'name': theme['name']} for theme_id, theme in research_list.themes.items()]
    return {'company': COMPANY, 'fiscal_year_note': research_list.fiscal_note(COMPANY, case['item']['publication_date'], english=True),
            'themes': themes, 'thesis': case['thesis'], 'item': case['item']}


def run(cases, passes, folder, cap_usd, *, research_list, texts, transport=None, workers=8, shared=None):
    """Send every case once in each pass. Returns (outcomes written, the limit). The folder must not exist. `shared` is a run's
    shared ledger (WIRING-DESIGN.md §B2, D448)."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=False)
    limit = StageALimit(cap_usd, folder / 'spend.jsonl', attempt=transport, shared=shared)
    checksum = hashlib.sha256(json.dumps({'system': texts['system'], 'closing': texts['closing'], 'schema': texts['schema'],
                                          'setting': [SETTING.model, SETTING.reasoning_effort, SETTING.max_output_tokens]},
                                         ensure_ascii=False).encode()).hexdigest()[:16]
    call_config = SimpleNamespace(provider='openai', version='clean-ladder-stage-a', checksum=checksum)
    archives, outcome_files = {}, {}
    for pass_number in passes:
        (folder / f'send-{pass_number}').mkdir()
        archives[pass_number] = model.Archive(str(folder / f'send-{pass_number}' / 'archive.sqlite'))
        outcome_files[pass_number] = folder / f'send-{pass_number}' / 'outcomes.jsonl'
    write_lock = threading.Lock()
    written = []

    def work(job):
        case, pass_number = job
        labelled = SimpleNamespace(request_number=0)
        labelled.send = lambda provider, request: limit.send_labelled(f"{case['case']}|{pass_number}|{labelled.request_number}", provider, request)
        call_model = model_calls.model_caller(model, archives[pass_number], call_config, SETTING, labelled)

        def counted_call(system_text, user_text, schema):
            labelled.request_number += 1
            return call_model(system_text, user_text, schema)

        def check(answer):
            return ladder_step.check_answer(answer, thesis=case['thesis'], article=case['item'], company=COMPANY, research_list=research_list,
                                            repair_quote=extraction.repair_quote, normalise=extraction.normalise,
                                            quote_tokens=extraction._quote_tokens,
                                            beyond_next_year=extraction.beyond_next_year, binding_horizon_days=extraction.BINDING_HORIZON_DAYS)
        try:
            outcome = ladder_step.ladder_for_thesis(payload_for(case, research_list), system_text=texts['system'], closing_text=texts['closing'],
                                                    schema=texts['schema'], call_model=counted_call, check=check)
            view = None
            if outcome['status'] == 'ladder':
                view = ladder_step.write_view(outcome['answer']['ladder'], outcome['passage'], thesis=case['thesis'],
                                              article_day=case['item']['publication_date'], company=COMPANY,
                                              research_list=research_list)
            row = {'case': case['case'], 'pass': pass_number, 'status': outcome['status'], 'reason': outcome['reason'],
                   'requests': outcome['requests'], 'answer': outcome['answer'], 'passage': outcome['passage'], 'view': view}
            with write_lock:
                with outcome_files[pass_number].open('a') as handle:
                    handle.write(ladder_step.as_json(row) + '\n')
                    handle.flush()
                    os.fsync(handle.fileno())
                written.append((case['case'], pass_number, outcome['status']))
        except (Stopped, budget.OverBudget):
            return
        except Exception as error:                      # not an answer's own fault, the writing of the outcome included: stop every worker
            limit.stop(f"{case['case']} pass {pass_number}: {type(error).__name__}: {error}")
            return

    jobs = [(case, pass_number) for pass_number in passes for case in cases]
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(work, jobs))                      # the pool waits for every worker before the spend is read
    return written, limit, len(jobs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', required=True)
    parser.add_argument('--cap', type=float, required=True)
    parser.add_argument('--passes', type=int, default=3)
    parser.add_argument('--cases', default='', help='comma-separated case names; all 44 when empty')
    parser.add_argument('--cases-file', default=str(HERE / 'cases.json'), help="the cases to send (default: Stage A's 44)")
    parser.add_argument('--shared-ledger', default=None, help='a run\'s shared ledger (budget_replay.SharedLedger), reserved inside each attempt')
    arguments = parser.parse_args()
    cases = json.loads(Path(arguments.cases_file).read_text())
    if arguments.cases:
        wanted = arguments.cases.split(',')
        cases = [case for case in cases if case['case'] in wanted]
        if len(cases) != len(wanted):
            raise SystemExit(f'a named case is not in {Path(arguments.cases_file).name}')
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    shared = None
    if arguments.shared_ledger:
        import importlib.util
        spec = importlib.util.spec_from_file_location('budget_replay', ROOT / 'clean-arch/e2e-comparison-2026-11-13/budget_replay.py')
        budget_replay = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(budget_replay)
        shared = budget_replay.SharedLedger(arguments.shared_ledger)
        budget_replay.install_stop_gate(shared)            # every actual send reads the run's stop first (council mo R1)
    written, limit, job_count = run(cases, list(range(1, arguments.passes + 1)), arguments.folder, arguments.cap, research_list=research_list,
                                    texts=request_texts(), shared=shared)
    known, in_full, dropped = ledger_total(Path(arguments.folder) / 'spend.jsonl')
    statuses = {}
    for _, _, status in written:
        statuses[status] = statuses.get(status, 0) + 1
    print(f'{len(written)} of {job_count} sends have an outcome: {statuses}')
    print(f'spent ${known + in_full:.4f} (known ${known:.4f}, reserves counted in full ${in_full:.4f}); cap ${arguments.cap:.2f}'
          + ('; a last ledger line that was not whole was dropped' if dropped else ''))
    if limit.stopped or len(written) != job_count:
        raise SystemExit(f'STOPPED: {limit.stop_reason}. The result reads NOT MEASURED; this folder is not started again.')


if __name__ == '__main__':
    main()
