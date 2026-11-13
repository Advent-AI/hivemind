"""The second-look test (D422): each sampled answer of the fourth Stage A is sent back once, in its own conversation, with one
instruction that names no fault; the returned answer is put through the step's checks.

The first turn is rebuilt as the fourth Stage A sent it (the system and user texts of the stored request; the schema as sent,
kept beside that run), the model's accepted answer follows as its own turn, then the instruction. Every send is the same but
for the conversation it continues; nothing says which answers readers faulted.

  python3 clean-arch/step4-2026-11-10/probe-second-look-2026-11-10/run.py check              # $0: every conversation rebuilds; no group is in any request
  python3 clean-arch/step4-2026-11-10/probe-second-look-2026-11-10/run.py send <new folder>
"""
import concurrent.futures
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch' / 'e2e-2026-11-09'), str(STEP / 'ladder'), str(STEP / 'stage_a')]
import budget  # noqa: E402
import ladder_step  # noqa: E402
import stage_a  # noqa: E402
from hivemind import extraction, model, universe  # noqa: E402

RUN = ROOT / 'poc' / 'data' / 'clean-ladder-stage-a-2026-11-10' / 'run-4'
CAP_USD = 0.20
INSTRUCTION = ('Check your answer once more against each rule above, one rule at a time. If it breaks none, return it unchanged. '
               'If it breaks one, return the corrected answer.')


def conversations():
    """(send, the stored outcome, the request that continues its conversation) for every sampled send."""
    schema = json.loads((RUN / 'code-as-sent' / 'candidate-schema.json').read_text())
    sample = [tuple(send) for send in json.loads((HERE / 'sample.json').read_text())]
    built = []
    for case, pass_number in sample:
        folder = RUN / f'send-{pass_number}'
        outcome = [row for line in (folder / 'outcomes.jsonl').read_text().splitlines() for row in [json.loads(line)] if row['case'] == case][0]
        accepted = outcome['requests'][-1]
        if accepted['result'] not in ('ladder', 'no ladder'):
            raise SystemExit(f'{case} send {pass_number}: the sampled answer was not accepted')
        connection = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
        stored = json.loads(connection.execute('select request_json from model_calls where request_sha256 = ?', (accepted['request_sha256'],)).fetchone()[0])
        connection.close()
        system_text, user_text = stored['messages'][0]['content'], stored['messages'][1]['content']
        first_turn = model.build_request(stage_a.SETTING, system_text, user_text, schema, 'clean_ladder', 'openai')
        if model.request_identity(first_turn)[1] != accepted['request_sha256']:
            raise SystemExit(f'{case} send {pass_number}: the first turn does not rebuild the stored request')
        request = dict(first_turn, messages=first_turn['messages'] + [{'role': 'assistant', 'content': accepted['answer_text']},
                                                                      {'role': 'user', 'content': INSTRUCTION}])
        built.append(((case, pass_number), outcome, request))
    return built


def checked(answer_text, case, research_list):
    """(the answer or None, the reasons code refuses it for)."""
    try:
        answer = ladder_step.parse_exactly(answer_text)
    except (ValueError, RecursionError, TypeError) as error:
        return None, [f'the answer could not be read: {type(error).__name__}']
    if (answer.get('no_ladder') is None) == (answer.get('ladder') is None):
        return answer, ['exactly one of no_ladder and ladder must be null']
    reasons, _ = ladder_step.check_answer(answer, thesis=case['thesis'], article=case['item'], company=stage_a.COMPANY, research_list=research_list,
                                          repair_quote=extraction.repair_quote, normalise=extraction.normalise, quote_tokens=extraction._quote_tokens,
                                          beyond_next_year=extraction.beyond_next_year, binding_horizon_days=extraction.BINDING_HORIZON_DAYS)
    return answer, reasons


def main():
    built = conversations()
    print(f'{len(built)} conversations rebuilt; each first turn has its stored request\'s identity; the instruction is the same in all')
    if sys.argv[1:] == ['check']:
        return
    if len(sys.argv) != 3 or sys.argv[1] != 'send':
        raise SystemExit(__doc__)
    folder = Path(sys.argv[2])
    folder.mkdir(parents=True, exist_ok=False)
    cases = {case['case']: case for case in json.loads((STEP / 'stage_a' / 'cases.json').read_text())}
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    limit = budget.Budget(CAP_USD)

    def ask(job):
        send, outcome, request = job
        response = limit.send('openai', request)
        second_text = response['choices'][0]['message']['content']
        first_text = outcome['requests'][-1]['answer_text']
        answer, reasons = checked(second_text, cases[send[0]], research_list)
        same = answer is not None and json.loads(second_text) == json.loads(first_text)
        usage = response.get('usage') or {}
        return {'case': send[0], 'pass': send[1], 'first_text': first_text, 'second_text': second_text, 'same': same, 'second_refused_for': reasons,
                'kept': 'first' if (reasons or same) else 'second', 'input_tokens': usage.get('prompt_tokens'), 'output_tokens': usage.get('completion_tokens')}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(ask, built))
    (folder / 'second-looks.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in results))
    changed = [row for row in results if not row['same']]
    print(f'{len(results)} second looks stored; unchanged {len(results) - len(changed)}; changed {len(changed)}, of them refused by code '
          f"{sum(1 for row in changed if row['second_refused_for'])}; spent ${limit.spent_usd:.4f} (cap ${CAP_USD:.2f})")


if __name__ == '__main__':
    main()
