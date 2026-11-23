"""A check of one class after the small send of the three-outcome request (a few cents): did the request's change move the
declining of theses whose matter no listed theme covers, or was one draw unlucky? (AGENTS §7.3: "A model call is a sampler.
Re-send a stored request before calling its answer a defect.")

The same theses are sent three times with the request as it now stands and three times with the request as first sent (kept
beside the first run's result), through the same runner; each send has its own archive, so each is a fresh sample. Only the
decision is read: a ladder, with its object, or a refusal with its reason.

  python3 clean-arch/step4-2026-11-10/stage_a/decline_check.py <new folder> <cap in dollars> <case,case,...>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stage_a  # noqa: E402
from hivemind import universe  # noqa: E402

FIRST_REQUEST = stage_a.ROOT / 'poc' / 'data' / 'clean-ladder-stage-a-2026-11-10' / 'run-rechecked-2' / 'code-as-read' / 'ladder'


def first_request_texts():
    return {'system': (FIRST_REQUEST / 'candidate-system.txt').read_text(), 'closing': (FIRST_REQUEST / 'candidate-closing.txt').read_text().strip(),
            'schema': json.loads((FIRST_REQUEST / 'candidate-schema.json').read_text())}


def decisions(folder):
    found = {}
    for pass_folder in sorted(Path(folder).glob('send-*')):
        for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines():
            row = json.loads(line)
            first_answer = json.loads(row['requests'][0]['answer_text']) if row['requests'][0]['answer_text'] else {}
            ladder = first_answer.get('ladder')                      # the model's own first decision, before any check
            found.setdefault(row['case'], []).append('declined' if ladder is None else f"ladder ({ladder.get('object')})")
    return found


def main():
    folder, cap, wanted = Path(sys.argv[1]), float(sys.argv[2]), sys.argv[3].split(',')
    cases = [case for case in json.loads((HERE / 'cases.json').read_text()) if case['case'] in wanted]
    research_list = universe.load(str(stage_a.ROOT / 'poc' / 'universe.json'))
    folder.mkdir(parents=True, exist_ok=False)
    arms = {'the request as it now stands': stage_a.request_texts(), 'the request as first sent': first_request_texts()}
    spent, tables = 0.0, {}
    for number, (arm, texts) in enumerate(arms.items(), start=1):
        _, limit, _ = stage_a.run(cases, [1, 2, 3], folder / f'arm-{number}', cap - spent, research_list=research_list, texts=texts)
        if limit.stopped:
            raise SystemExit(f'STOPPED: {limit.stop_reason}')
        known, in_full, _ = stage_a.ledger_total(folder / f'arm-{number}' / 'spend.jsonl')
        spent += known + in_full
        tables[arm] = decisions(folder / f'arm-{number}')
    for case in wanted:
        print(case)
        for arm in arms:
            print(f'   {arm}: {tables[arm].get(case)}')
    print(f'spent ${spent:.4f}')


if __name__ == '__main__':
    main()
