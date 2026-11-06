"""The architecture benchmark's measurement harness (plan-final C-8.1, adopted 2026-11-05). One draw of one configuration over the frozen
ruler's window (2026-07-01..07-14, NVDA) from a ledger that holds the 22 frozen seed questions as a labelled measurement fixture: the seeds are
part of the frozen ruler (AGENTS §7.1) and the judgement scorer refuses a run whose seed questions differ. `scripts/replay.py` keeps refusing
seeded ledgers (D370); this harness is a measurement, never the product's entry point, and calls the same `hivemind.replay.run` the entry point
calls: the frozen configuration through the parallel day as its control draws ran, a split configuration item by item.

Every draw starts from one fixture ledger (`fixture/views.sqlite`: the 22 seeds planted once, its sha256 recorded in each draw's manifest), so
both arms begin from the byte-identical ledger. Each draw's manifest records the sha256 of the configuration, every prompt file it names, every
`src/hivemind` module and this harness, and the names of the files changed since the last commit.

--offline answers every request from the archive and refuses any other: the comparability gate replays a stored draw at no cost.

  PYTHONPATH=src python3 docs/research/2026-11-06-architecture-benchmark/bench_run.py --config C --run-folder F [--offline] [--archive-from A]"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, model, parallel_day, replay, seeding, universe  # noqa: E402
from hivemind.views import store  # noqa: E402

SEED = os.path.join(ROOT, 'poc', 'seeds', 'nvda-2026-07-01-v2.json')
SEED_SHA256 = 'fca16f42dd7153e852c42527883552b86567f33d7e1ed3c11ef600c8a37037d6'
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
ITEMS_SHA256 = '57bc25441fea325b8a1fe0a6e064640c3337f56c1943824e60367ddd9ce3ccd8'
WINDOW = ('2026-07-01', '2026-07-14')
FIXTURE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixture', 'views.sqlite')
SCORING = ['/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/score_gold.py',
           '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/final-2026-10-30/final_scores.py',
           '/Users/lchingen/hivemind/docs/research/2026-10-31-reference-context/score_ref.py',
           '/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py',
           '/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json',
           '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json',
           '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-test.json',
           '/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html']


def sha(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


class ReplayArchive(model.Archive):
    """For --offline only: a request with no accepted answer whose stored answer a code check refused (its archive key carries the ':refused:'
    suffix, `model.Archive.retire`) is answered with that refused answer once, so the check refuses it again and the retry the draw sent is
    answered from the archive in turn. Checked on the gate's archive only (r10-control-v108/d1: seven refused judgements, none with an accepted
    answer under the same key, every retry found); not a general replay of an archive's order."""

    def __init__(self, path):
        super().__init__(path)
        self.used_refusals = set()

    def lookup(self, sha):
        hit = super().lookup(sha)
        if hit:
            return hit
        with self.lock:
            for row in self.conn.execute('select call_id, answer_json, prompt_chars, input_tokens, output_tokens from model_calls '
                                         'where request_sha256 like ? order by call_id', (sha + ':refused:%',)):
                if row[0] not in self.used_refusals:
                    self.used_refusals.add(row[0])
                    return row
        return None


class Offline:
    """A transport that refuses every request the archive could not answer, and counts them."""

    def __init__(self):
        self.refused = 0

    def __call__(self, *parameters):
        self.refused += 1
        raise model.TransportError('offline: request not in the archive')


def fixture():
    """The seeded starting ledger every draw copies; written once."""
    if not os.path.exists(FIXTURE):
        os.makedirs(os.path.dirname(FIXTURE), exist_ok=True)
        conn = store.open_db(FIXTURE)
        seeding.seed_views(conn, SEED, created_at=WINDOW[0] + 'T00:00:00Z')
        conn.close()
    return FIXTURE


