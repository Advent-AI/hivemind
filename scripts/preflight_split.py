"""Preflight for the split extraction (plan-final C-6), $0. For every item a split run dispatched on the days from --from on, rebuild from the ledger,
the item database and the archive:
- the item's snapshot (every question open before its sequence) and the universe it was read with (the configured subjects plus the research
  subjects written before it);
- the A and B requests of each section, and the record-preparation request built from the archived A and B answers. Each must be in the archive
  under its identity, which is the request's content: the production code builds the request dict and sends it in that build order, so a request
  rebuilt by the same code carries the same order;
- the format check the production call runs on every answer (`model.check_schema`), on each archived answer replayed;
- the handover built from the archived answers, with the research subjects registered as the run registered them. It must equal the stored one in
  full: every evidence and candidate field, the drops and the declared groups.
The population is reconciled: every dispatched item whose extraction succeeded must have exactly one stored handover and its input; a missing one is
refused, never skipped. The archive keeps each request in sorted-key form only, so the byte order a request was sent in is not recorded; the
identity check proves the content, and the order follows from the production code that builds and sends the dict. Archived split answers that
cannot be replayed (no answer, or refused and retired) are counted and printed. Only the days from --from on are judged (a split run may start from a ledger another configuration wrote; replay never
backdates, so those days are the split run's own). Prints, per check, the cases judged, skipped (with why) and refused with reasons; exits 1 on a
refusal or when nothing was judged.

Usage: PYTHONPATH=src python3 scripts/preflight_split.py --config C --views LEDGER --archive ARCHIVE --testdb ITEMS --from DAY [--universe U]"""
import argparse
import json
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, model, split, testdb, universe as universe_module  # noqa: E402
from hivemind.views import store  # noqa: E402


def subjects_before(conn, seq):
    """An in-memory ledger holding only the research subjects written before the item, so registration runs as it ran for the item."""
    memory = sqlite3.connect(':memory:')
    memory.row_factory = sqlite3.Row
    memory.execute(f'create table research_subjects ({store.TABLES["research_subjects"]})')
    for row in conn.execute('select object_id, name, kind, created_seq, created_from_input from research_subjects where created_seq < ? order by rowid', (seq,)):
        memory.execute('insert into research_subjects values (?, ?, ?, ?, ?)', tuple(row))
    return memory


SCHEMA_CHECKS = {'judged': 0, 'refused': []}


def archived(archive_conn, setting, spec, cfg):
    """The archived answer to the rebuilt request, after the format check the production call runs on every answer (`model.check_schema`)."""
    request = model.build_request(setting, spec[0], spec[1], spec[2], spec[3], cfg.provider)
    _, sha = model.request_identity(request)
    row = archive_conn.execute('select answer_json from model_calls where request_sha256=?', (sha,)).fetchone()
    if not row or not row[0]:
        return None
    answer = json.loads(row[0])
    SCHEMA_CHECKS['judged'] += 1
    errors = model.check_schema(answer, spec[2])
    if errors:
        SCHEMA_CHECKS['refused'].append((spec[3], '; '.join(errors)[:200]))
    return answer


def canonical(handover):
    return json.dumps({k: handover.get(k) for k in ('evidence', 'candidates', 'dropped', 'new_groups')}, sort_keys=True, ensure_ascii=False)


