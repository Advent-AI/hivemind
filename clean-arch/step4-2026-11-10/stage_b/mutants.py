"""Mutants of stage_b/ladder_adapter.py and run_stage_b.py, each run in a mirrored scratch tree (real data and frozen code linked,
the two modules copied, one mutated). The unmutated control must pass; every mutant must fail the test written for that behaviour
with an assertion (or the expected exception check), not by a crash elsewhere.

  python3 clean-arch/step4-2026-11-10/stage_b/mutants.py <scratch folder>
"""
import os, re, shutil, subprocess, sys
from pathlib import Path
REPO = Path('/Users/lchingen/hivemind')
STAGE_B = REPO / 'clean-arch/step4-2026-11-10/stage_b'
TREE = Path(sys.argv[1]).resolve() / 'tree'      # a scratch folder given as the one argument, never inside the repository
OUTPUTS = Path(sys.argv[1]).resolve() / 'outputs'   # each mutant's whole pytest output, kept
OUTPUTS.mkdir(parents=True, exist_ok=True)
A, L = 'ladder_adapter.py', 'run_stage_b.py'
MUTANTS = {   # name: (file, [(old, new)], tests that must fail)
    'control': (A, [], []),
    'links to a thesis with no ladder go to the base writer': (A, [("        if evidence_id is not None and thesis_id in self.unjudged:\n            self.counts['links to an unjudged thesis'] += 1\n            return\n", "")],
        ['test_links_reach_a_laddered_view_and_the_judge_and_links_to_a_thesis_with_no_ladder_are_counted_not_written']),
    'the due-day guard does nothing': (A, [("    def due_day_guard(self, day):\n", "    def due_day_guard(self, day):\n        return\n")],
        ['test_an_open_view_due_inside_the_window_stops_the_replay', 'test_a_view_opened_on_its_due_day_is_stopped_before_it_is_judged']),
    'the guard after the day\'s writes is removed': (A, [("        runner.due_day_guard(day)                    # again", "        pass  # runner.due_day_guard(day)                    # again")],
        ['test_a_view_opened_on_its_due_day_is_stopped_before_it_is_judged']),
    'a thesis with no ladder still names a view in its row': (A, [("store.insert(self.conn, 'clean_ladders', thesis_id=thesis_id, view_id=view_id,", "store.insert(self.conn, 'clean_ladders', thesis_id=thesis_id, view_id=f'v{number}',")],
        ['test_every_opened_thesis_has_one_ladder_row_and_a_thesis_with_no_ladder_has_no_view']),
    'the ledger records no charge': (A, [("                    self._write({'attempt': attempt_id, 'charge': reserve if charged is None else charged, 'known': charged is not None})\n", "")],
        ['test_the_ledger_holds_every_attempt_and_sums_to_the_spend']),
    'a limit starts from nothing': (A, [("        self.spent_usd = ledger_total(self.ledger_path)", "        self.spent_usd = 0.0")],
        ['test_a_limit_starts_from_its_ledger_so_a_later_process_cannot_pass_the_cap']),
    'the identity check is removed': (A, [("        if differing:\n            raise SystemExit(f'{name}: the stored case and the trace describe different theses ({differing})')\n", "")],
        ['test_a_stored_case_that_describes_another_thesis_is_refused']),
    'a view takes the thesis outcome as its question': (A, [("looks_at=view['looks_at'], question=view['question']", "looks_at=view['looks_at'], question=view['looks_at']")],
        ['test_every_laddered_thesis_is_a_view_with_its_stored_ladder_and_there_is_no_other_view']),
    'the cap is not checked': (A, [("                if self.spent_usd + self.reserved_usd + reserve > self.cap_usd:\n", "                if False:\n")],
        ['test_the_cap_stops_the_replay', 'test_the_launcher_stops_every_draw_at_the_cap']),
    'a row names the answers file instead of the configuration': (A, [("    source = ladder_configuration()", "    source = 'answers file'")],
        ['test_every_ladder_row_names_the_configuration_that_wrote_it']),
    'the launcher resends every stop': (L, [("    return isinstance(error, (judging.JudgementRefused, model.SchemaError, model.TransportError))", "    return True")],
        ['test_the_launcher_does_not_resend_a_stop_that_code_decides']),
    'the launcher resends nothing': (L, [("    return isinstance(error, (judging.JudgementRefused, model.SchemaError, model.TransportError))", "    return False")],
        ['test_the_launcher_resends_a_draw_stopped_by_a_refused_judgement_once_then_marks_it_incomplete']),
}
def build():
    shutil.rmtree(TREE, ignore_errors=True)
    (TREE / 'clean-arch/step4-2026-11-10/stage_b').mkdir(parents=True)
    for link in ('poc', 'src'):
        os.symlink(REPO / link, TREE / link)
    for link in ('e2e-2026-11-09', 'step2', 'step1', 'unseeded-2026-11-10'):
        os.symlink(REPO / 'clean-arch' / link, TREE / 'clean-arch' / link)
    for link in ('stage_a', 'ladder'):
        os.symlink(REPO / 'clean-arch/step4-2026-11-10' / link, TREE / 'clean-arch/step4-2026-11-10' / link)
    for name in ('test_ladder_adapter.py', A, L):
        shutil.copy(STAGE_B / name, TREE / 'clean-arch/step4-2026-11-10/stage_b' / name)
bad = 0
for name, (target, edits, must_fail) in MUTANTS.items():
    build()
    path = TREE / 'clean-arch/step4-2026-11-10/stage_b' / target
    text = path.read_text()
    applied = True
    for old, new in edits:
        if text.count(old) != 1:
            print(f'BAD  {name}: mutation not applied'); bad += 1; applied = False; break
        text = text.replace(old, new)
    if not applied:
        continue
    path.write_text(text)
    run = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', '-rf', '--tb=short', 'test_ladder_adapter.py'],
                         cwd=path.parent, capture_output=True, text=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    failed = set(re.findall(r'^FAILED test_ladder_adapter.py::(\w+)', run.stdout, re.M))
    errored = 'error' in run.stdout.strip().splitlines()[-1] if run.stdout.strip() else True
    (OUTPUTS / f"{re.sub(r'[^a-z0-9]+', '-', name.lower())}.txt").write_text(run.stdout + run.stderr)
    sections = dict(re.findall(r'^_+ (test_\w+) _+\n(.*?)(?=\n_+ test_\w+ _+\n|\n={5,})', run.stdout, re.S | re.M))
    by_assertion = all(re.search(r'AssertionError|^E\s+assert |DID NOT RAISE|Failed: DID NOT RAISE', sections.get(test, ''), re.M) for test in must_fail)
    good = (not failed and run.returncode == 0) if name == 'control' else (set(must_fail) <= failed and not errored and by_assertion)
    bad += not good
    print(f"{'ok  ' if good else 'BAD '} {name}: failed {sorted(failed) or 'none'}" + (' (errors)' if errored else '')
          + ('' if name == 'control' or by_assertion else ' (a named test did not fail by an assertion)'))
print('all as expected' if bad == 0 else f'{bad} not as expected')
