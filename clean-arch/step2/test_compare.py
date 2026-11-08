"""Step 2 outcome and forward-order contract (PRD §5; Alex 2026-11-08: a record matching several groups joins only the one it is most
like); Jev and the embeddings are fakes, the Step 3 library is real."""
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


compare = load('clean_step2_compare', HERE / 'compare.py')
library = load('clean_step3_library', HERE.parent / 'step3/library.py')


def answer(choice, same_probability):
    rest = (1 - same_probability) / 2
    return {'choice': choice, 'probabilities': {'same_statement': same_probability, 'supersedes': rest, 'different': rest}}


def record(record_id, article, summary, party='NVIDIA'):
    return {'id': record_id, 'article': article, 'publisher': 'Reuters', 'publication_date': '2026-07-06', 'summary': summary,
            'passages': [summary], 'original_party': party, 'reporting_speaker': 'Reuters', 'tier': 'party_statement',
            'statement_date': '2026-07-06', 'evidence_period': None, 'thesis_ids': ['clean-1']}


class OutcomeTest(unittest.TestCase):
    def test_several_repeats_join_only_the_most_likely_group(self):
        result = compare.outcome({'1:e1': answer('same_statement', 0.62), '2:e1': answer('same_statement', 0.91),
                                  '3:e1': answer('different', 0.05)}, ['1:e1', '2:e1', '3:e1'])
        self.assertEqual(result, {'kind': 'repeat', 'repeat_of': ['2:e1'], 'revises': []})

    def test_equal_probabilities_go_to_the_earliest_group(self):
        result = compare.outcome({'2:e1': answer('same_statement', 0.8), '1:e1': answer('same_statement', 0.8)}, ['1:e1', '2:e1'])
        self.assertEqual(result['repeat_of'], ['1:e1'])

    def test_repeat_with_a_supersedes_answer_elsewhere_keeps_the_revision_link(self):
        result = compare.outcome({'1:e1': answer('same_statement', 0.9), '2:e1': answer('supersedes', 0.1)}, ['1:e1', '2:e1'])
        self.assertEqual(result, {'kind': 'repeat', 'repeat_of': ['1:e1'], 'revises': ['2:e1']})

    def test_supersedes_without_a_repeat_is_a_revision_and_no_match_is_new(self):
        self.assertEqual(compare.outcome({'1:e1': answer('supersedes', 0.1)}, ['1:e1']), {'kind': 'revision', 'revises': ['1:e1']})
        self.assertEqual(compare.outcome({'1:e1': answer('different', 0.1)}, ['1:e1']), {'kind': 'new'})


