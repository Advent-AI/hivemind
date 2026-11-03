"""Read-only latency accounting for the two completed trials; no provider calls."""
import heapq
import json
from pathlib import Path
import re
import sqlite3

HERE = Path(__file__).resolve().parent


def connect(path):
    conn = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def profile(name, attempts):
    folder = HERE / name
    result = json.loads((folder / 'result.json').read_text())
    assert result['failure'] is None and result['audit']['errors'] == []
    # A request hash can recur in another trial. Bind to this trial's attempt IDs.
    own = [attempts[a['id']] for a in result['new_attempts']]
    accepted = {a['request_sha256'] for a in result['audit']['accepted_requests']}
    totals = {k: 0.0 for k in ('accepted_extract', 'discarded_extract', 'match', 'judge')}
    calls, judges = [], []
    with connect(folder / 'archive.sqlite') as conn:
        for row in conn.execute('select * from model_calls order by call_id'):
            matches = [a for a in own if a['request_sha256'] == row['request_sha256']]
            assert len(matches) == 1, (name, row['call_id'])
            attempt = matches[0]
            assert attempt['state'] == 'complete'
            usage = json.loads(attempt['response_json'])['usage']
            token_key = 'prompt_tokens' if attempt['provider'] == 'openai' else 'input_tokens'
            assert usage[token_key] == row['input_tokens']
            request = json.loads(row['request_json'])
            category = row['purpose']
            target = ''
            if category == 'extract':
                category = 'accepted_extract' if row['request_sha256'] in accepted else 'discarded_extract'
                target = re.search(r'^\[Item\] id (.+?), category ', request['messages'][1]['content'], re.M)[1]
            elif category == 'judge':
                target = re.search(r'^Thesis (\S+)', request['messages'][1]['content'])[1]
                judges.append((attempt['id'], attempt['seconds']))
            totals[category] += attempt['seconds']
            calls.append({'archive_call_id': row['call_id'], 'journal_attempt_id': attempt['id'],
                          'category': category, 'target': target, 'provider_seconds': attempt['seconds'],
                          'caller_seconds_including_wait': row['seconds'],
                          'output_tokens': row['output_tokens']})
    with connect(folder / 'views.sqlite') as conn:
        assert conn.execute('select count(*) from dependencies').fetchone()[0] == 0
        phases = [len(json.loads(r['shown_json'])['requests']) for r in conn.execute(
            'select shown_json from match_records where seq>=21 order by id')]
    # Both trials have independent judgments; the transport admits two at once.
    # This is a schedule estimate from recorded durations, not a new timing run.
    workers = [0.0, 0.0]
    for _, duration in sorted(judges):
        heapq.heappush(workers, heapq.heappop(workers) + duration)
    judge_wall = max(workers)
    critical = totals['accepted_extract'] + totals['match'] + judge_wall
    residual = result['seconds'] - critical
    assert abs(residual) < 1, (name, residual)
    return {'wall_seconds': result['seconds'], 'provider_time_sums': totals,
            'judge_count': len(judges), 'judge_wall_seconds_estimate': judge_wall,
            'nonprovider_residual_seconds_estimate': residual,
            'matching_jobs_per_phase': phases, 'calls': calls,
            'accepted_extractions': len(accepted),
            'stale_preparations': sum(e['event'] == 'stale' for e in result['events']),
            'reused_preparations': sum(e['event'] == 'reused' for e in result['events'])}


with connect(HERE / 'budget.sqlite') as conn:
    attempts = {r['id']: dict(r) for r in conn.execute('select * from attempts')}
rows = {name: profile(name, attempts) for name in ('control-1', 'concurrent-1')}
control, concurrent = rows['control-1'], rows['concurrent-1']
assert concurrent['matching_jobs_per_phase'] == [1, 1, 1]
assert concurrent['stale_preparations'] == 2
same_work_serial = (concurrent['provider_time_sums']['accepted_extract']
                    + concurrent['provider_time_sums']['match']
                    + concurrent['judge_wall_seconds_estimate'])
print(json.dumps({'scope': 'Two completed trials only; timing sums use trial-scoped journal attempts.',
                  'trials': rows,
                  'observed_wall_reduction_seconds': control['wall_seconds'] - concurrent['wall_seconds'],
                  'judge_wall_reduction_seconds_estimate': control['judge_wall_seconds_estimate'] - concurrent['judge_wall_seconds_estimate'],
                  'same_accepted_work_serial_provider_path_seconds_estimate': same_work_serial,
                  'inference': 'No usable later-item extraction overlap and one Jev job per concurrent matching phase. The recorded accepted-work schedule remains serial; the raw wall-time difference does not isolate concurrency benefit.'}, indent=2))
