"""A letter-suffixed extraction prompt version (D255 arm, 2026-11-01: role-v53b is role-v53's text with its one_line sentence
rewritten) keeps its number's behaviour flags and reads its own prompt files, so a text variant never takes the next free number's
architecture (v59–v66 send the end-of-request review, v71 shows the day's open questions and files linked statements without the
placement call)."""
from hivemind import extraction


def test_suffixed_version_keeps_its_numbers_behaviour():
    assert extraction.version_number('v53b') == 53
    assert extraction.version_number('53b') == 53
    assert extraction.version_number('v53') == 53 and extraction.version_number(None) == 0
    assert extraction.places('v53b') and extraction.ledger_blind('v53b')
    assert not extraction.open_questions('v53b') and not extraction.reviews('v53b')
