"""Preflight: run every code check and every prompt against the stored model answers before a paid run ($0).

AGENTS.md §3 "Strictness is code too" and §4 "a check must judge something": a check is accepted on real data,
reports how many cases it judged, and a check over an empty population is unexercised. This script replays what
the archive and the earlier runs' views databases already hold through the current code and prints, per check,
the cases judged, the cases refused and the reasons with examples:

  A. answers the schema refused (prompt and schema disagree: a value the prompt's wording suggested but the enum lacks)
  B. extraction's code checks (extraction.sift) over every stored extraction answer
  C. matching's code checks (matching.check) over every stored matching record, with the lists shown at the time
  D. every schema enum value appears verbatim in the prompt that asks for it

Usage: python3 scripts/preflight.py [--views DB ...]   (defaults: the archive, the window test database, the
current views database and every old-*/views.sqlite under poc/data). Exit status 1 when a check judged no case.
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

SCHEMAS = {'extract': extraction.SCHEMA, 'match': matching.SCHEMA, 'judge': judging.SCHEMA}
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
        for error in model.check_schema(json.loads(answer_json), SCHEMAS.get(purpose, {})):
            key = f'{purpose}: {normalise_reason(error)}'
            reasons[key] += 1
            examples[key].append(error[:140])
    tally('A. answers the schema refused (prompt/schema disagreements; empty when the provider enforces the schema server-side)', judged, judged, reasons, examples)
    return judged


class Unverifiable(Exception):
    """A stored request whose source this preflight cannot rebuild (a Chinese version, or v17's paragraph accounts): counted and
    named in the output, not replayed, and not a failure of the archive."""


def _preflight_extract_inputs(request, item, cfg):
    """Validate the stored source and recover exactly the IDs production showed."""
    setting = cfg.extraction_setting(item['category'])
    version = setting.prompt_version.rpartition('-')[2]
    if not extraction.is_english(version) or extraction.accounts(version):
        raise Unverifiable(f'extraction {version}')
    text = (item['text'] or '')[:extraction.MAX_TEXT_CHARS]          # production sends the first MAX_TEXT_CHARS characters
    user = next(m['content'] for m in request['messages'] if m['role'] == 'user')
    header = extraction.item_header(item, item['category'])
    if user.count(header) != 1:
        raise ValueError('source metadata does not match archived request')
    before, after = user.split(header, 1)
    if not after.startswith(text + '\n\nReturn evidence and candidates per the JSON schema.'):
        raise ValueError('source text does not match archived request')
    blocks = before.split('\n\n')
    views = [b for b in blocks if b.startswith('[Existing theses of these objects]')]
    groups = [b for b in blocks if b.startswith('[Research groups]')]
    if extraction.ledger_blind(version):
        if views or groups != [extraction.groups_block(())]:
            raise ValueError('archived blind request contains shown views or groups')
        view_ids, group_ids = [], []
    else:
        if len(views) != 1:
            raise ValueError('unidentifiable existing-theses block')
        view_lines = views[0].splitlines()[1:]
        view_ids = []
        for line in view_lines:
            match = re.match(r'^  - (v\d+) \(', line)
            if not match:
                raise ValueError('malformed existing-theses block')
            view_ids.append(match.group(1))
        if not view_ids and not views[0].startswith('[Existing theses of these objects] None yet.'):
            raise ValueError('empty existing-theses block lacks the empty marker')
        group_ids = []
        if extraction.has_groups(version):
            if len(groups) != 1:
                raise ValueError('unidentifiable research-groups block')
            for line in groups[0].splitlines()[1:]:
                match = re.match(r'^  - (g\d+) "', line)
                if not match:
                    raise ValueError('malformed research-groups block')
                group_ids.append(match.group(1))
            if not group_ids and groups[0] != extraction.groups_block(()):
                raise ValueError('empty research-groups block lacks the empty marker')
        elif groups:
            raise ValueError('unexpected research-groups block')
    schema = request['response_format']['json_schema']['schema']
    if schema != extraction.schema_for(version, group_ids, view_ids):
        raise ValueError('archived schema does not match configuration and shown IDs')
    return version, view_ids, group_ids


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
            item = dict(row)
            if not re.fullmatch(r'[A-Za-z0-9_-]+', config_version or ''):
                raise ValueError('unidentifiable archived configuration')
            key = (config_version, checksum)
            if key not in configs:
                path = Path(ROOT) / 'poc' / 'config' / (config_version + '.json')
                cfg = config.load(str(path))
                if cfg.version != config_version or cfg.checksum != checksum:
                    raise ValueError(f'archived configuration mismatch: {config_version}')
                configs[key] = cfg
            cfg = configs[key]
            version, shown_ids, group_ids = _preflight_extract_inputs(request, item, cfg)
            data = json.loads(answer_json)
            flat = extraction.flatten_account(data)
            evidence, candidates, dropped, _ = extraction.sift_with_groups(
                data, item, item['text'] or '', set(shown_ids), uni, english=extraction.is_english(version),
                shown_group_ids=group_ids, version=version, keep_unlinked=extraction.places(version))
            judged += 1
            produced_e += len(flat.get('evidence', [])); kept_e += len(evidence)
            produced_c += len(flat.get('candidates', [])); kept_c += len(candidates)
            for ident, why in dropped:
                reason = normalise_reason(why)
                reasons[reason] += 1
                examples[reason].append(f'{input_id[:48]} {ident}: {why[:80]}')
        except Unverifiable as error:
            unverifiable[str(error)] += 1
        except (ValueError, KeyError, TypeError, OSError, StopIteration) as error:
            failures.append(f'{input_id}: {error}')
    print(f'\n   extraction archive rows {len(rows)}: replayed {judged}, earlier refused {other}, source not rebuildable {sum(unverifiable.values())}, '
          f'unidentifiable {len(failures)}')
    for version, count in sorted(unverifiable.items()):
        print(f'   not replayed, source not rebuildable for {version}: {count}')
    for error in failures:
        print(f'   cannot replay: {error}')
    print(f'   extraction answers {judged}: evidence produced {produced_e} kept {kept_e}; candidates produced {produced_c} kept {kept_c}')
    tally('B. current extraction checks before placement, using the supplied universe', produced_e + produced_c, (produced_e - kept_e) + (produced_c - kept_c), reasons, examples)
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
    missing = []
    # each prompt file is checked against the enum set of its own version: Chinese up to role-v5 / matching-v1 / judging-v2, English after
    checks = [
        ('role', lambda v: (extraction.TIERS + vocabulary.KINDS + vocabulary.ASSET_LABELS) if extraction.is_english(v)
                 else (extraction.LEGACY_TIERS + extraction.LEGACY_KINDS + list(vocabulary.LEGACY['label'])[:5])),
        ('matching', lambda v: (matching.OUTCOMES + matching.EVIDENCE_OUTCOMES + vocabulary.DIRECTIONS) if matching.is_english(f'matching-{v}')
                     else (matching.LEGACY_OUTCOMES + matching.LEGACY_EVIDENCE_OUTCOMES)),
        ('judging', lambda v: judging.PUSHES if judging.is_english(f'judging-{v}') else judging.LEGACY_PUSHES),
    ]
    judged = 0
    for kind, values_of in checks:
        for path in sorted(glob.glob(os.path.join(config.PROMPTS, f'{kind}-v*.txt'))):
            text = open(path, encoding='utf-8').read()
            version = os.path.basename(path).rpartition('-')[2].removesuffix('.txt')
            for value in values_of(version):
                judged += 1
                if value not in text:
                    missing.append(f'{os.path.basename(path)} lacks the enum value {value!r}')
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', default=os.path.join(ROOT, 'poc', 'data', 'archive.sqlite'))
    parser.add_argument('--items', default=os.path.join(ROOT, 'poc', 'data', 'items-window.sqlite'))
    parser.add_argument('--views', nargs='*', default=None)
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    args = parser.parse_args()
    views_paths = args.views or [p for p in [os.path.join(ROOT, 'poc', 'data', 'views.sqlite')] + sorted(glob.glob(os.path.join(ROOT, 'poc', 'data', 'old-*', 'views.sqlite'))) if os.path.exists(p)]
    archive_conn = sqlite3.connect(f'file:{args.archive}?mode=ro', uri=True)
    archive_conn.row_factory = sqlite3.Row
    items_conn = testdb.open_db(args.items)
    uni = universe.load(args.universe)
    print('preflight over', args.archive, 'and', len(views_paths), 'views databases:', ', '.join(os.path.basename(os.path.dirname(p)) for p in views_paths))
    part_a(archive_conn)
    counts = [part_b(archive_conn, items_conn, uni), part_c(archive_conn, views_paths, uni), part_d()]
    part_e(views_paths)          # informational for unkeyed ledgers; judged counts are reported per ledger
    if min(counts) == 0:
        print('\nUNEXERCISED: a check judged no case')
        sys.exit(1)
    print('\npreflight done')


if __name__ == '__main__':
    main()
