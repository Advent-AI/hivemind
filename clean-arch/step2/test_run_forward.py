"""How Step 2 reads a stored Step 1 trace (run_forward.step1_records): Step 1's verified passages travel with each record, so a
passage not found in the source stays marked. A link resolves as the runner resolves it, by its type (an existing target among the
theses shown open, a new target among those the answer opened); any other link stays out of the record's thesis ids instead of
stopping the run."""
import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('clean_step2_run_forward', HERE / 'run_forward.py')
run_forward = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_forward)

THESIS = {'id': 'clean-1', 'entity': 'NVDA', 'description': 'Will hyperscaler capex reach $1 trillion in 2027?',
          'outcome': 'Combined capex', 'period': 'calendar 2027'}


class Step1RecordsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.trace = Path(self.tmp.name) / 'trace.sqlite'
        payload = {'source_item': {'id': 'gnews:a1', 'publisher': 'Example News', 'publication_date': '2026-09-05', 'title': 'Capex'}}
        evidence = {'local_id': 'e1', 'summary': 'Microsoft raised its capital spending plan.', 'source_passages': ['Microsoft raised capex.'],
                    'verified_source_passages': [None], 'original_party': 'Microsoft', 'reporting_speaker': None, 'tier': 'fact',
                    'statement_date': '2026-09-04', 'statement_date_text': None, 'evidence_period': None, 'figures': [],
                    'links': [{'target_type': 'existing', 'target_id': 'clean-1', 'relevance': 'capex'},
                              {'target_type': 'existing', 'target_id': 'clean-9', 'relevance': 'capex'},
                              {'target_type': 'new', 'target_id': 'clean-1', 'relevance': 'a new thesis never opened, named like an open one'},
                              {'target_type': 'existing', 'target_id': 'clean-2', 'relevance': 'opened only by this answer'}]}
        request = {'messages': [{'role': 'system', 'content': 'system'},
                                {'role': 'user', 'content': json.dumps(payload) + '\n\nClosing check.\n'}]}
        with sqlite3.connect(self.trace) as conn:
            conn.execute('create table run (manifest text)')
            conn.execute('create table trace (sequence integer, input_id text, request text, result text, before_state text, '
                         'after_state text, status text)')
            conn.execute('insert into run values (?)', (json.dumps({'item_ids': ['gnews:a1']}),))
            conn.execute('insert into trace values (1, ?, ?, ?, ?, ?, ?)',
                         ('gnews:a1', json.dumps(request), json.dumps({'evidence': [evidence], 'new_thesis_ids': {}}),
                          json.dumps([THESIS]), json.dumps([THESIS, dict(THESIS, id='clean-2')]), 'complete'))

    def test_verified_passages_travel_and_an_unresolved_link_is_listed_apart(self):
        articles, questions, opened = run_forward.step1_records(str(self.trace))
        record = articles[0][0]
        self.assertEqual(record['verified_passages'], [None])
        self.assertEqual(record['thesis_ids'], ['clean-1'])
        self.assertEqual(record['unresolved_thesis_ids'], ['existing:clean-2', 'existing:clean-9', 'new:clean-1'])


if __name__ == '__main__':
    unittest.main()
