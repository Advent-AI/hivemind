"""The answer-choice step on gpt-6-astra for the release comparison (D667 item 1, plan §1.5 D). `stage_a.py` is run as it is, with
two additions and nothing else:
- `stage_a.SETTING` is the frozen setting with the model set to gpt-6-astra (the pattern of reflection-6's gate1_candidate.py);
- every request, the first send and the resend with its refusal note alike, is rebuilt from the same system text, user text and
  schema through `model.build_request` twice, once on the frozen luna setting and once on astra. The two must be byte-equal except
  for the model string, and the request reaching the transport must be the astra one. Any difference raises before the reservation,
  so nothing is sent; stage_a's worker then stops its run, and with a shared ledger the draw.

Reservations, retries and the stop gate stay stage_a's own (StageALimit, the shared ledger).

    python3 stage_a_astra.py <stage_a.py's arguments>
"""
import dataclasses
import importlib.util
import json
import sys
import threading
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
STAGE_A = ROOT / 'clean-arch/step4-2026-11-10/stage_a/stage_a.py'
ASTRA_MODEL = 'gpt-6-astra'


class NotTheFrozenRequest(RuntimeError):
    """A request differs from the frozen luna request by more than its model string."""


def load_stage_a():
    spec = importlib.util.spec_from_file_location('stage_a', STAGE_A)
    module = importlib.util.module_from_spec(spec)
    sys.modules['stage_a'] = module
    spec.loader.exec_module(module)
    return module


def install(stage_a):
    """Switch `stage_a` to astra with the per-request check. Returns (luna setting, astra setting)."""
    luna = stage_a.SETTING
    if luna.model != 'gpt-6-luna':
        raise SystemExit(f'stage_a.SETTING is {luna.model}, not the frozen gpt-6-luna: refused')
    astra = dataclasses.replace(luna, model=ASTRA_MODEL)
    model = stage_a.model
    expected = threading.local()
    original_caller = stage_a.model_calls.model_caller
    original_send = stage_a.StageALimit.send_labelled

    def model_caller(model_module, archive, call_config, setting, limit, purpose='clean-ladder'):
        if setting.model != ASTRA_MODEL:
            raise NotTheFrozenRequest(f'the caller was given {setting.model}, not {ASTRA_MODEL}')
        call_model = original_caller(model_module, archive, call_config, setting, limit, purpose)

        def checked(system_text, user_text, schema):
            frozen = json.dumps(model.build_request(luna, system_text, user_text, schema, 'clean_ladder', call_config.provider))
            built = json.dumps(model.build_request(astra, system_text, user_text, schema, 'clean_ladder', call_config.provider))
            if frozen.count('"model": "gpt-6-luna"') != 1 or built != frozen.replace('"model": "gpt-6-luna"', f'"model": "{ASTRA_MODEL}"'):
                raise NotTheFrozenRequest('the astra request differs from the frozen request beyond the model string')
            expected.request = built
            return call_model(system_text, user_text, schema)
        return checked

    def send_labelled(self, label, provider, request):
        if json.dumps(request) != getattr(expected, 'request', None):
            raise NotTheFrozenRequest(f'{label}: the request at the transport is not the checked astra request')
        return original_send(self, label, provider, request)

    stage_a.SETTING = astra
    stage_a.model_calls.model_caller = model_caller
    stage_a.StageALimit.send_labelled = send_labelled
    return luna, astra


def configuration_checksum(stage_a):
    """The `config_checksum` stage_a writes to every archive row under astra (its own formula, stage_a.run)."""
    import hashlib
    texts = stage_a.request_texts()
    setting = stage_a.SETTING
    return hashlib.sha256(json.dumps({'system': texts['system'], 'closing': texts['closing'], 'schema': texts['schema'],
                                      'setting': [setting.model, setting.reasoning_effort, setting.max_output_tokens]},
                                     ensure_ascii=False).encode()).hexdigest()[:16]


if __name__ == '__main__':
    module = load_stage_a()
    install(module)
    sys.argv[0] = str(STAGE_A)
    module.main()
