"""The current config and model calls do not expose the retired sampling setting."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, model  # noqa: E402


def test_new_defaults_remove_only_the_retired_setting_and_keep_request_bytes():
    for old_name, new_name in (
        ('poc-v117.json', 'poc-v118.json'),
        ('poc-v33-idea.json', 'poc-v118-idea.json'),
        ('poc-v1.json', 'poc-v118-from-v1.json'),
        ('poc-v2.json', 'poc-v118-from-v2.json'),
        ('poc-v7.json', 'poc-v118-from-v7.json'),
        ('poc-v9.json', 'poc-v118-from-v9.json'),
    ):
        old_raw, new_raw = (json.loads((ROOT / 'poc/config' / n).read_text()) for n in (old_name, new_name))

        def without_retired(value):
            if isinstance(value, dict):
                return {k: without_retired(v) for k, v in value.items() if k not in ('temperature', 'version', '_note')}
            return value

        assert without_retired(old_raw) == without_retired(new_raw)
        assert 'temperature' not in json.dumps(new_raw)
        old, new = (config.load(ROOT / 'poc/config' / n) for n in (old_name, new_name))
        assert old.checksum != new.checksum
        args = ('system', 'user', {'type': 'object', 'properties': {}, 'required': [], 'additionalProperties': False}, 'test')
        settings = [(old.extraction[k], new.extraction[k]) for k in old.extraction]
        settings += [(getattr(old, k), getattr(new, k)) for k in ('matching', 'rejudging', 'final_verdict', 'idea', 'idea_summary', 'collision', 'placement', 'baseline') if getattr(old, k) is not None]
        for old_setting, new_setting in settings:
            assert not hasattr(new_setting, 'temperature')
            assert json.dumps(model.build_request(old_setting, *args, 'openai')) == json.dumps(model.build_request(new_setting, *args, 'openai'))
            for provider in ('openai', 'alternate'):
                assert 'temperature' not in model.build_request(new_setting, *args, provider)


def test_default_entrypoints_name_the_new_versions():
    assert "'poc-v118.json'" in (ROOT / 'scripts/replay.py').read_text()
    assert "'poc-v118-idea.json'" in (ROOT / 'scripts/hivemind_api.py').read_text()
    for script, name in (('mock_translate.py', 'v2'), ('idea_eval.py', 'v7'), ('idea_probe.py', 'v9'),
                         ('idea_stability.py', 'v9'), ('idea_gold.py', 'v9'), ('agent_day0.py', 'v1')):
        assert f"'poc-v118-from-{name}.json'" in (ROOT / 'scripts' / script).read_text()


def test_identical_openai_request_reuses_the_original_archive_row(tmp_path):
    old = config.load(ROOT / 'poc/config/poc-v117.json')
    new = config.load(ROOT / 'poc/config/poc-v118.json')
    schema = {'type': 'object', 'properties': {'ok': {'type': 'boolean'}}, 'required': ['ok'], 'additionalProperties': False}
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    def send(provider, request):
        return {'choices': [{'message': {'content': '{"ok": true}'}}], 'usage': {}}
    first = model.call(archive, old, old.extraction['T8'], 'system', 'user', schema, 'test', 'extract', transport=send)
    def refuse(provider, request):
        raise AssertionError('a cached request must not be sent')
    second = model.call(archive, new, new.extraction['T8'], 'system', 'user', schema, 'test', 'extract', transport=refuse)
    assert not first.cached and second.cached and first.call_id == second.call_id
    assert archive.conn.execute('select config_version from model_calls').fetchone()[0] == old.version
    archive.conn.close()
