"""D157: a bounded, isolated two-article stream using the current Chinese pipeline.

The registered scope and checks live in docs/research/2026-10-25-ohio-grouping-poc.md.
No default pipeline configuration or historical ledger is modified.
"""
import argparse
import copy
import dataclasses
import fcntl
import hashlib
import json
import re
import sqlite3
import time
import urllib.request
from pathlib import Path

import ingestion_threads as groups
import study
from hivemind import config, dispatch, extraction, model, universe
from hivemind.views import matching, store, writing

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / 'poc/reports/2026-10-25-ohio-grouping-01'
ITEMS_DB = ROOT / 'poc/data/items-window-tags2-2026-10-24.sqlite'
PREFIX = ROOT / 'poc/reports/2026-10-25-direct-subjects-01/sample-2-retained/item2-result.json'
ITEM_IDS = ('gnews:b25b5b3109fbe06f1a394164', 'gnews:bb0d23846735c94b7c1722d2')
LABELS = tuple(f'{arm}-{sample}' for sample in range(1, 4) for arm in ('control', 'grouped'))
MAX_REQUESTS, MAX_USD, MAX_SECONDS = 30, 1.5, 1800
GROUP_PROMPT = '''同时把候选观点归入所谈的持续业务过程，例如产品推出、投资项目或政策过程；公司相同不够。
可以复用下面展示的研究主线编号，也可以在 threads 声明有名称和范围的新主线；在候选的 thread_ids 引用。
同一过程的不同问题可以共用主线，一个问题也可以属于多条。归组不合并问题，也不表示因果或依赖。
只更新已有观点的证据时不用再造候选或主线。'''
TABLES = ('views', 'view_keys', 'rungs', 'evidence', 'evidence_sources', 'evidence_links', 'replacements',
          'threads', 'thread_members')


class Refused(ValueError):
    """A completed model answer did not meet the registered contract; do not resample."""


def write(path, value):
    study.write_json(Path(path), value)


def read(path):
    return json.loads(Path(path).read_text())


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def schema():
    result = extraction.keyed_schema()
    result['required'].append('threads')
    result['properties']['threads'] = {'type': 'array', 'items': copy.deepcopy(groups.THREAD_SCHEMA)}
    candidate = result['properties']['candidates']['items']
    candidate['required'].append('thread_ids')
    candidate['properties']['thread_ids'] = {'type': 'array', 'minItems': 1, 'items': {'type': 'string'}}
    return result


def validate_references(raw, offered):
    errors = model.check_schema(raw, schema())
    if errors:
        raise Refused('; '.join(errors))
    ids = [g['id'] for g in raw['threads']]
    candidate_ids = [c['id'] for c in raw['candidates']]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise Refused('ambiguous candidate IDs')
    if len(ids) != len(set(ids)) or any(re.fullmatch(r't[1-9][0-9]*', ident) is None for ident in ids):
        raise Refused('new groups need unique local t IDs')
    if any(not g['name'].strip() or not g['scope'].strip() for g in raw['threads']):
        raise Refused('group name and scope must be nonempty')
    allowed = set(ids) | {g['thread_id'] for g in offered}
    for c in raw['candidates']:
        refs = c['thread_ids']
        if not refs or len(refs) != len(set(refs)) or set(refs) - allowed:
            raise Refused(f'{c["id"]}: invalid group references')


def context(conn, item, uni, grouped):
    shown = store.views_for_prompt(conn, [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])])
    offered = []
    if grouped:
        for row in conn.execute('select * from threads order by rowid'):
            group = dict(row)
            group['members'] = [r[0] for r in conn.execute(
                'select view_id from thread_members where thread_id=? order by rowid', (row['thread_id'],))]
            offered.append(group)
        member_ids = {v for g in offered for v in g['members']}
        shown_ids = {v['view_id'] for v in shown}
        for vid in sorted(member_ids - shown_ids):
            shown.append(dict(store.view(conn, vid), depends_on=[]))
    system, user = extraction.build_prompt(item, item['text'], shown, uni, 'v5')
    if grouped:
        system += '\n\n' + GROUP_PROMPT
        user += '\n\n【可用研究主线】\n' + json.dumps(offered, ensure_ascii=False)
    return system, user, shown, offered


