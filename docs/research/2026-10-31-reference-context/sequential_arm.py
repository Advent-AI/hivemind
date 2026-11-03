"""design-seq.md: a sequential cold-start run of the reference-context arm. Day by day over the development gold's 118 articles, every
article of a day is sent with the open questions this run opened on earlier days (D251 daily snapshot); at the day's end the day's
candidates that match no open question and no earlier candidate of the day (score_ref.same_question) open as q<N>. One draw is one
independent run from an empty ledger. Answers: loop-2026-10-29/SEQ-v53R-d<d>/answers.sqlite; ledger: ledger-SEQ-v53R-d<d>.json.
The control (REF-v53) is ledger-blind, so its stored draws are reused; `python3 sequential_arm.py control-ledger` applies the same
opening rule to them offline, for S2/S3.

    python3 sequential_arm.py run 1 | run 2 | run 3 | control-ledger
"""
import concurrent.futures
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import reference_arm as ra  # noqa: E402
import score_ref as sr  # noqa: E402


def by_day():
    days = {}
    for a in sr.articles:
        days.setdefault(a['publication_day'], []).append(a['input_id'])
    return dict(sorted(days.items()))


def question_line(q):
    return f'  - {q["id"]} ({q["kind"]} {q["object"]}, due {q["due_day"]}): {q["question"]}'


ROLE_FILE = None          # a reshaped role text replacing the system message (design-v67.md); None keeps the configuration's role
EXTRA_FIELDS = {}         # evidence fields added to the schema with their descriptions, written first in the item (design-v67.md)
FIELD_NOTES_V67 = {
    'new_in_it': 'What is new in this statement, as a fact: a new event or step, figure, forecast, plan, policy step or specific judgement. Written before the quote.',
    'moves': 'The question whose answer this statement makes more or less likely, and through which path (demand, supply and inputs, competition, pricing, product progress, policy, capital and obligations).',
}


def arm_request(request, questions, before_day):
    body = copy.deepcopy(request)
    if ROLE_FILE:
        body['messages'][0] = dict(body['messages'][0], content=Path(ROLE_FILE).read_text().strip())
    user = body['messages'][-1]['content']
    at = user.index('[Item] id ')
    lines = '\n'.join(question_line(q) for q in questions) or '  None yet.'
    instruction = '' if ROLE_FILE else ' ' + ra.INSTRUCTION          # the reshaped role carries its own linking rule
    body['messages'][-1] = dict(body['messages'][-1], content=user[:at] + f'[Open questions as of {before_day}]{instruction}\n{lines}\n\n' + user[at:])
    item = body['response_format']['json_schema']['schema']['properties']['evidence']['items']
    item['properties']['links'] = dict(item['properties']['links'], description=ra.LINKS_NOTE)
    if EXTRA_FIELDS:
        item['properties'] = {**{k: {'type': 'string', 'description': v} for k, v in EXTRA_FIELDS.items()}, **item['properties']}
        item['required'] = list(EXTRA_FIELDS) + [r for r in item['required'] if r not in EXTRA_FIELDS]
    return body


def scope_words(c):
    return sr.sg.words((c.get('scope') or '') + ' ' + (c.get('looks_at') or '')) - sr.sg.STOP - {'nvidia', 'nvidia\'s', 'will', 'report', 'what', 'how', 'much'}


def same_identity(c, q):
    """Code identity only (AGENTS §2, D248): a quantity is the same question when object, measure and year agree and the scopes share
    half of the shorter one's words (a company-wide measure has no scope); an event when object agrees and the product or matter named
    in scope/looks_at shares half of the shorter one's words, whatever the milestone (launch or shipment) or deadline (D248 items 2, 3)."""
    if (c.get('object') or '') != (q.get('object') or ''):
        return False
    a, b = scope_words(c), scope_words(q)
    scope_same = (not a and not b) or (bool(a and b) and len(a & b) >= 0.5 * min(len(a), len(b)))
    if (c.get('measure') or '') == 'event' or (q.get('measure') or '') == 'event':
        return (c.get('measure') or '') == (q.get('measure') or '') and scope_same
    return (c.get('measure') or '') == (q.get('measure') or '') and str(c.get('year') or '') == str(q.get('year') or '') and scope_same


def open_new(ledger, day, candidates_by_article):
    """The day's candidates that are the same question (same_identity) as no open question and no earlier candidate of the day open as
    q<N>; returns the opened ones."""
    opened = []
    for iid, cands in candidates_by_article:
        for c in cands:
            if any(same_identity(c, q) for q in ledger + opened):
                continue
            opened.append({'id': f'q{len(ledger) + len(opened) + 1}', 'kind': c.get('kind', ''), 'object': c.get('object', ''), 'due_day': c.get('due_day', ''),
                           'question': c.get('question', ''), 'looks_at': c.get('looks_at', ''), 'measure': c.get('measure', ''), 'scope': c.get('scope', ''),
                           'event_type': c.get('event_type', ''), 'year': c.get('year', ''), 'opened_day': day, 'from': iid, 'candidate_id': c.get('id')})
    ledger.extend(opened)
    return opened


