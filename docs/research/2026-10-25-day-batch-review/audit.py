"""Read D170 ledgers to measure day-start visibility and batching headroom.

The timing projection reuses recorded durations. It does not call a provider,
predict rate limits, simulate new model answers or certify batching semantics.
"""
import argparse
import collections
import contextlib
import datetime
import hashlib
import heapq
import json
from pathlib import Path
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[3]
ARMS = {'jev': ('english-v23-jev-2026-10-25', 'poc-v23'),
        'llm': ('english-v23-llm-2026-10-25', 'poc-v23-llm')}
ITEM = re.compile(r'^\[Item\] id (.+?), category .*?published (\d{4}-\d{2}-\d{2}), title:', re.M)
VIEW = re.compile(r'^  - (v\d+) \(', re.M)
GROUP = re.compile(r'^  - (g\d+)\b', re.M)


def fingerprint(path):
    result = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def connect(path):
    if not path.is_file():
        raise ValueError(f'missing input {path}')
    conn = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return contextlib.closing(conn)


def wave(durations, workers):
    """Fixed-order, work-conserving scheduling; no duration-based clairvoyance."""
    heap = [0.0] * workers
    for duration in durations:
        heapq.heappush(heap, heapq.heappop(heap) + duration)
    return max(heap)


def epoch(stamp):
    return datetime.datetime.fromisoformat(stamp).timestamp()


