#!/usr/bin/env python3
"""The D392 control: production configuration poc-v108 re-run on a ledger seeded with the 22 seed questions, 2026-07-01..07-14.

`scripts/replay.py` refuses seeded ledgers, so this harness calls `hivemind.replay.run` itself, with the arguments the 11-03 reference
run passed (`poc/data/e2e-r9-frozen-v108-2026-11-03/d1/manifest.json`; launcher `docs/research/2026-11-01-e2e-loop/harness/run_arm.sh`
at commit a907eba, which called `scripts/replay.py --only NVDA --cap 3 --workers 16 --seed poc/seeds/nvda-2026-07-01-v2.json`; that
script seeded with created_at '<from>T00:00:00Z' and ran `hivemind.parallel_day.ParallelDay` with 16 extraction and 8 Jev workers).

  python3 clean-arch/e2e-2026-11-09/control_v108.py prove <new folder>           $0: every request answered from the reference archive
  python3 clean-arch/e2e-2026-11-09/control_v108.py live <new folder> --cap 2    paid: the same call with the real transports

`prove` checks the following and raises ProofError when any fails:
1. Inputs. The configuration, every prompt file it names, the seed file and the items database have the sha256 the reference
   manifest records; the window and worker counts are the reference's.
2. Dispatch. Before a day's first request is prepared, the day's routed inputs (input id, sequence number, item hash, in that order)
   must equal the reference run's `manifests/day-<day>.json`; a difference stops the run before that day sends anything. Every
   reference day must be reached. The same guard runs in `live`.
3. Requests. The reference archive stores each request only in canonical form: `request_json` is
   json.dumps(request, sort_keys=True, ensure_ascii=False), the text `model.request_identity` digests. Each outgoing request is
   serialized the same way and must equal one stored `request_json` byte for byte; that row's stored response is returned. A request
   not found raises `ReferenceMissError` naming its sha256 and is written to `<folder>/misses/`; the proof fails. Each stored row
   answers exactly one send (a refused answer's row and the re-send after it are answered in stored order), and every stored row must
   be used.
   - Jev requests: `jev.transport` sends that same sorted text, so the comparison is of the bytes sent.
   - Model requests: `model.openai_transport` sends json.dumps(request) in the dict's insertion order, which the archive does not keep.
     The order is reconstructed instead of assumed: the reference commit's own `src/hivemind` (a907eba, read with `git archive` into
     `<folder>/reference-code/`) is replayed in a subprocess over the same seeded ledger and the same stored answers, and the sha256 of
     each request as that code sends it is recorded. The current code's as-sent bytes must have the same sha256 for every request.
     That replay is also the positive control: the code that wrote the archive must reproduce every request in it, or the harness
     itself is wrong and the proof stops.
4. Outcome. The replay's totals equal the final totals line of the reference `replay.log`.

What it does not prove: that the 11-03 process sent exactly the reconstructed bytes (this rests on dict order being a deterministic
function of code and inputs, and on the archive having been written by commit a907eba, as the reference manifest records); the HTTP
headers and transport retries, which are outside the request; anything about live answers, which are new samples.

A passing proof writes `<folder>/control-proof.json` with the sha256 of the current code (every .py and prompt file of src/hivemind,
and this file) and of the inputs. `live` refuses to start unless a sibling folder holds a passing proof with the same digests.
During `prove` the model and Jev credential readers are replaced by a refusal, so a request that escaped the archive transport cannot
reach a provider.
"""
import argparse
import ast
import collections
import contextlib
import dataclasses
import datetime
import hashlib
import importlib
import io
import json
import os
import sqlite3
import subprocess
import sys
import tarfile
import threading
from pathlib import Path

sys.dont_write_bytecode = True

HARNESS_FILE = Path(__file__).resolve()
REPOSITORY_ROOT = HARNESS_FILE.parents[2]
PROOF_MARKER = 'control-proof.json'
CAPTURE_RESULT = 'capture.json'


