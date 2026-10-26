"""The cost column prices tokens at the published rates (model.PRICES): cached input tokens at the published cached rate (10% of
the input rate, developers.openai.com/api/docs/models/gpt-6-luna, 2026-10-27), the rest of the input at the input rate, output at
the output rate. The provider's bill is the measurement; this is the estimate every report reads."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, model  # noqa: E402

CFG = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v29.json'))
SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['ok'], 'properties': {'ok': {'type': 'boolean'}}}


def test_cached_input_tokens_are_priced_at_the_cached_rate(tmp_path):
    def send(provider, request):
        return {'choices': [{'message': {'content': json.dumps({'ok': True})}}],
                'usage': {'prompt_tokens': 1_000_000, 'completion_tokens': 100_000, 'prompt_tokens_details': {'cached_tokens': 400_000, 'cache_write_tokens': 600_000}}}
    answer = model.call(model.Archive(str(tmp_path / 'archive.sqlite')), CFG, CFG.rejudging, 'system', 'user', SCHEMA, 'probe', 'judge', transport=send)
    price_in, price_out = model.PRICES['gpt-6-luna']
    assert answer.cost_usd == round(600_000 / 1e6 * price_in + 400_000 / 1e6 * price_in * model.CACHED_INPUT_SHARE + 100_000 / 1e6 * price_out, 6) == 0.114
    assert answer.input_tokens == 1_000_000                       # the token columns stay the measurement