def snapshot(conn, seq):
    result = {table: [dict(r) for r in conn.execute(f'select * from {table} order by rowid')] for table in TABLES}
    result['details'] = [groups.thread_detail(conn, r['thread_id'], seq) for r in result['threads']]
    return result


def process(conn, archive, cfg, uni, item, grouped, directory, transport):
    """One dispatch, extract, match and atomic write; no hidden repair call."""
    route = dispatch.route(conn, item, uni)
    if route.kind != 'extract':
        return {'route': route.kind, 'input_id': item['input_id']}
    if route.resume_from:
        raise Refused('This measurement does not resume unfinished sequences')
    seq = route.sequence_no
    system, user, shown, offered = context(conn, item, uni, grouped)
    write(directory / 'context.json', {'shown': shown, 'offered': offered, 'before': snapshot(conn, seq - 1)})
    answer = model.call(archive, cfg, cfg.extraction_setting(item['category']), system, user,
                        schema() if grouped else extraction.keyed_schema(), 'extraction', 'extract', transport=transport)
    if answer.cached:
        raise Refused('Fresh sample unexpectedly used a cached answer')
    write(directory / 'extraction.json', answer.data)
    if grouped:
        validate_references(answer.data, offered)
    evidence, candidates, dropped = extraction.sift(answer.data, item, item['text'], {v['view_id'] for v in shown}, uni)
    handover = extraction.Handover(evidence, candidates, dropped, answer.call_id, answer.request_sha256, False, answer.cost_usd)
    write(directory / 'handover.json', dataclasses.asdict(handover))

    def match(name, handover, lists, shown, extra_views=()):
        result = matching.decide(archive, cfg, conn, item, handover.candidates, handover.evidence, lists, shown,
                                 extra_views=extra_views, transport=transport)
        if result.cached:
            raise Refused('Fresh matching sample unexpectedly used cache')
        checked = matching.check(conn, uni, result.data, handover.candidates, handover.evidence, lists, shown)
        write(directory / f'{name}.json', {'answer': result.data, 'outcomes': checked.outcomes,
              'evidence': [[*key, *value] for key, value in checked.evidence.items()],
              'refusals': checked.refusals, 'not_opened': checked.not_opened, 'notes': checked.notes})
        if checked.refusals:
            conn.rollback()
            raise Refused('; '.join(checked.refusals))
        return checked

    checked = matching.Checked({}, {}, [], {})
    second = {}
    if evidence or candidates:
        checked = match('matching', handover, matching.build_lists(conn, handover, shown, cfg.search_top_n), shown)
        pending = [(e, checked.outcomes[link][1]) for e in evidence for link in e['links']
                   if link in checked.outcomes and checked.outcomes[link][0] == matching.OUTCOMES[0]]
        if pending:
            mapped = {e['id']: dict(e, links=list(dict.fromkeys(v for x, v in pending if x['id'] == e['id']))) for e, _ in pending}
            second_handover = dataclasses.replace(handover, candidates=[], evidence=list(mapped.values()))
            lists = matching.Lists({}, {(e['id'], vid): matching.rank_evidence(conn, vid, e['one_line'], cfg.search_top_n) for e, vid in pending})
            second = match('matching-evidence', second_handover, lists, [], sorted({vid for _, vid in pending})).evidence
    # The group write is in the SAME outer transaction as the current product writer.
    try:
        with conn:
            written = writing.write(conn, uni, seq, item, handover, checked, second)
            bindings, affected = [], []
            if grouped:
                used = {ref for c in candidates for ref in c['thread_ids']}
                definitions = [g for g in answer.data['threads'] if g['id'] in used]
                bindings, affected = groups.write_threads(conn, definitions, {ref: ref for ref in used}, handover, checked, written, seq, item)
            store.insert(conn, 'handovers', input_id=item['input_id'], seq=seq, handover_json=json.dumps(dataclasses.asdict(handover), ensure_ascii=False))
            dispatch.mark(conn, item, seq, 'written', 'ok', json.dumps({'new': written.new_views, 'changed': sorted(written.changed_views)}))
            dispatch.mark(conn, item, seq, 'handed_over', 'ok', '')
    except Exception:
        conn.rollback()
        raise
    result = {'route': 'written', 'input_id': item['input_id'], 'seq': seq, 'new_views': written.new_views,
              'evidence_ids': written.evidence_ids, 'bindings': bindings, 'affected_threads': affected,
              'notes': written.notes, 'snapshot': snapshot(conn, seq)}
    write(directory / 'result.json', result)
    return result


