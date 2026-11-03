"""One day's items with concurrent request preparation and one ordered writer (D172, D181).

An item's accepted extraction must answer the exact request built from the ledger committed by the items before it,
as in serial processing (D159). Extraction requests for later items are sent early, from the ledger as it stands;
after each commit, every waiting request that commit changed is built again and sent again, and at its turn an item
accepts a prepared answer only if its request is byte-identical to the request built now. Matching questions within
an item run concurrently and are applied in their planned order. Only this coordinator reads or writes the ledger;
workers receive copies and write only the thread-safe call archive. Opt-in through `replay.run(day_runner=...)`;
the default replay stays serial. The run's spend cap is checked after each committed item, so in-flight early
requests can pass it by at most the worker count's calls.
"""
import concurrent.futures
import copy
import dataclasses
import hashlib
import json
from pathlib import Path
import time

from . import extraction, model
from .views import round as rounds, store

PACKAGE = Path(__file__).resolve().parent


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def environment_key(cfg, universe):
    return model.request_identity({'config': dataclasses.asdict(cfg), 'universe': vars(universe)})[1]


def runtime_key():
    files = sorted(PACKAGE.rglob('*.py')) + sorted((PACKAGE / 'prompts').glob('*'))
    return model.request_identity({str(path.relative_to(PACKAGE.parent)): digest(path) for path in files if path.is_file()})[1]


def item_key(item):
    return model.request_identity(item)[1]


def extraction_key(cfg, item, text, shown, universe, groups):
    setting, system, user, schema = extraction.request_for(cfg, item, text, shown, universe, groups)
    return model.request_identity(model.build_request(setting, system, user, schema, 'extraction', cfg.provider))[1]


