"""Preflight: run every code check and every prompt against the stored model answers before a paid run ($0).

AGENTS.md §3 "Strictness is code too" and §4 "a check must judge something": a check is accepted on real data,
reports how many cases it judged, and a check over an empty population is unexercised. This script replays what
the archive and the earlier runs' views databases already hold through the current code and prints, per check,
the cases judged, the cases refused and the reasons with examples:

  A. answers the schema refused (prompt and schema disagree: a value the prompt's wording suggested but the enum lacks)
  B. extraction's code checks (extraction.sift) over every stored extraction answer
  C. matching's code checks (matching.check) over every stored matching record, with the lists shown at the time
  D. every schema enum value appears verbatim in the prompt that asks for it
  F. the judging checks (judging-v7, judging-v8) over every judgement the ledger accepted, each against what its request showed and the
     thesis's last judgement and card before it; an answer refused at the time has no judgement and is counted as not verifiable

It replays the answers of the versions the code builds (extraction v74i, judging-v7); a row of a retired version, or one whose
configuration file is gone, is counted as not replayed and named. Usage: python3 scripts/preflight.py [--archive A] [--items I]
[--views DB ...] (defaults: draw 1 of the frozen v108 run, poc/data/e2e-r9-frozen-v108-2026-11-03/d1, and the NVDA items database).
Exit status 1 when a check judged no case.
"""
import argparse
import collections
import glob
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, extraction, model, testdb, universe, vocabulary  # noqa: E402
from hivemind.views import judging, matching  # noqa: E402

SCHEMAS = {'extract': extraction.schema_for(extraction.SUPPORTED_VERSIONS[0]), 'match': matching.SCHEMA, 'judge': judging.schema_for(judging.SUPPORTED_VERSIONS[0])}
# the stored requests of both prompt languages (D163): Chinese headers up to extraction v5 / matching-v1, English from v6 / matching-v2
ITEM_ID = re.compile(r'【信息】编号 (\S+?)，类别 |\[Item\] id (\S+?), category ')
MATCH_SHOWN = re.compile(r'^· (v\d+)\s?[（(]', re.M)
JEV_ASKED = re.compile(r'\b(v\d+): ')          # a Jev candidate reason names every thesis it was asked about: 'jev: v1: different 0.55; …'


def normalise_reason(text):
    text = re.sub(r"'[^']*'", "'…'", text)
    text = re.sub(r'\[\d+\]', '[]', text)
    text = re.sub(r'\b[ev]\d+\b|\bc\d+\b', '#', text)
    text = re.sub(r'\d{4}-\d{2}-\d{2}', 'DATE', text)
    return text[:90]


def tally(title, judged, refused, reasons, examples):
    share = f'{refused / judged:.0%}' if judged else 'n/a'
    print(f'\n== {title}: judged {judged}, refused/dropped {refused} ({share})')
    for reason, count in reasons.most_common(20):
        print(f'   {count:5d}  {reason}')
        for example in examples.get(reason, [])[:2]:
            print(f'          e.g. {example}')


def part_a(archive_conn):
    reasons, examples, judged = collections.Counter(), collections.defaultdict(list), 0
    rows = archive_conn.execute("select purpose, request_sha256, answer_json from model_calls where request_sha256 like '%:schema:%' or request_sha256 like '%:malformed:%' or request_sha256 like '%:refused:%'")
    for purpose, sha, answer_json in (tuple(r) for r in rows):
        judged += 1
        if ':malformed:' in sha or not answer_json:
            reasons[f'{purpose}: not JSON'] += 1
            continue
        stored = archive_conn.execute('select request_json from model_calls where request_sha256=?', (sha,)).fetchone()
        try:
            schema = json.loads(stored[0])['response_format']['json_schema']['schema']           # the shape that request asked for
        except (TypeError, KeyError, ValueError):
            schema = SCHEMAS.get(purpose, {})
        for error in model.check_schema(json.loads(answer_json), schema):
            key = f'{purpose}: {normalise_reason(error)}'
            reasons[key] += 1
            examples[key].append(error[:140])
    tally('A. answers the schema refused (prompt/schema disagreements; empty when the provider enforces the schema server-side)', judged, judged, reasons, examples)
    return judged


