"""D266 (2026-11-02): the quote repair widened by two rules, the stored quote still the exact source passage. (1) A quote a word or two
off one source window (the company's name for "the company's", "As" for "While"; two edits up to 30 words, three above), none of the
edits a number, is that window. (2) A quote that copies one passage exactly and runs on into other text keeps the copied passage when it
ends at a sentence end. A paraphrase and a changed number stay refused. On the three v92 draws' 41 refused quotes: 31 repaired, 10 refused."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import extraction  # noqa: E402

TEXT = ("Despite this news, the stock isn't showing much reaction. That's likely because the company's current-generation Rubin systems are already "
        "in full production and set to start shipping this fall to eight major cloud partners, including Amazon. While the AI hyperscalers plan to spend "
        "$650 billion on data center capital expenditures this year, next year that figure could be over $1 trillion. Micron's latest revenue growth was "
        "about 346 percent, compared with Nvidia's 85 percent.")


def test_a_quote_a_function_word_or_the_companys_name_off_the_source_is_stored_as_the_source_passage():
    quote = "Nvidia's current-generation Rubin systems are already in full production and set to start shipping this fall to eight major cloud partners"
    assert extraction.repair_quote(quote, TEXT, subject_names=('NVIDIA',)) == \
        "company's current-generation Rubin systems are already in full production and set to start shipping this fall to eight major cloud partners"
    assert extraction.repair_quote(quote, TEXT) is None                           # another company's name for "the company's" is not harmless
    assert extraction.repair_quote('As the AI hyperscalers plan to spend $650 billion on data center capital expenditures this year', TEXT) == \
        'While the AI hyperscalers plan to spend $650 billion on data center capital expenditures this year'


def test_a_changed_number_a_changed_party_and_a_paraphrase_stay_refused():
    assert extraction.repair_quote('While the AI hyperscalers plan to spend $560 billion on data center capital expenditures this year', TEXT) is None
    assert extraction.repair_quote('While the AI hyperscalers plan to spend $650 billion on data center capital expenditures last year', TEXT) is None
    page = 'Nvidia representatives said Vera chips were delivered to clients, including OpenAI , Anthropic , and SpaceX , in June.'
    assert extraction.repair_quote('Nvidia representatives said Vera chips were delivered to clients, including OpenAI, Anthropic, and SpaceX, in May.', page, ('NVIDIA',)) is None
    assert extraction.repair_quote("Nvidia's latest revenue growth was about 85 percent", TEXT, subject_names=('NVIDIA',)) is None
    page = 'Unlike Hesai, Huawei challenged both rulings in court and lost both cases, the court record shows.'
    assert extraction.repair_quote('Unlike Huawei, Hesai challenged both rulings in court and lost both cases, the court record shows.', page) is None


def test_a_quote_that_runs_on_past_the_copied_passage_keeps_that_passage():
    quote = ("That's likely because the company's current-generation Rubin systems are already in full production and set to start shipping this fall to "
             "eight major cloud partners, including Amazon. The partners have confirmed their orders for the fall.")
    assert extraction.repair_quote(quote, TEXT) == ("That's likely because the company's current-generation Rubin systems are already in full production and "
                                                    "set to start shipping this fall to eight major cloud partners, including Amazon.")
