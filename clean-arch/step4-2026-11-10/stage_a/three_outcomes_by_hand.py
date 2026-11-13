"""The three-outcome answer for an event (D409), written by hand for the stored theses whose answers had a gap or an overlap in
the first Stage A, put through the schema, the code checks and the view writer at no cost (AGENTS §6: "Write one answer that
follows the prompt and run every code check on it"). For each thesis it then lists the outcomes that fell between rungs in the
first run, with the rung each lands in now: the placement is the author's reading and is what the council is asked to
challenge. Nothing here is offered as the model's answer, and the script does not compute a rung from facts: it prints the
rungs code writes and the author's placements beside them.

  python3 clean-arch/step4-2026-11-10/stage_a/three_outcomes_by_hand.py
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

COMPANY = 'NVDA'


def answer(question, target, happened, ruled_out, due_day, basis, not_judged):
    return {'no_ladder': None, 'ladder': {'question': question, 'object': target, 'not_judged': [{'part': part, 'why': why} for part, why in not_judged],
                                          'event': {'happened': happened, 'ruled_out': ruled_out}, 'figure': None, 'reference': None,
                                          'due_day': due_day, 'due_day_basis': basis}}


BY_HAND = {
    'acc/clean-2': (answer(
        "Will Nvidia complete its announced acquisition of Hugging Face by 2028-03-05, as reported in Nvidia's Form 8-K, Form 10-Q or Form 10-K?", 'NVDA',
        'Nvidia has completed the acquisition of Hugging Face on or before 2028-03-05.',
        "A termination of the acquisition announced by Nvidia or Hugging Face after 2026-09-05, or a regulator's block of it after that day, stands on 2028-03-05.",
        '2028-03-05', 'stated',
        [('whether the deal closes on restructured terms or at another price', 'a difference inside the completion of the acquisition')]),
        [('completed at a revised price (the first run split completion by its terms, with no line between them)', 1),
         ('terminated by announcement, or blocked', 2),
         ('the agreement expires and both parties confirm they will not go on (a way the condition does not name: code\'s sentence takes it)', 2),
         ('not completed, and nothing has ended it', 3)]),
    'u1/clean-12': (answer(
        "Will France's competition authority publish the conclusion of its antitrust investigation into Nvidia's cloud-AI and GPU-market practices by 2027-01-31?", 'NVDA',
        'On or before 2027-01-31 the authority has published its decision or conclusion in the investigation.',
        'After 2026-07-09 the authority has closed or dropped the investigation without publishing a decision or conclusion, and that stands on 2027-01-31.',
        '2027-01-31', 'period_end',
        [('any remedies or fines imposed', 'the second thing the outcome names; the outcome tracks the conclusion of the investigation first')]),
        [('a conclusion that neither finds nor clears the conduct and imposes nothing (no rung in the first run)', 1),
         ('a remedy accepted with no finding of an infringement (no rung in the first run)', 1),
         ('the case dropped with no published conclusion', 2),
         ('no decision and no closing by the day', 3)]),
    'u2/clean-3': (answer(
        'Will Chinese authorities permit NVIDIA to sell H200 AI chips in mainland China by 2027-01-31, as shown by an official Chinese announcement or by NVIDIA disclosing H200 sales or shipments into mainland China?', 'chip-export-controls',
        'On or before 2027-01-31 an official Chinese announcement has permitted H200 sales in mainland China, or NVIDIA has disclosed H200 sales or shipments into mainland China.',
        'An official Chinese decision not to permit H200 sales in mainland China, announced after 2026-07-02, stands on 2027-01-31.',
        '2027-01-31', 'period_end',
        [('conditions or quantity limits attached to a permission', 'a difference inside the permission'),
         ("NVIDIA's China share remaining at zero", 'the effect of the block; the outcome tracks the decision')]),
        [('a permission with conditions, and sales disclosed (two states at once in the first run)', 1),
         ('a new official decision not to permit', 2),
         ('no decision either way: the block as it stood on the article\'s day goes on (the first run divided this by whether a review was pending, which nobody outside can know)', 3)]),
    'u3/clean-12': (answer(
        'Will the US Commerce Department adopt a binding restriction, a licensing rule or any other, on advanced AI-chip shipments to third countries beyond its May 2026 guidance by 2027-01-31, as shown by a Federal Register rule or a formal export-control action?', 'chip-export-controls',
        'On or before 2027-01-31 the Commerce Department has adopted a binding restriction, a licensing rule or any other, on advanced AI-chip shipments to third countries beyond its May 2026 guidance.',
        'An announcement by the Commerce Department, made after 2026-07-14, that it will adopt no such restriction stands on 2027-01-31.',
        '2027-01-31', 'period_end',
        [("the resulting constraint on Nvidia's sales to those markets", 'the outcome tracks the rule; the effect on sales is read from later results'),
         ('how far the restriction goes: a licensing rule or another, and which countries it covers', 'a difference inside the restriction being adopted')]),
        [('a licensing rule and another restriction both adopted (two states at once in the first run)', 1),
         ('every proposal formally withdrawn, none adopted (a way the condition does not name: code\'s sentence takes it)', 2),
         ('one proposal pending while another has been rejected (two states at once in the first run)', 3)]),
    'u3/clean-5': (answer(
        "Will Nvidia make H200 sales to customers in China by 2027-01-31, as shown by Nvidia's disclosures or by official Chinese statements published on or before that day?", 'NVDA',
        "On or before 2027-01-31 Nvidia has made H200 sales to customers in China, as shown by Nvidia's disclosures or by official Chinese statements published on or before that day.",
        'A formal Chinese prohibition on purchases of H200 chips by Chinese customers, imposed after 2026-07-02, stands on 2027-01-31.',
        '2027-01-31', 'period_end',
        [('Beijing permitting purchases where no sale has yet been made', 'a permission is not a sale; the outcome tracks sales taking place'),
         ('the US clearance of H200 exports in December 2025', 'the background to the question, already given')]),
        [('sales shown by a disclosure', 1),
         ('no sale, and a formal prohibition, with a review of it pending (no rung in the first run)', 2),
         ('no sale, a permission announced (taken as sales in one send of the first run)', 3)]),
    'u1/clean-3': (answer(
        "Will NVIDIA's Vera Rubin platform begin first shipments by 2026-12-31?", 'NVDA',
        'First shipments of Vera Rubin have taken place on or before 2026-12-31.',
        'An announcement by NVIDIA, made after 2026-07-02, that first shipments will not begin until after 2026-12-31 stands on that day.',
        '2026-12-31', 'period_end', []),
        [('no shipment, and NVIDIA has announced a delay into 2027', 2),
         ('no shipment, and no announcement', 3)]),
    'u1/clean-11': (answer(
        'Will Chinese authorities approve imports of Nvidia H200 chips by Chinese firms by 2027-01-31, as shown by official Chinese government decisions or announcements?', 'chip-export-controls',
        'On or before 2027-01-31 Chinese authorities have officially approved imports of H200 chips by at least one Chinese firm.',
        'An official Chinese refusal of the requests to import H200 chips, or a prohibition of the imports, issued after 2026-07-08, stands on 2027-01-31 with no firm approved.',
        '2027-01-31', 'period_end',
        [('how many chips are approved, such as a total below 200,000', 'a difference inside the approval'),
         ('which firms are approved', 'a difference inside the approval'),
         ("Nvidia's resulting H200 revenue in China", 'the effect of the approval; the outcome tracks the approval')]),
        [('a limited approval for some firms', 1),
         ('every request refused, none approved', 2),
         ('every request withdrawn by the firms, none approved (a way the condition does not name: code\'s sentence takes it)', 2),
         ('requests still undecided, none approved', 3)]),
    'u3/clean-9': (answer(
        "Will France's competition authority publish the conclusion of its investigation into Nvidia's cloud-AI and GPU practices by 2027-01-31, as shown by its published decision or conclusion statement?", 'NVDA',
        'On or before 2027-01-31 the authority has published its decision or conclusion in the investigation.',
        'After 2026-07-09 the authority has closed or dropped the investigation without publishing a decision or conclusion, and that stands on 2027-01-31.',
        '2027-01-31', 'period_end',
        [('the date of the decision', 'the due day already bounds it'),
         ('what the conclusion finds, and any fine or remedy it imposes', 'further things the outcome names; the outcome tracks the conclusion of the probe first')]),
        [('a remedy with no finding of an infringement (no rung in the first run)', 1),
         ('a published conclusion with no fine and no remedy, whatever it finds', 1),
         ('the case dropped with no published conclusion', 2),
         ('no decision and no closing by the day', 3)]),
}


def main():
    cases = {case['case']: case for case in json.loads((HERE / 'cases.json').read_text())}
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    # A record of its time: these answers carry the ruling out as one sentence, the shape the second Stage A sent. They are checked
    # against that run's schema (kept in the three-arm probe's folder and shown there to equal the stored one), not the working one,
    # which since D416 asks who decides and what they decide. The code checks and the view writer read both shapes.
    schema = json.loads((STEP / 'probe-direction-2026-11-10' / 'old-schema.json').read_text())
    refused = 0
    print('Each "->" line places an outcome by reading the rung texts, taking the facts in it as known. Whether a fact is known on')
    print('the day is not settled here: the judge forecasts the rung from the evidence it has (judging-v7: "Only fact can establish')
    print('that a rung\'s outcome already holds"). What code guarantees is narrower: whatever is true, exactly one rung holds.')
    for case_name, (hand_answer, outcomes) in BY_HAND.items():
        case = cases[case_name]
        exact_answer = ladder_step.parse_exactly(json.dumps(hand_answer))
        schema_problems = model.check_schema(hand_answer, schema)
        reasons, passage = ladder_step.check_answer(exact_answer, thesis=case['thesis'], article=case['item'], company=COMPANY, research_list=research_list,
                                                    repair_quote=extraction.repair_quote, normalise=extraction.normalise, quote_tokens=extraction._quote_tokens,
                                                    beyond_next_year=extraction.beyond_next_year, binding_horizon_days=extraction.BINDING_HORIZON_DAYS)
        refused += bool(schema_problems or reasons)
        print('=' * 110)
        print(f"{case_name} | schema: {schema_problems or 'fits'} | checks: {reasons or 'accepted'}")
        if schema_problems or reasons:
            continue
        view = ladder_step.write_view(exact_answer['ladder'], passage, thesis=case['thesis'], article_day=case['item']['publication_date'],
                                      company=COMPANY, research_list=research_list)
        print(f"  {view['object_id']} ({view['kind']}), due {view['due_day']} | {view['question']}")
        for position, rung in enumerate(view['rungs'], start=1):
            print(f"    rung {position} {rung['label']}: {rung['condition']}")
        print('  not judged:', [part['part'] for part in hand_answer['ladder']['not_judged']])
        for outcome, rung in outcomes:
            print(f"    -> {outcome}: rung {rung} {view['rungs'][rung - 1]['label']}")
    print(f'{len(BY_HAND)} answers written by hand; refused by the schema or a check: {refused}')
    if refused:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