@dataclasses.dataclass(frozen=True)
class ControlInputs:
    """Everything the control reads; the defaults are the reference run's own inputs."""
    repository_root: Path = REPOSITORY_ROOT
    reference_run: Path = REPOSITORY_ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03/d1'
    config_path: Path = REPOSITORY_ROOT / 'poc/config/poc-v108.json'
    seed_path: Path = REPOSITORY_ROOT / 'poc/seeds/nvda-2026-07-01-v2.json'
    items_database: Path = REPOSITORY_ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
    universe_path: Path = REPOSITORY_ROOT / 'poc/universe.json'
    from_day: str = '2026-07-01'
    until_day: str = '2026-07-14'
    only_objects: tuple = ('NVDA',)
    seed_created_at: str = '2026-07-01T00:00:00Z'        # scripts/replay.py at a907eba: created_at=f'{args.from_day}T00:00:00Z'
    extraction_workers: int = 16
    jev_workers: int = 8
    reference_commit: str = 'a907eba1f6b1061f3db3c67c7a6110b66ad5c345'


def inputs_to_json(inputs):
    """ControlInputs as JSON, paths as strings: prove hands its inputs to the reference-code subprocess this way."""
    return json.dumps({name: str(value) if isinstance(value, Path) else value for name, value in dataclasses.asdict(inputs).items()}, indent=1)


def inputs_from_json(text):
    defaults = ControlInputs()
    return ControlInputs(**{name: type(getattr(defaults, name))(value) if isinstance(getattr(defaults, name), (Path, tuple)) else value
                            for name, value in json.loads(text).items()})


@dataclasses.dataclass(frozen=True)
class RunPaths:
    folder: Path
    views: Path
    archive: Path
    manifests: Path
    log: Path


class ProofError(RuntimeError):
    """The byte proof failed; the message names every failed check."""


class ReferenceMissError(RuntimeError):
    """An outgoing request has no unused byte-identical row in the reference archive."""


class InputsMismatchError(RuntimeError):
    """A day's routed inputs differ from the reference run's manifest of that day."""


class ProofMissingError(RuntimeError):
    """`live` found no passing proof of this code and these inputs in a sibling folder."""


class LiveCallRefused(BaseException):
    """A credential was read while a proof ran. A BaseException, so the pipeline's `except Exception` cannot record it as an item failure."""


# ---------------------------------------------------------------- the hivemind package this process runs

_code_root = None


def use_code_root(code_root):
    """Select the tree whose src/hivemind this process imports; prove's positive control runs the reference commit's tree."""
    global _code_root
    code_root = Path(code_root).resolve()
    if _code_root is not None and _code_root != code_root:
        raise RuntimeError(f'hivemind is already loaded from {_code_root}')
    if 'hivemind' in sys.modules:
        loaded_from = Path(sys.modules['hivemind'].__file__).resolve().parents[1]
        if loaded_from != code_root / 'src':
            raise RuntimeError(f'hivemind is already imported from {loaded_from}, not {code_root / "src"}')
    elif str(code_root / 'src') not in sys.path:
        sys.path.insert(0, str(code_root / 'src'))
    _code_root = code_root


def hivemind_module(name):
    if _code_root is None:
        use_code_root(REPOSITORY_ROOT)
    return importlib.import_module(f'hivemind.{name}')


# ---------------------------------------------------------------- digests

def file_sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_text(request):
    """The archive's form of a request: model.request_identity's serialization (sorted keys, non-ASCII kept)."""
    return json.dumps(request, sort_keys=True, ensure_ascii=False)


def text_sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def item_hash(item):
    """parallel_day.item_key: the sha256 of the item's canonical text, as the day manifests record it."""
    return text_sha256(canonical_text(item))


def code_digest(code_root):
    """The sha256 over every .py and prompt file of <code_root>/src/hivemind and this harness file."""
    package = Path(code_root) / 'src' / 'hivemind'
    files = sorted(package.rglob('*.py')) + sorted((package / 'prompts').glob('*'))
    listing = {str(path.relative_to(package.parent)): file_sha256(path) for path in files if path.is_file()}
    listing['harness:' + HARNESS_FILE.name] = file_sha256(HARNESS_FILE)
    return text_sha256(canonical_text(listing))


def input_digests(inputs):
    settings = {field.name: str(getattr(inputs, field.name)) for field in dataclasses.fields(inputs)
                if field.name not in ('repository_root', 'reference_run')}
    return {'config': file_sha256(inputs.config_path), 'seed': file_sha256(inputs.seed_path),
            'items': file_sha256(inputs.items_database), 'universe': file_sha256(inputs.universe_path),
            'reference_archive': file_sha256(inputs.reference_run / 'archive.sqlite'),
            'budget': file_sha256(Path(__file__).resolve().parent / 'budget.py'), 'settings': text_sha256(canonical_text(settings))}


