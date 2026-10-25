"""T1 of docs/poc/keyed-views-plan.md: give every view of a ledger its key (measure, scope, period, basis, unit, event type)
by one model call per view, into a new copy of the ledger (the source is never written), then report the key
collisions for an analyst to read. A collision between two open views with the same key is a duplicate the current
pipeline let through; near-collisions (same object, measure and period, different scope) are listed separately.

  python3 scripts/key_views.py --views poc/data/sealed-.../views.sqlite --out poc/data/keyed-2026-10-25/sealed-keyed.sqlite [--only 3]
"""
import argparse
import collections
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, model, service, universe  # noqa: E402
from hivemind.views import store  # noqa: E402

MEASURES = ['total_revenue', 'segment_revenue', 'product_revenue', 'gross_margin', 'operating_expense_growth', 'tax_rate', 'capex',
            'shipments_or_capacity', 'event', 'spend_total', 'price', 'capacity', 'growth_rate', 'policy_event', 'other']
EVENTS = ['launch', 'shipment', 'licence', 'approval', 'deal_close', 'deployment', 'other', 'n/a']
BASES = ['GAAP', 'non_GAAP', 'n/a']
UNITS = ['USD', 'percent', 'count', 'GW', 'MW', 'TWD', 'multiple', 'n/a']
SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['measure', 'scope', 'period_start', 'period_end', 'basis', 'unit', 'event_type'],
          'properties': {'measure': {'type': 'string', 'enum': MEASURES}, 'scope': {'type': 'string'},
                         'period_start': {'type': 'string'}, 'period_end': {'type': 'string'},
                         'basis': {'type': 'string', 'enum': BASES}, 'unit': {'type': 'string', 'enum': UNITS}, 'event_type': {'type': 'string', 'enum': EVENTS}}}
PROMPT = """你给研究库里的一条观点填「键」，让代码能判断两条观点是不是同一个量。只填字段，不改观点。
- measure：从清单里选最贴的量。公司的数：total_revenue（全年总收入）、segment_revenue（某分部）、product_revenue（某产品线）、gross_margin、operating_expense_growth、tax_rate、capex、shipments_or_capacity（出货量或产能）；事件：event；世界的数：spend_total（某群体的支出或资本开支合计）、price、capacity、growth_rate（行业增速）、policy_event（监管或政策的决定）；都不是：other。
- scope：量的限定名，英文短名词，规范写法：分部名（Data Center、Compute & Networking）、产品线（Blackwell+Rubin、Vera）、口径群（five hyperscalers、Big Tech、global AI infrastructure）、事件对象（Rubin、H20/H200 China licence）；没有限定写 "" 。
- period_start / period_end：这个量覆盖的起止日 ISO 格式。财年按给你的财年注换算（NVIDIA FY2027 = 2026-02-01 到 2027-01-31）；自然年 2026 = 2026-01-01 到 2026-12-31；事件写到期日所在的期间（start 为观点提出的年初，end 为到期日）。
- basis：GAAP、non_GAAP 或 n/a。unit：USD、percent、count、GW、MW、TWD、multiple 或 n/a。
- event_type：measure 为 event 或 policy_event 时选 launch、shipment、licence、approval、deal_close、deployment、other；否则 n/a。
只按给你的文字填，不用外部知识。"""


def normalize(scope):
    return re.sub(r'\s+', ' ', scope.replace('＋', '+').replace('&amp;', '&')).strip().casefold()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--views', required=True)
    parser.add_argument('--out', required=True, help='a new file: a copy of the ledger with a view_keys table')
    parser.add_argument('--archive', default=os.path.join(ROOT, 'poc', 'data', 'keyed-2026-10-25', 'key-archive.sqlite'))
    parser.add_argument('--config', default=os.path.join(ROOT, 'poc', 'config', 'poc-v7.json'), help='the idea setting (gpt-6-luna, effort low) is used for the keying call')
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    parser.add_argument('--as-of', default=None)
    parser.add_argument('--only', type=int, default=None)
    args = parser.parse_args()
    if os.path.exists(args.out):
        raise SystemExit(f'refused: {args.out} exists; keying writes a new copy')
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    shutil.copyfile(args.views, args.out)
    conn = store.open_read_only(args.views) if hasattr(store, 'open_read_only') else None
    ledger = service.open_ledger(args.views)
    out = __import__('sqlite3').connect(args.out)
    out.execute('create table if not exists view_keys (view_id text primary key, measure text, scope text, scope_key text, period_start text, period_end text, basis text, unit text, event_type text, answer_json text)')
    cfg = config.load(args.config); setting = cfg.idea; uni = universe.load(args.universe)
    archive = model.Archive(args.archive)
    as_of = args.as_of or service.default_as_of(ledger)
    rows = service.views(ledger, None, as_of, include_closed=True) if 'include_closed' in service.views.__code__.co_varnames else service.views(ledger, None, as_of)
    spent = 0.0
    for record in rows[:args.only]:
        rungs = store.rungs_of(ledger, record['view_id'])
        note = uni.fiscal_note(record['object'], record.get('due_day') or as_of) if uni.has(record['object']) else ''
        user = json.dumps({'view_id': record['view_id'], 'object': record['object'], 'object_kind': record['object_kind'], 'kind': record['kind'], 'looks_at': record['looks_at'],
                           'question': record.get('question', ''), 'due_day': record.get('due_day'), 'year': record.get('year'),
                           'rungs': [{'label': r['label'], 'condition': r['condition']} for r in rungs], 'fiscal_note': note}, ensure_ascii=False)
        answer = model.call(archive, cfg, setting, PROMPT, user, SCHEMA, 'view_key', 'keying')
        spent += answer.cost_usd
        d = answer.data
        out.execute('insert or replace into view_keys values (?,?,?,?,?,?,?,?,?,?)', (record['view_id'], d['measure'], d['scope'], normalize(d['scope']), d['period_start'], d['period_end'], d['basis'], d['unit'], d['event_type'], json.dumps(d, ensure_ascii=False)))
        out.commit()
        print(f"{record['view_id']:4s} {record['object']:20s} {d['measure']:24s} [{d['scope'][:28]:28s}] {d['period_start']}..{d['period_end']} {d['basis']:8s} {d['unit']:7s} {d['event_type']:10s} | {record['looks_at'][:50]}", flush=True)
    keys = collections.defaultdict(list); near = collections.defaultdict(list)
    for r in out.execute('select k.*, v.looks_at from view_keys k join views v on v.view_id=k.view_id'):
        view_id, measure, scope, scope_key, start, end, basis, unit, event_type = r[:9]; looks_at = r[-1]; obj = next(x['object'] for x in rows if x['view_id'] == view_id)
        keys[(obj, measure, scope_key, start, end, basis, event_type)].append((view_id, looks_at))
        near[(obj, measure, start, end)].append((view_id, scope, looks_at))
    collisions = {k: v for k, v in keys.items() if len(v) > 1}
    nears = {k: v for k, v in near.items() if len({s for _, s, _ in v}) > 1}
    print(f"\nkeyed {sum(len(v) for v in keys.values())} views, spent ${spent:.3f}; key collisions (same object, measure, scope, period, basis): {len(collisions)} groups, {sum(len(v) for v in collisions.values())} views")
    for k, v in collisions.items():
        print('   SAME KEY', k[:3], k[3], '..', k[4], '→', [(vid, la[:40]) for vid, la in v])
    print(f"near-collisions (same object, measure, period; different scope): {len(nears)} groups")
    for k, v in nears.items():
        print('   NEAR', k, '→', [(vid, s, la[:30]) for vid, s, la in v])


if __name__ == '__main__':
    main()