def pinned_files(config_path):
    here = os.path.dirname(os.path.abspath(__file__))
    files = [config_path, os.path.join(ROOT, 'poc', 'universe.json'), SEED] + [os.path.join(here, n) for n in os.listdir(here) if n.endswith('.py')] + SCORING
    for folder, _, names in os.walk(os.path.join(ROOT, 'src', 'hivemind')):
        files += [os.path.join(folder, n) for n in names if n.endswith('.py')]
    raw = json.load(open(config_path))
    stems = set()

    def walk(value):
        if isinstance(value, dict):
            for v in value.values():
                walk(v)
        elif isinstance(value, list):
            for v in value:
                walk(v)
        elif isinstance(value, str) and len(value) < 60 and ' ' not in value:
            stems.add(value)
            found = re.fullmatch(r'T\d+-v(\d+[a-z]?)', value)
            if found:
                stems.update(f'{stem}-v{found.group(1)}' for stem in ('role', 'categories', 'review'))
    walk(raw)
    for stem in stems:
        for extension in ('txt', 'json'):
            path = os.path.join(ROOT, 'src', 'hivemind', 'prompts', f'{stem}.{extension}')
            if os.path.exists(path):
                files.append(path)
    pins = {os.path.relpath(f, ROOT) if f.startswith(ROOT) else f: sha(f) for f in sorted(set(files))}
    pins['fixture'] = sha(fixture())
    pins['items'] = ITEMS_SHA256
    return pins


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--run-folder', required=True)
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--archive-from', help='copy this archive into a new run folder first (identical requests are answered from it)')
    parser.add_argument('--workers', type=int, default=8, help='extraction workers of the frozen configuration\'s parallel day (its control draws: 8)')
    parser.add_argument('--cap', type=float, default=5.0)
    args = parser.parse_args()
    folder = os.path.abspath(args.run_folder)
    os.makedirs(folder, exist_ok=True)
    views, archive_path = os.path.join(folder, 'views.sqlite'), os.path.join(folder, 'archive.sqlite')
    if sha(SEED) != SEED_SHA256:
        raise SystemExit('the seed file differs from the frozen ruler\'s')
    items = os.path.join(folder, 'items.sqlite')
    if not os.path.exists(items):
        shutil.copyfile(ITEMS, items)
    if sha(items) != ITEMS_SHA256:
        raise SystemExit('the items database differs from the one the frozen ruler\'s draws read')
    if args.archive_from and not args.offline:
        raise SystemExit('--archive-from is for the offline gate only: a paid draw re-sends every request from an empty archive')
    if args.archive_from and not os.path.exists(archive_path):
        shutil.copyfile(args.archive_from, archive_path)
    cfg = config.load(args.config)
    split_mode = cfg.split is not None
    git = lambda *a: subprocess.run(['git', '-C', ROOT, *a], capture_output=True, text=True).stdout.strip()
    manifest_path = os.path.join(folder, 'manifest.json')
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {}
    pins = pinned_files(os.path.abspath(args.config))
    if not manifest.get('runs') and (os.path.exists(views) or (os.path.exists(archive_path) and not args.archive_from)):
        raise SystemExit(f'{folder} holds a ledger or an archive without a manifest: use a new run folder')
    if manifest.get('runs') and manifest['runs'][0]['offline'] != args.offline:
        raise SystemExit('refused: this folder began in the other mode (offline gate or paid draw); a draw keeps one mode; use a new run folder')
    if manifest.get('runs') and (manifest['runs'][0]['files_sha256'] != pins or manifest['runs'][0]['config'] != args.config):
        changed = sorted(k for k in set(pins) | set(manifest['runs'][0]['files_sha256']) if pins.get(k) != manifest['runs'][0]['files_sha256'].get(k))
        raise SystemExit(f'refused: this draw began under other files {changed[:8]}; a resumed draw must run the same version; use a new run folder')
    manifest.setdefault('runs', []).append({
        'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), 'code_commit': git('rev-parse', 'HEAD'),
        'tree_dirty_files': [l for l in git('status', '--short', '--', 'src', 'scripts', 'poc/config', 'docs/research/2026-11-06-architecture-benchmark').splitlines() if l.strip()],
        'files_sha256': pins, 'config': args.config, 'config_version': cfg.version,
        'config_checksum': cfg.checksum, 'config_sha256': sha(args.config), 'seed_sha256': SEED_SHA256, 'items_sha256': ITEMS_SHA256,
        'window': WINDOW, 'offline': args.offline, 'archive_from': args.archive_from, 'workers': None if split_mode else args.workers})
    if args.offline:                                 # the gate: seeded in place, as the stored draw was
        conn = store.open_db(views)
        seeding.seed_views(conn, SEED, created_at=WINDOW[0] + 'T00:00:00Z')
        conn.close()
    elif not os.path.exists(views):
        shutil.copyfile(fixture(), views)
    manifest['runs'][-1]['fixture_sha256'] = sha(fixture()) if not args.offline else None
    json.dump(manifest, open(manifest_path, 'w'), indent=1)
    seeded = [v['view_id'] for v in json.load(open(SEED))['questions']]
    log_file = open(os.path.join(folder, 'replay.log'), 'a', encoding='utf-8')

    def log(*parts):
        line = ' '.join(str(p) for p in parts)
        print(line, flush=True)
        log_file.write(line + '\n')
        log_file.flush()
    log(f'--- bench {WINDOW[0]}..{WINDOW[1]} config {cfg.version}/{cfg.checksum} offline {args.offline} seeded {len(seeded)} split {split_mode}')
    day_runner = None if split_mode else parallel_day.ParallelDay(
        items, os.path.join(folder, 'manifests'), extraction_workers=args.workers, jev_workers=8 if cfg.matching.engine == 'jev' else 1)
    offline = Offline() if args.offline else None
    totals = replay.run(testdb_path=items, views_path=views, archive=(ReplayArchive if args.offline else model.Archive)(archive_path), cfg=cfg, universe=universe.load(os.path.join(ROOT, 'poc', 'universe.json')),
                        from_day=WINDOW[0], until_day=WINDOW[1], spend_cap_usd=args.cap, log=log, only_objects={'NVDA'}, day_runner=day_runner,
                        matching_workers=8 if split_mode else 1, transport=offline)
    log('totals:', totals)
    if offline is not None:
        log('offline refusals:', offline.refused)
    manifest = json.load(open(manifest_path))
    manifest['runs'][-1]['finished_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    json.dump(manifest, open(manifest_path, 'w'), indent=1)
    print('BENCH-DONE', flush=True)


if __name__ == '__main__':
    main()
