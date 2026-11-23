"""T2 and T4 of the citation-only judge's $0 test (DESIGN.md §5; D713).

T2 (evidence from the archived text): for every stored judge request of old-1, old-2, old-3 and the two pilot arms' fresh rows, the
closed lists are taken from the request's text (evidence entries, dependency entries, theme entries), judging-v12's format is built
from them, and the stored answer goes through the real `model.check_schema`. Pass: every committed answer and every valid uncommitted
one validates; every refused answer fails on an id. The population is printed.

T4: the largest format over those archives and over the sealed D358 archive: evidence ids, enum values with the shared evidence enum
counted once and counted per reference, and characters, against the provider's documented limits.

  python3 t2_offline.py
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / 'src'))
from hivemind import model                                              # noqa: E402
from hivemind.views import judging                                     # noqa: E402

RUN = REPO / 'poc/data/comparison-2026-11-17/run'
PILOT_COPIES = Path('/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad')
PILOT_TOP = 8737                                                        # the pilots' archives copy old-2's rows up to this call
SOURCES = [('old-1', RUN / 'old-1/prod', 0), ('old-2', RUN / 'old-2/prod', 0), ('old-3', RUN / 'old-3/prod', 0),
           ('control-1', PILOT_COPIES / 'control-1-copy', PILOT_TOP), ('linked-1', PILOT_COPIES / 'linked-1-copy', PILOT_TOP)]
SEALED = REPO / 'poc/data/sealed-2026-10-28-v34-nvda-3m-through-0828/archive.sqlite'
PUSH_ENUM_VALUES = 6                                                    # the two existing 3-value push enums
PROVIDER_ENUM_LIMIT = 1000
RETRY_MARK = '\n\nThe code returned the previous answer because: '


def dependencies_shown_in(user):
    block = user.split('\n[Current conclusions of the theses it depends on]', 1)
    return set(re.findall(r'^- (v\d+) \(', block[1].split('\n\n[', 1)[0], re.M)) if len(block) == 2 else set()


def lists_from_text(user):
    return {'evidence': sorted(judging.evidence_shown_in(user)), 'dependencies': sorted(dependencies_shown_in(user)),
            'themes': sorted(judging.themes_shown_in(user))}


def size(lists, schema):
    e, d, t = len(lists['evidence']), len(lists['dependencies']), len(lists['themes'])
    return {'evidence': e, 'enum values, shared enum counted once': e + d + t + PUSH_ENUM_VALUES,
            'enum values, counted per reference': 2 * e + d + t + PUSH_ENUM_VALUES, 'format chars': len(json.dumps(schema))}


def t2():
    population = {'archive rows': 0, 'distinct request-answer pairs': 0, 'committed': 0, 'refused': 0, 'valid uncommitted': 0}
    failures, refused_detail, seen, sizes, open_chars = [], [], set(), [], []
    open_format_chars = len(json.dumps(judging.schema_for('judging-v7')))
    for label, folder, top in SOURCES:
        archive = sqlite3.connect(f'file:{folder / "archive.sqlite"}?mode=ro', uri=True)
        views = sqlite3.connect(f'file:{folder / "views.sqlite"}?mode=ro', uri=True)
        committed_calls = {r[0] for r in views.execute('select call_id from judgements')}
        for call_id, sha, request_json, answer_json in archive.execute(
                "select call_id, request_sha256, request_json, answer_json from model_calls where purpose='judge' and call_id>? order by call_id", (top,)):
            population['archive rows'] += 1
            request = json.loads(request_json)
            user = request['messages'][1]['content']
            pair = (sha.split(':')[0], answer_json)
            if pair in seen:
                continue
            seen.add(pair)
            population['distinct request-answer pairs'] += 1
            lists = lists_from_text(user.split(RETRY_MARK, 1)[0])        # a retry carries the first request's text, then the note
            schema = judging.schema_for('judging-v12', lists)
            sizes.append(size(lists, schema))
            errors = model.check_schema(json.loads(answer_json), schema)
            refused = ':refused:' in sha or ':schema:' in sha
            if refused:
                population['refused'] += 1
                refused_detail.append({'source': label, 'call': call_id, 'format errors': errors[:3]})
                if not errors:
                    failures.append({'source': label, 'call': call_id, 'why': 'a refused answer passes the closed format'})
            else:
                population['committed' if call_id in committed_calls else 'valid uncommitted'] += 1
                if errors:
                    failures.append({'source': label, 'call': call_id, 'why': errors[:3]})
    chars = sorted(s['format chars'] for s in sizes)
    return {'population': population, 'T2 failures': failures, 'refused answers and their format errors': refused_detail,
            'T2 pass': not failures and population['refused'] > 0,
            'format chars': {'judging-v7': open_format_chars, 'v12 median': chars[len(chars) // 2], 'v12 max': chars[-1]},
            'largest (T4)': max(sizes, key=lambda s: s['evidence'])}


def t4_sealed():
    archive = sqlite3.connect(f'file:{SEALED}?mode=ro', uri=True)
    sizes = []
    for (request_json,) in archive.execute("select request_json from model_calls where purpose='judge'"):
        user = json.loads(request_json)['messages'][1]['content']
        lists = lists_from_text(user)
        sizes.append(size(lists, judging.schema_for('judging-v12', lists)))
    over_once = sum(s['enum values, shared enum counted once'] > PROVIDER_ENUM_LIMIT for s in sizes)
    over_twice = sum(s['enum values, counted per reference'] > PROVIDER_ENUM_LIMIT for s in sizes)
    return {'requests': len(sizes), 'largest': max(sizes, key=lambda s: s['evidence']),
            f'over {PROVIDER_ENUM_LIMIT} with the shared enum counted once': over_once,
            f'over {PROVIDER_ENUM_LIMIT} counted per reference': over_twice}


def main():
    result = t2()
    result['T4 sealed D358 archive'] = t4_sealed()
    (HERE / 't2-result.json').write_text(json.dumps(result, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in result.items() if k != 'refused answers and their format errors'}, indent=1, ensure_ascii=False))
    for row in result['refused answers and their format errors']:
        print(row['source'], row['call'], row['format errors'][:1])
    sys.exit(0 if result['T2 pass'] else 1)


if __name__ == '__main__':
    main()
