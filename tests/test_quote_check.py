"""The quote check reads a quote as the same text when the source differs only in the spacing around punctuation or in
typographic quote and dash glyphs (05-extraction step 3: a quote must be in the item). The class, counted on the
three-month run's archive on 2026-10-28 (docs/research/2026-10-28-extraction-quality/report.md): 174 pieces refused as
'quote not in item', 66 of them because the cleaned page text carries " , " or " ." where the model wrote "," or ".",
27 of those linked to a shown thesis and lost."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import extraction  # noqa: E402

# The CNBC Vera CPU page of 2026-07-21 (gnews:69c31079960ffe4f9805834c) as the cleaned database stores it: a space before
# each comma where an inline tag stood; the model wrote the sentence with ordinary punctuation.
PAGE = ("On Tuesday, Nvidia released new information about its data center CPU, called Vera. Nvidia representatives said "
        "Vera chips were delivered to clients, including OpenAI , Anthropic , and SpaceX , in June.")
QUOTE = "Nvidia representatives said Vera chips were delivered to clients, including OpenAI, Anthropic, and SpaceX, in June."
ITEM = {'input_id': 'gnews:69c31079960ffe4f9805834c', 'publication_day': '2026-07-21', 'publisher_type': 'media'}


def answer(quote):
    return {'candidates': [], 'evidence': [{'id': 'e1', 'quote': quote, 'one_line': 'Vera chips were delivered to OpenAI, Anthropic and SpaceX in June 2026.',
                                           'speaker': 'Nvidia representatives', 'original_who': 'Nvidia representatives', 'original_day': '',
                                           'tier': 'party_statement', 'event_time': '2026-06', 'links': ['v7']}]}


def test_a_quote_that_differs_only_in_punctuation_spacing_is_in_the_item():
    evidence, _, dropped = extraction.sift(answer(QUOTE), ITEM, PAGE, {'v7'}, english=True)
    assert [e['id'] for e in evidence] == ['e1'], dropped


def test_typographic_quotes_and_dashes_read_as_their_plain_forms():
    page = "Intrator said, “pricing for prior generation SKUs is at or above where it was years ago” — on the call."
    quote = 'Intrator said, "pricing for prior generation SKUs is at or above where it was years ago" - on the call.'
    evidence, _, dropped = extraction.sift(answer(quote), ITEM, page, {'v7'}, english=True)
    assert [e['id'] for e in evidence] == ['e1'], dropped


def test_a_quote_with_other_words_is_still_refused():
    evidence, _, dropped = extraction.sift(answer(QUOTE.replace('in June', 'in May')), ITEM, PAGE, {'v7'}, english=True)
    assert evidence == [] and dropped == [('e1', 'quote not in item')]


# D236: a quote that differs from the source only by punctuation, quotation marks, footnote markers or case, or that leaves out
# one run of words inside one sentence, is the item's text; the stored quote becomes the exact source passage. Cases from the
# 2026-10-29 census of 38 refusals (docs/research/2026-10-29-analyst-standard/quote-check-2026-10-29/census.json).
DENIAL_PAGE = ('An Nvidia representative responded with a short statement to Tom\'s Hardware : "Our roadmap is intact." '
               'It is not clear which roadmap the company meant.')


def test_a_quote_with_one_run_left_out_inside_a_sentence_is_kept_as_the_source_text():
    quote = 'An Nvidia representative responded to Tom\'s Hardware : "Our roadmap is intact."'
    evidence, _, dropped = extraction.sift(answer(quote), ITEM, DENIAL_PAGE, {'v7'}, english=True)
    assert [e['quote'] for e in evidence] == ['An Nvidia representative responded with a short statement to Tom\'s Hardware : "Our roadmap is intact."'], dropped


def test_a_quote_without_its_quotation_marks_or_footnote_is_kept_as_the_source_text():
    page = 'Kress said losing that market, which NVIDIA sizes at “close to about $50 billion in the future,” would be material [3] .'
    quote = 'losing that market, which NVIDIA sizes at close to about $50 billion in the future, would be material'
    evidence, _, dropped = extraction.sift(answer(quote), ITEM, page, {'v7'}, english=True)
    assert [e['quote'] for e in evidence] == ['losing that market, which NVIDIA sizes at “close to about $50 billion in the future,” would be material'], dropped


def test_a_left_out_run_that_crosses_a_sentence_end_is_refused():
    quote = 'An Nvidia representative responded with a short statement to Tom\'s Hardware : the company meant.'
    evidence, _, dropped = extraction.sift(answer(quote), ITEM, DENIAL_PAGE, {'v7'}, english=True)
    assert evidence == [] and dropped == [('e1', 'quote not in item')]


def test_a_quote_naming_another_party_is_refused():
    page = 'Unlike Hesai, Huawei challenged both rulings in court and lost both cases.'
    evidence, _, dropped = extraction.sift(answer('Unlike Huawei, Hesai challenged both rulings in court and lost both cases.'), ITEM, page, {'v7'}, english=True)
    assert evidence == [] and dropped == [('e1', 'quote not in item')]


def test_a_left_out_run_longer_than_the_quote_is_refused():
    page = 'Nvidia said on a long call with many analysts and reporters present in the room that demand is strong.'
    evidence, _, dropped = extraction.sift(answer('Nvidia said demand is strong.'), ITEM, page, {'v7'}, english=True)
    assert evidence == [] and dropped == [('e1', 'quote not in item')]

