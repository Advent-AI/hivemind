"""A page-readable store of the fortnight ($0; not-judged-display/DESIGN.md, "A store the page can read"): the stored draw of D563
replayed through the accepted writer (D564, D567) into a new folder, every judge request answered from the draw's stored archive by
its identity. Exits 1 unless every request is answered, their number equals the stored draw's, every judgement and every ladder row
equals the stored draw's, and the store holds processing records and completed days.

  python3 page_store.py <new output folder>
"""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'clean-arch/step4-2026-11-10/stage_b'), str(ROOT / 'clean-arch/e2e-2026-11-09'), str(ROOT / 'src')]
import ladder_adapter  # noqa: E402
import stored_judgements  # noqa: E402
from hivemind import model  # noqa: E402

DRAW = ROOT / 'poc/data/clean-carried-run-2026-11-16/c1'


def main(output):
    output = Path(output)
    stored_dir = DRAW / 'judge/draw-c1'
    stored_judgements.refuse_split_store(sqlite3.connect(f"file:{stored_dir / 'views.sqlite'}?mode=ro", uri=True), 'page_store')   # before any read
    stored = sqlite3.connect(f"file:{stored_dir / 'archive.sqlite'}?mode=ro", uri=True)
    answers = {sha: json.loads(response) for sha, response in stored.execute('select request_sha256, response_json from model_calls where response_json is not null')}
    stored_calls = stored.execute("select count(*) from model_calls where purpose='judge' and answer_json is not null").fetchone()[0]
    calls = []

    def from_the_archive(provider, request):
        sha = model.request_identity(request)[1]
        calls.append(sha)
        if sha not in answers:
            raise SystemExit(f'a judge request with no stored answer: {sha[:16]}')
        return answers[sha]

    inputs = {'trace': str(DRAW / 'step1/trace.sqlite'), 'step2': str(DRAW / 'step2'), 'ladders': str(DRAW / 'ladder/send-1/outcomes.jsonl'),
              'ladder_archive': str(DRAW / 'ladder/send-1/archive.sqlite'), 'cases': str(DRAW / 'cases/cases.json'), 'output_root': str(output.parent)}
    ladder_adapter.replay('c1', output, transport=from_the_archive, cap_usd=5.0, inputs=inputs)
    new = sqlite3.connect(output / 'views.sqlite')
    old = sqlite3.connect(f"file:{stored_dir / 'views.sqlite'}?mode=ro", uri=True)
    judged = 'select view_id, seq, input_id, rung, reasons, cited_evidence_json from judgements order by judgement_id'
    ladders = 'select thesis_id, view_id, status, reason, checked_answer from clean_ladders order by thesis_id'
    checks = {
        f'every judge request answered from the archive, as many as the stored draw made ({len(calls)} of {stored_calls})': len(calls) == stored_calls,
        'every judgement equals the stored draw\'s': new.execute(judged).fetchall() == old.execute(judged).fetchall(),
        'every ladder row equals the stored draw\'s': new.execute(ladders).fetchall() == old.execute(ladders).fetchall(),
        'processing records present': new.execute('select count(*) from processing_steps').fetchone()[0] > 0,
        'completed days present': new.execute('select count(*) from days_completed').fetchone()[0] > 0,
    }
    for name, holds in checks.items():
        print(('ok   ' if holds else 'FAIL ') + name)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    main(sys.argv[1])
