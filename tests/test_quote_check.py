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