class ForwardTest(unittest.TestCase):
    def test_a_later_article_joins_the_group_and_records_of_one_article_never_see_each_other(self):
        guidance = record('1:e1', 1, 'NVIDIA guided Q2 revenue to about $91 billion.')
        same_article = record('1:e2', 1, 'NVIDIA guided Q2 revenue to about $91 billion, plus or minus 2%.')
        retelling = record('2:e1', 2, 'NVIDIA guided Q2 revenue to $91 billion and assumes no China data-centre revenue.')
        texts = [compare.doc_text(r) for r in (guidance, same_article, retelling)] + \
                [compare.query_text(r, 'Will data-centre revenue grow?') for r in (guidance, same_article, retelling)]
        vectors = {text: [1.0, 0.0] for text in texts}
        asked = []
        def ask(state, questions):
            asked.append((state, len(questions)))
            return {q: answer('same_statement', 0.9) for q in questions}
        store = library.Library()
        decisions = compare.forward([[guidance, same_article], [retelling]], store, vectors, {'clean-1': 'Will data-centre revenue grow?'}, ask)
        self.assertEqual(store.order, ['1:e1', '1:e2'])
        self.assertEqual([m['id'] for m in store.groups['1:e1']['members']], ['2:e1'])
        self.assertEqual(len(asked), 1)
        self.assertEqual(decisions[2]['outcome'], {'kind': 'repeat', 'repeat_of': ['1:e1'], 'revises': []})

    def test_figures_never_change_the_search_or_comparison_text(self):
        # STEP1-CONDITIONS-DESIGN.md §14: a wrongly paired figure cannot change Step 2.
        right = dict(record('1:e1', 1, 'Revenue was $81.6 billion and gross margin 75%.'),
                     figures=[{'measure': 'revenue', 'period': 'Q1', 'value': '$81.6 billion', 'kind': 'actual', 'basis': None}])
        wrong = dict(right, figures=[{'measure': 'gross margin', 'period': 'Q1', 'value': '$81.6 billion', 'kind': 'actual', 'basis': None}])
        for build in (compare.doc_text, lambda r: compare.query_text(r, 'Q?'), lambda r: compare.piece_text(r, 'INCOMING PIECE')):
            self.assertEqual(build(right), build(wrong))

    def test_the_comparison_reads_the_full_passages(self):
        # §15: no cut at 600 characters; a qualification late in a long passage reaches Jev.
        long = dict(record('1:e1', 1, 'NVIDIA guided revenue.'), passages=['x' * 700 + ' excluding China'])
        self.assertIn('excluding China', compare.piece_text(long, 'INCOMING PIECE'))

    def test_a_condition_with_no_thesis_is_still_compared_with_the_library(self):
        # §10.1: a record with no association gets one entity-wide query of its own text; without it a repeat is saved as new.
        stored = record('1:e1', 1, 'NVIDIA guided Q2 revenue to about $91 billion.')
        condition = dict(record('2:e1', 2, 'NVIDIA guided Q2 revenue to $91 billion.'), thesis_ids=[],
                         figures=[{'measure': 'revenue', 'period': 'Q2', 'value': '$91 billion', 'kind': 'guidance', 'basis': None}])
        vectors = {compare.doc_text(stored): [1.0, 0.0], compare.query_text(stored, 'Q?'): [1.0, 0.0], compare.doc_text(condition): [1.0, 0.0]}
        store = library.Library()
        decisions = compare.forward([[stored], [condition]], store, vectors, {'clean-1': 'Q?'},
                                    lambda state, questions: {q: answer('same_statement', 0.9) for q in questions})
        self.assertEqual(decisions[1]['outcome'], {'kind': 'repeat', 'repeat_of': ['1:e1'], 'revises': []})
        self.assertEqual(store.groups['1:e1']['members'][0]['figures'][0]['value'], '$91 billion')

    def test_a_thesis_opened_by_an_article_is_linked_later_to_earlier_unlinked_statements(self):
        # Alex, 2026-11-08: kept and linked when a related thesis opens; the opening article's own records are not re-judged.
        early = dict(record('1:e1', 1, 'Dell is bringing the RTX Spark chip to its XPS laptops.'), thesis_ids=[])
        opener = dict(record('2:e1', 2, 'Microsoft launched a laptop with the RTX Spark chip.'), thesis_ids=['rtx-spark'])
        same_article = dict(record('2:e2', 2, 'Reviewers praised the laptop screen.'), thesis_ids=[])
        questions = {'rtx-spark': 'Will RTX Spark laptops ship in volume?'}
        vectors = {}
        for r in (early, opener, same_article):
            vectors[compare.doc_text(r)] = [0.0, 1.0] if r is early else [1.0, 0.0]
            vectors[compare.query_text(r, questions['rtx-spark'])] = [1.0, 0.0]
        def ask(state, qs):
            if state.startswith('THESIS:'):
                return {q: {'noul': 0.9} for q in qs}
            return {q: answer('different', 0.1) for q in qs}
        store = library.Library()
        compare.forward([[early], [opener, same_article]], store, vectors, questions, ask, opened=[[], ['rtx-spark']])
        self.assertEqual(store.groups['1:e1']['links'], {'rtx-spark': '1:e1'})
        self.assertEqual(store.groups['2:e2']['links'], {})
        self.assertEqual(store.later_log, [{'thesis': 'rtx-spark', 'article': 2, 'linked': ['1:e1'], 'pending': [], 'judged': 1}])

    def test_pending_later_links_are_retried_on_the_next_write_to_the_thesis(self):
        # Design §11.1: a batch that fails twice stays pending and is judged again when the thesis is next written to.
        early = dict(record('1:e1', 1, 'Dell is bringing the RTX Spark chip to its XPS laptops.'), thesis_ids=[])
        opener = dict(record('2:e1', 2, 'Microsoft launched a laptop with the RTX Spark chip.'), thesis_ids=['rtx-spark'])
        writer = dict(record('3:e1', 3, 'HP will ship an RTX Spark laptop in December.'), thesis_ids=['rtx-spark'])
        questions = {'rtx-spark': 'Will RTX Spark laptops ship in volume?'}
        vectors = {}
        for r, v in ((early, [0.0, 1.0]), (opener, [1.0, 0.0]), (writer, [0.5, 0.5])):
            vectors[compare.doc_text(r)] = v
            vectors[compare.query_text(r, questions['rtx-spark'])] = v
        calls = {'thesis': 0}
        def ask(state, qs):
            if state.startswith('THESIS:'):
                calls['thesis'] += 1
                if calls['thesis'] <= 2:
                    raise RuntimeError('Jev timeout')
                return {q: {'noul': 0.9} for q in qs}
            return {q: answer('different', 0.1) for q in qs}
        store = library.Library()
        compare.forward([[early], [opener], [writer]], store, vectors, questions, ask, opened=[[], ['rtx-spark'], []])
        self.assertEqual([e['pending'] for e in store.later_log], [['1:e1'], []])
        self.assertEqual(store.groups['1:e1']['links'], {'rtx-spark': '1:e1'})

    def test_a_comparison_that_fails_twice_is_refused_and_reported_and_the_run_continues(self):
        # STEP1-CONDITIONS-DESIGN.md, "Retry after a failed comparison: retried once; then refused and reported, not saved".
        first = record('1:e1', 1, 'NVIDIA guided Q2 revenue to about $91 billion.')
        second = record('2:e1', 2, 'NVIDIA guided Q2 revenue to $91 billion.')
        third = record('3:e1', 3, 'NVIDIA guided Q2 revenue to $91 billion again.')
        vectors = {t: [1.0] for r in (first, second, third) for t in (compare.doc_text(r), compare.query_text(r, 'Q'))}
        calls = []
        def ask(state, questions):
            calls.append(state)
            if len(calls) <= 2:
                raise RuntimeError('Jev answer set differs from the questions')
            return {q: answer('same_statement', 0.9) for q in questions}
        store = library.Library()
        decisions = compare.forward([[first], [second], [third]], store, vectors, {'clean-1': 'Q'}, ask)
        self.assertIn('comparison failed', decisions[1]['refused'])
        self.assertNotIn('2:e1', store.placement)
        self.assertEqual(decisions[2]['group'], '1:e1')

    def test_a_comparison_that_fails_once_is_retried_and_its_answer_used(self):
        first = record('1:e1', 1, 'NVIDIA guided Q2 revenue to about $91 billion.')
        second = record('2:e1', 2, 'NVIDIA guided Q2 revenue to $91 billion.')
        vectors = {t: [1.0] for r in (first, second) for t in (compare.doc_text(r), compare.query_text(r, 'Q'))}
        calls = []
        def ask(state, questions):
            calls.append(state)
            if len(calls) == 1:
                raise RuntimeError('Jev timeout')
            return {q: answer('same_statement', 0.9) for q in questions}
        store = library.Library()
        decisions = compare.forward([[first], [second]], store, vectors, {'clean-1': 'Q'}, ask)
        self.assertEqual(calls[0], calls[1])
        self.assertEqual(decisions[1]['group'], '1:e1')


if __name__ == '__main__':
    unittest.main()