def audit_arm(folder, config):
    base = ROOT / 'poc/data' / folder
    paths = [base / 'views.sqlite', base / 'archive.sqlite']
    hashes = {p.name: fingerprint(p) for p in paths}
    with connect(paths[0]) as db, connect(paths[1]) as archive:
        items = {r['input_id']: dict(r) for r in db.execute(
            "select input_id, min(sequence_no) seq, min(publication_day) day, min(at) started "
            "from processing_steps where sequence_no>0 and input_id not like 'day:%' group by input_id")}
        hands = {r['input_id']: json.loads(r['handover_json']) for r in db.execute('select * from handovers order by id')}
        views = {r['view_id']: dict(r) for r in db.execute('select * from views')}
        pieces = {r['evidence_id']: dict(r) for r in db.execute('select * from evidence')}
        groups = {r['group_id']: dict(r) for r in db.execute('select * from thesis_groups')}
        calls = [dict(r) for r in archive.execute('select * from model_calls where config_version=? order by call_id', (config,))]
        if not calls or not hands:
            raise ValueError(f'unexercised {folder}')
        examples = collections.defaultdict(list)
        counts = collections.Counter()

        def same_day(target, item, seq_field='created_seq'):
            return (target[seq_field] < item['seq']
                    and items[target['created_from_input']]['day'] == item['day'])

        def hit(kind, detail):
            counts[kind] += 1
            if len(examples[kind]) < 3:
                examples[kind].append(detail)

        extraction_calls, call_item = {}, {}
        per_day_records = collections.defaultdict(lambda: [0, 0])
        last_input = None
        days = collections.defaultdict(lambda: {'extract': [], 'match': [], 'judge': []})
        judge_days = {r['call_id']: r['publication_day'] for r in db.execute('select call_id,publication_day from judgements')}
        for call in calls:
            if call['purpose'] == 'extract':
                user = json.loads(call['request_json'])['messages'][1]['content']
                found = ITEM.search(user)
                if not found or found[1] not in items:
                    raise ValueError(f'unidentified extraction call {call["call_id"]}')
                last_input, day = found.groups()
                if day != items[last_input]['day']:
                    raise ValueError('request day disagrees with processing day')
                extraction_calls[last_input] = call
                call_item[call['call_id']] = last_input
            elif call['purpose'] == 'match':
                if last_input is None:
                    raise ValueError('matching precedes its extraction')
                day = items[last_input]['day']
                call_item[call['call_id']] = last_input
            elif call['purpose'] == 'judge':
                if call['call_id'] not in judge_days:
                    raise ValueError(f'unrecorded judgement {call["call_id"]}')
                day = judge_days[call['call_id']]
            else:
                raise ValueError(f'unexpected purpose {call["purpose"]}')
            days[day][call['purpose']].append(call['seconds'])
        if set(extraction_calls) != set(hands):
            raise ValueError('handover/extraction population differs')
        for input_id, hand in hands.items():
            item = items[input_id]
            for index, field in enumerate(('candidates', 'evidence')):
                counts[f'cross_item_same_day_{field}_pairs'] += per_day_records[item['day']][index] * len(hand[field])
                per_day_records[item['day']][index] += len(hand[field])
            call = extraction_calls[input_id]
            user = json.loads(call['request_json'])['messages'][1]['content']
            context = user.split('[Existing theses of these objects]', 1)[1].split('[Item]', 1)[0]
            shown_views = VIEW.findall(context)
            shown_groups = GROUP.findall(context)
            if any(same_day(views[v], item) for v in shown_views):
                hit('extractions_shown_same_day_thesis', {'input_id': input_id, 'day': item['day']})
            if any(same_day(groups[g], item) for g in shown_groups):
                hit('extractions_shown_same_day_group', {'input_id': input_id, 'day': item['day']})
            for evidence in hand['evidence']:
                for target in evidence['links']:
                    counts['handover_evidence_links'] += 1
                    if target in views and same_day(views[target], item):
                        hit('evidence_links_to_same_day_thesis', {'input_id': input_id, 'id': evidence['id'], 'target': target,
                                                                'quote': evidence['quote'][:240], 'target_question': views[target]['question']})
            for candidate in hand['candidates']:
                for target in candidate.get('group_refs', []):
                    counts['candidate_group_refs'] += 1
                    if target in groups and same_day(groups[target], item):
                        hit('candidate_refs_same_day_group', {'input_id': input_id, 'id': candidate['id'], 'target': target})
            counts['candidates'] += len(hand['candidates'])
            counts['new_group_declarations'] += len(hand.get('new_groups', []))
            counts['evidence'] += len(hand['evidence'])
        final = {}
        for row in db.execute('select * from match_records order by id'):
            if row['call_id'] == 0 and not row['request_sha256']:
                counts['matching_records_without_api_call'] += 1
            elif call_item.get(row['call_id']) != row['input_id']:
                raise ValueError(f'matching call attribution differs: {row["id"]}')
            final[(row['input_id'], 1 if row['call_no'] <= 2 else 2)] = dict(row)
        pair_decisions = {}
        for (input_id, phase), row in final.items():
            if json.loads(row['checks_json'])['refusals']:
                raise ValueError(f'final matching attempt refused: {input_id}')
            item = items[input_id]
            answer = json.loads(row['decisions_json'])
            for decision in answer['candidates']:
                counts['candidate_decisions'] += 1
                target = decision.get('target_view_id')
                if target in views and same_day(views[target], item):
                    hit('candidate_decisions_to_same_day_thesis', {'input_id': input_id, **decision})
            for decision in answer['evidence']:
                pair_decisions[(input_id, decision['id'], decision['view_id'])] = decision
        for (input_id, _, _), decision in pair_decisions.items():
            counts['evidence_pair_decisions'] += 1
            if decision['outcome'] not in ('repeat', 'replace'):
                continue
            counts['repeat_replace_decisions'] += 1
            target = decision.get('target_evidence_id')
            if target not in pieces:
                raise ValueError(f'missing evidence target: {target}')
            if same_day(pieces[target], items[input_id]):
                hit('repeat_replace_targets_same_day', {'input_id': input_id, **decision,
                                                       'target_quote': pieces[target]['quote'][:240]})
        timing = []
        for day, stages in sorted(days.items()):
            first = min(epoch(i['started']) for i in items.values() if i['day'] == day)
            completed = db.execute('select at from days_completed where day=?', (day,)).fetchone()
            if not completed:
                raise ValueError(f'incomplete day {day}')
            elapsed = epoch(completed[0]) - first
            projected = {}
            for workers in (6, 12, 24, 32):
                # Optimistic: all existing judge and match calls independent; new reconciliation work omitted.
                seconds = sum(wave(stages[stage], workers) for stage in ('extract', 'match', 'judge'))
                projected[str(workers)] = {'seconds': round(seconds, 2),
                                           'ratio_to_observed': round(elapsed / seconds, 2) if seconds else None}
            timing.append({'day': day, 'observed_seconds': elapsed,
                           'counts': {k: len(v) for k, v in stages.items()},
                           'recorded_work_seconds': {k: round(sum(v), 2) for k, v in stages.items()},
                           'longest_call_seconds': max(max(v, default=0) for v in stages.values()),
                           'unlimited_workers_stage_floor': round(sum(max(v, default=0) for v in stages.values()), 2),
                           'optimistic_projection': projected})
        collisions = collections.Counter(c['id'] for h in hands.values() for c in h['candidates'])
        counts['reused_candidate_local_ids'] = sum(n > 1 for n in collisions.values())
        counts['handover_count'] = len(hands)
        counts['dependency_rows'] = db.execute('select count(*) from dependencies').fetchone()[0]
        result = {'folder': folder, 'config': config, 'hashes': hashes, 'counts': dict(counts),
                  'examples': dict(examples), 'timing': timing,
                  'projection_limits': ['recorded durations reused; no new call measurements',
                                        'judgement dependencies relaxed: optimistic only',
                                        'extra reconciliation calls, rate limits and token limits omitted',
                                        'observed time may include pauses; sum-of-work ratio is not wall-clock speedup']}
    if hashes != {p.name: fingerprint(p) for p in paths}:
        raise ValueError('input changed during audit')
    return result


def gold_inventory():
    result = {}
    for name in ('week-benchmark-v23-2026-10-25.json', 'august-benchmark-v23-2026-10-25.json'):
        path = ROOT / 'poc/eval/gold' / name
        raw = json.loads(path.read_text())
        result[name] = {'sha256': fingerprint(path), 'labelled_by': raw['_about'],
                        'candidate_labels': {k: len(v) for k, v in raw['candidates'].items() if not k.startswith('_')},
                        'membership_groups': {k: len(v) for k, v in raw['memberships'].items() if not k.startswith('_')}}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error('output exists; choose a new dated report')
    result = {'baseline_commit': 'da06fbd', 'arms': {k: audit_arm(*v) for k, v in ARMS.items()}, 'golds': gold_inventory()}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x') as handle:
        json.dump(result, handle, indent=2)
    for name, arm in result['arms'].items():
        print(name, json.dumps(arm['counts']))
        print('July 27:', next(d for d in arm['timing'] if d['day'] == '2026-07-27'))


if __name__ == '__main__':
    main()