def check_reference_inputs(inputs, code_root):
    """Refuses unless the configuration, the prompt files it names (under code_root), the seed file, the items database, the window
    and the worker counts are the ones the reference manifest records. Returns the manifest."""
    manifest = json.loads((inputs.reference_run / 'manifest.json').read_text(encoding='utf-8'))
    problems = []
    if manifest.get('code_commit') != inputs.reference_commit:
        problems.append(f'reference commit {manifest.get("code_commit")} is not {inputs.reference_commit}')
    if Path(manifest['config']).name != inputs.config_path.name or file_sha256(inputs.config_path) != manifest['config_sha256']:
        problems.append(f'configuration {inputs.config_path} differs from the reference {manifest["config"]}')
    for relative_path, recorded in sorted(manifest['prompt_files'].items()):
        prompt_path = Path(code_root) / relative_path
        if not prompt_path.is_file() or file_sha256(prompt_path) != recorded:
            problems.append(f'prompt file {prompt_path} differs from the reference')
    if Path(manifest['seed_file']).name != inputs.seed_path.name or file_sha256(inputs.seed_path) != manifest['seed_sha256']:
        problems.append(f'seed file {inputs.seed_path} differs from the reference {manifest["seed_file"]}')
    if file_sha256(inputs.items_database) != manifest['items_sha256']:
        problems.append(f'items database {inputs.items_database} differs from the reference')
    if list(manifest['window']) != [inputs.from_day, inputs.until_day] or manifest.get('only') != ','.join(inputs.only_objects):
        problems.append(f'window or object filter {manifest["window"]} {manifest.get("only")} differs from the control')
    if manifest.get('workers') != inputs.extraction_workers:
        problems.append(f'reference extraction workers {manifest.get("workers")} is not {inputs.extraction_workers}')
    if problems:
        raise ProofError('reference inputs differ:\n  ' + '\n  '.join(problems))
    return manifest


def reference_totals(reference_run):
    """The final 'totals:' line of the reference replay.log (the log holds an earlier, abandoned start before it)."""
    lines = [line for line in (reference_run / 'replay.log').read_text(encoding='utf-8').splitlines() if line.startswith('totals: ')]
    if not lines:
        raise ProofError(f'no totals line in {reference_run / "replay.log"}')
    return ast.literal_eval(lines[-1][len('totals: '):])


# ---------------------------------------------------------------- 1. prepare

def prepare(run_folder, *, created_at, seed_path=ControlInputs.seed_path):
    """A new run folder: views.sqlite seeded through seeding.seed_views at `created_at`, and the path of an archive not yet created."""
    folder = Path(run_folder)
    if folder.exists():
        raise FileExistsError(f'{folder} exists; a control run gets a new folder')
    folder.mkdir(parents=True)
    paths = RunPaths(folder=folder, views=folder / 'views.sqlite', archive=folder / 'archive.sqlite', manifests=folder / 'manifests',
                     log=folder / 'replay.log')
    store = hivemind_module('views.store')
    seeding = hivemind_module('seeding')
    ledger = store.open_db(str(paths.views))
    try:
        written = seeding.seed_views(ledger, str(seed_path), created_at=created_at)
    finally:
        ledger.close()
    seed_count = len(json.loads(Path(seed_path).read_text(encoding='utf-8'))['questions'])
    if len(written) != seed_count:
        raise RuntimeError(f'seeded {len(written)} of {seed_count} questions into a new ledger')
    return paths


# ---------------------------------------------------------------- 2. the archive transport and the dispatch guard

