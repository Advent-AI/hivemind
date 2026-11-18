"""Contract checks for the isolated Step 1 run; the model transport is fake."""
import importlib.util
import json
import sqlite3
import subprocess
import tempfile
import unittest
import urllib.error
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('clean_step1_runner', Path(__file__).with_name('runner.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
PRD = ROOT / 'clean-arch/PRD.md'


class Step1Test(unittest.TestCase):
    # The opening fields the adopted schema requires of every new thesis (D384, D387).
    OPENING = {'opens_as': 'product_node', 'settled_by': "The retailer's next annual report.", 'closest_open_thesis': None,
               'why_a_separate_bet': 'No open thesis asks it.'}

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.source = Path(self.tmp.name) / 'source.sqlite'
        self.output = Path(self.tmp.name) / 'run.sqlite'
        with sqlite3.connect(self.source) as c:
            c.execute('create table items (input_id text primary key, publication_day text, object_identifiers text, text text, publisher text, published_at text, source_uri text, title text, feed integer, copy_of text, supersedes text)')
            for item_id, text in [('a', 'The retailer raised its sales forecast.'), ('b', 'The retailer lowered its sales forecast.')]:
                c.execute('insert into items values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                          (item_id, '2026-01-10', '[{"kind":"ticker","value":"RETAILER"}]', text,
                           'Example publisher', '2026-01-10T10:00:00Z', 'https://example.com/article', 'Forecast', 1, None, None))
        self.manifest = {'entity': 'RETAILER', 'from_day': '2026-01-01', 'until_day': '2026-01-31',
                         'item_ids': ['a', 'b'], 'item_limit': 2}
        self.settings = {'provider': 'openai', 'model': 'gpt-6-luna', 'reasoning_effort': 'low', 'max_output_tokens': 2000}

    @staticmethod
    def evidence(text, target_type, target_id):
        return {'local_id': 'e1', 'summary': text, 'source_passages': [text], 'original_party': 'retailer',
                'reporting_speaker': None, 'tier': 'party_statement', 'statement_date': None,
                'statement_date_text': None, 'evidence_period': None, 'figures': [],
                'links': [{'target_type': target_type, 'target_id': target_id, 'relevance': 'The forecast informs sales.'}]}

    def invoke(self, transport, initial=None):
        runner.run(self.source, self.output, self.manifest, initial or [], self.settings, transport, PRD)
        with sqlite3.connect(self.output) as c:
            c.row_factory = sqlite3.Row
            return [dict(r) for r in c.execute('select * from trace order by sequence')]

    def test_new_thesis_is_visible_to_next_article_and_existing_reference_is_reused(self):
        first = {'new_theses': [{'local_id': 'n1', 'description': 'Will sales grow?',
                                  'outcome': 'Sales growth', 'period': None, **self.OPENING}],
                 'evidence': [self.evidence('The retailer raised its sales forecast.', 'new', 'n1')]}
        second = {'new_theses': [], 'evidence': [self.evidence('The retailer lowered its sales forecast.', 'existing', 'clean-1')]}
        responses = [{'choices': [{'message': {'content': json.dumps(result)}}]} for result in (first, second)]
        traces = self.invoke(runner.RecordedTransport(responses))
        seen = [json.JSONDecoder().raw_decode(json.loads(t['request'])['messages'][1]['content'])[0] for t in traces]   # the closing check follows the payload (D387)
        self.assertEqual([x['status'] for x in traces], ['complete', 'complete'])
        self.assertEqual(seen[1]['open_theses'][0]['id'], 'clean-1')
        self.assertEqual(len(json.loads(traces[1]['after_state'])), 1)

    def test_candidate_closing_check_ends_the_user_message_after_the_item(self):
        # AGENTS §6: a test the model applies to each statement is read last, after the item it judges.
        answer = {'new_theses': [], 'evidence': []}
        responses = [{'choices': [{'message': {'content': json.dumps(answer)}}]} for _ in range(2)]
        runner.run(self.source, self.output, self.manifest, [], self.settings, runner.RecordedTransport(responses), PRD,
                   texts=('Candidate system prompt.', 'Closing check: return only what passes.'))
        with sqlite3.connect(self.output) as c:
            request = json.loads(c.execute('select request from trace where sequence=1').fetchone()[0])
        user = request['messages'][1]['content']
        self.assertTrue(user.endswith('\n\nClosing check: return only what passes.'))
        payload, end = json.JSONDecoder().raw_decode(user)
        self.assertEqual(request['messages'][0]['content'], 'Candidate system prompt.')
        self.assertEqual(payload['source_item']['text'], 'The retailer raised its sales forecast.')
        self.assertEqual(user[end:], '\n\nClosing check: return only what passes.')

    def test_a_run_without_candidate_files_sends_the_adopted_c8_request(self):
        # D387 (Alex, 2026-11-09: "采用 c8"): the PRD carries c8's system prompt, closing check and schema, byte for byte the frozen files.
        arms = ROOT / 'clean-arch/step1-unfiled-2026-11-08/arms'
        answer = {'new_theses': [], 'evidence': []}
        responses = [{'choices': [{'message': {'content': json.dumps(answer)}}]} for _ in range(2)]
        traces = self.invoke(runner.RecordedTransport(responses))
        request = json.loads(traces[0]['request'])
        self.assertEqual(request['messages'][0]['content'], (arms / 'c8-system.txt').read_text(encoding='utf-8'))
        self.assertTrue(request['messages'][1]['content'].endswith('\n\n' + (arms / 'c8-closing.txt').read_text(encoding='utf-8')))
        self.assertEqual(runner.draft(PRD)[1], json.loads((arms / 'c8-schema.json').read_text(encoding='utf-8')))

    def test_material_evidence_with_no_thesis_is_kept_unlinked(self):
        # Alex, 2026-11-08 (second amendment of D209): a statement the model returns as material but no thesis takes is kept, unlinked,
        # in the company's record; it is stored with the run's evidence, and no thesis is invented for it.
        schema = json.loads(json.dumps(runner.draft(PRD)[1]))
        schema['properties']['evidence']['items']['properties']['links']['minItems'] = 0
        unfiled = dict(self.evidence('The retailer raised its sales forecast.', 'new', 'n1'), links=[])
        answer = {'new_theses': [], 'evidence': [unfiled]}
        responses = [{'choices': [{'message': {'content': json.dumps(answer)}}]} for _ in range(2)]
        runner.run(self.source, self.output, self.manifest, [], self.settings, runner.RecordedTransport(responses), PRD, schema=schema)
        with sqlite3.connect(self.output) as c:
            result, after = c.execute('select result, after_state from trace where sequence=1').fetchone()
        result = json.loads(result)
        self.assertEqual([ev['summary'] for ev in result['evidence']], ['The retailer raised its sales forecast.'])
        self.assertEqual(result['evidence'][0]['links'], [])
        self.assertEqual(result['unfiled_evidence'], [])
        self.assertEqual(json.loads(after), [])

    def figures_schema(self):
        schema = json.loads(json.dumps(runner.draft(PRD)[1]))
        items = schema['properties']['evidence']['items']
        items['properties']['links']['minItems'] = 0
        items['properties']['figures'] = {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False,
            'required': ['measure', 'period', 'value', 'kind', 'basis'],
            'properties': {'measure': {'type': 'string'}, 'period': {'anyOf': [{'type': 'string'}, {'type': 'null'}]},
                           'value': {'type': 'string'}, 'kind': {'type': 'string', 'enum': ['actual', 'guidance', 'estimate']},
                           'basis': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}}}}
        return schema

    def test_a_statement_keeps_all_its_figures_in_one_item(self):
        # STEP1-CONDITIONS-DESIGN.md §16: a statement with several figures stays one item listing them all; with no thesis it is kept.
        text = 'Quarterly revenue was $12.1 billion, up 8%, and gross margin was 41%. The retailer opened a new store.'
        revenue = {'measure': 'quarterly revenue', 'period': 'the quarter', 'value': '$12.1 billion', 'kind': 'actual', 'basis': None}
        margin = dict(revenue, measure='gross margin', value='41%')
        figure = dict(self.evidence('Quarterly revenue was $12.1 billion, up 8%, and gross margin was 41%.', 'new', 'n1'), links=[],
                      figures=[revenue, margin])
        store = dict(self.evidence('The retailer opened a new store.', 'new', 'n1'), local_id='e2', links=[], figures=[])
        result = runner.validate({'new_theses': [], 'evidence': [figure, store]}, self.figures_schema(), {'text': text}, [])
        self.assertEqual([ev['local_id'] for ev in result['evidence']], ['e1', 'e2'])
        self.assertEqual([f['measure'] for f in result['evidence'][0]['figures']], ['quarterly revenue', 'gross margin'])
        self.assertEqual(result['evidence'][1]['figures'], [])
        self.assertEqual(result['figure_issues'], [])

    def test_figure_must_be_quoted_with_numeric_boundaries(self):
        # STEP1-CONDITIONS-DESIGN.md §12.1: "2.1" inside "12.1" is not the figure; the figure is removed with its reason and the
        # statement itself is still kept.
        text = 'Quarterly revenue was $12.1 billion, up 8%.'
        wrong = dict(self.evidence(text, 'new', 'n1'), links=[],
                     figures=[{'measure': 'quarterly revenue', 'period': None, 'value': '2.1 billion', 'kind': 'actual', 'basis': None}])
        result = runner.validate({'new_theses': [], 'evidence': [wrong]}, self.figures_schema(), {'text': text}, [])
        self.assertEqual(result['figure_issues'][0]['reason'], 'figure value not quoted in a verified passage')
        self.assertEqual(result['evidence'][0]['figures'], [])

    def test_figure_boundaries(self):
        found = runner.figure_in_passages
        self.assertTrue(found('$96.2 billion', ['Revenue was $96.2 billion.']))
        self.assertFalse(found('2.1', ['Margin rose to 12.1%.']))
        self.assertFalse(found('96', ['Revenue was $96.2 billion.']))
        self.assertFalse(found('234', ['Units of 1,234 shipped.']))
        self.assertTrue(found('8%', ['up 8%, on demand']))
        self.assertFalse(found('8%', [None]))

    def test_unresolved_reference_is_recorded_without_inventing_a_thesis(self):
        self.manifest['item_ids'] = ['a']
        bad = {'new_theses': [], 'evidence': [self.evidence('The retailer raised its sales forecast.', 'existing', 'missing')]}
        response = {'choices': [{'message': {'content': json.dumps(bad)}}]}
        traces = self.invoke(runner.RecordedTransport([response]))
        self.assertEqual(len(traces), 1)
        self.assertEqual(traces[0]['status'], 'complete')
        self.assertEqual(json.loads(traces[0]['after_state']), [])
        self.assertEqual(json.loads(traces[0]['result'])['unresolved_links'][0]['target_id'], 'missing')
        self.assertEqual(json.loads(json.loads(traces[0]['raw_response'])['choices'][0]['message']['content']), bad)

    def test_repair_is_visible_and_changed_number_or_date_is_not_accepted(self):
        _, schema = runner.draft(PRD)
        item = {'text': 'The retailer raised guidance , effective in June.'}
        ev = self.evidence('The retailer raised guidance, effective in June.', 'existing', 't1')
        answer = {'new_theses': [], 'evidence': [ev]}
        result = runner.validate(answer, schema, item, [{'id': 't1'}])
        self.assertTrue(result['evidence'][0]['source_passages_repaired'][0])
        self.assertEqual(result['evidence'][0]['verified_source_passages'][0], item['text'])
        ev['source_passages'] = ['The retailer raised guidance, effective in May.']
        result = runner.validate(answer, schema, item, [{'id': 't1'}])
        self.assertEqual(result['evidence'][0]['verified_source_passages'], [None])

    def test_one_evidence_can_cite_separate_passages_without_losing_either(self):
        _, schema = runner.draft(PRD)
        first = 'The retailer raised its annual sales forecast.'
        second = 'The company expects growth to exceed ten percent.'
        item = {'text': first + ' Background appears between the statements. ' + second}
        ev = self.evidence(first, 'existing', 't1')
        ev['source_passages'] = [first, second]
        result = runner.validate({'new_theses': [], 'evidence': [ev]}, schema, item, [{'id': 't1'}])
        self.assertEqual(result['evidence'][0]['verified_source_passages'], [first, second])
        self.assertEqual(result['evidence'][0]['source_passages_repaired'], [False, False])
        ev['source_passages'] = [first + ' ... ' + second]
        result = runner.validate({'new_theses': [], 'evidence': [ev]}, schema, item, [{'id': 't1'}])
        self.assertEqual(result['evidence'][0]['verified_source_passages'], [None])

    def test_missing_or_empty_passage_stops_item_without_advancing(self):
        for passages in ([], ['The retailer raised its sales forecast.', '']):
            bad = {'new_theses': [{'local_id': 'n1', 'description': 'Will sales grow?',
                                   'outcome': 'Sales growth', 'period': None, **self.OPENING}],
                   'evidence': [self.evidence('The retailer raised its sales forecast.', 'new', 'n1')]}
            bad['evidence'][0]['source_passages'] = passages
            if self.output.exists(): self.output.unlink()
            response = {'choices': [{'message': {'content': json.dumps(bad)}}]}
            traces = self.invoke(runner.RecordedTransport([response]))
            self.assertEqual(traces[0]['status'], 'failed')
            self.assertEqual(json.loads(traces[0]['after_state']), [])

    def test_unmatched_passage_is_visible_and_does_not_stop_next_article(self):
        first = {'new_theses': [{'local_id': 'n1', 'description': 'Will sales grow?', 'outcome': 'Sales growth', 'period': None, **self.OPENING}],
                 'evidence': [self.evidence('A paraphrased sales forecast.', 'new', 'n1')]}
        second = {'new_theses': [], 'evidence': [self.evidence('The retailer lowered its sales forecast.', 'existing', 'clean-1')]}
        responses = [{'choices': [{'message': {'content': json.dumps(x)}}]} for x in (first, second)]
        traces = self.invoke(runner.RecordedTransport(responses))
        self.assertEqual([x['status'] for x in traces], ['complete', 'complete'])
        result = json.loads(traces[0]['result'])['evidence'][0]
        self.assertEqual(result['source_passages'], ['A paraphrased sales forecast.'])
        self.assertEqual(result['verified_source_passages'], [None])
        self.assertEqual(json.JSONDecoder().raw_decode(json.loads(traces[1]['request'])['messages'][1]['content'])[0]['open_theses'][0]['id'], 'clean-1')

    def test_repair_refuses_reversed_comparison(self):
        _, schema = runner.draft(PRD)
        quote = 'The retailer reported quarterly sales > $200 million for this period.'
        item = {'text': 'The retailer reported quarterly sales < $200 million for this period.'}
        answer = {'new_theses': [], 'evidence': [self.evidence(quote, 'existing', 't1')]}
        result = runner.validate(answer, schema, item, [{'id': 't1'}])
        self.assertEqual(result['evidence'][0]['verified_source_passages'], [None])

    def test_repair_refuses_changed_tense_and_moved_comparison(self):
        _, schema = runner.draft(PRD)
        cases = [
            ('The company did reduce production during the next scheduled operating period.',
             'The company will reduce production during the next scheduled operating period.'),
            ('The company reported profit > $100 million and revenue $200 million.',
             'The company reported profit $100 million and revenue > $200 million.'),
            ('The company said it will increase its shipments next year.',
             'The company said it will not increase its shipments next year.'),
            ('The company said quarterly sales were > $200 million for the period.',
             'The company said quarterly sales were >= $200 million for the period.'),
            ('The company recorded a change of + $200 million during the quarter.',
             'The company recorded a change of - $200 million during the quarter.'),
        ]
        for quote, source in cases:
            answer = {'new_theses': [], 'evidence': [self.evidence(quote, 'existing', 't1')]}
            result = runner.validate(answer, schema, {'text': source}, [{'id': 't1'}])
            self.assertEqual(result['evidence'][0]['verified_source_passages'], [None])

    def test_repair_accepts_punctuation_spacing_and_added_final_period(self):
        _, schema = runner.draft(PRD)
        quote = 'The retailer raised guidance, effective in June'
        item = {'text': 'The retailer raised guidance , effective in June.'}
        answer = {'new_theses': [], 'evidence': [self.evidence(quote, 'existing', 't1')]}
        result = runner.validate(answer, schema, item, [{'id': 't1'}])
        self.assertEqual(result['evidence'][0]['verified_source_passages'], [item['text']])

    def test_full_normalized_match_keeps_original_source_punctuation(self):
        _, schema = runner.draft(PRD)
        source = 'The survey results were reported by Counterpoint .'
        quote = 'The survey results were reported by Counterpoint.'
        result = runner.validate({'new_theses': [], 'evidence': [self.evidence(quote, 'existing', 't1')]},
                                 schema, {'text': source}, [{'id': 't1'}])
        evidence = result['evidence'][0]
        self.assertEqual(evidence['source_passages'], [quote])
        self.assertEqual(evidence['verified_source_passages'], [source])
        self.assertEqual(evidence['source_passages_repaired'], [True])
        self.assertNotIn('quote_lookup_errors', result)

    def test_lookup_error_is_recorded_without_stopping_later_articles(self):
        first_evidence = self.evidence('A paraphrased sales forecast.', 'new', 'n1')
        first_evidence['source_passages'].append('A different paraphrased forecast.')
        first = {'new_theses': [{'local_id': 'n1', 'description': 'Will sales grow?', 'outcome': 'Sales growth', 'period': None, **self.OPENING}],
                 'evidence': [first_evidence]}
        second = {'new_theses': [], 'evidence': [self.evidence('The retailer lowered its sales forecast.', 'existing', 'clean-1')]}
        responses = [{'choices': [{'message': {'content': json.dumps(x)}}]} for x in (first, second)]
        with patch.object(runner.quote_lookup, 'build_index', side_effect=ValueError('index failure')) as build:
            traces = self.invoke(runner.RecordedTransport(responses))
        self.assertEqual([t['status'] for t in traces], ['complete', 'complete'])
        build.assert_called_once()
        result = json.loads(traces[0]['result'])
        self.assertEqual(result['evidence'][0]['verified_source_passages'], [None, None])
        self.assertEqual(result['quote_lookup_errors'], [
            {'evidence_id': 'e1', 'passage_number': 1, 'error_type': 'ValueError', 'message': 'index failure'},
            {'evidence_id': 'e1', 'passage_number': 2, 'error_type': 'ValueError', 'message': 'index failure'},
        ])
        self.assertEqual(json.loads(traces[1]['before_state'])[0]['id'], 'clean-1')

    def test_normalized_candidates_with_different_source_bytes_remain_unverified(self):
        _, schema = runner.draft(PRD)
        quote = 'Shipments began in May.'
        source = 'Shipments began in May . SHIPMENTS began in May .'
        result = runner.validate({'new_theses': [], 'evidence': [self.evidence(quote, 'existing', 't1')]},
                                 schema, {'text': source}, [{'id': 't1'}])
        self.assertEqual(result['evidence'][0]['verified_source_passages'], [None])

    def test_one_lookup_error_does_not_prevent_the_next_passage_from_being_located(self):
        _, schema = runner.draft(PRD)
        first = 'Quarterly sales were 100 dollars.'
        second = 'Quarterly profit was 20 dollars.'
        source = 'Quarterly sales were 100 dollars . Quarterly profit was 20 dollars .'
        evidence = self.evidence(first, 'existing', 't1')
        evidence['source_passages'].append(second)
        original = runner.quote_lookup.find_quote

        def lookup(quote, text, index):
            if quote == first:
                raise ValueError('lookup failed')
            return original(quote, text, index)

        with patch.object(runner.quote_lookup, 'build_index', wraps=runner.quote_lookup.build_index) as build:
            with patch.object(runner.quote_lookup, 'find_quote', side_effect=lookup):
                result = runner.validate({'new_theses': [], 'evidence': [evidence]}, schema,
                                         {'text': source}, [{'id': 't1'}])
        build.assert_called_once()
        self.assertEqual(result['evidence'][0]['source_passages'], [first, second])
        self.assertEqual(result['evidence'][0]['verified_source_passages'], [None, 'Quarterly profit was 20 dollars .'])
        self.assertEqual(result['quote_lookup_errors'], [
            {'evidence_id': 'e1', 'passage_number': 1, 'error_type': 'ValueError', 'message': 'lookup failed'}])

    def test_prepared_source_still_requires_its_captured_page(self):
        _, schema = runner.draft(PRD)
        quote = 'The survey results were reported by Counterpoint.'
        source = 'The survey results were reported by Counterpoint .'
        answer = {'new_theses': [], 'evidence': [self.evidence(quote, 'existing', 't1')]}
        for page, expected in [(source, source), (None, None), ('A different page.', None)]:
            with self.subTest(page=page):
                result = runner.validate(answer, schema, {'text': source, 'text_page': page, 'source_preparation': 'prepared'}, [{'id': 't1'}])
                self.assertEqual(result['evidence'][0]['verified_source_passages'], [expected])

    def test_prepared_page_rejection_does_not_trigger_a_new_lookup(self):
        _, schema = runner.draft(PRD)
        quote = 'The retailer raised guidance, effective in June'
        source = 'The retailer raised guidance , effective in June.'
        answer = {'new_theses': [], 'evidence': [self.evidence(quote, 'existing', 't1')]}
        with patch.object(runner.quote_lookup, 'build_index') as build:
            result = runner.validate(answer, schema,
                                     {'text': source, 'text_page': 'A different page.', 'source_preparation': 'prepared'},
                                     [{'id': 't1'}])
        build.assert_not_called()
        self.assertEqual(result['evidence'][0]['verified_source_passages'], [None])

    def test_new_thesis_without_evidence_and_impossible_date_are_refused(self):
        _, schema = runner.draft(PRD)
        answer = {'new_theses': [{'local_id': 'n1', 'description': 'Will sales grow?', 'outcome': 'Sales growth', 'period': None, **self.OPENING}], 'evidence': []}
        result = runner.validate(answer, schema, {'text': 'No evidence.'}, [])
        self.assertEqual(result['unlinked_new_thesis_ids'], ['n1'])
        ev = self.evidence('The retailer raised its sales forecast.', 'existing', 't1')
        ev['statement_date'] = '2026-02-30'
        with self.assertRaises(runner.ContractError):
            runner.validate({'new_theses': [], 'evidence': [ev]}, schema, {'text': ev['source_passages'][0]}, [{'id': 't1'}])

    def test_missing_link_and_orphan_are_retained_but_only_linked_thesis_advances(self):
        first = {'new_theses': [{'local_id': 'n1', 'description': 'Will sales grow?', 'outcome': 'Sales growth', 'period': None, **self.OPENING},
                                 {'local_id': 'n2', 'description': 'Will margins grow?', 'outcome': 'Margin growth', 'period': None, **self.OPENING}],
                 'evidence': [self.evidence('The retailer raised its sales forecast.', 'new', 'n1'),
                              {**self.evidence('The retailer raised its sales forecast.', 'new', 'missing'), 'local_id': 'e2'}]}
        second = {'new_theses': [], 'evidence': [self.evidence('The retailer lowered its sales forecast.', 'existing', 'clean-1')]}
        responses = [{'choices': [{'message': {'content': json.dumps(x)}}]} for x in (first, second)]
        traces = self.invoke(runner.RecordedTransport(responses))
        result = json.loads(traces[0]['result'])
        self.assertEqual(result['unlinked_new_thesis_ids'], ['n2'])
        self.assertEqual(result['unresolved_links'][0]['target_id'], 'missing')
        self.assertEqual([x['description'] for x in json.loads(traces[0]['after_state'])], ['Will sales grow?'])
        self.assertEqual(len(json.loads(traces[1]['before_state'])), 1)

    def test_empty_thesis_question_fails_without_advancing(self):
        bad = {'new_theses': [{'local_id': 'n1', 'description': ' ', 'outcome': 'Sales growth', 'period': None, **self.OPENING}],
               'evidence': [self.evidence('The retailer raised its sales forecast.', 'new', 'n1')]}
        response = {'choices': [{'message': {'content': json.dumps(bad)}}]}
        traces = self.invoke(runner.RecordedTransport([response]))
        self.assertEqual(traces[0]['status'], 'failed')
        self.assertEqual(json.loads(traces[0]['after_state']), [])

    def test_selection_refuses_feed_copies_and_corrections(self):
        with sqlite3.connect(self.source) as c:
            c.execute('update items set copy_of=? where input_id=?', ('a', 'b'))
        with self.assertRaises(runner.ContractError):
            runner.selected_items(self.source, self.manifest)

    def test_live_transport_is_refused_before_creating_output(self):
        with self.assertRaises(runner.ContractError):
            self.invoke(lambda provider, request: None)
        self.assertFalse(self.output.exists())

    def test_invalid_initial_thesis_is_refused_before_creating_output(self):
        initial = [{'id': 't1', 'entity': 'RETAILER', 'description': ' ', 'outcome': 'Sales', 'period': None}]
        with self.assertRaises(runner.ContractError):
            self.invoke(runner.RecordedTransport([]), initial)
        self.assertFalse(self.output.exists())

    def test_live_request_records_exact_sent_body_and_rejects_incomplete_response(self):
        from live import LiveTransport
        bodies = []
        def send(provider, request, timeout, max_attempts):
            bodies.append(json.dumps(request).encode())
            self.assertEqual(max_attempts, 1)
            response = {'choices': [{'finish_reason': 'length', 'message': {'content': '{"new_theses":[],"evidence":[]}'}}]}
            return response
        limits = {'max_usd': 1, 'max_seconds': 60, 'max_calls': 2,
                  'input_usd_per_million': .5, 'output_usd_per_million': 1}
        traces = self.invoke(LiveTransport(limits, send=send))
        self.assertEqual(traces[0]['status'], 'failed')
        self.assertEqual(traces[0]['request'].encode(), bodies[0])
        self.assertGreater(traces[0]['reserved_usd'], 0)
        self.assertIn('incomplete', traces[0]['error'])

    def test_live_budget_stops_before_network_and_http_body_is_retained(self):
        from live import LiveTransport
        response_body = b'{"error":"request rejected"}'
        called = []
        def send(provider, request, timeout, max_attempts):
            from hivemind import model
            called.append(True)
            error = model.TransportError('HTTP 400')
            error.http_status = 400
            error.response_body = response_body.decode()
            raise error
        limits = {'max_usd': .000001, 'max_seconds': 60, 'max_calls': 1,
                  'input_usd_per_million': .5, 'output_usd_per_million': 1}
        transport = LiveTransport(limits, send=send)
        traces = self.invoke(transport)
        self.assertEqual(called, [])
        self.assertEqual(traces[0]['status'], 'failed')
        self.assertIn('limit reached', traces[0]['error'])
        self.output.unlink()
        limits['max_usd'] = 1
        traces = self.invoke(LiveTransport(limits, send=send))
        self.assertEqual(json.loads(traces[0]['raw_response'])['raw_body'], response_body.decode())
        self.assertEqual(json.loads(traces[0]['raw_response'])['http_status'], 400)
        self.assertGreater(traces[0]['reserved_usd'], 0)

    def test_invalid_live_limits_and_output_cap_refuse_before_send(self):
        from live import LiveTransport
        limits = {'max_usd': 1, 'max_seconds': 60, 'max_calls': 1,
                  'input_usd_per_million': .5, 'output_usd_per_million': 1}
        for value in (0, .5, True, float('nan')):
            with self.assertRaises(ValueError):
                LiveTransport({**limits, 'max_calls': value}, send=lambda *_: self.fail('sent'))
        for value in (0, -1, True, 1.5):
            self.settings['max_output_tokens'] = value
            with self.assertRaises(runner.ContractError):
                self.invoke(LiveTransport(limits, send=lambda *_: self.fail('sent')))
            self.assertFalse(self.output.exists())

    def test_live_path_uses_existing_archive_and_advances_state(self):
        from live import LiveTransport
        count = []
        def send(provider, request, timeout, max_attempts):
            count.append(1)
            if len(count) == 1:
                answer = {'new_theses': [{'local_id': 'n1', 'description': 'Will sales grow?',
                                           'outcome': 'Sales growth', 'period': None, **self.OPENING}],
                          'evidence': [self.evidence('The retailer raised its sales forecast.', 'new', 'n1')]}
            else:
                answer = {'new_theses': [], 'evidence': [self.evidence('The retailer lowered its sales forecast.', 'existing', 'clean-1')]}
            return {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps(answer)}}],
                    'usage': {'prompt_tokens': 100, 'completion_tokens': 50}}
        limits = {'max_usd': 1, 'max_seconds': 60, 'max_calls': 2,
                  'input_usd_per_million': .5, 'output_usd_per_million': 1}
        traces = self.invoke(LiveTransport(limits, send=send))
        self.assertEqual([row['status'] for row in traces], ['complete', 'complete'])
        with sqlite3.connect(self.output) as c:
            self.assertEqual(c.execute('select count(*) from model_calls').fetchone()[0], 2)
            self.assertGreater(c.execute('select sum(cost_usd) from model_calls').fetchone()[0], 0)

    def test_network_and_format_retries_of_one_step_are_both_recorded(self):
        """NETWORK-RETRY-DESIGN.md, council round 10: a network retry and a format resend in the same step are both kept in retry_reason."""
        from live import LiveTransport
        from hivemind import model
        cut = {'choices': [{'finish_reason': 'length', 'message': {'content': '{"new_theses":'}}], 'usage': {'prompt_tokens': 10, 'completion_tokens': 5}}
        def good(text):
            answer = {'new_theses': [], 'evidence': [self.evidence(text, 'existing', 'clean-1')]}
            return {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps(answer)}}], 'usage': {'prompt_tokens': 100, 'completion_tokens': 50}}
        outcomes = [model.TransportError('IncompleteRead(1 bytes read)'), cut, good('The retailer raised its sales forecast.'),
                    good('The retailer lowered its sales forecast.')]
        def send(provider, request, timeout, max_attempts):
            outcome = outcomes.pop(0)
            if isinstance(outcome, BaseException):
                raise outcome
            return outcome
        limits = {'max_usd': 1, 'max_seconds': 60, 'max_calls': 4, 'input_usd_per_million': .5, 'output_usd_per_million': 1}
        initial = [{'id': 'clean-1', 'entity': 'RETAILER', 'description': 'Will sales grow?', 'outcome': 'Sales growth', 'period': None}]
        traces = self.invoke(LiveTransport(limits, send=send, wait=lambda seconds: None), initial)
        self.assertEqual([row['status'] for row in traces], ['complete', 'complete'])
        self.assertIn('network retry, attempt 1: TransportError', traces[0]['retry_reason'])
        self.assertIn('SchemaError', traces[0]['retry_reason'])
        self.assertIsNone(traces[1]['retry_reason'])

    def deepseek_sends(self, answers):
        """A fake DeepSeek endpoint returning the given answers in order; records what was sent."""
        sent = []
        def send(provider, request, timeout, max_attempts):
            sent.append((provider, request))
            return {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps(answers[len(sent) - 1])}}],
                    'usage': {'prompt_tokens': 100, 'completion_tokens': 50}}
        self.settings = dict(self.settings, provider='deepseek', model='deepseek-flash', reasoning_effort='high')
        return sent, send

    def test_deepseek_is_sent_in_json_mode_with_the_schema_and_the_sent_bytes_are_kept(self):
        # DeepSeek refuses a strict schema: the schema rides in the system text and the sent bytes are kept.
        from live import LiveTransport
        good = {'new_theses': [], 'evidence': [self.evidence('The retailer raised its sales forecast.', 'new', 'n1')]}
        sent, send = self.deepseek_sends([good, good])
        limits = {'max_usd': 1, 'max_seconds': 60, 'max_calls': 2, 'input_usd_per_million': .5, 'output_usd_per_million': 1}
        traces = self.invoke(LiveTransport(limits, send=send))
        provider, request = sent[0]
        self.assertEqual((provider, request['model'], request['response_format'], request['reasoning_effort']),
                         ('deepseek', 'deepseek-flash', {'type': 'json_object'}, 'high'))
        self.assertIn('"required": ["new_theses", "evidence"]', request['messages'][0]['content'])
        self.assertEqual(json.loads(traces[0]['raw_response'])['sent_request'], request)

    def test_nonconforming_answer_is_sent_once_more_and_kept_when_the_retry_conforms(self):
        # Alex, 2026-11-08: a format failure is retried once with the identical request.
        from live import LiveTransport
        good = {'new_theses': [], 'evidence': [self.evidence('The retailer raised its sales forecast.', 'new', 'n1')]}
        sent, send = self.deepseek_sends([{'evidence': []}, good, good])
        limits = {'max_usd': 1, 'max_seconds': 60, 'max_calls': 3, 'input_usd_per_million': .5, 'output_usd_per_million': 1}
        traces = self.invoke(LiveTransport(limits, send=send))
        self.assertEqual([row['status'] for row in traces], ['complete', 'complete'])
        self.assertEqual(sent[0][1], sent[1][1])
        self.assertIn('SchemaError', traces[0]['retry_reason'])
        self.assertIsNone(traces[1]['retry_reason'])

    def test_answer_failing_the_format_twice_marks_its_item_failed_and_the_run_continues(self):
        # Alex, 2026-11-08: after the retry also fails, the item is failed with both reasons and the next item still runs.
        from live import LiveTransport
        good = {'new_theses': [], 'evidence': [self.evidence('The retailer lowered its sales forecast.', 'new', 'n1')]}
        sent, send = self.deepseek_sends(['not an object', {'evidence': []}, good])
        limits = {'max_usd': 1, 'max_seconds': 60, 'max_calls': 3, 'input_usd_per_million': .5, 'output_usd_per_million': 1}
        outcome = runner.run(self.source, self.output, self.manifest, [], self.settings, LiveTransport(limits, send=send), PRD)
        with sqlite3.connect(self.output) as c:
            c.row_factory = sqlite3.Row
            traces = [dict(r) for r in c.execute('select * from trace order by sequence')]
        self.assertEqual([row['status'] for row in traces], ['failed', 'complete'])
        self.assertIn('retry: SchemaError', traces[0]['error'])
        self.assertEqual(outcome['status'], 'complete_with_failures')
        self.assertEqual([f['input_id'] for f in outcome['failed_items']], ['a'])
        self.assertEqual(len(sent), 3)

    def test_an_answer_cut_at_the_output_limit_is_sent_once_more(self):
        # Alex, 2026-11-08: "an answer that is not JSON ... is sent once more unchanged"; a cut answer is not JSON (LOG §30).
        from live import LiveTransport
        good = {'new_theses': [], 'evidence': [self.evidence('The retailer raised its sales forecast.', 'new', 'n1')]}
        sent = []
        def send(provider, request, timeout, max_attempts):
            sent.append(request)
            if len(sent) == 1:
                return {'choices': [{'finish_reason': 'length', 'message': {'content': '{"new_theses": ['}}],
                        'usage': {'prompt_tokens': 100, 'completion_tokens': 32000}}
            return {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps(good)}}],
                    'usage': {'prompt_tokens': 100, 'completion_tokens': 50}}
        self.settings = dict(self.settings, provider='deepseek', model='deepseek-flash', reasoning_effort='high')
        limits = {'max_usd': 1, 'max_seconds': 60, 'max_calls': 3, 'input_usd_per_million': .5, 'output_usd_per_million': 1}
        traces = self.invoke(LiveTransport(limits, send=send))
        self.assertEqual([row['status'] for row in traces], ['complete', 'complete'])
        self.assertEqual(sent[0], sent[1])
        self.assertIn('incomplete output', traces[0]['retry_reason'])

    def test_a_failure_other_than_the_format_still_stops_the_run(self):
        # A provider refusal is not a format failure: the run stops (LOG §16, corrected in §30).
        from live import LiveTransport
        sent = []
        def send(provider, request, timeout, max_attempts):
            sent.append(request)
            return {'choices': [{'finish_reason': 'stop', 'message': {'content': None, 'refusal': 'I cannot help with that.'}}],
                    'usage': {'prompt_tokens': 100, 'completion_tokens': 50}}
        self.settings = dict(self.settings, provider='deepseek', model='deepseek-flash', reasoning_effort='high')
        limits = {'max_usd': 1, 'max_seconds': 60, 'max_calls': 4, 'input_usd_per_million': .5, 'output_usd_per_million': 1}
        traces = self.invoke(LiveTransport(limits, send=send))
        self.assertEqual([row['status'] for row in traces], ['failed'])
        self.assertEqual(len(sent), 1)

    def test_existing_transport_can_send_once_without_retry(self):
        from hivemind import model
        with patch.object(model, '_key', return_value='test-key'), \
             patch.object(model.urllib.request, 'urlopen', side_effect=urllib.error.URLError('offline')) as send, \
             patch.object(model.time, 'sleep') as sleep:
            with self.assertRaises(model.TransportError):
                model.openai_transport('openai', {'model': 'gpt-6-luna'}, max_attempts=1)
        self.assertEqual(send.call_count, 1)
        sleep.assert_not_called()

    def test_existing_transport_retains_invalid_utf8_body(self):
        import base64
        from hivemind import model
        class Response:
            status = 200
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self): return b'bad\xffbody'
        with patch.object(model, '_key', return_value='test-key'), \
             patch.object(model.urllib.request, 'urlopen', return_value=Response()):
            with self.assertRaises(model.TransportError) as caught:
                model.openai_transport('openai', {'model': 'gpt-6-luna'}, max_attempts=1)
        self.assertEqual(caught.exception.http_status, 200)
        self.assertEqual(base64.b64decode(caught.exception.response_body_base64), b'bad\xffbody')

    def test_offline_command_reports_failure_and_preserves_trace(self):
        bad = {'new_theses': [], 'evidence': [self.evidence('The retailer raised its sales forecast.', 'existing', 'missing')]}
        bad['evidence'][0]['statement_date'] = '2026-02-30'
        values = {'manifest': self.manifest, 'initial': [], 'settings': self.settings,
                  'responses': [{'choices': [{'message': {'content': json.dumps(bad)}}]}]}
        command = ['python3', str(Path(__file__).with_name('run_offline.py')), '--source', str(self.source), '--output', str(self.output)]
        for name, value in values.items():
            path = Path(self.tmp.name) / (name + '.json')
            path.write_text(json.dumps(value), encoding='utf-8')
            command.extend(['--' + name, str(path)])
        completed = subprocess.run(command, text=True, capture_output=True)
        self.assertEqual(completed.returncode, 1)
        self.assertIn('invalid original statement date', completed.stderr)
        with sqlite3.connect(self.output) as c:
            self.assertEqual(c.execute('select status from trace').fetchone()[0], 'failed')


if __name__ == '__main__':
    unittest.main()
