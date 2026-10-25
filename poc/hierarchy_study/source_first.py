"""D162 isolated source selection followed by question construction; existing storage stays authoritative."""
import argparse
import copy
import dataclasses
import json
import re
from pathlib import Path

import ohio_sequence as ohio
from hivemind import extraction, model


def source_schema():
    evidence = copy.deepcopy(extraction.SCHEMA['properties']['evidence']['items'])
    evidence['required'].remove('links')
    del evidence['properties']['links']
    evidence['properties']['id']['pattern'] = r'^e[1-9][0-9]*$'
    return ohio.study.obj({'observations': {'type': 'array', 'items': evidence}})


def check_source(data):
    errors = model.check_schema(data, source_schema())
    if errors:
        raise ohio.Refused('; '.join(errors))
    ids = [e['id'] for e in data['observations']]
    if len(ids) != len(set(ids)) or any(re.fullmatch(r'e[1-9][0-9]*', eid) is None for eid in ids):
        raise ohio.Refused('Source observations require unique e IDs')


def organisation_schema(observations, offered):
    result = ohio.schema(offered)
    del result['properties']['evidence']
    result['required'].remove('evidence')
    candidate = result['properties']['candidates']['items']
    del candidate['properties']['evidence_ids']
    candidate['required'].remove('evidence_ids')
    disposition = ohio.study.obj({'links': {'type': 'array', 'items': {'type': 'string'}},
                                  'omit_reason': {'type': 'string'}})
    result['properties']['dispositions'] = ohio.study.obj({e['id']: copy.deepcopy(disposition) for e in observations})
    result['required'].append('dispositions')
    return result


def assemble(source, organised, offered):
    """Preserve source fields and derive both readers' evidence relationships from dispositions.links."""
    check_source(source)
    observations = source['observations']
    errors = model.check_schema(organised, organisation_schema(observations, offered))
    if errors:
        raise ohio.Refused('; '.join(errors))
    evidence = []
    for observation in observations:
        decision = organised['dispositions'][observation['id']]
        if bool(decision['links']) == bool(decision['omit_reason'].strip()):
            raise ohio.Refused(f'{observation["id"]}: choose links or an omission reason')
        if decision['links']:
            evidence.append(dict(copy.deepcopy(observation), links=copy.deepcopy(decision['links'])))
    candidates = [dict(copy.deepcopy(c), evidence_ids=[e['id'] for e in evidence if c['id'] in e['links']])
                  for c in organised['candidates']]
    result = {'evidence': evidence, 'candidates': candidates, 'threads': copy.deepcopy(organised['threads'])}
    ohio.validate_references(result, offered)
    return result


def research_context(item, shown, uni):
    objects = [o['value'] for o in item.get('object_identifiers', [])]
    return {
        'item': {key: item.get(key) for key in ('input_id', 'category', 'publisher', 'publisher_type', 'publication_day', 'title')},
        'category_reading': extraction._categories('v5')[item['category']],
        'objects': objects,
        'themes': uni.theme_list(),
        'fiscal_notes': [note for o in objects if (note := uni.fiscal_note(o, item['publication_day']))],
        'research_references': {o: uni.watch_list(o) for o in objects},
        'existing_questions': [{key: v.get(key) for key in ('view_id', 'object_id', 'question', 'looks_at', 'due_day', 'depends_on')}
                               for v in shown],
    }


class SourceFirstReader:
    def __init__(self, source_role):
        self.source_role = source_role

    def __call__(self, *, archive, cfg, uni, item, shown, offered, directory, transport, role_text):
        setting = cfg.extraction_setting(item['category'])
        context = research_context(item, shown, uni)
        source_user = json.dumps(dict(context, text=item['text'][:extraction.MAX_TEXT_CHARS]), ensure_ascii=False)
        first = model.call(archive, cfg, setting, self.source_role, source_user, source_schema(),
                           'source_selection', 'source_selection', transport=transport)
        if first.cached:
            raise ohio.Refused('Fresh source selection unexpectedly used cache')
        ohio.write(directory / 'source.json', first.data)
        check_source(first.data)
        provenance = {'source': {'call_id': first.call_id, 'request_sha256': first.request_sha256}, 'organisation': None}
        ohio.write(directory / 'reader-calls.json', provenance)
        if not first.data['observations']:
            return dataclasses.replace(first, data={'evidence': [], 'candidates': [], 'threads': []})
        organised_user = json.dumps(dict(context, groups=offered, observations=first.data['observations']), ensure_ascii=False)
        second = model.call(archive, cfg, setting, role_text + '\n\n' + ohio.GROUP_PROMPT, organised_user,
                            organisation_schema(first.data['observations'], offered),
                            'question_construction', 'question_construction', transport=transport)
        if second.cached:
            raise ohio.Refused('Fresh question construction unexpectedly used cache')
        ohio.write(directory / 'organisation.json', second.data)
        provenance['organisation'] = {'call_id': second.call_id, 'request_sha256': second.request_sha256}
        ohio.write(directory / 'reader-calls.json', provenance)
        data = assemble(first.data, second.data, offered)
        return dataclasses.replace(second, data=data, cost_usd=first.cost_usd + second.cost_usd,
                                   input_tokens=first.input_tokens + second.input_tokens,
                                   output_tokens=first.output_tokens + second.output_tokens,
                                   prompt_chars=first.prompt_chars + second.prompt_chars)


def prepare(out, *, source_role_path, organiser_role_path, control_role_path, design_path):
    source_role_path = source_role_path.resolve()
    if not source_role_path.read_text().strip():
        raise ValueError('Source role must not be empty')
    ohio.prepare(out, role_path=organiser_role_path, control_role_path=control_role_path,
                 item_ids=(*ohio.ITEM_IDS, 'gnews:eb74b9d16d227f0c2b7a39d8'), max_requests=63, design_path=design_path)
    manifest = ohio.read(out / 'manifest.json')
    manifest.update(requires_reader=True, reader_kind='source_first', source_role_path=str(source_role_path))
    for path in (Path(__file__).resolve(), source_role_path):
        manifest['dependencies'][str(path)] = ohio.digest(path)
    ohio.write(out / 'manifest.json', manifest)


def run(out):
    ohio.verify(out)
    manifest = ohio.read(out / 'manifest.json')
    if manifest.get('reader_kind') != 'source_first':
        raise ValueError('This entry point requires a registered source_first experiment')
    ohio.run(out, reader=SourceFirstReader(Path(manifest['source_role_path']).read_text()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('prepare', 'run'))
    parser.add_argument('--out', type=Path, required=True)
    for option in ('source-role-path', 'organiser-role-path', 'control-role-path', 'design-path'):
        parser.add_argument('--' + option, type=Path)
    args = parser.parse_args()
    paths = {name: getattr(args, name) for name in ('source_role_path', 'organiser_role_path', 'control_role_path', 'design_path')}
    if args.command == 'prepare':
        if not all(paths.values()):
            parser.error('prepare requires all four role/design paths')
        prepare(args.out.resolve(), **paths)
    else:
        if any(paths.values()):
            parser.error('run uses the frozen manifest paths')
        run(args.out.resolve())


if __name__ == '__main__':
    main()
