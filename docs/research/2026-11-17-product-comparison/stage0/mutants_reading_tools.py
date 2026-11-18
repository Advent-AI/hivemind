"""In-memory mutants of the comparison's reading tools (score_comparison.py, mapping.py, mark_cards.py; D672, D675). Each mutant is a tool's
source with one change, executed as a fresh module placed in `sys.modules` before its tests are collected, so the tests import it in place
of the real one; nothing is written to disk. The control (no change) must pass; each mutant must fail the test written for its rule.

    python3 mutants_reading_tools.py
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MUTANTS = [
    # (name, module, [(old, new)], test file, [tests])
    ('control: scorer', 'score_comparison', [], 'test_score_comparison.py', []),
    ('control: mapping', 'mapping', [], 'test_mapping.py', []),
    ('control: marking', 'mark_cards', [], 'test_mark_cards.py', []),
    ('control: cards', 'build_cards', [], 'test_build_cards.py', []),
    ('control: eligibility', 'eligibility', [], 'test_eligibility.py', []),
    ('control: d400', 'd400_code_check', [], 'test_d400_code_check.py', []),
    ('too small ignores N', 'score_comparison', [("    if n < 20:", "    if False:")], 'test_score_comparison.py',
     ['test_too_small_when_n_under_20_or_a_draw_under_30_distinct_bets_either_way']),
    ('the margin is 2', 'score_comparison', [("    margin = max(3, math.ceil(0.15 * n))", "    margin = 2")], 'test_score_comparison.py',
     ['test_a_practical_lead_needs_the_margin_twice_b_and_every_guardrail_exercised_and_passing']),
    ('the 10-point bar in floating point', 'score_comparison',
     [("        breach = exercised and (new['share'] - old['share']) > Fraction(1, 10)",
       "        breach = exercised and (float(new['share']) - float(old['share'])) > 0.10")], 'test_score_comparison.py',
     ['test_exactly_ten_points_is_not_a_breach_and_more_is']),
    ('2 of 4 supported controls suffice', 'score_comparison',
     [("    if sum(m == 'supported' for m in controls['supported']) < 3:", "    if sum(m == 'supported' for m in controls['supported']) < 2:")],
     'test_score_comparison.py', ['test_fewer_than_three_supported_controls_or_two_repeats_is_invalid']),
    ('1 of 3 repeats suffices', 'score_comparison',
     [("    if sum(bool(x) for x in controls['repeats_same']) < 2:", "    if sum(bool(x) for x in controls['repeats_same']) < 1:")],
     'test_score_comparison.py', ['test_fewer_than_three_supported_controls_or_two_repeats_is_invalid']),
    ('five draws are scored', 'score_comparison', [("        if sorted(DRAWS) != draws:", "        if False:")], 'test_score_comparison.py',
     ['test_readings_without_all_six_draws_are_refused']),
    ('covering cards enter the shares', 'score_comparison',
     [("                if not card['guardrail'] or covering:", "                if not card['guardrail']:")], 'test_score_comparison.py',
     ['test_a_sampled_card_that_covers_a_matter_is_not_in_the_shares']),
    ('two different rejections make the reading invalid', 'score_comparison',
     [("        return m in REJECTED or (isinstance(m, dict) and 'split' in m and all(x in REJECTED for x in m['split']))",
       "        return m in REJECTED")], 'test_score_comparison.py', ['test_a_plant_both_readers_rejected_with_different_labels_is_rejected']),
    ('the reader names the duplicate', 'mapping',
     [("    duplicates = {max(str(r['duplicate']), str(r['of']), key=order.__getitem__) for r in rows if r.get('duplicate') is not None}",
       "    duplicates = {str(r['duplicate']) for r in rows if r.get('duplicate') is not None}")], 'test_mapping.py',
     ['test_a_pair_named_in_either_order_has_the_later_opened_question_as_its_duplicate']),
    ('a missing third mark is a split', 'mapping', [("                    if missing:", "                    if False:"),
                                                    ("                    thirds = [json.loads(p.read_text())['covers'] for p in paths]",
                                                     "                    thirds = [json.loads(p.read_text())['covers'] for p in paths if p.exists()]")], 'test_mapping.py',
     ['test_a_disagreement_without_both_third_marks_is_refused']),
    ('unknown ids pass', 'mapping', [("        if unknown:", "        if False:")], 'test_mapping.py',
     ['test_an_answer_naming_an_id_outside_the_library_or_a_matter_twice_is_void']),
    ('the judge store is always the first attempt', 'mapping',
     [("        folder = root / judge['folder'] / inner['attempts'][-1]['folder']", "        folder = root / judge['folder'] / f'draw-{draw}'")],
     'test_mapping.py', ['test_the_judge_store_is_the_attempt_its_record_completed_and_an_incomplete_draw_is_refused']),
    ('an incomplete draw is read', 'mapping', [("    if record.get('state') != 'complete':\n        raise SystemExit(f'refused: {draw} is",
                                                "    if False:\n        raise SystemExit(f'refused: {draw} is")],
     'test_mapping.py', ['test_the_judge_store_is_the_attempt_its_record_completed_and_an_incomplete_draw_is_refused']),
    ('opened with no id is accepted', 'mapping', [("        if r['status'] in ('opened', 'narrower') and not r.get('ids'):", "        if False:")],
     'test_mapping.py', ['test_an_answer_naming_an_id_outside_the_library_or_a_matter_twice_is_void']),
    ('narrower without a main-outcome judgement is accepted', 'mapping',
     [("        if r['status'] == 'narrower' and not isinstance(r.get('main_outcome'), bool):", "        if False:")],
     'test_mapping.py', ['test_an_answer_naming_an_id_outside_the_library_or_a_matter_twice_is_void']),
    ('export ignores eligibility', 'mapping', [("    if not eligibility.get('eligible') and not diagnostic:", "    if False:")], 'test_mapping.py',
     ['test_export_refuses_draws_that_are_not_eligible']),
    ('the launch window is ignored', 'eligibility', [("    if launches and max(launches) - min(launches) > LAUNCH_WINDOW:", "    if False:")],
     'test_eligibility.py', ['test_a_launch_over_an_hour_apart_or_a_call_after_72_hours_is_not_eligible']),
    ('the send window is 30 days', 'eligibility', [("SEND_WINDOW = datetime.timedelta(hours=72)", "SEND_WINDOW = datetime.timedelta(hours=720)")],
     'test_eligibility.py', ['test_a_launch_over_an_hour_apart_or_a_call_after_72_hours_is_not_eligible']),
    ('a split cover is out of the shares in both countings', 'score_comparison',
     [("                covering = card['covering'] if card['covering'] != 'split' else fav      # covers > does not cover",
       "                covering = bool(card['covering'])")], 'test_score_comparison.py', ['test_a_split_cover_on_a_sampled_card_resolves_per_counting']),
    ('the guardrail sample draws from the neutral ids', 'mark_cards',
     [("    ids = sorted(neutral)\n    return", "    neutral = {v: v for v in neutral.values()}\n    ids = sorted(neutral)\n    return")],
     'test_mark_cards.py', ['test_the_guardrail_sample_draws_from_the_system_ids_sorted_as_strings']),
    ('a settled field follows the last round', 'mark_cards',
     [("    out, a, b = settled_marks(folder, cid, 2)\n    for field in ('worth', 'answer'):",
       "    _, a, b = settled_marks(folder, cid, 2)\n    out = {f: a.get(f) for f in ('worth', 'answer') if a.get(f) == b.get(f)}\n    for field in ('worth', 'answer'):")],
     'test_mark_cards.py', ['test_a_field_agreed_in_a_round_stays_settled']),
    ('a plant enters without confirmation', 'mark_cards', [("            if ok:\n                admitted.append(c)", "            if True:\n                admitted.append(c)")],
     'test_mark_cards.py', ['test_the_deck_admits_a_plant_only_when_a_reader_confirms_it_is_not_supported']),
    ('the deck overwrites its key', 'mark_cards', [("    if KEY.exists():\n        raise SystemExit(f'refused: {KEY} exists; a deck never overwrites a key')", "    pass")],
     'test_mark_cards.py', ['test_the_deck_holds_six_plants_four_supported_controls_three_repeats_and_never_overwrites_its_key']),
    ('the string null is kept', 'mark_cards', [("    return dict(row, answer=None) if isinstance(row, dict) and row.get('answer') == 'null' else row", "    return row")],
     'test_mark_cards.py', ['test_an_empty_answer_written_as_the_string_null_is_null']),
    ('a draw with other options is eligible', 'eligibility', [("        if record.get('identity') != expected_identity(run_root, draw):", "        if False:")],
     'test_eligibility.py', ['test_a_draw_registered_with_other_options_or_a_late_failed_attempt_is_not_eligible']),
    ('failed attempts are not counted', 'eligibility', [("        if attempt and (latest is None or attempt > latest):", "        if False:")],
     'test_eligibility.py', ['test_a_draw_registered_with_other_options_or_a_late_failed_attempt_is_not_eligible']),
    ('the matter rows are not compared', 'score_comparison', [("    if readings['matters'] != frozen or ", "    if ")],
     'test_score_comparison.py', ['test_readings_not_made_from_their_named_inputs_are_refused']),
    ('the mapping file is not compared', 'score_comparison',
     [("    if mapped['mapping'] != readings['mapping'] or mapped['distinct'] != readings['distinct']:", "    if False:")],
     'test_score_comparison.py', ['test_readings_not_made_from_their_named_inputs_are_refused']),
    ('splits reported per card only', 'score_comparison', [("                    if q['covers'] == 'split':", "                    if False:")],
     'test_score_comparison.py', ['test_every_split_matter_question_pair_is_reported_with_its_resolution']),
    ('the card drops the hidden-items line', 'build_cards', [("        if ctx.get('hidden'):", "        if False:")],
     'test_build_cards.py', ['test_the_card_carries_what_the_request_gave_besides_its_evidence']),
    ('the card shows theme rungs by label', 'build_cards',
     [("'answer': rungs.get(int(m.group(4))),", "'answer': 'Middle',")],
     'test_build_cards.py', ['test_the_card_carries_what_the_request_gave_besides_its_evidence']),
    ('the card hides its own place', 'build_cards', [("('   <- this question' if e['question_id'] == entry['question_id'] else '')", "''")],
     'test_build_cards.py', ['test_the_card_carries_what_the_request_gave_besides_its_evidence']),
    ('card marks are taken from the readings', 'score_comparison', [("    if keyed != held:", "    if set(keyed) != set(held):")],
     'test_score_comparison.py', ['test_card_marks_that_differ_from_the_deck_key_are_refused']),
    ('an unreconciled log is trusted', 'eligibility', [("        if unreconciled:", "        if False:")],
     'test_eligibility.py', ['test_an_attempt_log_that_does_not_reconcile_with_its_ledger_leaves_the_timing_unestablished']),
    ('a cut material list passes', 'build_cards', [("    if len(chunks) - 1 != stated:", "    if False:")],
     'test_build_cards.py', ['test_a_request_whose_items_the_card_cannot_all_read_is_refused']),
    ('theme rungs are not listed', 'build_cards', [("                lines.append('  Its possible answers: '", "                (lambda *a: None)('  Its possible answers: '")],
     'test_build_cards.py', ['test_the_card_carries_what_the_request_gave_besides_its_evidence']),
    ('the support floor credits a split', 'score_comparison',
     [("                supported += card['answer'] == 'supported'", "                supported += resolve(card['answer'], 'answer', fav) == 'supported'")],
     'test_score_comparison.py', ['test_the_support_floor_gives_an_unresolved_answer_no_credit_in_either_counting']),
    ('a diagnostic export writes the release key', 'mapping', [("    key_file = KEY_FOLDER / ('mapping-key-diagnostic.json' if diagnostic else 'mapping-key.json')",
                                                              "    key_file = KEY_FOLDER / 'mapping-key.json'")],
     'test_mapping.py', ['test_a_diagnostic_export_takes_only_finished_draws_under_its_own_key']),
    ('floors drop covering cards', 'score_comparison', [("            if not card['guardrail']:                       # every random-sample card",
                                                        "            if not card['guardrail'] or card['covering']:                       # every random-sample card")],
     'test_score_comparison.py', ['test_the_floors_count_every_random_sample_card_covering_or_not']),
    ('not measured outranks a miss', 'd400_code_check',
     [("    status = ('failed' if 'missed' in states else 'not measured' if accounting.NOT_MEASURED in states else 'passed')",
       "    status = ('not measured' if accounting.NOT_MEASURED in states else 'failed' if 'missed' in states else 'passed')")],
     'test_d400_code_check.py', ['test_a_missed_part_blocks_release_ahead_of_a_part_not_measured']),
    ('the early verdicts compute the printed items strictly', 'score_comparison',
     [("        try:\n            shown[name] = compute(readings, per_counting)\n        except Exception as error:\n            flags.append(f'{name}: {type(error).__name__}: {error}')",
       "        shown[name] = compute(readings, per_counting)")],
     'test_score_comparison.py', ['test_a_diagnostic_that_cannot_be_computed_never_stops_an_invalid_or_too_small_verdict']),
    ('the size check runs when invalid', 'score_comparison', [("    if not invalid:                                            # the size check runs only when the controls hold",
                                                             "    if True:")],
     'test_score_comparison.py', ['test_a_diagnostic_that_cannot_be_computed_never_stops_an_invalid_or_too_small_verdict']),
    ('a debate reads its own round', 'mark_cards',
     [("        settled, a, b = settled_marks(folder, p.stem, round_number - 1)", "        settled, a, b = settled_marks(folder, p.stem, round_number)"),
      ("    for n in range(upto, -1, -1):", "    for n in range(2, -1, -1):")], 'test_mark_cards.py', ['test_a_debate_round_reads_only_earlier_rounds']),
    ('readings without the debate', 'mark_cards', [("    for n in (0, 1, 2):\n        if not (folder / f'round-{n}.done').exists():",
                                                    "    for n in ():\n        if not (folder / f'round-{n}.done').exists():")],
     'test_mark_cards.py', ['test_readings_refuse_a_deck_whose_debate_rounds_are_not_complete']),
    ('a one-rung ladder is planted', 'mark_cards', [("    if moved is None or moved == entry['answer']:\n        return None",
                                                     "    if moved is None:\n        moved = entry['answer']"),
                                                    ("    return planted if planted != card_text else None", "    return planted")],
     'test_mark_cards.py', ['test_a_card_without_a_different_adjacent_rung_is_not_planted']),
]

RUNNER = r'''
import json, sys, types
from pathlib import Path
here, module, changes, test_file, tests = sys.argv[1], sys.argv[2], json.loads(sys.argv[3]), sys.argv[4], json.loads(sys.argv[5])
sys.path[:0] = [here, here + '/census']
path = Path(here) / f'{module}.py'
source = path.read_text()
for old, new in changes:
    if source.count(old) != 1:
        print('MUTANT DID NOT APPLY:', old[:80])
        sys.exit(3)
    source = source.replace(old, new)
mutant = types.ModuleType(module)
mutant.__file__ = str(path)
sys.modules[module] = mutant
exec(compile(source, str(path), 'exec'), mutant.__dict__)
import pytest
args = ['-q', '-p', 'no:cacheprovider', str(Path(here) / test_file)] + (['-k', ' or '.join(tests)] if tests else [])
sys.exit(pytest.main(args))
'''


def main():
    lines, wrong = [], 0
    for name, module, changes, test_file, tests in MUTANTS:
        done = subprocess.run([sys.executable, '-c', RUNNER, str(HERE), module, json.dumps(changes), test_file, json.dumps(tests)],
                              capture_output=True, text=True, env={'PYTHONDONTWRITEBYTECODE': '1', 'PATH': '/usr/bin:/bin'})
        expected = 0 if name.startswith('control') else 1
        tail = [l for l in done.stdout.splitlines() if l.startswith('E ') or l.startswith('MUTANT DID NOT APPLY') or ' passed' in l or ' failed' in l]
        ok = done.returncode == expected
        wrong += not ok
        lines.append(f"== {name}: exit {done.returncode}, {'as predicted' if ok else 'NOT AS PREDICTED'} | " + ' | '.join(tail[:2] + tail[-1:]))
    print('\n'.join(lines))
    print('all as predicted' if not wrong else f'{wrong} NOT AS PREDICTED')
    return wrong


if __name__ == '__main__':
    sys.exit(main())