class ReferenceArchiveTransport:
    """Answers each request with the stored response of the byte-identical request in the reference archive.

    Called as the model transport, (provider, request), or as the Jev transport, (request,): the same object serves both, as
    replay.run passes one transport to both. Each stored row answers one send, in call_id order for rows of the same request."""

    MODEL_SEND = 'model'
    JEV_SEND = 'jev'

    def __init__(self, reference_archive_path):
        uri = Path(reference_archive_path).resolve().as_uri() + '?mode=ro'
        with contextlib.closing(sqlite3.connect(uri, uri=True)) as reference:
            rows = reference.execute('select call_id, request_sha256, request_json, response_json from model_calls order by call_id').fetchall()
        self.unanswered = collections.defaultdict(collections.deque)
        for call_id, stored_sha, request_json, response_json in rows:
            base_sha = stored_sha.split(':', 1)[0]
            if text_sha256(request_json) != base_sha:
                raise ProofError(f'reference row {call_id}: request_json does not hash to its request_sha256')
            self.unanswered[base_sha].append((call_id, request_json, response_json))
        self.reference_rows = len(rows)
        self.lock = threading.Lock()
        self.matched = collections.Counter()
        self.misses = []                                        # (sha256, label, canonical text)
        self.sent_digests = collections.defaultdict(set)        # canonical sha256 -> sha256 of the bytes as sent

    def __call__(self, *arguments):
        if len(arguments) == 2:
            provider, request = arguments
            send_kind = self.MODEL_SEND
            sent_bytes = json.dumps(request).encode('utf-8')                                     # model.openai_transport's body
            label = f'{request.get("response_format", {}).get("json_schema", {}).get("name", "?")} ({provider}, {request.get("model")})'
        elif len(arguments) == 1:
            (request,) = arguments
            send_kind = self.JEV_SEND
            sent_bytes = json.dumps(request, sort_keys=True, ensure_ascii=False).encode('utf-8')  # jev.transport's body
            label = f'jev ({request.get("model")})'
        else:
            raise TypeError(f'a transport takes (provider, request) or (request,), not {len(arguments)} arguments')
        canonical = canonical_text(request)
        sha = text_sha256(canonical)
        with self.lock:
            queue = self.unanswered.get(sha)
            if not queue:
                self.misses.append((sha, label, canonical))
                raise ReferenceMissError(f'{label} request {sha} has no unused byte-identical row in the reference archive')
            call_id, stored_request, stored_response = queue.popleft()
            if stored_request != canonical:
                raise ReferenceMissError(f'{label} request {sha} hashes like row {call_id} but its text differs')
            self.matched[label] += 1
            self.sent_digests[sha].add(hashlib.sha256(sent_bytes).hexdigest())
        return json.loads(stored_response)

    def unused_rows(self):
        with self.lock:
            return sorted(call_id for queue in self.unanswered.values() for call_id, _, _ in queue)


class ReferenceInputsGuard:
    """A day runner for replay.run: before the production ParallelDay prepares any request of a day, the day's routed inputs (input id,
    sequence number, item hash, in order) must equal the reference manifest of that day."""

    def __init__(self, day_runner, reference_manifest_dir):
        self.day_runner = day_runner
        self.reference_manifest_dir = Path(reference_manifest_dir)
        self.days_checked = []
        self.inputs_checked = 0

    def __call__(self, conn, archive, cfg, universe, items, *, day, transport=None, log=print):
        dispatched = [{'input_id': item['input_id'], 'seq': route.sequence_no, 'hash': item_hash(item)} for item, route in items]
        check_day_inputs(day, dispatched, self.reference_manifest_dir / f'day-{day}.json')
        self.days_checked.append(day)
        self.inputs_checked += len(dispatched)
        return self.day_runner(conn, archive, cfg, universe, items, day=day, transport=transport, log=log)

    def reference_days(self):
        return sorted(path.name[len('day-'):-len('.json')] for path in self.reference_manifest_dir.glob('day-*.json'))


def check_day_inputs(day, dispatched, reference_manifest_path):
    """Refuses unless `dispatched` equals the reference manifest's inputs entry for entry, in order."""
    if not Path(reference_manifest_path).is_file():
        raise InputsMismatchError(f'{day}: no reference manifest {reference_manifest_path}')
    reference = json.loads(Path(reference_manifest_path).read_text(encoding='utf-8'))
    expected = [{'input_id': entry['input_id'], 'seq': entry['seq'], 'hash': entry['hash']} for entry in reference['inputs']]
    if reference.get('day') != day:
        raise InputsMismatchError(f'{day}: reference manifest {reference_manifest_path} is for {reference.get("day")}')
    for position, (got, wanted) in enumerate(zip(dispatched, expected)):
        if got != wanted:
            raise InputsMismatchError(f'{day}: input {position} is {got}, the reference dispatched {wanted}')
    if len(dispatched) != len(expected):
        raise InputsMismatchError(f'{day}: {len(dispatched)} inputs dispatched, the reference dispatched {len(expected)}')


@contextlib.contextmanager
def refuse_credentials():
    """While a proof runs, reading a model or Jev credential raises LiveCallRefused instead."""
    model, jev = hivemind_module('model'), hivemind_module('jev')
    saved = (model._key, jev._key)

    def refuse(*arguments):
        raise LiveCallRefused('a credential was read during a $0 proof: a request escaped the archive transport')
    model._key, jev._key = refuse, refuse
    try:
        yield
    finally:
        model._key, jev._key = saved


