"""Replay a stored draw of the frozen v108 run through the current code with no paid call ($0).

Every model and Jev request is answered from a copy of the draw's archive: an accepted answer by its request hash, and an answer
the code refused at the time by the same hash's refused row, in the order it was given, so the code refuses it again as it did.
A request the archive cannot answer stops the run (a BaseException the pipeline cannot record as an item failure).
It writes the request bytes as built (key order kept) per archive key, and a digest of the ledger beside the stored ledger's.

usage: python3 cached_replay.py <draw folder> <output folder> [config]   (config: poc/config/poc-v108.json by default)

Kept with the argument-card work (log.md step 1, H1): it proves a code change leaves the frozen v108 path byte for byte as it was. The
ledger comparison leaves out the arguments table and the arrival_use_json column, which judging-v8 adds and v7 never writes.
"""
import hashlib
import json
import os
import shutil
import sqlite3
import sys
import threading

ROOT = '/Users/lchingen/hivemind'
sys.path.insert(0, os.path.join(ROOT, 'src'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from hivemind import jev, model  # noqa: E402


class ArchiveMiss(BaseException):
    pass


draw_folder, output_folder = sys.argv[1], sys.argv[2]
os.makedirs(output_folder, exist_ok=False)
cache_path = os.path.join(output_folder, 'archive.sqlite')
shutil.copyfile(os.path.join(draw_folder, 'archive.sqlite'), cache_path)
views_path = os.path.join(output_folder, 'views.sqlite')

lookup_lock = threading.Lock()
stored = sqlite3.connect(f'file:{os.path.join(draw_folder, "archive.sqlite")}?mode=ro', uri=True, check_same_thread=False)
refused_given = {}
built_requests = {}
misses = []


def stored_refused_answer(request):
    _, sha = model.request_identity(request)
    with lookup_lock:
        rows = stored.execute("select call_id, response_json from model_calls where request_sha256 like ? order by call_id", (sha + ':%',)).fetchall()
        index = refused_given.get(sha, 0)
        if index >= len(rows):
            misses.append(sha)
            raise ArchiveMiss(f'no stored answer for request {sha[:12]}')
        refused_given[sha] = index + 1
        return json.loads(rows[index][1])


def refuse_key(*arguments):
    raise ArchiveMiss('a credential was asked for: the request was not in the archive')


original_build_request, original_request_for = model.build_request, jev.request_for


def recording_build_request(*arguments, **keywords):
    request = original_build_request(*arguments, **keywords)
    with lookup_lock:
        built_requests[model.request_identity(request)[1]] = hashlib.sha256(json.dumps(request, ensure_ascii=False).encode()).hexdigest()
    return request


def recording_request_for(*arguments, **keywords):
    request = original_request_for(*arguments, **keywords)
    with lookup_lock:
        built_requests[model.request_identity(request)[1]] = hashlib.sha256(json.dumps(request, ensure_ascii=False).encode()).hexdigest()
    return request


model._key = refuse_key
jev._key = refuse_key
model.build_request = recording_build_request
jev.request_for = recording_request_for
model.openai_transport = lambda provider, request, timeout=180: stored_refused_answer(request)
jev.transport = lambda request, timeout=60: stored_refused_answer(request)

import replay as replay_script  # noqa: E402

config_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(ROOT, 'poc/config/poc-v108.json')
sys.argv = ['replay.py', '--from', '2026-07-01', '--until', '2026-07-14', '--only', 'NVDA', '--config', config_path,
            '--views', views_path, '--archive', cache_path, '--testdb', os.path.join(ROOT, 'poc/data/items-nvda-2026-07-01-10-27.sqlite'),
            '--workers', '16', '--seed', os.path.join(ROOT, 'poc/seeds/nvda-2026-07-01-v2.json')]
try:
    replay_script.main()
finally:
    json.dump(dict(sorted(built_requests.items())), open(os.path.join(output_folder, 'built-requests.json'), 'w'), indent=0)
    json.dump({'misses': misses, 'refused_answers_given': sum(refused_given.values())}, open(os.path.join(output_folder, 'misses.json'), 'w'))

VOLATILE = {'at', 'created_at', 'updated_at', 'seconds', 'completed_at', 'arrival_use_json'}
ADDED_TABLES = {'arguments'}


def ledger_digest(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    digest = {}
    for (table,) in conn.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%' and name not like '%fts%' order by name"):
        if table in ADDED_TABLES:
            continue
        columns = [c[1] for c in conn.execute(f'pragma table_info("{table}")') if c[1] not in VOLATILE]
        rows = sorted(json.dumps(r, ensure_ascii=False, default=str) for r in conn.execute(f'select {",".join(chr(34) + c + chr(34) for c in columns)} from "{table}"'))
        digest[table] = (len(rows), hashlib.sha256('\n'.join(rows).encode()).hexdigest()[:16])
    return digest


replayed, original = ledger_digest(views_path), ledger_digest(os.path.join(draw_folder, 'views.sqlite'))
differ = {t: (original.get(t), replayed.get(t)) for t in sorted(set(replayed) | set(original)) if replayed.get(t) != original.get(t)}
json.dump({'replayed': replayed, 'original': original, 'differ': differ}, open(os.path.join(output_folder, 'ledger-digest.json'), 'w'), indent=1)
print(f'requests built: {len(built_requests)}; misses: {len(misses)}; refused answers replayed: {sum(refused_given.values())}')
print(f'ledger tables: {len(replayed)}; differing from the stored ledger: {len(differ)}')
for table, (before, after) in differ.items():
    print(f'  {table}: stored {before} replayed {after}')