class Unverifiable(Exception):
    """A stored request of a retired version, or whose configuration file is gone: counted and named in the output, not replayed,
    and not a failure of the archive."""


def _preflight_extract_inputs(request, item, cfg):
    """Validate the stored source and recover exactly the question ids production showed (its [Open questions] block)."""
    setting = cfg.extraction_setting(item['category'])
    version = setting.prompt_version.rpartition('-')[2]
    if version not in extraction.SUPPORTED_VERSIONS:
        raise Unverifiable(f'extraction {version} (retired)')
    text = (item['text'] or '')[:extraction.MAX_TEXT_CHARS]          # production sends the first MAX_TEXT_CHARS characters
    user = next(m['content'] for m in request['messages'] if m['role'] == 'user')
    header = extraction.item_header(item, item['category'])
    if user.count(header) != 1:
        raise ValueError('source metadata does not match archived request')
    before, after = user.split(header, 1)
    if not after.startswith(text + '\n\n' + extraction.CLOSING):
        raise ValueError('source text does not match archived request')
    blocks = before.split('\n\n')
    questions = [b for b in blocks if b.startswith('[Open questions at the start of ')]
    if len(questions) != 1 or [b for b in blocks if b.startswith('[Research groups]')] != [extraction.GROUPS_INSTRUCTION]:
        raise ValueError('unidentifiable open-questions or research-groups block')
    view_ids = re.findall(r'^  - (v\d+) \(', questions[0], re.M)
    if not view_ids and not questions[0].endswith('\n  None yet.'):
        raise ValueError('empty open-questions block lacks the empty marker')
    if request['response_format']['json_schema']['schema'] != extraction.schema_for(version):
        raise ValueError('archived schema does not match the configuration')
    return version, view_ids


def part_b(archive_conn, items_conn, uni):
    reasons, examples = collections.Counter(), collections.defaultdict(list)
    judged = produced_e = kept_e = produced_c = kept_c = 0
    failures, configs, unverifiable = [], {}, collections.Counter()
    rows = list(archive_conn.execute("select config_version, config_checksum, request_sha256, request_json, answer_json from model_calls where purpose='extract'"))
    other = 0
    for config_version, checksum, sha, request_json, answer_json in rows:
        if any(marker in sha for marker in (':schema:', ':malformed:', ':refused:')):
            other += 1
            continue
        if ':' in sha:
            failures.append(f'unrecognized archive marker: {sha}')
            continue
        input_id = '(unidentified)'
        try:
            request = json.loads(request_json)
            user = next(m['content'] for m in request['messages'] if m['role'] == 'user')
            found = ITEM_ID.search(user)
            if not found:
                raise ValueError('unidentifiable stored extraction request')
            input_id = found.group(1) or found.group(2)
            row = items_conn.execute('select * from items where input_id=?', (input_id,)).fetchone()
            if row is None:
                raise ValueError(f'missing source item: {input_id}')
            item = testdb.item_of(row)
            if not re.fullmatch(r'[A-Za-z0-9_-]+', config_version or ''):
                raise ValueError('unidentifiable archived configuration')
            key = (config_version, checksum)
            if key not in configs:
                path = Path(ROOT) / 'poc' / 'config' / (config_version + '.json')
                if not path.exists():
                    raise Unverifiable(f'{config_version} (configuration retired)')
                cfg = config.load(str(path))
                if cfg.version != config_version or cfg.checksum != checksum:
                    raise ValueError(f'archived configuration mismatch: {config_version}')
                configs[key] = cfg
            cfg = configs[key]
            version, shown_ids = _preflight_extract_inputs(request, item, cfg)
            data = json.loads(answer_json)
            evidence, candidates, dropped, _ = extraction.sift_with_groups(data, item, item['text'] or '', set(shown_ids), uni)
            judged += 1
            produced_e += len(data.get('evidence', [])); kept_e += len(evidence)
            produced_c += len(data.get('candidates', [])); kept_c += len(candidates)
            for ident, why in dropped:
                reason = normalise_reason(why)
                reasons[reason] += 1
                examples[reason].append(f'{input_id[:48]} {ident}: {why[:80]}')
        except Unverifiable as error:
            unverifiable[str(error)] += 1
        except (ValueError, KeyError, TypeError, OSError, StopIteration) as error:
            failures.append(f'{input_id}: {error}')
    print(f'\n   extraction archive rows {len(rows)}: replayed {judged}, earlier refused {other}, retired {sum(unverifiable.values())}, '
          f'unidentifiable {len(failures)}')
    for version, count in sorted(unverifiable.items()):
        print(f'   not replayed: {version}: {count}')
    for error in failures:
        print(f'   cannot replay: {error}')
    print(f'   extraction answers {judged}: evidence produced {produced_e} kept {kept_e}; candidates produced {produced_c} kept {kept_c}')
    tally('B. current extraction checks before the handover, using the supplied universe', produced_e + produced_c, (produced_e - kept_e) + (produced_c - kept_c), reasons, examples)
    if failures:
        raise ValueError('source or archived configuration cannot be verified for all extraction calls')
    return judged