# ---------------------------------------------------------------- the one call both modes make

def guarded_day_runner(paths, inputs):
    """The production day runner (ParallelDay, the reference worker counts) behind the reference-inputs guard."""
    parallel_day = hivemind_module('parallel_day')
    day_runner = parallel_day.ParallelDay(str(Path(inputs.items_database).resolve()), str(paths.manifests.resolve()),
                                          extraction_workers=inputs.extraction_workers, jev_workers=inputs.jev_workers)
    return ReferenceInputsGuard(day_runner, inputs.reference_run / 'manifests')


def run_control(paths, inputs, guard, *, transport, spend_cap_usd, log):
    """hivemind.replay.run over the window with the reference run's arguments; `transport` None is the real transports."""
    config, model, replay, universe = (hivemind_module(name) for name in ('config', 'model', 'replay', 'universe'))
    cfg = config.load(str(inputs.config_path))
    if getattr(cfg, 'baseline', None) is not None:
        raise ProofError(f'{cfg.version} has a coverage-start reading; the v108 control has none')
    loaded_universe = universe.load(str(inputs.universe_path))
    archive = model.Archive(str(paths.archive))
    log(f'--- control {inputs.from_day}..{inputs.until_day} config {cfg.version}/{cfg.checksum} provider {cfg.provider} universe '
        f'{loaded_universe.version} workers {inputs.extraction_workers}/{inputs.jev_workers} transport {"reference archive" if transport else "real"}')
    totals = replay.run(testdb_path=str(Path(inputs.items_database).resolve()), views_path=str(paths.views), archive=archive, cfg=cfg,
                        universe=loaded_universe, from_day=inputs.from_day, until_day=inputs.until_day, day0=None,
                        spend_cap_usd=spend_cap_usd, transport=transport, log=log, only_objects=set(inputs.only_objects),
                        max_items_per_day=None, day_runner=guard)
    log('totals:', totals)
    return totals


def file_logger(log_path):
    def log(*parts):
        line = ' '.join(str(part) for part in parts)
        print(line, flush=True)
        with open(log_path, 'a', encoding='utf-8') as handle:
            handle.write(line + '\n')
    return log


def replay_against_reference(paths, inputs):
    """Runs the control over the reference archive; returns (failures, counts, sent digests). Never sends a live request."""
    log = file_logger(paths.log)
    transport = ReferenceArchiveTransport(inputs.reference_run / 'archive.sqlite')
    guard = guarded_day_runner(paths, inputs)
    failures, totals = [], None
    manifest = json.loads((inputs.reference_run / 'manifest.json').read_text(encoding='utf-8'))
    try:
        with refuse_credentials():
            totals = run_control(paths, inputs, guard, transport=transport, spend_cap_usd=manifest['cap_usd'], log=log)
    except Exception as error:              # the failure is reported with the misses below; LiveCallRefused is not caught
        failures.append(f'the replay stopped: {error!r}')
    if transport.misses:
        miss_folder = paths.folder / 'misses'
        miss_folder.mkdir(exist_ok=True)
        for sha, label, canonical in transport.misses:
            (miss_folder / f'{sha}.json').write_text(canonical, encoding='utf-8')
        failures.append(f'{len(transport.misses)} requests not in the reference archive (written to {miss_folder}); first: '
                        f'{transport.misses[0][1]} {transport.misses[0][0]}')
    unused = transport.unused_rows()
    if unused:
        failures.append(f'{len(unused)} of {transport.reference_rows} reference rows were never requested; first call_ids {unused[:10]}')
    if guard.days_checked != guard.reference_days():
        failures.append(f'days checked {guard.days_checked} are not the reference days {guard.reference_days()}')
    if totals is not None and totals != reference_totals(inputs.reference_run):
        failures.append(f'totals {totals} differ from the reference {reference_totals(inputs.reference_run)}')
    counts = {'reference_rows': transport.reference_rows, 'requests_matched': sum(transport.matched.values()),
              'matched_by_kind': dict(sorted(transport.matched.items())), 'misses': len(transport.misses), 'unused_reference_rows': len(unused),
              'days_checked': len(guard.days_checked), 'inputs_checked': guard.inputs_checked, 'totals': totals}
    return failures, counts, {sha: sorted(digests) for sha, digests in transport.sent_digests.items()}


