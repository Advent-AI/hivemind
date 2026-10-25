"""D172 offline POC: speculative extraction, validated at ordered commit time.

The coordinator alone reads/writes the thesis ledger. Workers receive copied
inputs and only write the thread-safe model archive. Use an explicit offline
transport; live cost reservation is not implemented by this POC.
"""
import concurrent.futures
import copy
import dataclasses
import hashlib
import json
from pathlib import Path
import time

from hivemind import extraction, model
from hivemind.views import round as rounds, store

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def environment_key(cfg, universe):
    return model.request_identity({'config': dataclasses.asdict(cfg), 'universe': vars(universe)})[1]


def runtime_key():
    files = sorted((ROOT / 'src/hivemind').rglob('*.py')) + sorted((ROOT / 'src/hivemind/prompts').glob('*')) + [Path(__file__)]
    return model.request_identity({str(path.relative_to(ROOT)): digest(path) for path in files if path.is_file()})[1]


def item_key(item):
    return model.request_identity(item)[1]


def extraction_key(cfg, item, text, shown, universe, groups):
    setting, system, user, schema = extraction.request_for(cfg, item, text, shown, universe, groups)
    return model.request_identity(model.build_request(setting, system, user, schema, 'extraction', cfg.provider))[1]


class DayRunner:
    """Opt-in day_runner for replay.run; defaults remain on the serial path."""

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
        if not path.exists():
            if conn.execute("select 1 from processing_steps where publication_day=? and step in ('extracted','written','handed_over') limit 1", (day,)).fetchone():
                raise ValueError('cannot adopt a partially processed day without its concurrency manifest')
            with path.open('x', encoding='utf-8') as handle:
                json.dump(dict(metadata, inputs=entries), handle, sort_keys=True)
        try:
            saved = json.loads(path.read_text())
        except (OSError, ValueError) as error:
            raise ValueError('unreadable concurrency manifest; refusing to guess its inputs') from error
        if {k: saved.get(k) for k in metadata} != metadata:
            raise ValueError('concurrency manifest source, configuration or runtime changed')
        remaining = [entry for entry in saved['inputs'] if not store.is_processed(conn, entry['input_id'])]
        if remaining != entries:
            raise ValueError('concurrency manifest input order or content changed')
        return metadata

    def __call__(self, conn, archive, cfg, universe, items, *, day, transport=None, log=print):
        if transport is None:
            raise ValueError('offline concurrency POC requires an explicit transport; live cost reservation is not implemented')
        if cfg.matching.engine != 'jev' and self.jev_workers != 1:
            raise ValueError('parallel matching is only implemented for Jev')
        metadata = self._manifest(conn, cfg, universe, items, day)
        frozen_cfg, frozen_universe = copy.deepcopy(cfg), copy.deepcopy(universe)
        pending, prepared_futures, next_index = {}, [], 0
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=self.extraction_workers)

        def current_request(item):
            objects = [o['value'] for o in item.get('object_identifiers') or [] if frozen_universe.has(o['value'])]
            shown = copy.deepcopy(store.views_for_prompt(conn, objects))
            groups = copy.deepcopy(store.groups_for_prompt(conn, objects, item.get('title') or ''))
            owned_item = copy.deepcopy(item)
            return owned_item, shown, groups, extraction_key(frozen_cfg, owned_item, owned_item['text'], shown, frozen_universe, groups)

        def submit(item, owned_item, shown, groups, key):
            future = pool.submit(extraction.extract, archive, frozen_cfg, owned_item, owned_item['text'], shown,
                                 frozen_universe, shown_groups=groups, transport=transport)
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
                answer = future.result()
                validate_inputs()
                if answer.request_sha256 != current_key:
                    raise ValueError('prepared extraction does not match its validated request')
                self._event(item['input_id'], 'reused', request=current_key)
                return answer
            future.cancel()
            self._event(item['input_id'], 'stale', before=prior_key, request=current_key)
            answer = extraction.extract(current_archive, current_cfg, item, text, shown, current_universe,
                                        shown_groups=shown_groups, transport=transport)
            validate_inputs()
            self._event(item['input_id'], 'reextracted', request=current_key)
            return answer

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
