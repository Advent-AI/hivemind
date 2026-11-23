"""Replay a stored Stage A run through the checks as they now stand, at no cost (AGENTS §5: a code change is accepted by replaying
stored decisions through the code, never by a new sample).

For each send, the stored first answer is checked again. Where the corrected check accepts an answer the old check refused, the
send's outcome is that first answer and the second request, sent only because of the old refusal, is dropped. Where the reasons
are the same, the stored outcome stands. Where the reasons differ in any other way, the resend was asked something else than the
corrected code would ask: the script stops and names the send, since only a new model call could answer it.

It was run on the first Stage A, whose answers hold an event as yes/no or five states. The step now answers an event in three
outcomes (D409) and refuses those shapes, so the first run is replayed only with the code kept beside its result
(`poc/data/clean-ladder-stage-a-2026-11-10/run-rechecked-2/code-as-read/`).

  python3 clean-arch/step4-2026-11-10/stage_a/recheck_stored_run.py <stored run folder> <new folder>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(STEP / 'ladder')]
import ladder_step  # noqa: E402
from hivemind import extraction, universe  # noqa: E402

COMPANY = 'NVDA'


def main():
    stored, rechecked = Path(sys.argv[1]), Path(sys.argv[2])
    rechecked.mkdir(parents=True, exist_ok=False)
    cases = {case['case']: case for case in json.loads((HERE / 'cases.json').read_text())}
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))

    def check(case, answer):
        return ladder_step.check_answer(answer, thesis=case['thesis'], article=case['item'], company=COMPANY, research_list=research_list,
                                        repair_quote=extraction.repair_quote, normalise=extraction.normalise,
                                        quote_tokens=extraction._quote_tokens,
                                        beyond_next_year=extraction.beyond_next_year, binding_horizon_days=extraction.BINDING_HORIZON_DAYS)

    changed, unchanged, cannot_replay = [], 0, []
    for pass_folder in sorted(stored.glob('send-*')):
        (rechecked / pass_folder.name).mkdir()
        lines = []
        for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines():
            row = json.loads(line)
            case, first = cases[row['case']], row['requests'][0]
            if first['result'] != 'refused' or not first['answer_text']:
                unchanged += 1
                lines.append(line)
                continue
            try:
                answer = ladder_step.parse_exactly(first['answer_text'])
                reasons, passage = check(case, answer)
            except (ValueError, RecursionError, KeyError, TypeError):
                unchanged += 1                    # an answer the step could not read: the stored refusal stands
                lines.append(line)
                continue
            if reasons == first['reasons']:
                if len(row['requests']) > 1 and row['requests'][1]['answer_text']:
                    try:
                        second_reasons = check(case, ladder_step.parse_exactly(row['requests'][1]['answer_text']))[0]
                    except (ValueError, RecursionError, KeyError, TypeError):
                        second_reasons = row['requests'][1].get('reasons', ['not readable'])
                    if bool(second_reasons) != bool(row['requests'][1].get('reasons')):
                        cannot_replay.append((row['case'], row['pass'], 'the second answer\'s verdict changes'))
                unchanged += 1
                lines.append(line)
            elif not reasons:
                view = None
                if answer['ladder'] is not None:
                    view = ladder_step.write_view(answer['ladder'], passage, thesis=case['thesis'], article_day=case['item']['publication_date'],
                                                  company=COMPANY, research_list=research_list)
                new_row = {'case': row['case'], 'pass': row['pass'], 'status': 'ladder' if view else 'no ladder',
                           'reason': None if view else answer['no_ladder'], 'requests': [{**first, 'result': 'ladder' if view else 'no ladder'}],
                           'answer': answer, 'passage': passage, 'view': view,
                           'rechecked': 'the corrected check accepts the first answer; the stored second request, sent only because of the '
                                        'old refusal, is dropped', 'stored_status': row['status'], 'old_reasons': first['reasons']}
                new_row['requests'][0].pop('reasons', None)
                changed.append((row['case'], row['pass'], row['status'], new_row['status']))
                lines.append(ladder_step.as_json(new_row))
            else:
                cannot_replay.append((row['case'], row['pass'], 'the reasons differ: only a new resend could answer'))
        (rechecked / pass_folder.name / 'outcomes.jsonl').write_text('\n'.join(lines) + '\n')
    print(f'{unchanged} sends unchanged; {len(changed)} changed:')
    for item in changed:
        print('   ', item)
    if cannot_replay:
        raise SystemExit(f'cannot be replayed at no cost: {cannot_replay}')
    (rechecked / 'RECHECKED.json').write_text(json.dumps({'stored run': str(stored), 'changed': changed, 'unchanged': unchanged}, indent=1) + '\n')


if __name__ == '__main__':
    main()
