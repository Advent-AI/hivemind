"""Extraction v74d / poc-v103 (D271, D272, the default before the freeze) and v74i / poc-v108 (D274, the frozen production prompt): the v74 request with the deep-review text (the definition of a related party's
action, whose own business figures stay kind 2; the standard's named examples without amounts; an exception that only lifts its own line; the
decision on the one statement a record keeps; a participant's deal under a programme as its own item; evidence decided before filing); v74's
behaviour (no classification fields, the closing check) and v74's schema. Real ledger on a
temporary path; the universe the pipeline reads."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, extraction  # noqa: E402
from test_one_decider import snapshot_ledger  # noqa: E402
from test_placement import ITEM, TEXT, UNI  # noqa: E402

V94 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v94.json'))
V103 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v103.json'))


def test_v74d_changes_only_the_text_of_the_v74_request(tmp_path):
    conn = snapshot_ledger(tmp_path)
    _, system94, user94, schema94 = extraction.request_for(V94, ITEM, TEXT, extraction.shown_views(conn, V94, ITEM, ['NVDA']), UNI)
    _, system, user, schema = extraction.request_for(V103, ITEM, TEXT, extraction.shown_views(conn, V103, ITEM, ['NVDA']), UNI)
    assert json.dumps(schema) == json.dumps(schema94)                                          # same answer shape, no classification fields
    assert 'party' not in schema['properties']['evidence']['items']['properties']
    assert 'An action is a step the item reports as news' in system and 'An action is a step' not in system94
    assert 'it never keeps a statement by itself' in system and 'never that a statement is material' in system
    assert 'its own revenue, capacity, orders or contracted amounts are figures under (2)' in system                 # standard 5.1 kind 2: their reported figures
    assert 'a deal one party signs under a wider programme' in system and 'Copy its quote verbatim, without translation.' in system
    assert '"a bank chose a rival\'s system"' in system                                       # the standard's own kind-2 example, another industry
    assert user.rstrip().endswith('Return only the items you keep.') and 'three insurers run claims' in user
    assert 'NVIDIA' not in system.replace('NVDA', '') and 'Nvidia' not in system               # a general analyst prompt: no covered company named



def test_v74i_states_the_paths_once_and_narrows_the_three_exceptions(tmp_path):
    """D273-D274 (design-v78-fields.md §13): the frozen v74i sends numeric takes lines without the shared tail, the links rule with the company-wide
    revenue question as the home of indirect evidence, and the closing check with the three exceptions narrowed to the standard's words; v74d sends
    the tail and the v72 rule."""
    conn = snapshot_ledger(tmp_path)
    v108 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v108.json'))

    def request(cfg):
        _, system, user, schema = extraction.request_for(cfg, ITEM, TEXT, extraction.shown_views(conn, cfg, ITEM, ['NVDA']), UNI)
        return system, user, schema['properties']['evidence']['items']['properties']['links']['description']
    tail = 'more or less likely: the demand, supply, competition and pricing behind it'
    _, u103, l103 = request(V103)
    s108, u108, l108 = request(v108)
    assert tail in u103 and tail not in u108
    assert 'company-wide revenue question of its period' in l108 and 'company-wide revenue question of its period' not in l103
    assert 'newly disclosed revenue, capacity, orders or contracted amount' in u108 and 'a specific consequence' not in u108
    assert 'a reported movement of a named price, rental rate, lead time or order book' in u108
    assert 'The four kinds describe what material statements usually look like' in s108
    assert 'NVIDIA' not in s108.replace('NVDA', '') and 'Nvidia' not in s108                           # a general analyst prompt: no covered company named