def shown_for_record(archive_conn, rec, decisions):
    """The theses a stored matching record was shown, or None when the record cannot be identified: a generative record by its
    archived request; a Jev record (its request hash combines several calls) by the theses its candidate reasons name."""
    request_row = archive_conn.execute('select request_json from model_calls where request_sha256=?', (rec['request_sha256'],)).fetchone()
    if request_row:
        user = json.loads(request_row['request_json'])['messages'][1]['content']
        return [{'view_id': v} for v in dict.fromkeys(MATCH_SHOWN.findall(user))]
    reasons = [x.get('reason', '') for x in decisions.get('candidates', []) + decisions.get('evidence', [])]
    if reasons and all(r.startswith('jev:') for r in reasons):
        return [{'view_id': v} for v in dict.fromkeys(JEV_ASKED.findall(' '.join(x.get('reason', '') for x in decisions.get('candidates', []))))]
    return None


def part_c(archive_conn, views_paths, uni):
    reasons, examples = collections.Counter(), collections.defaultdict(list)
    judged = refused_records = 0
    per_ledger = []
    for path in views_paths:
        ledger_judged, skipped = 0, collections.Counter()
        # matching.check writes suggested themes to the review pool, so it runs on a scratch copy, never on the real file
        scratch = os.path.join(tempfile.mkdtemp(), 'views.sqlite')
        shutil.copy(path, scratch)
        conn = sqlite3.connect(scratch)
        conn.row_factory = sqlite3.Row
        for rec in conn.execute('select input_id, call_no, shown_json, decisions_json, request_sha256 from match_records order by id'):
            handover_row = conn.execute('select handover_json from handovers where input_id=? order by id desc limit 1', (rec['input_id'],)).fetchone()
            if not handover_row or not rec['decisions_json']:
                skipped['no handover or no decision'] += 1
                continue
            shown_views = shown_for_record(archive_conn, rec, json.loads(rec['decisions_json']))
            if shown_views is None:
                skipped['request not in this archive'] += 1
                continue
            handover = json.loads(handover_row['handover_json'])
            shown = json.loads(rec['shown_json'])
            lists = matching.Lists(shown.get('candidates', {}), {tuple(k.split('|', 1)): v for k, v in shown.get('evidence', {}).items()})
            if rec['call_no'] <= 2:
                candidates, evidence = handover['candidates'], handover['evidence']
            else:                                   # the second call: candidate-linked evidence under its destination
                wanted = {k[0] for k in lists.evidence_lists}
                candidates, evidence = [], [dict(e, links=[k[1] for k in lists.evidence_lists if k[0] == e['id']]) for e in handover['evidence'] if e['id'] in wanted]
            try:
                checked = matching.check(conn, uni, json.loads(rec['decisions_json']), candidates, evidence, lists, shown_views)
            except Exception as error:
                key = 'check raised ' + type(error).__name__
                reasons[key] += 1; examples[key].append(f'{os.path.basename(os.path.dirname(path))} {rec["input_id"][:40]}: {error!r}'[:140])
                judged += 1; refused_records += 1; ledger_judged += 1
                continue
            judged += 1
            ledger_judged += 1
            if checked.refusals:
                refused_records += 1
            for refusal in checked.refusals:
                key = normalise_reason(refusal)
                reasons[key] += 1
                examples[key].append(f'{os.path.basename(os.path.dirname(path))} {rec["input_id"][:40]}: {refusal[:90]}')
        per_ledger.append((os.path.basename(os.path.dirname(path)) or path, ledger_judged, skipped))
    tally('C. matching code checks over stored records (database state is the final one, not the state at the time)', judged, refused_records, reasons, examples)
    unjudged = []
    for name, ledger_judged, skipped in per_ledger:
        print(f'       ledger {name}: judged {ledger_judged}, skipped {sum(skipped.values())} {dict(skipped) if skipped else ""}')
        if skipped and not ledger_judged:
            unjudged.append(name)
    if unjudged:
        print(f'NOT JUDGED: every matching record of {unjudged} was skipped; pass the archive these records were written with')
        return 0
    return judged


