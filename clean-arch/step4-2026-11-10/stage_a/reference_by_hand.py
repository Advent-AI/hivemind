"""The reference as D411 decides it, shown on stored answers at no cost: the second Stage A's own answers for the theses whose
reference both readers failed, with only the reference rewritten by hand into the new shape (its kind; a range by its two
ends), put through the schema, the checks and the view writer. It shows what the judge would be told before and after, and
that the request asks for nothing a check refuses. Nothing here is the model's answer to the changed request.

  python3 clean-arch/step4-2026-11-10/stage_a/reference_by_hand.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(STEP / 'ladder')]
import ladder_step  # noqa: E402
from hivemind import extraction, model, universe  # noqa: E402

RUN = ROOT / 'poc' / 'data' / 'clean-ladder-stage-a-2026-11-10' / 'run-2'
BY_HAND = {      # send: (what was wrong as both readers marked it, the reference's kind, value and value_to under D411)
    ('u1/clean-7', 1): ('the $119 billion already reported was carried as what the market expects', 'last_reported', 119000000000, None),
    ('u3/clean-8', 1): ('the same', 'last_reported', 119000000000, None),
    ('acc/clean-8', 1): ('"approximately 50%-60%" had no place in a field of one number, so the judge was told there was no reference figure', 'expected', 50, 60),
    ('u1/clean-4', 1): ('nothing: a control, a stated projection of $1 trillion', 'expected', 1000000000000, None),
    # A counter-case the checks accept and that is wrong: "guarantees of up to $105 billion" is a ceiling for one project, not the
    # amount last reported for the total the thesis asks. Code reads the words, the kind's form and the middle range, never the
    # meaning; mark XR owns it ("the same thing measured the same way: not a part of it, a ceiling on it or another quantity").
    ('acc/clean-3', 1): ('WRONG ON PURPOSE: a ceiling for one project entered as the amount last reported for the total; the checks cannot see it', 'last_reported', 105000000000, None),
}


def main():
    cases = {case['case']: case for case in json.loads((HERE / 'cases.json').read_text())}
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    schema = json.loads((STEP / 'ladder' / 'candidate-schema.json').read_text())
    outcomes = {(row['case'], row['pass']): row for pass_folder in sorted(RUN.glob('send-*'))
                for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines() for row in [json.loads(line)]}
    refused = 0
    for send, (fault, kind, value, value_to) in BY_HAND.items():
        stored, case = outcomes[send], cases[send[0]]
        answer = json.loads(json.dumps(stored['answer'], default=str))
        answer['ladder']['reference'] = {'words': stored['passage'], 'kind': kind, 'value': value, 'value_to': value_to}
        for one_range in answer['ladder']['figure']['ranges']:
            one_range['lo'] = None if one_range['lo'] is None else float(one_range['lo'])
            one_range['hi'] = None if one_range['hi'] is None else float(one_range['hi'])
        schema_problems = model.check_schema(answer, schema)
        exact_answer = ladder_step.parse_exactly(json.dumps(answer))
        reasons, passage = ladder_step.check_answer(exact_answer, thesis=case['thesis'], article=case['item'], company='NVDA', research_list=research_list,
                                                    repair_quote=extraction.repair_quote, normalise=extraction.normalise, quote_tokens=extraction._quote_tokens,
                                                    beyond_next_year=extraction.beyond_next_year, binding_horizon_days=extraction.BINDING_HORIZON_DAYS)
        refused += bool(schema_problems or reasons)
        print('=' * 110)
        print(f'{send[0]} pass {send[1]} | as both readers marked it: {fault}')
        print(f"  schema: {schema_problems or 'fits'} | checks: {reasons or 'accepted'}")
        print('  the middle rung as the judge was shown it:', [rung['condition'] for rung in stored['view']['rungs'] if '(' in rung['condition']][0][:230])
        if not (schema_problems or reasons):
            view = ladder_step.write_view(exact_answer['ladder'], passage, thesis=case['thesis'], article_day=case['item']['publication_date'],
                                          company='NVDA', research_list=research_list)
            print('  the middle rung under D411             :', [rung['condition'] for rung in view['rungs'] if '(' in rung['condition']][0][:230])
            print('  reference status:', view['reference_status'])
    print(f'{len(BY_HAND)} answers; refused by the schema or a check: {refused}')
    if refused:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
