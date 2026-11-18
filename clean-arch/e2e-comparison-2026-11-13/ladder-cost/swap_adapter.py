"""D467's ladder-cost arm: the seeded Stage 2 adapter (`clean-arch/e2e-2026-11-09/adapter.py`) unchanged, except that the named seed views
take another ladder (question, due day, year and rungs) when the seeds are written. Everything else — the 22 seed views from the
first day, their keys and dependencies, every fact, link, revision and judging day — is the control's, by construction, so the two arms
differ only in those ladders. A swap of a view to its own seed ladder must rebuild the control exactly (`proof_swap.py`).

  replay_swapped(trace, step2, output, transport=..., swaps={view_id: view}, q23=None)
"""
import contextlib
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/e2e-2026-11-09')]
import adapter  # noqa: E402

ORIGINAL_SEEDS = adapter.SEEDS
SWAPPED_FIELDS = ('question', 'due_day', 'year', 'rungs')


@contextlib.contextmanager
def swapping(swaps):
    """The views table is append-only, so the swap is made where the seeds are written: a temporary copy of the seed file, under the same
    file name (the views' source label stays the same), with the named questions' ladders replaced; the frozen seed file is not touched."""
    seeds = json.loads(ORIGINAL_SEEDS.read_text(encoding='utf-8'))
    known = {q['view_id'] for q in seeds['questions']}
    unknown = set(swaps) - known
    if unknown:
        raise SystemExit(f'not seed views: {sorted(unknown)}')
    for question in seeds['questions']:
        if question['view_id'] in swaps:
            question.update({field: swaps[question['view_id']][field] for field in SWAPPED_FIELDS})
    with tempfile.TemporaryDirectory() as folder:
        copy = Path(folder) / ORIGINAL_SEEDS.name
        copy.write_text(json.dumps(seeds, ensure_ascii=False, indent=1), encoding='utf-8')
        adapter.SEEDS = copy
        try:
            yield
        finally:
            adapter.SEEDS = ORIGINAL_SEEDS


def replay_swapped(trace, step2, output, *, transport, swaps, q23=None, cap_usd=10.0):
    with swapping(swaps):
        return adapter.replay(trace, step2, output, transport=transport, cap_usd=cap_usd, q23=q23)
