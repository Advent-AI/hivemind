"""The grouping contract of the isolated Step 3 library (PRD §6, Alex 2026-11-08), one test per row of the agreed state × event table
(clean-arch/step2-validation-2026-11-07/council/group/a-codex.md, b-codex.md), on records shaped like stored Step 1 items."""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('clean_step3_library', Path(__file__).with_name('library.py'))
library = importlib.util.module_from_spec(spec)
spec.loader.exec_module(library)


def record(record_id, article, summary, theses=('clean-1',), publisher='Reuters', party='NVIDIA', day='2026-07-06'):
    return {'id': record_id, 'article': article, 'publisher': publisher, 'publication_date': day, 'summary': summary,
            'passages': [summary], 'original_party': party, 'reporting_speaker': None, 'tier': 'party_statement',
            'statement_date': day, 'evidence_period': 'Q2 FY2027', 'thesis_ids': list(theses)}


GUIDANCE = 'NVIDIA guided second-quarter fiscal 2027 revenue to about $91 billion with non-GAAP gross margin of about 75%.'
GUIDANCE_DETAIL = ('NVIDIA guided second-quarter fiscal 2027 revenue to $91 billion, plus or minus 2%, and said the guidance assumes no '
                   'China data-centre compute revenue.')


class GroupContractTest(unittest.TestCase):
    def setUp(self):
        self.library = library.Library()
        self.library.apply(record('12:e1', 12, GUIDANCE), {'kind': 'new'})

    def test_new_record_starts_a_group_under_its_own_id(self):
        self.assertEqual(self.library.order, ['12:e1'])
        self.assertEqual(self.library.groups['12:e1']['members'], [])

    def test_repeat_keeps_the_later_records_own_text_and_leaves_the_original_unchanged(self):
        placed = self.library.apply(record('31:e2', 31, GUIDANCE_DETAIL, publisher='Motley Fool', day='2026-07-09'),
                                    {'kind': 'repeat', 'repeat_of': ['12:e1']})
        group = self.library.groups['12:e1']
        self.assertEqual(placed, '12:e1')
        self.assertEqual(group['original']['summary'], GUIDANCE)
        self.assertEqual(group['members'][0]['summary'], GUIDANCE_DETAIL)
        self.assertNotIn('31:e2', self.library.groups)

    def test_missing_thesis_link_is_added_once_with_the_record_that_brought_it(self):
        self.library.apply(record('31:e2', 31, GUIDANCE_DETAIL, theses=('clean-1', 'clean-5')), {'kind': 'repeat', 'repeat_of': ['12:e1']})
        self.assertEqual(self.library.groups['12:e1']['links'], {'clean-1': '12:e1', 'clean-5': '31:e2'})
        self.assertEqual(self.library.dossier('clean-5'), ['12:e1'])

    def test_revision_is_its_own_group_linked_to_the_revised_group(self):
        self.library.apply(record('40:e1', 40, 'NVIDIA raised its second-quarter revenue guidance to $95 billion.'),
                           {'kind': 'revision', 'revises': ['12:e1']})
        self.assertEqual(self.library.groups['40:e1']['revises'], [{'group': '12:e1', 'by': '40:e1'}])
        self.assertEqual(self.library.groups['12:e1']['original']['summary'], GUIDANCE)

    def test_repeat_that_also_revises_another_group_joins_the_repeat_and_names_the_member_behind_the_link(self):
        self.library.apply(record('20:e1', 20, 'NVIDIA expects gross margin in the mid-70s.'), {'kind': 'new'})
        self.library.apply(record('31:e2', 31, GUIDANCE_DETAIL), {'kind': 'repeat', 'repeat_of': ['12:e1'], 'revises': ['20:e1']})
        self.assertEqual(self.library.groups['12:e1']['revises'], [{'group': '20:e1', 'by': '31:e2'}])
        self.assertEqual(self.library.placement['31:e2'], '12:e1')

    def test_failed_comparison_is_refused_and_writes_nothing(self):
        with self.assertRaises(library.Refused):
            self.library.apply(record('31:e2', 31, GUIDANCE_DETAIL), {'kind': 'failed', 'reason': 'Jev answer set differs from the questions'})
        self.assertNotIn('31:e2', self.library.placement)
        self.assertEqual(self.library.groups['12:e1']['members'], [])

    def test_several_repeat_targets_are_refused(self):
        self.library.apply(record('20:e1', 20, 'Sharon AI will deploy up to 40,000 GB300 GPUs.'), {'kind': 'new'})
        with self.assertRaises(library.Refused):
            self.library.apply(record('31:e2', 31, GUIDANCE_DETAIL), {'kind': 'repeat', 'repeat_of': ['12:e1', '20:e1']})
        self.assertNotIn('31:e2', self.library.placement)

    def test_two_records_from_one_article_stay_distinct_members_and_count_the_article_once(self):
        for local in ('e2', 'e3'):
            self.library.apply(record(f'31:{local}', 31, GUIDANCE_DETAIL), {'kind': 'repeat', 'repeat_of': ['12:e1']})
        group = self.library.groups['12:e1']
        self.assertEqual([m['id'] for m in group['members']], ['31:e2', '31:e3'])
        self.assertEqual(self.library.articles(group), [12, 31])

    def test_replayed_record_adds_no_member_but_adds_a_missing_link_once(self):
        later = record('31:e2', 31, GUIDANCE_DETAIL)
        self.library.apply(later, {'kind': 'repeat', 'repeat_of': ['12:e1']})
        self.library.apply(dict(later, thesis_ids=['clean-1', 'clean-7']), {'kind': 'repeat', 'repeat_of': ['12:e1']})
        group = self.library.groups['12:e1']
        self.assertEqual(len(group['members']), 1)
        self.assertEqual(group['links']['clean-7'], '31:e2')

    def test_replayed_id_with_different_content_is_refused(self):
        # AGENTS §3, Identity: an identifier names one thing; a changed record needs a new id.
        self.library.apply(record('31:e2', 31, GUIDANCE_DETAIL), {'kind': 'repeat', 'repeat_of': ['12:e1']})
        with self.assertRaises(library.Refused):
            self.library.apply(record('31:e2', 31, 'NVIDIA cut its Q2 revenue guidance.'), {'kind': 'repeat', 'repeat_of': ['12:e1']})
        self.assertEqual(self.library.groups['12:e1']['members'][0]['summary'], GUIDANCE_DETAIL)

    def test_replayed_record_with_a_different_placement_is_refused(self):
        self.library.apply(record('31:e2', 31, GUIDANCE_DETAIL), {'kind': 'repeat', 'repeat_of': ['12:e1']})
        with self.assertRaises(library.Refused):
            self.library.apply(record('31:e2', 31, GUIDANCE_DETAIL), {'kind': 'new'})

    def test_unknown_group_is_refused(self):
        with self.assertRaises(library.Refused):
            self.library.apply(record('31:e2', 31, GUIDANCE_DETAIL), {'kind': 'repeat', 'repeat_of': ['99:e9']})

    def test_a_passage_step1_did_not_find_in_the_source_is_shown_as_unverified(self):
        # Step 1 marks a passage it could not find in the source (verified value None); a reader must not see it as a quote.
        unverified = dict(record('31:e2', 31, GUIDANCE_DETAIL), verified_passages=[None])
        self.library.apply(unverified, {'kind': 'new'})
        shown = library.group_text(self.library, '31:e2', 'E2', {'31:e2': 'E2'})
        self.assertIn('Unverified quote:', shown)
        self.assertNotIn('  Quote:', shown)

    def test_a_repaired_quote_is_shown_as_the_source_text_step1_found(self):
        # A passage Step 1 matched only after repairing spacing or punctuation is shown as the source's own text.
        repaired = dict(record('31:e2', 31, GUIDANCE_DETAIL), passages=['NVIDIA guided revenue to $91 billion , plus or minus 2%.'],
                        verified_passages=['NVIDIA guided revenue to $91 billion, plus or minus 2%.'])
        self.library.apply(repaired, {'kind': 'new'})
        shown = library.group_text(self.library, '31:e2', 'E2', {'31:e2': 'E2'})
        self.assertIn('Quote: "NVIDIA guided revenue to $91 billion, plus or minus 2%."', shown)
        self.assertEqual(self.library.groups['31:e2']['original']['passages'], repaired['passages'])

    def test_group_text_shows_the_later_detail_and_does_not_call_repeats_confirmation(self):
        self.library.apply(record('31:e2', 31, GUIDANCE_DETAIL, publisher='Motley Fool', day='2026-07-09'),
                           {'kind': 'repeat', 'repeat_of': ['12:e1']})
        shown = library.group_text(self.library, '12:e1', 'E1', {'12:e1': 'E1'})
        source_only = library.group_text(self.library, '12:e1', 'E1', {'12:e1': 'E1'}, member_text=False)
        self.assertIn('assumes no China data-centre compute revenue', shown)
        self.assertNotIn('assumes no China', source_only)
        self.assertIn('1 further articles', shown)
        self.assertIn('do not by themselves confirm it independently', shown)