class ParallelDay:
    """A `day_runner` for replay.run: per-day manifest, bounded early extraction, validated ordered commits."""

    def __init__(self, source_path, manifest_dir, *, extraction_workers=2, jev_workers=2):
        for workers in (extraction_workers, jev_workers):
            if not isinstance(workers, int) or isinstance(workers, bool) or workers < 1:
                raise ValueError('worker counts must be positive integers')
        self.source_path, self.manifest_dir = Path(source_path), Path(manifest_dir)
        if not self.source_path.is_absolute() or not self.source_path.is_file() or not self.manifest_dir.is_absolute():
            raise ValueError('use an existing absolute source path and an absolute manifest directory')
        self.extraction_workers, self.jev_workers = extraction_workers, jev_workers
        self.events = []

    def _event(self, input_id, event, **fields):
        self.events.append(dict(fields, input_id=input_id, event=event, t=time.perf_counter()))

    def _manifest(self, conn, cfg, universe, items, day):
        self.manifest_dir.mkdir(parents=True, exist_ok=True)
        path = self.manifest_dir / f'day-{day}.json'
        metadata = {'day': day, 'environment': environment_key(cfg, universe), 'runtime': runtime_key(),
                    'source': digest(self.source_path), 'extraction_workers': self.extraction_workers,
                    'jev_workers': self.jev_workers}
        entries = [{'input_id': item['input_id'], 'seq': route.sequence_no, 'hash': item_key(item)} for item, route in items]
        started = conn.execute("select 1 from processing_steps where publication_day=? and step in ('extracted','written','handed_over') limit 1", (day,)).fetchone()
        if not started:
            # Nothing of this day is written in this ledger: a manifest left by another run or ledger guards nothing here.
            path.write_text(json.dumps(dict(metadata, inputs=entries), sort_keys=True), encoding='utf-8')
        elif not path.exists():
            raise ValueError('cannot adopt a partially processed day without its parallel-day manifest; finish it with --workers 1')
        try:
            saved = json.loads(path.read_text())
        except (OSError, ValueError) as error:
            raise ValueError('unreadable parallel-day manifest; refusing to guess its inputs') from error
        if {k: saved.get(k) for k in metadata} != metadata:
            raise ValueError('parallel-day manifest source, configuration or runtime changed')
        remaining = [entry for entry in saved['inputs'] if not store.is_processed(conn, entry['input_id'])]
        if remaining != entries:
            raise ValueError('parallel-day manifest input order or content changed')
        return metadata

    def __call__(self, conn, archive, cfg, universe, items, *, day, transport=None, log=print):
        if cfg.matching.engine != 'jev' and self.jev_workers != 1:
            raise ValueError('parallel matching is only implemented for Jev')
        metadata = self._manifest(conn, cfg, universe, items, day)
        frozen_cfg, frozen_universe = copy.deepcopy(cfg), copy.deepcopy(universe)
        pending, prepared_futures, next_index = {}, [], 0
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=self.extraction_workers)

        def current_request(item):
            objects = [o['value'] for o in item.get('object_identifiers') or [] if frozen_universe.has(o['value'])]
            shown = copy.deepcopy(extraction.shown_views(conn, frozen_cfg, item, objects))
            groups = copy.deepcopy(store.groups_for_prompt(conn, objects, item.get('title') or ''))
            owned_item = copy.deepcopy(item)
            return owned_item, shown, groups, extraction_key(frozen_cfg, owned_item, owned_item['text'], shown, frozen_universe, groups)

        def submit(item, owned_item, shown, groups, key):
            future = pool.submit(extraction.read_item, archive, frozen_cfg, owned_item, owned_item['text'], shown,
                                 frozen_universe, shown_groups=groups, transport=transport)      # the read; filing waits for the turn
            pending[item['input_id']] = (key, item_key(owned_item), future, item)
            prepared_futures.append((item['input_id'], future))
            self._event(item['input_id'], 'prepared', request=key)

        def fill():
            nonlocal next_index
            while next_index < len(items) and len(pending) < self.extraction_workers:
                item, route = items[next_index]
                next_index += 1
                if route.resume_from and route.resume_from != 'extracted':
                    continue  # The authoritative saved handover is owned by normal recovery.
                submit(item, *current_request(item))

        def refresh():
            """Re-prepare, right after a commit, every waiting request that commit changed; the turn still validates."""
            for input_id, (key, _, future, item) in list(pending.items()):
                owned_item, shown, groups, current = current_request(item)
                if current != key:
                    future.cancel()
                    self._event(input_id, 'stale', before=key, request=current)
                    submit(item, owned_item, shown, groups, current)

        def accepted_extraction(current_archive, current_cfg, item, text, shown, current_universe, *, shown_groups=(), transport=None):
            prior_key, source_key, future, _ = pending[item['input_id']]
            def validate_inputs():
                if (environment_key(current_cfg, current_universe) != metadata['environment']
                        or environment_key(cfg, universe) != metadata['environment'] or runtime_key() != metadata['runtime']):
                    raise ValueError('configuration, universe or runtime changed during the day')
                if item_key(item) != source_key or text != item['text']:
                    raise ValueError('source changed after preparation')
            validate_inputs()
            current_key = extraction_key(current_cfg, item, text, shown, current_universe, shown_groups)
            if current_key == prior_key:
                reading = future.result()
                validate_inputs()
                if reading.answer.request_sha256 != current_key:
                    raise ValueError('prepared extraction does not match its validated request')
                self._event(item['input_id'], 'reused', request=current_key)
                return extraction.file_reading(reading, current_archive, current_cfg, item, shown, transport=transport)   # filed under the theses open now
            future.cancel()
            self._event(item['input_id'], 'stale', before=prior_key, request=current_key)
            reading = extraction.read_item(current_archive, current_cfg, item, text, shown, current_universe,
                                      shown_groups=shown_groups, transport=transport)
            validate_inputs()
            self._event(item['input_id'], 'reextracted', request=current_key)
            return extraction.file_reading(reading, current_archive, current_cfg, item, shown, transport=transport)

        try:
            fill()
            for item, route in items:
                self._event(item['input_id'], 'turn')
                result = rounds.run(conn, archive, frozen_cfg, frozen_universe, item, route.sequence_no, resume_from=route.resume_from,
                                    transport=transport, log=log, extractor=accepted_extraction, matching_workers=self.jev_workers)
                self._event(item['input_id'], 'failed' if result.failed else 'accepted')
                yield result
                if result.failed:
                    return
                pending.pop(item['input_id'], None)
                refresh()
                fill()
        finally:
            # Running calls may still archive a response; none can become a handover here.
            for _, _, future, _ in pending.values():
                future.cancel()
            pool.shutdown(wait=True, cancel_futures=True)
            for input_id, future in prepared_futures:
                if not future.cancelled() and future.exception() is not None:
                    self._event(input_id, 'speculative_error', error=type(future.exception()).__name__)