# ---------------------------------------------------------------- the positive control: the reference commit's code

def extract_reference_code(inputs, destination):
    """Writes src/hivemind of the reference commit under `destination`, read from the repository's object store with `git archive`."""
    archive_bytes = subprocess.run(['git', '-C', str(inputs.repository_root), 'archive', '--format=tar', inputs.reference_commit, 'src/hivemind'],
                                   check=True, capture_output=True).stdout
    destination = Path(destination)
    destination.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(archive_bytes)) as bundle:
        bundle.extractall(destination)
    return destination


def capture(capture_folder, inputs):
    """Run inside the subprocess whose hivemind is the reference commit's: replays over the reference archive and writes capture.json."""
    check_reference_inputs(inputs, code_root=_code_root)
    paths = prepare(capture_folder, created_at=inputs.seed_created_at, seed_path=inputs.seed_path)
    failures, counts, sent_digests = replay_against_reference(paths, inputs)
    (paths.folder / CAPTURE_RESULT).write_text(json.dumps({'code_root': str(_code_root), 'failures': failures, 'counts': counts,
                                                            'sent_digests': sent_digests}, indent=1, sort_keys=True), encoding='utf-8')
    return failures


# ---------------------------------------------------------------- 2. prove

def prove(run_folder, *, inputs=ControlInputs()):
    """The $0 byte proof (module docstring). Writes control-proof.json and returns the counts when every check passes; else ProofError."""
    use_code_root(inputs.repository_root)
    check_reference_inputs(inputs, code_root=inputs.repository_root)
    paths = prepare(run_folder, created_at=inputs.seed_created_at, seed_path=inputs.seed_path)
    reference_code = extract_reference_code(inputs, paths.folder / 'reference-code')
    capture_folder = paths.folder / 'reference-code-replay'
    inputs_file = paths.folder / 'control-inputs.json'
    inputs_file.write_text(inputs_to_json(inputs), encoding='utf-8')
    completed = subprocess.run([sys.executable, str(HARNESS_FILE), 'capture', '--code-root', str(reference_code), '--inputs', str(inputs_file),
                                str(capture_folder)],
                               env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    capture_path = capture_folder / CAPTURE_RESULT
    if not capture_path.is_file():
        raise ProofError(f'the reference-code replay wrote no {CAPTURE_RESULT} (exit status {completed.returncode})')
    reference_capture = json.loads(capture_path.read_text(encoding='utf-8'))
    if completed.returncode != 0 or reference_capture['failures']:
        raise ProofError('positive control failed: the reference commit does not reproduce its own archive, so the harness cannot judge:\n  '
                         + '\n  '.join(reference_capture['failures'] or [f'exit status {completed.returncode}']))

    failures, counts, sent_digests = replay_against_reference(paths, inputs)
    reference_digests = reference_capture['sent_digests']
    order_differs = sorted(sha for sha in sent_digests if sha in reference_digests and sent_digests[sha] != reference_digests[sha])
    if order_differs:
        failures.append(f'{len(order_differs)} requests match canonically but are sent with other bytes (key order) than the reference '
                        f'code sends; first {order_differs[:5]}')
    if not failures and set(sent_digests) != set(reference_digests):
        failures.append('the current and the reference code sent different request sets')
    counts.update(as_sent_compared=sum(1 for sha in sent_digests if sha in reference_digests), as_sent_differing=len(order_differs),
                  positive_control=reference_capture['counts'])
    if failures:
        (paths.folder / 'control-proof-failed.json').write_text(json.dumps({'failures': failures, 'counts': counts}, indent=1), encoding='utf-8')
        raise ProofError('byte proof failed:\n  ' + '\n  '.join(failures))
    marker = {'passed': True, 'code_digest': code_digest(inputs.repository_root), 'inputs': input_digests(inputs),
              'reference_run': str(inputs.reference_run), 'reference_commit': inputs.reference_commit, 'counts': counts}
    (paths.folder / PROOF_MARKER).write_text(json.dumps(marker, indent=1, sort_keys=True), encoding='utf-8')
    return counts


# ---------------------------------------------------------------- 3. live

def find_sibling_proof(run_folder, inputs):
    """A passing control-proof.json in a folder beside `run_folder` whose code and input digests are the current ones."""
    current_code, current_inputs = code_digest(inputs.repository_root), input_digests(inputs)
    parent = Path(run_folder).resolve().parent
    for marker_path in sorted(parent.glob(f'*/{PROOF_MARKER}')):
        try:
            marker = json.loads(marker_path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            continue
        if marker.get('passed') is True and marker.get('code_digest') == current_code and marker.get('inputs') == current_inputs:
            return marker_path
    raise ProofMissingError(f'no passing {PROOF_MARKER} for this code and these inputs in a folder beside {run_folder}; run prove first')


def run_live(run_folder, spend_cap_usd, *, inputs=ControlInputs()):
    """The same call as prove with the real transports (replay.run's default), on a new seeded ledger; refuses without a sibling proof."""
    if isinstance(spend_cap_usd, bool) or not isinstance(spend_cap_usd, (int, float)) or not spend_cap_usd > 0:
        raise ValueError('a live control needs a positive spend cap in USD')
    use_code_root(inputs.repository_root)
    if Path(run_folder).exists():
        raise FileExistsError(f'{run_folder} exists; a control run gets a new folder')
    proof_path = find_sibling_proof(run_folder, inputs)
    check_reference_inputs(inputs, code_root=inputs.repository_root)
    paths = prepare(run_folder, created_at=inputs.seed_created_at, seed_path=inputs.seed_path)
    git = lambda *arguments: subprocess.run(['git', '-C', str(inputs.repository_root), *arguments], capture_output=True, text=True).stdout.strip()
    manifest = {'control': 'D392 v108 control', 'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
                'code_commit': git('rev-parse', 'HEAD'), 'tree_dirty_files': [line for line in git('status', '--short').splitlines() if line.strip()],
                'code_digest': code_digest(inputs.repository_root), 'proof': str(proof_path), 'config': str(inputs.config_path),
                'inputs': input_digests(inputs), 'seed_created_at': inputs.seed_created_at, 'window': [inputs.from_day, inputs.until_day],
                'only': ','.join(inputs.only_objects), 'cap_usd': float(spend_cap_usd),
                'workers': [inputs.extraction_workers, inputs.jev_workers]}
    manifest_path = paths.folder / 'manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=1) + '\n', encoding='utf-8')
    (paths.folder / 'run.pid').write_text(f'{os.getpid()}\n', encoding='utf-8')
    guard = guarded_day_runner(paths, inputs)
    sys.path.insert(0, str(HARNESS_FILE.parent))   # imported here: budget imports hivemind, which use_code_root must place first
    import budget
    limit = budget.Budget(float(spend_cap_usd))    # a hard cap on every attempt; replay.run's own cap is kept and checked after the fact
    try:
        totals = run_control(paths, inputs, guard, transport=limit, spend_cap_usd=float(spend_cap_usd), log=file_logger(paths.log))
    finally:
        manifest.update(hard_cap_spent_usd=round(limit.spent_usd, 4))
        manifest_path.write_text(json.dumps(manifest, indent=1) + '\n', encoding='utf-8')
    manifest.update(finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), totals=totals,
                    days_checked=len(guard.days_checked), inputs_checked=guard.inputs_checked)
    manifest_path.write_text(json.dumps(manifest, indent=1) + '\n', encoding='utf-8')
    return totals


# ---------------------------------------------------------------- CLI

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('prove', help='$0 byte proof over the reference archive').add_argument('folder')
    live_parser = commands.add_parser('live', help='the paid control run; needs a passing proof beside it')
    live_parser.add_argument('folder')
    live_parser.add_argument('--cap', type=float, required=True, help='USD spend cap for this run')
    capture_parser = commands.add_parser('capture', help='internal: run by prove with the reference commit\'s code')
    capture_parser.add_argument('--code-root', required=True)
    capture_parser.add_argument('--inputs', required=True, help='the control-inputs.json prove wrote')
    capture_parser.add_argument('folder')
    arguments = parser.parse_args(argv)
    if arguments.command == 'capture':
        use_code_root(arguments.code_root)
        failures = capture(Path(arguments.folder), inputs_from_json(Path(arguments.inputs).read_text(encoding='utf-8')))
        return 1 if failures else 0
    if arguments.command == 'prove':
        counts = prove(Path(arguments.folder))
        print('byte proof passed:', json.dumps(counts, indent=1, sort_keys=True))
        return 0
    totals = run_live(Path(arguments.folder), arguments.cap)
    print('live control finished:', totals)
    return 0


if __name__ == '__main__':
    sys.exit(main())
