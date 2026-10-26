"""Config (docs/prd/03-config.md): a versioned file of the settings a person chooses, with a checksum written into
every model call's record. A version that references a missing setting is refused whole."""
import dataclasses
import hashlib
import json
import os

PROMPTS = os.path.join(os.path.dirname(__file__), 'prompts')


class ConfigError(ValueError):
    pass


def prompt_path(name):
    """The file of a prompt the config names, for example role-v1.txt or matching-v1.txt."""
    return os.path.join(PROMPTS, name)


def _prompt_files(extraction, matching, rejudging, idea=None, collision=None):
    """03-config: a version that names a prompt that does not exist is refused whole. An extraction setting's
    prompt_version is '<category>-<v>': block 2 and 4 come from categories-<v>.json (the category's entry) and the
    role from role-<v>.txt; matching, re-judging and the idea reading name their file without the extension."""
    for category, setting in extraction.items():
        prefix, _, version = setting.prompt_version.rpartition('-')
        if prefix != category or not version:
            raise ConfigError(f'extraction.{category}: prompt_version {setting.prompt_version!r} must be {category}-<version>')
        categories_file = prompt_path(f'categories-{version}.json')
        if not os.path.exists(categories_file) or not os.path.exists(prompt_path(f'role-{version}.txt')):
            raise ConfigError(f'extraction.{category}: prompts for version {version!r} do not exist')
        with open(categories_file, encoding='utf-8') as handle:
            if category not in json.load(handle):
                raise ConfigError(f'extraction.{category}: categories-{version}.json has no entry for {category}')
    for setting in (matching, rejudging, idea, collision):
        if setting is not None and not os.path.exists(prompt_path(setting.prompt_version + '.txt')):
            raise ConfigError(f'{setting.name}: prompt {setting.prompt_version}.txt does not exist')


@dataclasses.dataclass(frozen=True)
class Setting:
    name: str
    model: str
    prompt_version: str
    temperature: float
    reasoning_effort: str
    max_output_tokens: int
    engine: str = 'llm'       # matching only: 'llm' (the generative call) or 'jev' (TypeSafe Jev, views/jev_matching.py)


ENGINES = ('llm', 'jev')


@dataclasses.dataclass(frozen=True)
class Config:
    version: str
    checksum: str
    provider: str
    search_top_n: int
    extraction: dict          # category -> Setting
    matching: Setting
    rejudging: Setting
    final_verdict: Setting
    idea: Setting = None      # the service's reading of a user's idea (docs/poc/idea-card.md); absent in pipeline-only configs
    collision: Setting = None # D190: the analyst question asked of the generative model when a candidate lists a thesis of its own object and measure; absent: Jev alone

    def extraction_setting(self, category):
        setting = self.extraction.get(category)
        if setting is None:
            raise ConfigError(f'no extraction setting for category {category} in config {self.version}')
        return setting


REQUIRED = ('model', 'prompt_version', 'temperature', 'reasoning_effort', 'max_output_tokens')


def _setting(name, raw):
    if not isinstance(raw, dict):
        raise ConfigError(f'setting {name} is missing')
    missing = [key for key in REQUIRED if key not in raw]
    if missing:
        raise ConfigError(f'setting {name} lacks {missing}')
    engine = str(raw.get('engine', 'llm'))
    if engine not in ENGINES:
        raise ConfigError(f'setting {name}: engine {engine!r} is not one of {ENGINES}')
    return Setting(name=name, model=str(raw['model']), prompt_version=str(raw['prompt_version']),
                   temperature=float(raw['temperature']), reasoning_effort=str(raw['reasoning_effort']),
                   max_output_tokens=int(raw['max_output_tokens']), engine=engine)


def load(path):
    with open(path, encoding='utf-8') as handle:
        text = handle.read()
    raw = json.loads(text)
    for key in ('version', 'provider', 'search_top_n', 'extraction', 'matching', 'rejudging', 'final_verdict'):
        if key not in raw:
            raise ConfigError(f'config lacks {key}')
    canonical = json.dumps({k: v for k, v in raw.items() if not k.startswith('_')}, sort_keys=True, ensure_ascii=False)
    checksum = hashlib.sha256(canonical.encode('utf-8')).hexdigest()[:16]
    extraction = {category: _setting(f'extraction.{category}', setting) for category, setting in raw['extraction'].items()}
    matching, rejudging = _setting('matching', raw['matching']), _setting('rejudging', raw['rejudging'])
    idea = _setting('idea', raw['idea']) if 'idea' in raw else None
    collision = _setting('collision', raw['collision']) if 'collision' in raw else None
    _prompt_files(extraction, matching, rejudging, idea, collision)       # final_verdict is kept in the file but no POC step calls it
    return Config(version=str(raw['version']), checksum=checksum, provider=str(raw['provider']),
                  search_top_n=int(raw['search_top_n']), extraction=extraction,
                  matching=matching, rejudging=rejudging, final_verdict=_setting('final_verdict', raw['final_verdict']), idea=idea, collision=collision)
