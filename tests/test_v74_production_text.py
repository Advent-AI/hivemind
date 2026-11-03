"""Extraction v74i / poc-v108 (D274, the frozen production prompt): the v74 request with the deep-review text (the definition of a related party's
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

def test_v74i_states_the_paths_once_and_narrows_the_three_exceptions(tmp_path):
    """D273-D274 (design-v78-fields.md §13): the frozen v74i sends numeric takes lines without the shared tail, the links rule with the
    company-wide revenue question as the home of indirect evidence, and the closing check with the three exceptions narrowed to the
    standard's words; it names no covered company (AGENTS §6)."""
    conn = snapshot_ledger(tmp_path)
    v108 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v108.json'))
    _, s108, u108, schema = extraction.request_for(v108, ITEM, TEXT, extraction.shown_views(conn, v108, ITEM, ['NVDA']), UNI)
    l108 = schema['properties']['evidence']['items']['properties']['links']['description']
    assert 'more or less likely: the demand, supply, competition and pricing behind it' not in u108
    assert 'company-wide revenue question of its period' in l108
    assert 'newly disclosed revenue, capacity, orders or contracted amount' in u108 and 'a specific consequence' not in u108
    assert 'a reported movement of a named price, rental rate, lead time or order book' in u108
    assert 'The four kinds describe what material statements usually look like' in s108
    assert 'NVIDIA' not in s108.replace('NVDA', '') and 'Nvidia' not in s108                           # a general analyst prompt: no covered company named