def part_d():
    """Every schema enum value appears in the prompt that asks for it: the extraction role and the judging prompt of the versions the
    code builds, and every matching prompt against its own version's set (Chinese up to matching-v1, English after)."""
    missing = []
    checks = [(f'role-{v}.txt', extraction.TIERS + vocabulary.KINDS + vocabulary.ASSET_LABELS) for v in extraction.SUPPORTED_VERSIONS]
    checks += [(f'{v}.txt', judging.PUSHES) for v in judging.SUPPORTED_VERSIONS]
    for path in sorted(glob.glob(os.path.join(config.PROMPTS, 'matching-v*.txt'))):
        version = os.path.basename(path).removesuffix('.txt')
        checks.append((os.path.basename(path), (matching.OUTCOMES + matching.EVIDENCE_OUTCOMES + vocabulary.DIRECTIONS) if matching.is_english(version)
                       else (matching.LEGACY_OUTCOMES + matching.LEGACY_EVIDENCE_OUTCOMES)))
    judged = 0
    for name, values in checks:
        text = open(os.path.join(config.PROMPTS, name), encoding='utf-8').read()
        for value in values:
            judged += 1
            if value not in text:
                missing.append(f'{name} lacks the enum value {value!r}')
    print(f'\n== D. schema enum values named in the prompts: judged {judged}, missing {len(missing)}')
    for line in missing:
        print('   ', line)
    return judged


def part_e(views_paths):
    """Keyed ledgers (keyed-views-plan.md 5): how many open views carry a key, how many keys collide among open views (the
    pipeline's identity rule says none should), and what the watch list sent to the review pool. A ledger written before
    keys is reported as unkeyed, not failed."""
    judged = 0
    for path in views_paths:
        conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
        conn.row_factory = sqlite3.Row
        tables = {r[0] for r in conn.execute("select name from sqlite_master where type='table'")}
        if 'view_keys' not in tables:
            print(f'\n== E. keyed views in {os.path.basename(path)}: unkeyed ledger (written before keys)')
            continue
        open_ids = {r[0] for r in conn.execute('select view_id from view_switches where id in (select max(id) from view_switches group by view_id) and open=1')}
        keys = collections.defaultdict(list)
        for r in conn.execute('select k.*, v.object_id from view_keys k join views v on v.view_id=k.view_id'):
            if r['view_id'] in open_ids:
                keys[(r['object_id'], r['measure'], r['scope_key'], r['period_start'], r['period_end'], r['basis'], r['unit'], r['event_type'])].append(r['view_id'])
        keyed = sum(len(v) for v in keys.values())
        collisions = {k: v for k, v in keys.items() if len(v) > 1}
        pool = conn.execute("select count(*) from review_pool_entries where kind='candidate_outside_watch'").fetchone()[0]
        judged += keyed
        print(f'\n== E. keyed views in {os.path.basename(path)}: open views {len(open_ids)}, keyed {keyed}, duplicate keys {len(collisions)} groups, review pool {pool} candidates outside the watch list')
        for k, v in list(collisions.items())[:10]:
            print(f'      {k[:3]} {k[3]}..{k[4]} → {v}')
    return judged


