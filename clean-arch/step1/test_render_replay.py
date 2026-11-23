"""Read-only viewer preserves the recorded thesis and evidence relationships."""
import importlib.util
import json
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('render_replay', Path(__file__).with_name('render_replay.py'))
viewer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(viewer)


class ReplayViewerTest(unittest.TestCase):
    def test_page_candidate_shows_sent_representation_prior_text_and_uncertainty(self):
        audit = {'representation': 'captured_page', 'source_identity': 'unassessed',
                 'source_completeness': 'unassessed', 'original_cleaned_text': 'Earlier <clean> text.',
                 'upstream_feed': 1, 'cleaned_feed': 0}
        item = {'title': 'Target', 'text': 'Captured page and related story.', 'publication_day': '2026-07-08',
                'retrieved_at': '2026-10-23T00:00:00Z', 'page_source_audit': json.dumps(audit)}
        row = {'sequence': 1, 'input_id': 'a', 'before_state': '[]', 'after_state': '[]',
               'result': json.dumps({'new_theses': [], 'evidence': []}), 'raw_response': None,
               'status': 'complete', 'error': None}
        page = viewer.render({'a': item}, [row], {})
        self.assertIn('Read the supplied source text', page)
        self.assertIn('Sent representation: captured_page', page)
        self.assertIn('Target-article identity: unassessed', page)
        self.assertIn('Source completeness: unassessed', page)
        self.assertIn('Captured at: 2026-10-23T00:00:00Z', page)
        self.assertIn('Earlier &lt;clean&gt; text.', page)

    def test_one_evidence_linked_to_existing_and_new_thesis_is_counted_once(self):
        existing = {'id': 't1', 'description': 'Will sales grow?', 'outcome': 'Sales growth', 'period': None}
        proposal = {'local_id': 'n1', 'description': 'Will exports be restricted?', 'outcome': 'Restriction', 'period': None}
        evidence = {'local_id': 'e1', 'summary': 'A proposed restriction may affect sales.', 'tier': 'fact',
                    'source_passages': ['First original passage.', 'Second original passage.'],
                    'verified_source_passages': ['First original passage.', 'Second original passage.'],
                    'source_passages_repaired': [False, False],
                    'links': [{'target_type': 'existing', 'target_id': 't1', 'relevance': 'It may affect sales.'},
                              {'target_type': 'new', 'target_id': 'n1', 'relevance': 'It states the proposal.'}]}
        result = {'new_theses': [proposal], 'new_thesis_ids': {'n1': 'clean-2'}, 'evidence': [evidence]}
        row = {'sequence': 1, 'input_id': 'a', 'before_state': json.dumps([existing]), 'after_state': json.dumps([existing]),
               'result': json.dumps(result), 'raw_response': None, 'status': 'complete', 'error': None}
        items = {'a': {'title': 'Article', 'publication_day': '2026-01-10', 'publisher': 'Publisher', 'text': '<script>alert(1)</script>'}}
        page = viewer.render(items, [row], {})
        self.assertIn('Existing thesis · t1', page)
        self.assertIn('New thesis · clean-2', page)
        self.assertIn('<strong>1</strong> evidence items', page)
        self.assertEqual(page.count('Evidence e1</span>'), 2)
        self.assertIn('Second original passage.', page)
        self.assertNotIn('<script>alert(1)</script>', page)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', page)

    def test_repaired_passage_keeps_original_and_verified_text_visible(self):
        evidence = {'source_passage': 'Original words ... omitted tail.',
                    'source_passage_verified': 'Original words.', 'source_passage_repaired': True}
        rendered = viewer.display_passages(evidence)
        self.assertIn('Original words.', rendered)
        self.assertIn('Original words ... omitted tail.', rendered)
        self.assertIn('repaired', rendered)

    def test_failed_item_is_not_shown_as_an_empty_success(self):
        row = {'sequence': 1, 'input_id': 'a', 'before_state': '[]', 'after_state': None,
               'result': None, 'raw_response': None, 'status': 'failed', 'error': 'source passage not found'}
        page = viewer.render({'a': {'title': 'Article', 'text': 'Text'}}, [row], {})
        self.assertIn('No completed extraction.', page)
        self.assertIn('source passage not found', page)
        self.assertNotIn('No thesis–evidence pairs were returned', page)

    def test_failed_item_shows_unaccepted_model_proposal_without_claiming_verification(self):
        proposal = {'new_theses': [], 'evidence': [{'local_id': 'e1', 'summary': 'A proposed deal.',
                    'source_passages': ['A paraphrased passage.'], 'links': [
                        {'target_type': 'existing', 'target_id': 't1', 'relevance': 'It is related.'}]}]}
        response = {'choices': [{'message': {'content': json.dumps(proposal)}}]}
        row = {'sequence': 1, 'input_id': 'a', 'before_state': json.dumps([{'id': 't1', 'description': 'Will sales grow?'}]),
               'after_state': None, 'result': None, 'raw_response': json.dumps(response),
               'status': 'failed', 'error': 'source passage not found'}
        page = viewer.render({'a': {'title': 'Article', 'text': 'Text'}}, [row], {})
        self.assertIn('Failed extraction: unaccepted model output.', page)
        self.assertIn('A proposed deal.', page)
        self.assertIn('unverified model passage', page)
        self.assertNotIn('located in input', page)

    def test_unresolved_link_is_visible_and_not_counted_as_a_defined_thesis(self):
        evidence = {'local_id': 'e1', 'summary': 'A reported product change.',
                    'source_passages': ['The product may change.'], 'verified_source_passages': [None],
                    'links': [{'target_type': 'new', 'target_id': 'missing', 'relevance': 'A product change.'}]}
        result = {'new_theses': [], 'evidence': [evidence], 'unresolved_links': [{'target_id': 'missing'}]}
        row = {'sequence': 1, 'input_id': 'a', 'before_state': '[]', 'after_state': '[]',
               'result': json.dumps(result), 'raw_response': None, 'status': 'complete', 'error': None}
        page = viewer.render({'a': {'title': 'Article', 'text': 'Text'}}, [row], {})
        self.assertIn('Unresolved new thesis reference · missing', page)
        self.assertIn('<strong>0</strong> defined theses shown', page)
        self.assertIn('unverified model passage', page)
        self.assertIn('The product may change.', page)

    def test_lookup_error_and_later_provisional_state_are_visible(self):
        evidence = {'local_id': 'e1', 'summary': 'A reported change.',
                    'source_passages': ['A model quotation.'], 'verified_source_passages': [None],
                    'links': [{'target_type': 'existing', 'target_id': 't1', 'relevance': 'It is related.'}]}
        result = {'new_theses': [], 'evidence': [evidence], 'quote_lookup_errors': [
            {'evidence_id': 'e1', 'passage_number': 1, 'error_type': 'ValueError', 'message': '<bad index>'}]}
        thesis = [{'id': 't1', 'description': 'Will sales grow?'}]
        rows = [
            {'sequence': 1, 'input_id': 'a', 'before_state': json.dumps(thesis), 'after_state': json.dumps(thesis),
             'result': json.dumps(result), 'raw_response': None, 'status': 'complete', 'error': None},
            {'sequence': 2, 'input_id': 'b', 'before_state': json.dumps(thesis), 'after_state': json.dumps(thesis),
             'result': json.dumps({'new_theses': [], 'evidence': []}), 'raw_response': None, 'status': 'complete', 'error': None},
        ]
        page = viewer.render({'a': {'text': 'Source one'}, 'b': {'text': 'Source two'}}, rows, {})
        self.assertIn('Source lookup error.', page)
        self.assertIn('Evidence e1, passage 1: ValueError: &lt;bad index&gt;', page)
        self.assertIn('A model quotation.', page)
        self.assertIn('An earlier article needs review.', page)

    def test_located_passage_is_not_described_as_verified_against_the_page(self):
        html = viewer.display_passages({'source_passages': ['A source passage.'],
                                        'verified_source_passages': ['A source passage.'],
                                        'source_passages_repaired': [False]})
        self.assertIn('located in input', html)
        self.assertNotIn('verified against', html)


if __name__ == '__main__':
    unittest.main()
