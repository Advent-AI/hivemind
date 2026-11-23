"""D580's $0 check: the production Idea planner (idea-summary-v8, the API's default configuration) on a stored new-system library.
Prints what the planner shows the model for a three-choice event, an undirected theme range and a directed company figure, the
endpoints its schema allows, and the plan a realistic answer binds to. No model call.

  python3 trace_planner.py <views.sqlite of a new-system store>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'src'))
from hivemind import bundle, idea_composite, service  # noqa: E402
from hivemind.views import store  # noqa: E402

CHOSEN = ('v3', 'v5', 'v2')       # in the fortnight's page store: an event, a theme range with no favourable end, a company figure


def main(views_db):
    conn = store.open_read_only(views_db)
    as_of = service.default_as_of(conn)
    records = {r['view_id']: r for r in service.summaries(conn, as_of)}
    chosen = [records[view_id] for view_id in CHOSEN]
    schema, _, bind = idea_composite.contract('idea-summary-v8', chosen, conn)
    shown = idea_composite.add_ladders(conn, [{'view_id': view_id} for view_id in CHOSEN], endpoints_only=True)
    allowed = {item['properties']['thesis_id']['enum'][0]: item['properties']['raises_outcome_position']['enum']
               for item in schema['properties']['composite']['items']['anyOf'] if 'raises_outcome_position' in item['properties']}
    for view_id, thesis in zip(CHOSEN, shown):
        full = [(r['position'], r['label']) for r in store.rungs_of(conn, view_id)]
        print(f'{view_id} {bundle.answer_shape(conn, view_id)}: all choices {full}')
        print(f'   shown to the planner {[(r["position"], r["label"]) for r in thesis["ladder"]]}; positions it may name {allowed.get(view_id)}')
    for event_end in ('1', '3'):
        answer = {'summary': 'China revenue outlook', 'outcome': 'NVIDIA data-center revenue growth', 'claim_direction': 'higher',
                  'composite': [{'thesis_id': 'v3', 'label': 'Blackwell export approval', 'raises_outcome_position': event_end,
                                 'reason': 'Approval opens China sales', 'weight_percent': 40, 'weight_reason': 'large market'},
                                {'thesis_id': 'v5', 'label': 'Hyperscaler capex', 'raises_outcome_position': '5',
                                 'reason': 'More capex, more GPUs', 'weight_percent': 40, 'weight_reason': 'main demand'},
                                {'thesis_id': 'v2', 'label': 'Supply commitments', 'raises_outcome_position': '5',
                                 'reason': 'Bigger commitments signal demand', 'weight_percent': 20, 'weight_reason': 'signal'}]}
        plan = bind(answer, chosen, records, as_of)
        print(f'event end named {event_end}: plan drivers', [(d['thesis_id'], d['supporting_end']) for d in plan['drivers']])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