def part_f(archive_conn, views_paths):
    """Every accepted judgement replayed through the current judging checks, against the closed sets its stored request showed and the
    thesis's last judgement and card before it (never the ledger's latest)."""
    reasons, examples = collections.Counter(), collections.defaultdict(list)
    judged = refused = retired = 0
    accepted, missing = set(), []
    built = {open(config.prompt_path(v + '.txt'), encoding='utf-8').read(): v for v in judging.SUPPORTED_VERSIONS}   # a request's version is its system text
    for path in views_paths:
        conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
        conn.row_factory = sqlite3.Row
        has_cards = bool(conn.execute("select 1 from sqlite_master where type='table' and name='arguments'").fetchone())
        for j in conn.execute('select judgement_id, view_id, seq, request_sha256 from judgements order by seq, judgement_id').fetchall():
            accepted.add(j['request_sha256'])
            row = archive_conn.execute('select request_json, answer_json from model_calls where request_sha256=?', (j['request_sha256'],)).fetchone()
            if not row or not row[1]:
                missing.append(f'{os.path.basename(os.path.dirname(path))} {j["view_id"]} seq {j["seq"]}')
                continue
            request_json, answer_json = row[0], row[1]
            request = json.loads(request_json)
            user = next(m['content'] for m in request['messages'] if m['role'] == 'user')
            version = built.get(next((m['content'] for m in request['messages'] if m['role'] == 'system'), ''))
            if version is None:                  # a retired judging version: not judged by the current checks
                retired += 1
                continue
            card = judging.writes_card(version)
            last = conn.execute('select judgement_id, rung, reasons, changed, seq, publication_day from judgements where view_id=? and seq<? order by judgement_id desc limit 1',
                                (j['view_id'], j['seq'])).fetchone()
            last = dict(last) if last else None
            data = vocabulary.judgement_answer(json.loads(answer_json))
            if card:
                argument = conn.execute('select * from arguments where view_id=? and seq<? order by id desc limit 1', (j['view_id'], j['seq'])).fetchone() if has_cards else None
                argument = dict(argument, card=json.loads(argument['card_json'])) if argument else None
                errors = judging.check_card_answer(conn, j['view_id'], data, user, previous=(last, argument))
            else:
                errors = judging.check_answer(conn, j['view_id'], data, user, previous=(last, None))
            judged += 1
            if errors:
                refused += 1
            for error in errors:
                key = normalise_reason(error)
                reasons[key] += 1
                examples[key].append(f'{os.path.basename(os.path.dirname(path))} {j["view_id"]} seq {j["seq"]}: {error[:100]}')
    answers = [r[0] for r in archive_conn.execute("select request_sha256 from model_calls where purpose='judge'")]
    unverifiable = sum(1 for sha in answers if sha.split(':', 1)[0] not in accepted or ':' in sha)
    print(f'\n   judging answers in the archive {len(answers)}: accepted and replayed {judged}; of a retired judging version {retired}; '
          f'refused at the time or never committed, not verifiable {unverifiable}')
    tally('F. judging checks over every accepted judgement (each against its own request and the state before it)', judged, refused, reasons, examples)
    if missing:                          # a check whose input is incomplete has not judged the ledger (AGENTS §4)
        raise ValueError(f'{len(missing)} accepted judgements have no answer in the archive: ' + ', '.join(missing[:5]))
    return judged


def main():
    parser = argparse.ArgumentParser()
    frozen_draw = os.path.join(ROOT, 'poc', 'data', 'e2e-r9-frozen-v108-2026-11-03', 'd1')
    parser.add_argument('--archive', default=os.path.join(frozen_draw, 'archive.sqlite'))
    parser.add_argument('--items', default=os.path.join(ROOT, 'poc', 'data', 'items-nvda-2026-07-01-10-27.sqlite'))
    parser.add_argument('--views', nargs='*', default=None)
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    args = parser.parse_args()
    views_paths = args.views or [os.path.join(frozen_draw, 'views.sqlite')]
    archive_conn = sqlite3.connect(f'file:{args.archive}?mode=ro', uri=True)
    archive_conn.row_factory = sqlite3.Row
    items_conn = testdb.open_db(args.items)
    uni = universe.load(args.universe)
    print('preflight over', args.archive, 'and', len(views_paths), 'views databases:', ', '.join(os.path.basename(os.path.dirname(p)) for p in views_paths))
    part_a(archive_conn)
    counts = [part_b(archive_conn, items_conn, uni), part_c(archive_conn, views_paths, uni), part_d(), part_f(archive_conn, views_paths)]
    part_e(views_paths)          # informational for unkeyed ledgers; judged counts are reported per ledger
    if min(counts) == 0:
        print('\nUNEXERCISED: a check judged no case')
        sys.exit(1)
    print('\npreflight done')


if __name__ == '__main__':
    main()
