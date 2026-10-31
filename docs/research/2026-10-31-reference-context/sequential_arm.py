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


def arm_request(request, questions, before_day):
    body = copy.deepcopy(request)
    user = body['messages'][-1]['content']
    at = user.index('[Item] id ')
    lines = '\n'.join(question_line(q) for q in questions) or '  None yet.'
    body['messages'][-1] = dict(body['messages'][-1], content=user[:at] + f'[Open questions as of {before_day}] {ra.INSTRUCTION}\n{lines}\n\n' + user[at:])
    fields = body['response_format']['json_schema']['schema']['properties']['evidence']['items']['properties']
    fields['links'] = dict(fields['links'], description=ra.LINKS_NOTE)
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
    usage = response.get('usage', {})
    with ra.LOCK:
        conn.execute('insert or replace into answers values (?,?,?,?,?,?,?,?,?,?)', (iid, ra.CONFIG, ra.model.request_identity(body)[1], json.dumps(response), content, completed,
                                                                                    usage.get('prompt_tokens'), usage.get('completion_tokens'), None, None))
        conn.commit()
    print(iid[:30], 'ok' if completed else 'INCOMPLETE', flush=True)
    return iid, (json.loads(content) if completed and content else {})


def run(draw):
    tag = f'SEQ-v53R-d{draw}'
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
    elif sys.argv[1] == 'control-ledger':
        control_ledger()