class BoundedTransport:
    """One request, durable budget reservation, exact request and raw response, no retries."""
    def __init__(self, out, label, deadline, send=None):
        self.out, self.label, self.deadline, self.send = out, label, deadline, send

    def __call__(self, provider, request):
        budget_path = self.out / 'budget.json'
        budget = read(budget_path)
        encoded = json.dumps(request, ensure_ascii=False).encode()
        price_in, price_out = model.PRICES[request['model']]
        reserve = (len(encoded) * price_in + request['max_completion_tokens'] * price_out) / 1e6
        if time.monotonic() >= self.deadline or len(budget['attempts']) >= MAX_REQUESTS or budget['reserved_or_spent'] + reserve > MAX_USD:
            raise RuntimeError('Registered time/call/cost limit reached; no request sent')
        record = {'status': 'started', 'label': self.label, 'request': request, 'reserved_usd': reserve}
        budget['attempts'].append({'label': self.label, 'status': 'started', 'reserved_usd': reserve})
        budget['reserved_or_spent'] += reserve
        write(budget_path, budget)
        path = self.out / self.label / f'call-{len(budget["attempts"]):02d}.json'
        write(path, record)
        started = time.monotonic()
        print(f'START {self.label} call={len(budget["attempts"])} reserve=${reserve:.4f}', flush=True)
        try:
            if self.send is not None:
                response = self.send(provider, request)
            else:
                url, _ = model.ENDPOINTS[provider]
                headers = {'Authorization': f'Bearer {model._key(provider)}', 'Content-Type': 'application/json'}
                req = urllib.request.Request(url, data=encoded, headers=headers, method='POST')
                with urllib.request.urlopen(req, timeout=min(180, max(1, self.deadline - time.monotonic()))) as handle:
                    response = json.loads(handle.read().decode())
            record.update(status='complete', response=response, seconds=time.monotonic() - started)
            usage = response.get('usage', {})
            cost = (usage.get('prompt_tokens', 0) * price_in + usage.get('completion_tokens', 0) * price_out) / 1e6
            if 'prompt_tokens' not in usage or 'completion_tokens' not in usage:
                cost = reserve
            budget['reserved_or_spent'] += cost - reserve
            budget['attempts'][-1].update(status='complete', estimated_usd=cost)
            record['estimated_usd'] = cost
            write(path, record)
            write(budget_path, budget)
            print(f'DONE {self.label} usd=${cost:.4f} seconds={record["seconds"]:.1f}', flush=True)
            return response
        except Exception as error:
            # Error type only: avoid logging headers or credential-bearing exception objects.
            record.update(status='failed', error_type=type(error).__name__, seconds=time.monotonic() - started)
            budget['attempts'][-1]['status'] = 'failed'
            write(path, record)
            write(budget_path, budget)
            raise RuntimeError(f'Network attempt failed ({type(error).__name__}); no resend') from None


