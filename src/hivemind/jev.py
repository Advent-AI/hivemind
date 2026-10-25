"""TypeSafe Jev (https://docs.typesafe.ai): typed answers over one state, no generated text. A request is `{model, state,
questions}`; each question is `noul` (yes/no → a probability), `choice` (labelled options → `choice`, `probabilities`,
`confidence`) or `score`. Every call is archived in `model_calls` like every other model call, keyed by the request's
digest, so a byte-identical request is served from the archive; input is priced from `model.PRICES`, output is free."""
import json
import os
import time
import urllib.error
import urllib.request
import uuid

from . import model

ENDPOINT = 'https://api.typesafe.ai/v1/systemone'
KEY_NAME = 'TYPESAFE_API_KEY'
RETRY_STATUSES = {429, 529}


def _key():
    if os.environ.get(KEY_NAME):
        return os.environ[KEY_NAME]
    with open(model.CREDENTIALS, encoding='utf-8') as handle:
        return json.load(handle)[KEY_NAME]


def transport(request, timeout=60):
    """POST the request; one retry after a pause on a rate-limit or overload status; any other failure is a TransportError.
    The body is the same sorted text the archive digests, so a cache hit is byte-identical to what was sent."""
    body = json.dumps(request, sort_keys=True, ensure_ascii=False).encode('utf-8')
    key = _key()
    for attempt in range(2):
        req = urllib.request.Request(ENDPOINT, body, {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                raw = response.read()
            break
        except urllib.error.HTTPError as error:
            if error.code in RETRY_STATUSES and attempt == 0:
                time.sleep(2)
                continue
            raise model.TransportError(f'Jev HTTP {error.code}') from None
        except (urllib.error.URLError, OSError) as error:
            raise model.TransportError(f'Jev transport failed: {type(error).__name__}') from None
    if key.encode('utf-8') in raw:
        raise model.TransportError('Jev response echoed the credential; not archived')
    return json.loads(raw.decode('utf-8'))


# Jev reports each probability rounded to two decimals independently of the choice it made on the unrounded values, so the
# chosen option may print one unit below another (0.47 against 0.48; 1 of 2,353 archived choice answers on 2026-10-25).
ROUNDING = 0.01


def validate(answers, questions):
    """The answers of a response against the request's questions; a list of problems."""
    problems = []
    if not isinstance(answers, dict) or set(answers) != set(questions):
        return ['answer set differs from the questions asked']
    for qid, question in questions.items():
        answer = answers[qid]
        if not isinstance(answer, dict) or answer.get('type') != question['type']:
            problems.append(f'{qid}: answer type mismatch')
            continue
        if question['type'] == 'noul':
            if not isinstance(answer.get('noul'), (int, float)) or not 0 <= answer['noul'] <= 1:
                problems.append(f'{qid}: noul out of range')
        elif question['type'] == 'choice':
            probabilities = answer.get('probabilities')
            if answer.get('choice') not in question['criteria'] or not isinstance(probabilities, dict) or set(probabilities) != set(question['criteria']):
                problems.append(f'{qid}: choice or probabilities do not match the criteria')
            elif any(not isinstance(v, (int, float)) or isinstance(v, bool) or not 0 <= v <= 1 for v in probabilities.values()) \
                    or abs(sum(probabilities.values()) - 1) > 0.005 * len(probabilities) + 1e-9:
                problems.append(f'{qid}: probabilities are not a distribution')
            elif probabilities[answer['choice']] < max(probabilities.values()) - ROUNDING - 1e-9:
                problems.append(f'{qid}: choice is not the most probable option')
    return problems


def request_for(setting, state, questions):
    """The complete Jev request used both for dispatch and in-flight identity."""
    return {'model': setting.model, 'state': state, 'questions': questions}


def ask(archive, cfg, setting, state, questions, purpose, *, transport=None):
    """One Jev request, archived; returns model.Answer whose data is the `answers` map."""
    request = request_for(setting, state, questions)
    request_json, sha = model.request_identity(request)
    prompt_chars = len(request_json)
    hit = archive.lookup(sha)
    if hit:
        call_id, answer_json, _, input_tokens, output_tokens = hit
        return model.Answer(json.loads(answer_json), call_id, sha, True, prompt_chars, input_tokens or 0, output_tokens or 0, 0.0)
    started = time.time()
    response = (transport or globals()['transport'])(request)
    seconds = round(time.time() - started, 2)
    answers = response.get('answers') if isinstance(response, dict) else None
    problems = validate(answers, questions)
    usage = response.get('usage') or {} if isinstance(response, dict) else {}
    input_tokens, output_tokens = int(usage.get('input_tokens') or 0), int(usage.get('output_tokens') or 0)
    price_in, _ = model.PRICES.get(setting.model, (0.0, 0.0))
    cost = round(input_tokens / 1e6 * price_in, 6)
    call_id = archive.record(purpose=purpose, config_version=cfg.version, config_checksum=cfg.checksum, model=setting.model,
                             request_sha256=sha if not problems else sha + ':schema:' + uuid.uuid4().hex[:8], request_json=request_json,
                             response_json=json.dumps(response, ensure_ascii=False)[:200000], answer_json=json.dumps(answers, ensure_ascii=False) if answers is not None else None,
                             prompt_chars=prompt_chars, input_tokens=input_tokens, output_tokens=output_tokens, cost_usd=cost,
                             seconds=seconds, created_at=time.strftime('%Y-%m-%dT%H:%M:%S'))
    if problems:
        raise model.SchemaError('; '.join(problems[:5]))
    return model.Answer(answers, call_id, sha, False, prompt_chars, input_tokens, output_tokens, cost)
