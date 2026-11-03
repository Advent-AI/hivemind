"""D359: the code builds only the frozen production prompts, extraction v74i (D274) and judging-v7 (D354); a configuration that names
any other version is refused before a request is built or sent."""
import dataclasses
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, extraction, model  # noqa: E402
from hivemind.views import judging  # noqa: E402
from test_placement import ITEM, TEXT, UNI  # noqa: E402
from test_theme_block import DAY, ledger  # noqa: E402

V108 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v108.json'))


def never_sent(*parameters):
    raise AssertionError('a request of a version the code does not build was sent')


def test_an_extraction_version_other_than_v74i_is_refused_before_any_call(tmp_path):
    other = dataclasses.replace(V108, extraction=dict(V108.extraction, T7=dataclasses.replace(V108.extraction['T7'], prompt_version='T7-v53')))
    with pytest.raises(ValueError, match="extraction 'v53' is not built"):
        extraction.extract(model.Archive(str(tmp_path / 'archive.sqlite')), other, ITEM, TEXT, [], UNI, transport=never_sent)


def test_a_judging_version_other_than_v7_is_refused_before_any_call(tmp_path):
    other = dataclasses.replace(V108, rejudging=dataclasses.replace(V108.rejudging, prompt_version='judging-v6'))
    with pytest.raises(ValueError, match="judging 'judging-v6' is not built"):
        judging.round_of_judgements(model.Archive(str(tmp_path / 'archive.sqlite')), other, ledger(tmp_path), ['v1'], 2, DAY, transport=never_sent)