if __name__ == '__main__':
    unittest.main()


class LaterLinkingTest(unittest.TestCase):
    """Alex, 2026-11-08: a material statement no thesis takes is kept and linked when a related thesis opens (design §§11.1, 17)."""

    def setUp(self):
        self.library = library.Library()
        self.library.apply(record('3:e1', 3, 'Dell is bringing the RTX Spark chip to its XPS laptops.', theses=()), {'kind': 'new'})
        self.library.apply(record('4:e1', 4, GUIDANCE), {'kind': 'new'})
        self.library.apply(record('5:e1', 5, 'A retailer cut prices on gaming monitors.', theses=()), {'kind': 'new'})

    def test_an_unlinked_statement_is_linked_when_a_related_thesis_opens_and_each_pair_is_judged_once(self):
        asked = []
        def judge(ids):
            asked.append(list(ids))
            return {g: g == '3:e1' for g in ids}
        result = self.library.link_later('rtx-spark', judge, before_article=6)
        self.assertEqual(result, {'linked': ['3:e1'], 'pending': [], 'judged': 2})
        self.assertEqual(self.library.groups['3:e1']['links'], {'rtx-spark': '3:e1'})
        self.assertEqual(asked, [['3:e1', '5:e1']])   # the group that arrived linked is not a candidate
        self.assertEqual(self.library.link_later('rtx-spark', judge, before_article=6)['judged'], 0)

    def test_only_earlier_articles_are_candidates(self):
        result = self.library.link_later('rtx-spark', lambda ids: {g: True for g in ids}, before_article=5)
        self.assertEqual(result['linked'], ['3:e1'])

    def test_a_batch_that_fails_twice_stays_pending_and_is_judged_on_the_next_call(self):
        calls = []
        def failing(ids):
            calls.append(ids)
            raise RuntimeError('Jev timeout')
        result = self.library.link_later('rtx-spark', failing, before_article=6)
        self.assertEqual((result['pending'], len(calls), self.library.judged), (['3:e1', '5:e1'], 2, {}))
        again = self.library.link_later('rtx-spark', lambda ids: {g: False for g in ids}, before_article=6)
        self.assertEqual((again['judged'], again['pending']), (2, []))

    def test_a_statement_linked_later_stays_a_candidate_for_another_thesis(self):
        self.library.link_later('rtx-spark', lambda ids: {g: g == '3:e1' for g in ids}, before_article=6)
        result = self.library.link_later('pc-demand', lambda ids: {g: True for g in ids}, before_article=6)
        self.assertEqual(sorted(result['linked']), ['3:e1', '5:e1'])
        self.assertEqual(self.library.groups['3:e1']['links'], {'rtx-spark': '3:e1', 'pc-demand': '3:e1'})


    def test_pending_pairs_keep_the_opening_boundary_when_judged_again(self):
        self.library.link_later('rtx-spark', lambda ids: (_ for _ in ()).throw(RuntimeError('Jev timeout')), before_article=5)
        self.assertEqual(self.library.pending, {'rtx-spark': ['3:e1']})
        self.library.apply(record('7:e1', 7, 'A retailer cut prices on laptops.', theses=()), {'kind': 'new'})
        again = self.library.link_later('rtx-spark', lambda ids: {g: True for g in ids}, before_article=8)
        self.assertEqual((again['linked'], self.library.pending), (['3:e1'], {}))   # 5:e1 and 7:e1 arrived at or after the opening
