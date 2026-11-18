"""Clean Steps 2–3 (`clean-arch/step2/run_forward.py`, frozen by D427) with every paid call held to a run's shared ledger
(WIRING-DESIGN.md §B, D448). No frozen file is edited: before `run_forward.main` runs, this module replaces two module attributes it
calls at call time, each with a wrapper that reserves on the ledger, then calls the captured original (never itself), then settles.

- `hivemind.search.openai_embeddings` (one batch a call; the helper tries up to three times inside): reserves three attempts of
  (2 × the request's JSON bytes + 4,096) tokens at `search.EMBEDDING_PRICE_PER_M`; settles at three times the reported total tokens,
  or at the reservation when the count is zero or missing.
- `hivemind.jev.transport` (Jev tries up to three times inside): as `budget_replay.BudgetTransport._jev`, but calling the captured
  original.

A refused reservation records the ledger's stop and raises `model.TransportError`; `run_forward` then ends the draw.

  python3 budget_step2.py --shared-ledger L <trace> <output folder>
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import jev, model, search  # noqa: E402

EMBEDDING_ATTEMPTS = 3                          # search.openai_embeddings' own loop


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


budget_replay = load('budget_replay', HERE / 'budget_replay.py')


def embedding_estimate(texts, embedding_model=search.EMBEDDING_MODEL):
    body = json.dumps({'model': embedding_model, 'input': texts}).encode('utf-8')
    return EMBEDDING_ATTEMPTS * (2 * len(body) + 4096) * search.EMBEDDING_PRICE_PER_M / 1e6


def install(ledger):
    """Replace the two module attributes with budgeted wrappers; returns a function that restores the originals."""
    original_embeddings, original_jev = search.openai_embeddings, jev.transport

    def budgeted_embeddings(texts, embedding_model=search.EMBEDDING_MODEL, timeout=120):
        estimate = embedding_estimate(texts, embedding_model)
        if not ledger.reserve(estimate):
            raise model.TransportError('the shared budget ceiling would be passed: embeddings not sent')
        try:
            vectors, tokens = original_embeddings(texts, embedding_model=embedding_model, timeout=timeout)
        except BaseException:
            ledger.settle(estimate, estimate, kind='embeddings')
            raise
        whole = isinstance(tokens, int) and not isinstance(tokens, bool) and tokens > 0
        ledger.settle(estimate, EMBEDDING_ATTEMPTS * tokens * search.EMBEDDING_PRICE_PER_M / 1e6 if whole else estimate, kind='embeddings',
                      tokens=tokens if whole else None)
        return vectors, tokens

    def budgeted_jev(request, timeout=60):
        estimate = budget_replay.jev_estimate(request)
        if not ledger.reserve(estimate):
            raise model.TransportError('the shared budget ceiling would be passed: Jev not sent')
        try:
            response = original_jev(request, timeout=timeout)
        except BaseException:
            ledger.settle(estimate, estimate, kind='jev')
            raise
        usage = response.get('usage') if isinstance(response, dict) else None
        tokens = usage.get('input_tokens') if isinstance(usage, dict) else None
        whole = isinstance(tokens, int) and not isinstance(tokens, bool) and tokens > 0
        ledger.settle(estimate, jev.ATTEMPTS * tokens * model.PRICES[request['model']][0] / 1e6 if whole else estimate, kind='jev',
                      tokens=tokens if whole else None)
        return response

    search.openai_embeddings, jev.transport = budgeted_embeddings, budgeted_jev

    def restore():
        search.openai_embeddings, jev.transport = original_embeddings, original_jev
    return restore


def main(argv):
    if len(argv) < 2 or argv[0] != '--shared-ledger':
        raise SystemExit(__doc__)
    ledger = budget_replay.SharedLedger(argv[1])
    if ledger.read().get('stopped'):
        raise SystemExit(f"the shared ledger is stopped ({ledger.read().get('stop_reason')}): nothing is sent")
    run_forward = load('clean_step2_run_forward', ROOT / 'clean-arch/step2/run_forward.py')
    restore = install(ledger)
    remove_gate = budget_replay.install_stop_gate(ledger)  # a helper's internal retry reads the run's stop too (council mo R1)
    saved_argv = sys.argv
    sys.argv = ['run_forward.py', *argv[2:]]
    try:
        return run_forward.main()
    finally:
        sys.argv = saved_argv
        remove_gate()
        restore()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