def rebuild(cfg, conn, archive_conn, item, seq, universe_path):
    """(None, handover, prepared) or (reason, None, None); a reason starts with the check it belongs to."""
    memory = subjects_before(conn, seq)
    uni = universe_module.load(universe_path)
    split.load_subjects(memory, uni)
    shown = split.latest_library(conn, seq)
    answers, proposed = [], []
    for part in split.sections(item['text']):
        _, a_spec, b_spec = split.requests(cfg, item, part, shown, uni, proposed)
        a, b = archived(archive_conn, cfg.split['a'], a_spec, cfg), archived(archive_conn, cfg.split['b'], b_spec, cfg)
        if a is None or b is None:
            return 'requests: A or B request not in the archive under its rebuilt identity', None, None
        answers.append((a, b))
        proposed += [q['question'] for q in a['questions']]
    stage = split.stage_answers(item, item['text'], answers, split.subject_names(item, uni))
    prep = {'candidates': {}, 'evidence': {}, 'unfiled': {}}
    if stage['questions']:
        prep = archived(archive_conn, cfg.split['preparation'], split.preparation_request(cfg, item, item['text'], uni, stage), cfg)
        if prep is None:
            return 'preparation: record-preparation request not in the archive under its rebuilt identity', None, None
    evidence, candidates, dropped, groups = split.build_handover(item, item['text'], shown, uni, stage, prep)
    split.register_subjects(memory, uni, candidates, seq, item['input_id'])
    handover = json.loads(json.dumps({'evidence': evidence, 'candidates': candidates, 'dropped': dropped, 'new_groups': groups}, ensure_ascii=False))
    return None, handover, bool(stage['questions'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--views', required=True)
    parser.add_argument('--archive', required=True)
    parser.add_argument('--testdb', required=True)
    parser.add_argument('--from', dest='from_day', required=True)
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    args = parser.parse_args()
    cfg = config.load(args.config)
    if cfg.split is None:
        raise SystemExit(f'{cfg.version} is not a split configuration')
    conn = store.open_read_only(args.views)
    archive_conn = sqlite3.connect(f'file:{args.archive}?mode=ro', uri=True)
    items = testdb.open_db(args.testdb)
    tally = {name: {'judged': 0, 'skipped': [], 'refused': []} for name in ('population', 'requests', 'preparation', 'handover')}
    extracted = [(r[0], r[1]) for r in conn.execute("select input_id, sequence_no from processing_steps where step='extracted' and result='ok' "
                                                    "and publication_day>=? order by sequence_no", (args.from_day,))]
    dispatched = {r[0] for r in conn.execute("select sequence_no from processing_steps where step='dispatched' and publication_day>=?", (args.from_day,))}
    stored = {}
    for row in conn.execute('select seq, input_id, handover_json from handovers'):
        stored.setdefault(row[0], []).append((row[1], row[2]))
    for input_id, seq in extracted:
        tally['population']['judged'] += 1
        rows = stored.get(seq, [])
        if len(rows) != 1 or rows[0][0] != input_id:
            tally['population']['refused'].append((seq, f'{len(rows)} stored handovers for an item whose extraction succeeded'))
            continue
        found = items.execute('select * from items where input_id=?', (input_id,)).fetchone()
        if found is None:
            tally['population']['refused'].append((seq, 'its input is not in the item database'))
            continue
        tally['requests']['judged'] += 1
        reason, handover, prepared = rebuild(cfg, conn, archive_conn, testdb.item_of(found), seq, args.universe)
        if reason:
            check, _, why = reason.partition(': ')
            if check == 'preparation':
                tally['preparation']['judged'] += 1
            tally[check]['refused'].append((seq, why))
            continue
        if prepared:
            tally['preparation']['judged'] += 1
        else:
            tally['preparation']['skipped'].append((seq, 'no new question, so no record preparation'))
        tally['handover']['judged'] += 1
        if canonical(handover) != canonical(json.loads(rows[0][1])):
            tally['handover']['refused'].append((seq, 'the handover rebuilt from the archived answers differs from the stored one'))
    succeeded = {seq for _, seq in extracted}
    for seq in sorted(set(stored) & dispatched - succeeded):
        tally['population']['refused'].append((seq, 'a stored handover with no successful extraction step'))
    unreplayed = archive_conn.execute("select purpose, count(*) from model_calls where purpose like 'split_%' and (answer_json is null or "
                                      "request_sha256 like '%:%') group by purpose").fetchall()
    print('archived split answers not replayable (no answer, or refused and retired): '
          + (', '.join(f'{purpose} {count}' for purpose, count in unreplayed) if unreplayed else 'none'))
    print(f'format check (model.check_schema) on every replayed answer: judged {SCHEMA_CHECKS["judged"]}, refused {len(SCHEMA_CHECKS["refused"])}')
    for name, why in SCHEMA_CHECKS['refused'][:20]:
        print(f'  refused {name}: {why}')
    failed = bool(SCHEMA_CHECKS['refused'])
    for name, t in tally.items():
        reasons = sorted({why for _, why in t['skipped']})
        print(f'{name}: judged {t["judged"]}, skipped {len(t["skipped"])}{" (" + "; ".join(reasons) + ")" if reasons else ""}, refused {len(t["refused"])}')
        for seq, why in t['refused'][:20]:
            print(f'  refused seq {seq}: {why}')
        failed = failed or bool(t['refused'])
    if tally['handover']['judged'] == 0 or SCHEMA_CHECKS['judged'] == 0:
        print('unexercised: no handover was judged')
        failed = True
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