def send_one(tag, iid, questions, before_day):
    item, uni, setting, schema, request, cfg = ra.bench.build(iid, ra.CONFIG)
    body = arm_request(request, questions, before_day)
    conn = ra.store(tag)
    row = conn.execute('select content, completed from answers where input_id=? and request_sha256=?', (iid, ra.model.request_identity(body)[1])).fetchone()
    if row and row[1]:
        return iid, json.loads(row[0])          # already sent with these bytes (a resumed run)
    response = ra.model.openai_transport(cfg.provider, body)
    choice = response['choices'][0]
    completed = int(choice['finish_reason'] == 'stop')
    content = choice['message'].get('content') or ''
    if EXTRA_FIELDS and completed and content:        # the production sift and the scorers read the answer without the research fields; the full response stays in response_json
        data = json.loads(content)
        for e in data.get('evidence', []):
            for k in EXTRA_FIELDS:
                e.pop(k, None)
        content = json.dumps(data, ensure_ascii=False)
    usage = response.get('usage', {})
    with ra.LOCK:
        conn.execute('insert or replace into answers values (?,?,?,?,?,?,?,?,?,?)', (iid, ra.CONFIG, ra.model.request_identity(body)[1], json.dumps(response), content, completed,
                                                                                    usage.get('prompt_tokens'), usage.get('completion_tokens'), None, None))
        conn.commit()
    print(iid[:30], 'ok' if completed else 'INCOMPLETE', flush=True)
    return iid, (json.loads(content) if completed and content else {})


def run(draw, tag_prefix='SEQ-v53R'):
    tag = f'{tag_prefix}-d{draw}'
    ledger, log, previous_day = [], [], None
    for day, ids in by_day().items():
        snapshot = list(ledger)                      # D251: frozen at the day's start
        before = previous_day or day
        with concurrent.futures.ThreadPoolExecutor(8) as pool:
            answers = list(pool.map(lambda i: send_one(tag, i, snapshot, before), ids))
        opened = open_new(ledger, day, [(iid, data.get('candidates', [])) for iid, data in answers])
        log.append({'day': day, 'articles': len(ids), 'shown': len(snapshot), 'candidates': sum(len(d.get('candidates', [])) for _, d in answers), 'opened': len(opened)})
        print(f'{day}: {len(ids)} articles, shown {len(snapshot)}, candidates {log[-1]["candidates"]}, opened {len(opened)} -> ledger {len(ledger)}', flush=True)
        previous_day = day
    (HERE / f'ledger-{tag}.json').write_text(json.dumps({'days': log, 'questions': ledger}, ensure_ascii=False, indent=1))
    print(f'DONE {tag}: {len(ledger)} questions opened')


def control_ledger():
    for draw in (1, 2, 3):
        ledger, log = [], []
        for day, ids in by_day().items():
            cands = [(iid, (sr.raw(f'REF-v53-d{draw}', iid) or {}).get('candidates', [])) for iid in ids]
            opened = open_new(ledger, day, cands)
            log.append({'day': day, 'articles': len(ids), 'candidates': sum(len(c) for _, c in cands), 'opened': len(opened)})
        (HERE / f'ledger-REF-v53-d{draw}.json').write_text(json.dumps({'days': log, 'questions': ledger}, ensure_ascii=False, indent=1))
        print(f'control d{draw}: candidates {sum(l["candidates"] for l in log)}, opened {len(ledger)}')


if __name__ == '__main__':
    if sys.argv[1] == 'run':
        run(int(sys.argv[2]))
    elif sys.argv[1] == 'run-v70':                 # design-v70.md (D252): v68a plus the paired noise examples section
        ROLE_FILE = str(HERE / 'role-v70-draft.txt')
        EXTRA_FIELDS = {'new_in_it': 'What is new here, in a few words (a new event, step, figure, forecast, plan, policy step or specific judgement). Not a sentence.',
                        'moves': 'The question this makes more or less likely (an open question id, your candidate id, or the question in a few words) and how, in a few words. Not a sentence.'}
        run(int(sys.argv[2]), 'SEQ-v70')
    elif sys.argv[1] == 'run-v69b':                # design-v69.md: v68a with new_in_it and moves defined so they cannot be answered in generic words
        ROLE_FILE = str(HERE / 'role-v69b-draft.txt')
        EXTRA_FIELDS = {'new_in_it': 'What the item reports that the analyst did not have before, in a few words; a restatement of the sentence is not an answer.',
                        'moves': 'The question whose answer this makes more or less likely (an open question id, your candidate id, or the question in a few words) and how, in a few words. "Demand" or "competitive position" alone is not a question.'}
        run(int(sys.argv[2]), 'SEQ-v69b')
    elif sys.argv[1] == 'run-v69a':                # design-v69.md: v68a with checkable newness and a question as a bet in moves
        ROLE_FILE = str(HERE / 'role-v69a-draft.txt')
        EXTRA_FIELDS = {'new_in_it': 'The date, step or figure the item is the first to report, in a few words; not a restatement of the sentence.',
                        'moves': 'The question (an open question id, your candidate id, or a bet a figure or event will settle) and how this changes its answer, in a few words. "Demand" or "competitive position" alone is not a question.'}
        run(int(sys.argv[2]), 'SEQ-v69a')
    elif sys.argv[1] in ('run-v68a', 'run-v68b'):   # design-v68.md: v67 with short fields and one matter one item; a keeps the analyst's note gate, b drops it
        ROLE_FILE = str(HERE / f'role-{sys.argv[1][4:]}-draft.txt')
        EXTRA_FIELDS = {'new_in_it': 'What is new here, in a few words (a new event, step, figure, forecast, plan, policy step or specific judgement). Not a sentence.',
                        'moves': 'The question this makes more or less likely (an open question id, your candidate id, or the question in a few words) and how, in a few words. Not a sentence.'}
        run(int(sys.argv[2]), f'SEQ-{sys.argv[1][4:]}')
    elif sys.argv[1] == 'run-v67':                 # design-v67.md: the reshaped role, two evidence fields first, the same daily ledger
        ROLE_FILE = str(HERE / 'role-v67-draft.txt')
        EXTRA_FIELDS = FIELD_NOTES_V67
        run(int(sys.argv[2]), 'SEQ-v67')
    elif sys.argv[1] == 'control-ledger':
        control_ledger()
