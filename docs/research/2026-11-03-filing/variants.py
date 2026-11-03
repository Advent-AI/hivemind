"""Request variants for test_filing.py. Each takes the stored production request and returns a copy with named sentences replaced; a
replacement that does not find its sentence raises, so a variant never silently tests the stored request.

  stored  the request as production sent it (the control)
  v1      what a question takes is defined by use: a numeric question's takes line names, besides its own figures, the same figure for a
          part of its period and another measure that tracks it; the system sentence files under the question an analyst would use the
          statement to estimate. The links rule (fallback, one question) is unchanged.
  v3      test 2: in the links rule only, the one-question sentence becomes: a statement often serves two specific questions and then goes
          under both, with three cross-domain examples; a broader question is still never added beside a specific one; the fallback stays.
  v4      test 3: each open question's takes line gains "; tracked by: <line>", the line the model wrote from the question alone
          (gen_tracked_by.py -> tracked-by.json); nothing else changes.
  nofallback  only the links rule's fallback sentence is removed (the challenger's simplest arm); nothing else changes.
  v2      v1, and in the links rule: a statement goes to every open question an analyst would use it to estimate, and the fallback to the
          company-wide revenue question is removed.
"""
import copy
import json
import re

SYS_OLD = "the narrowest open question whose takes line covers it, your own candidate, or both."
SYS_NEW = "the narrowest open question an analyst would use it to estimate, as that question's takes line says, your own candidate, or both."
SYS_NEW_V2 = "every open question an analyst would use it to estimate, as each question's takes line says, your own candidate, or both."
SYS_V3 = "the narrowest open questions whose takes lines cover it, your own candidate, or both."
TAKES = re.compile(r"takes: (\S+) figures, guidance, estimates and revisions for (.+?), this question's period (\S+)")


def takes_by_use(match):
    return (f"takes: what an analyst uses to estimate {match.group(2)} for {match.group(3)}: its own figures, guidance, estimates and "
            f"revisions; the same figure for a part of that period, such as a quarter of the year; and another measure that tracks it, such "
            f"as a supplier's sales of it or a buyer's budget for it")


LINKS_ONE = "compare the specific questions before a company-wide revenue or margin question and take that one only, never a broader question beside it; "
LINKS_MANY = ("file it under every open question an analyst would use it to estimate, the broader question too when the statement is used "
              "for that question's own answer and not only because the narrower question sits under it; ")
LINKS_HEAD_OLD = "the id of the narrowest open question in [Open questions] whose answer this statement makes more or less likely"
LINKS_HEAD_NEW = "the ids of the open questions in [Open questions] whose answer this statement makes more or less likely"
LINKS_TWO_USES = ("compare the specific questions before a company-wide revenue or margin question and never add a broader question beside "
                  "a specific one; a statement often serves two specific questions, and then it goes under both: a glass maker's sales to "
                  "carmakers rising 40% bears on carmakers' spending on glass and on the glass maker's share of that market; a rival drug's "
                  "prescriptions doubling bears on the drug class's total sales and on the company's share of them; a bank's first-quarter "
                  "net interest margin bears on its full-year margin; ")
LINKS_HEAD_V3 = "the ids of the narrowest open questions in [Open questions] whose answer this statement makes more or less likely"
LINKS_FALLBACK = ("when no specific question is connected, a statement that moves the demand, supply, competition or pricing behind the "
                  "company's results goes to the company-wide revenue question of its period; ")


def _replace(text, old, new, what):
    if old not in text:
        raise ValueError(f'variant sentence not found: {what}')
    return text.replace(old, new)


QUESTION_TAKES = re.compile(r'(^\s*- (v\d+) \([^)]*\): [^\n]+\n\s+takes: [^\n]+)', re.M)


def apply(arm, request):
    body = copy.deepcopy(request)
    if arm == 'stored':
        return body
    if arm == 'v4':
        import os
        tracked = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tracked-by.json')))
        user = body['messages'][1]
        user['content'], n = QUESTION_TAKES.subn(lambda m: m.group(1) + (f"; tracked by: {tracked[m.group(2)]}" if m.group(2) in tracked else ''), user['content'])
        if not any(f'tracked by: ' in l for l in user['content'].splitlines()):
            raise ValueError('no tracked-by line added')
        return body
    links = body['response_format']['json_schema']['schema']['properties']['evidence']['items']['properties']['links']
    if arm == 'v3':
        body['messages'][0]['content'] = _replace(body['messages'][0]['content'], SYS_OLD, SYS_V3, 'system filing sentence')
        text = _replace(links['description'], LINKS_HEAD_OLD, LINKS_HEAD_V3, 'links: the narrowest question')
        links['description'] = _replace(text, LINKS_ONE, LINKS_TWO_USES, 'links: one question only')
        return body
    if arm == 'nofallback':
        links['description'] = _replace(links['description'], LINKS_FALLBACK, '', 'links: revenue fallback')
        return body
    if arm not in ('v1', 'v2'):
        raise ValueError(f'unknown arm {arm}')
    system, user = body['messages'][0], body['messages'][1]
    system['content'] = _replace(system['content'], SYS_OLD, SYS_NEW_V2 if arm == 'v2' else SYS_NEW, 'system filing sentence')
    user['content'], n = TAKES.subn(takes_by_use, user['content'])
    if n == 0:
        raise ValueError('no numeric takes line found')
    if arm == 'v2':
        text = _replace(links['description'], LINKS_HEAD_OLD, LINKS_HEAD_NEW, 'links: the narrowest question')
        text = _replace(text, LINKS_ONE, LINKS_MANY, 'links: one question only')
        links['description'] = _replace(text, LINKS_FALLBACK, '', 'links: revenue fallback')
    return body


if __name__ == '__main__':                     # print what each variant changes on one stored request, $0
    import sqlite3, sys
    db = sqlite3.connect('file:' + sys.argv[1] + '?mode=ro', uri=True)
    req = json.loads(db.execute('select request_json from model_calls where call_id=?', (int(sys.argv[2]),)).fetchone()[0])
    for arm in ('v1', 'v2'):
        out = apply(arm, req)
        print(f'== {arm}: system', SYS_NEW_V2 if arm == 'v2' else SYS_NEW)
        print('   first takes line:', next(l.strip() for l in out['messages'][1]['content'].splitlines() if 'what an analyst uses' in l)[:300])
        if arm == 'v2':
            print('   links:', out['response_format']['json_schema']['schema']['properties']['evidence']['items']['properties']['links']['description'][:900])