def prepare(out):
    if (out / 'manifest.json').exists() or any((out / label).exists() for label in LABELS):
        raise ValueError('Use a new experiment directory')
    if not (out / 'preflight.txt').is_file():
        raise ValueError('Run and inspect preflight first')
    with sqlite3.connect(f'file:{ITEMS_DB}?mode=ro', uri=True) as conn:
        conn.row_factory = sqlite3.Row
        items = [dict(conn.execute('select * from items where input_id=?', (ident,)).fetchone()) for ident in ITEM_IDS]
    for item in items:
        item['object_identifiers'] = json.loads(item['object_identifiers'])
    seeds = [dict(g, seq=0, input_id='reference:' + g['input_id']) for g in read(PREFIX)['threads']]
    write(out / 'items.json', items)
    write(out / 'reference-groups.json', seeds)
    write(out / 'config.json', read(ROOT / 'poc/config/poc-v16.json'))
    write(out / 'universe.json', read(ROOT / 'poc/universe.json'))
    paths = list((ROOT / 'src/hivemind').rglob('*.py')) + list((ROOT / 'src/hivemind/prompts').glob('*'))
    paths += [Path(__file__), ROOT / 'poc/hierarchy_study/ingestion_threads.py', ROOT / 'poc/hierarchy_study/study.py',
              ROOT / 'docs/research/2026-10-25-ohio-grouping-poc.md', PREFIX]
    paths += [out / name for name in ('items.json', 'reference-groups.json', 'config.json', 'universe.json', 'preflight.txt')]
    write(out / 'manifest.json', {'version': 'ohio-sequence-v1', 'labels': LABELS, 'max_requests': MAX_REQUESTS,
          'max_usd': MAX_USD, 'max_seconds': MAX_SECONDS, 'dependencies': {str(p.resolve()): digest(p) for p in paths if p.is_file()}})
    write(out / 'budget.json', {'attempts': [], 'reserved_or_spent': 0})


def verify(out):
    for path, sha in read(out / 'manifest.json')['dependencies'].items():
        if digest(path) != sha:
            raise ValueError(f'Frozen input/code changed: {path}')


def run(out):
    with (out / 'run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        verify(out)
        if read(out / 'budget.json')['attempts'] or any((out / label).exists() for label in LABELS):
            raise ValueError('Measurement already started; no automatic resume')
        items = read(out / 'items.json')
        uni, cfg = universe.load(out / 'universe.json'), config.load(out / 'config.json')
        deadline = time.monotonic() + MAX_SECONDS
        statuses = {label: 'not_started' for label in LABELS}
        write(out / 'status.json', statuses)
        for label in LABELS:
            verify(out)
            folder = out / label
            folder.mkdir()
            conn = groups.open_db(folder / 'views.sqlite')
            archive = model.Archive(str(folder / 'calls.sqlite'))
            grouped = label.startswith('grouped')
            if grouped:
                for g in read(out / 'reference-groups.json'):
                    conn.execute('insert into threads values (?,?,?,?,?)', tuple(g[k] for k in ('thread_id', 'name', 'scope', 'seq', 'input_id')))
                conn.commit()
            transport = BoundedTransport(out, label, deadline)
            try:
                first = None
                for index, item in enumerate(items, 1):
                    directory = folder / f'item{index}'
                    directory.mkdir()
                    result = process(conn, archive, cfg, uni, item, grouped, directory, transport)
                    if result['route'] != 'written':
                        raise Refused(f'Expected extract route, got {result["route"]}')
                    if index == 1:
                        first = result
                historical = [groups.thread_detail(conn, g['thread_id'], first['seq']) for g in first['snapshot']['threads']]
                if historical != first['snapshot']['details']:
                    raise AssertionError('First article history changed')
                if any(dispatch.route(conn, item, uni).kind != 'skipped' for item in items):
                    raise AssertionError('Completed input not skipped on resend')
                write(folder / 'checks.json', {'history_unchanged': True, 'resend_skipped': True, 'semantic_status': 'pending'})
                statuses[label] = 'complete'
            except (Refused, model.SchemaError) as error:
                statuses[label] = 'refused'
                write(folder / 'failed.json', {'kind': type(error).__name__, 'reason': str(error)[:1000]})
            except Exception as error:
                statuses[label] = 'failed'
                write(folder / 'failed.json', {'kind': type(error).__name__, 'reason': str(error)[:1000]})
                write(out / 'status.json', statuses)
                raise
            finally:
                conn.rollback()
                conn.close()
                archive.conn.close()
            verify(out)
            write(out / 'status.json', statuses)
        print(json.dumps(statuses), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('prepare', 'run'))
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    out = args.out.resolve()
    (prepare if args.command == 'prepare' else run)(out)


if __name__ == '__main__':
    main()
