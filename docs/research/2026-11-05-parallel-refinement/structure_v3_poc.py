"""One-article diagnostic: read source matters, then link them to an immutable snapshot."""
import copy
import hashlib
import json
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_structure_v2 as prior
import run_small_scored
import b_matter_handover_poc
from hivemind import model

ARTICLE = 'gnews:4d1b1ca014068fb532f116b3'


def digest(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def prepare():
    cfg, uni, records = prior.build()
    base = next(r for r in records if r['variant'] == 'B2' and r['item']['input_id'] == ARTICLE)
    user = base['user']
    start, end = user.index('[Open questions immediately before this item]'), user.index('[Item]')
    questions = user[start:end]
    read_user = user[:start] + questions + user[end:]
    old_closing = 'Return only evidence per the schema. Each evidence link must be an ID of a supplied existing question.'
    if read_user.count(old_closing) != 1:
        raise ValueError('unexpected earlier closing')
    read_user = read_user.replace(old_closing, 'Return only evidence per the schema.', 1)
    old_test = "because it makes some question's answer more or less likely, about the company or its customers, suppliers, competitors, regulators or the economy"
    if read_user.count(old_test) != 1:
        raise ValueError('unexpected earlier note test')
    read_user = read_user.replace(old_test, 'because it makes the answer to a supplied research question about the company or a relevant theme more or less likely; for another company, identify the demand, supply, costs, competition or pricing path that affects the covered company and informs a supplied question about that company', 1)
    if base['item']['text'] not in read_user or questions not in read_user:
        raise ValueError('source input or question snapshot mismatch')
    schema = copy.deepcopy(base['schema'])
    evidence = schema['properties']['evidence']['items']
    for key in ('id', 'links'):
        del evidence['properties'][key]
        evidence['required'].remove(key)
    read_system = (HERE / 'structure-v3-read.txt').read_text()
    read_request = model.build_request(base['setting'], read_system, read_user, schema, 'extraction', cfg.provider)
    link_rule = base['schema']['properties']['evidence']['items']['properties']['links']['description']
    ambiguous = '(a variant, sibling or other name of the subject counts)'
    if link_rule.count(ambiguous) != 1:
        raise ValueError('unexpected link field')
    link_rule = link_rule.replace(ambiguous, '(a related variant can inform the question; related names alone do not establish identity)')
    return cfg, uni, base, questions, read_system, read_user, schema, read_request, link_rule


def link_input(base, questions, read_answer, read_request, link_rule):
    if model.check_schema(read_answer, read_request['response_format']['json_schema']['schema']):
        raise ValueError('invalid read answer')
    evidence = [dict(e, id='e' + str(i)) for i, e in enumerate(read_answer['evidence'], 1)]
    link_schema = {'type': 'object', 'additionalProperties': False, 'required': ['decisions'],
                   'properties': {'decisions': {'type': 'array', 'items': {
                       'type': 'object', 'additionalProperties': False, 'required': ['id', 'links'],
                       'properties': {'id': {'type': 'string'}, 'links': {'type': 'array',
                                      'items': {'type': 'string'}, 'description': link_rule}}}}}}
    binding = {'article': ARTICLE, 'article_sha256': digest(base['item']['text']),
               'questions_sha256': digest(questions), 'read_request_sha256': digest(read_request),
               'read_answer_sha256': digest(read_answer)}
    user = questions + '[Article]\n' + base['item']['text'] + '\n\n[Evidence items]\n' + json.dumps(evidence, ensure_ascii=False)
    return evidence, link_schema, user, binding


def join(base, evidence, link_result, binding, questions, read_answer, read_request, link_rule):
    expected_evidence, schema, user, expected_binding = link_input(base, questions, read_answer, read_request, link_rule)
    if binding != expected_binding or evidence != expected_evidence or binding['article'] != base['item']['input_id']:
        raise ValueError('cross-run or cross-article identity mismatch')
    system = (HERE / 'structure-v3-link.txt').read_text()
    request = model.build_request(base['setting'], system, user, schema, 'link', 'openai')
    if link_result['request_sha256'] != model.request_identity(request)[1]:
        raise ValueError('link answer belongs to a different request')
    decisions = link_result['data']
    if model.check_schema(decisions, schema):
        raise ValueError('invalid link answer')
    ids = [e['id'] for e in evidence]
    answers = decisions['decisions']
    if len(answers) != len(ids) or len({a['id'] for a in answers}) != len(ids) or {a['id'] for a in answers} != set(ids):
        raise ValueError('incomplete, duplicate, or foreign evidence identity')
    valid = {q['view_id'] for q in base['shown']}
    if any(not set(a['links']).issubset(valid) for a in answers):
        raise ValueError('unknown question identity')
    byid = {a['id']: a['links'] for a in answers}
    return {'evidence': [dict(e, links=byid[e['id']]) for e in evidence]}


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ('--preview', '--send'):
        raise SystemExit('usage: --preview|--send absolute-new-directory')
    out = Path(sys.argv[2])
    if not out.is_absolute() or out.exists():
        raise ValueError('output directory must be new and absolute')
    cfg, uni, base, questions, read_system, read_user, read_schema, read_request, link_rule = prepare()
    sample = {'evidence': [{'quote': 'Management guided Q2 FY27 revenue to $91.0 billion with non-GAAP gross margin holding at 75%.',
                            'one_line': 'Management guided FY2027 Q2 revenue to $91.0 billion and non-GAAP gross margin to 75%.',
                            'speaker': 'Article', 'original_who': 'NVIDIA management', 'original_day': '', 'tier': 'party_statement', 'event_time': 'FY2027 Q2'}]}
    evidence, link_schema, link_user, binding = link_input(base, questions, sample, read_request, link_rule)
    link_system = (HERE / 'structure-v3-link.txt').read_text()
    revenue = next(q['view_id'] for q in base['shown'] if q['view_id'] == 'v2')
    good = {'decisions': [{'id': 'e1', 'links': [revenue]}]}
    link_system = (HERE / 'structure-v3-link.txt').read_text()
    preview_link = model.build_request(base['setting'], link_system, link_user, link_schema, 'link', cfg.provider)
    def result(data, request=preview_link):
        return {'data': data, 'request_sha256': model.request_identity(request)[1]}
    if model.check_schema(sample, read_schema) or model.check_schema(good, link_schema):
        raise ValueError('fake positive schema failed')
    merged = join(base, evidence, result(good), binding, questions, sample, read_request, link_rule)
    h = b_matter_handover_poc.handover_by_record(merged, base, uni, run_small_scored.Dummy())
    if len(h['evidence']) != 1:
        raise ValueError('fake source-backed evidence failed handover')
    for bad in ({'decisions': []}, {'decisions': [good['decisions'][0], good['decisions'][0]]},
                {'decisions': [{'id': 'e1', 'links': ['v999999']}]}):
        try:
            join(base, evidence, result(bad), binding, questions, sample, read_request, link_rule)
        except ValueError:
            pass
        else:
            raise ValueError('invalid link control was accepted')
    fabricated = copy.deepcopy(merged)
    fabricated['evidence'][0]['quote'] = 'Fabricated quote absent from the article entirely.'
    if b_matter_handover_poc.handover_by_record(fabricated, base, uni, run_small_scored.Dummy())['evidence']:
        raise ValueError('invalid source accepted')
    other = dict(binding, read_answer_sha256='incorrect')
    try:
        join(base, evidence, result(good), other, questions, sample, read_request, link_rule)
    except ValueError:
        pass
    else:
        raise ValueError('cross-run binding mismatch accepted')
    changed_sample = copy.deepcopy(sample)
    changed_sample['evidence'][0]['one_line'] += ' Changed.'
    try:
        join(base, evidence, result(good), binding, questions, changed_sample, read_request, link_rule)
    except ValueError:
        pass
    else:
        raise ValueError('different read answer accepted')
    try:
        join(base, evidence, result(good), binding, questions + 'changed', sample, read_request, link_rule)
    except ValueError:
        pass
    else:
        raise ValueError('different question snapshot accepted')
    other_evidence, other_schema, other_user, other_binding = link_input(base, questions, changed_sample, read_request, link_rule)
    other_request = model.build_request(base['setting'], link_system, other_user, other_schema, 'link', cfg.provider)
    try:
        join(base, other_evidence, result(good), other_binding, questions, changed_sample, read_request, link_rule)
    except ValueError:
        pass
    else:
        raise ValueError('link answer from a different reading was accepted')
    join(base, other_evidence, result(good, other_request), other_binding, questions, changed_sample, read_request, link_rule)
    with tempfile.TemporaryDirectory(prefix='hivemind-v3-fake-') as temp:
        archive = model.Archive(str(Path(temp) / 'archive.sqlite'))
        def fake(provider, request):
            if json.dumps(request) not in (json.dumps(preview_link), json.dumps(other_request)):
                raise ValueError('fake transport received unexpected wire')
            return {'choices': [{'message': {'content': json.dumps(good)}}], 'usage': {}}
        actual1 = model.call(archive, cfg, base['setting'], link_system, link_user, link_schema, 'link', 'extract', transport=fake)
        actual2 = model.call(archive, cfg, base['setting'], link_system, other_user, other_schema, 'link', 'extract', transport=fake)
        result1 = {'data': actual1.data, 'request_sha256': actual1.request_sha256}
        result2 = {'data': actual2.data, 'request_sha256': actual2.request_sha256}
        join(base, evidence, result1, binding, questions, sample, read_request, link_rule)
        join(base, other_evidence, result2, other_binding, questions, changed_sample, read_request, link_rule)
        try:
            join(base, other_evidence, result1, other_binding, questions, changed_sample, read_request, link_rule)
        except ValueError:
            pass
        else:
            raise ValueError('model.call returned answer from another request was accepted')
        archive.conn.close()
    unlinked = join(base, evidence, result({'decisions': [{'id': 'e1', 'links': []}]}), binding, questions, sample, read_request, link_rule)
    if b_matter_handover_poc.handover_by_record(unlinked, base, uni, run_small_scored.Dummy())['evidence']:
        raise ValueError('no-home item was retained')
    for field in ('quote', 'one_line', 'speaker', 'original_who', 'original_day', 'tier', 'event_time'):
        if merged['evidence'][0][field] != sample['evidence'][0][field]:
            raise ValueError('linking changed source field ' + field)
    out.mkdir(parents=True)
    (out / 'preview.json').write_text(json.dumps({'read_request': read_request, 'link_request_sample': preview_link,
                                                  'binding_sample': binding}, ensure_ascii=False, indent=2) + '\n')
    print('Fake controls passed; preview written. Real link payload depends on the read answer.', flush=True)
    if sys.argv[1] == '--preview':
        return
    raise SystemExit('Sending is disabled until the complete request and controls receive independent review.')


if __name__ == '__main__':
    main()
