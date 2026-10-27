"""Restore the key order the production code sends. The archive stores a request serialised with sort_keys=True
(`model.request_identity`), while `model.call` sends the dict as built; a benchmark that re-sends the archived JSON
therefore sends an alphabetised schema (candidates before evidence; in a piece, links and event_time before quote).
Codex corrected this in D243; benchmark.py did not until 2026-10-27 19:30. `restore(request)` rebuilds the order from the
fresh builder: the schema is walked beside `extraction.schema_for` for the same version, and the request beside
`model.build_request`."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, extraction, model  # noqa: E402


def _reorder(value, template):
    if isinstance(value, dict) and isinstance(template, dict):
        ordered = {k: _reorder(value[k], template[k]) for k in template if k in value}
        ordered.update({k: v for k, v in value.items() if k not in ordered})
        return ordered
    if isinstance(value, list) and isinstance(template, list) and template:
        return [_reorder(v, template[min(i, len(template) - 1)]) for i, v in enumerate(value)]
    return value


def version_of(request):
    return re.search(r'\bT\d+-v(\d+)\b', request['messages'][1]['content']).group(1) if re.search(r'\bT\d+-v(\d+)\b', request['messages'][1]['content']) else None


def restore(request, version='v12', cfg_path=os.path.join(ROOT, 'poc', 'config', 'poc-v30.json'), category='T7'):
    cfg = config.load(cfg_path)
    template_schema = extraction.schema_for(version, ['g1'], ['v1'])
    template = model.build_request(cfg.extraction_setting(category), 'S', 'U', template_schema, 'extraction', cfg.provider)
    return _reorder(request, template)
