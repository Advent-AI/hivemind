"""The search engine over the views ledger (docs/poc/service.md).

Each view is indexed by its own text (object, kind, what it looks at, the question, the rung conditions), never by
its evidence: evidence is anchored under the view, so finding the view finds it. The index is a derived SQLite file
beside the ledger: one embedding per view, keyed by the sha256 of the text, so a rebuild re-embeds only views whose
text changed and a deleted index rebuilds to the same vectors. Query embeddings are cached the same way, so an
evaluation rerun costs nothing. The embedding key is read the way model.py reads the chat key and never stored.
"""
import hashlib
import json
import math
import os
import re
import sqlite3
import time
import urllib.error
import urllib.request

from . import model
from .views import store
from . import service

EMBEDDINGS_URL = 'https://api.openai.com/v1/embeddings'
EMBEDDING_MODEL = 'text-embedding-3-small'
EMBEDDING_PRICE_PER_M = 0.02
OBJECT_BOOST = 0.08
# Below this top similarity, an idea that names no object and matches no view text is off the library's subject
# altogether (null, D91): measured 2026-10-24 on 74 sentences, the ideas with a view all score 0.33 or more, a house
# purchase 0.19, "黄仁勋是个天才" 0.22; nonsense that still scores higher goes to the model, which answers "none".
NULL_FLOOR = 0.30
TEXT_BOOST = 0.04

SCHEMA_SQL = """
create table if not exists view_vectors (view_id text primary key, text_sha256 text, model text, vector_json text, tokens integer, built_at text);
create table if not exists query_vectors (text_sha256 text primary key, model text, vector_json text, tokens integer, built_at text);
"""


def open_index(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA_SQL)
    return conn


def view_text(record, rungs):
    """What a view is searched by: its object, kind, what it looks at, the question and the rung conditions."""
    return ' '.join([record['object_id'], record['kind'], record['looks_at'] or '', record['question'] or '', *(r['condition'] for r in rungs)])


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def openai_embeddings(texts, embedding_model=EMBEDDING_MODEL, timeout=120):
    """One embeddings call for a batch of texts: returns (vectors, total_tokens)."""
    body = json.dumps({'model': embedding_model, 'input': texts}).encode('utf-8')
    headers = {'Authorization': f'Bearer {model._key("openai")}', 'Content-Type': 'application/json'}
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(EMBEDDINGS_URL, data=body, headers=headers, method='POST'), timeout=timeout) as response:
                answer = json.loads(response.read().decode('utf-8'))
            vectors = [item['embedding'] for item in sorted(answer['data'], key=lambda d: d['index'])]
            return vectors, int((answer.get('usage') or {}).get('total_tokens') or 0)
        except urllib.error.HTTPError as error:
            # the status and the provider's error type only: the body of an auth error can echo the request's headers
            body = error.read().decode('utf-8', 'ignore')
            try:
                kind = (json.loads(body).get('error') or {}).get('type') or ''
            except (ValueError, AttributeError):
                kind = ''
            last = f'embeddings HTTP {error.code}' + (f' ({kind})' if kind else '')
            if error.code in (400, 401, 403, 404):
                raise model.TransportError(last)
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as error:
            last = repr(error)[:200]
        time.sleep(3 * (attempt + 1))
    raise model.TransportError(last or 'no answer')


def build_index(ledger, index, embed=openai_embeddings, embedding_model=EMBEDDING_MODEL, batch=64):
    """Embed every view whose text is new or changed, batch by batch, each batch committed as it lands. Returns
    (embedded, unchanged, tokens, error): on a failure the counts are what was done before it, never zero, and the
    error is the message without the provider's body. Never raises."""
    rows = [dict(r) for r in ledger.execute('select * from views order by created_seq')]
    todo, unchanged = [], 0
    for record in rows:
        text = view_text(record, store.rungs_of(ledger, record['view_id']))
        digest = sha(text)
        have = index.execute('select text_sha256, model, vector_json from view_vectors where view_id=?', (record['view_id'],)).fetchone()
        if have and have['text_sha256'] == digest and have['model'] == embedding_model and usable(json.loads(have['vector_json'])):
            unchanged += 1
        else:
            todo.append((record['view_id'], digest, text))
    embedded = tokens = 0
    for start in range(0, len(todo), batch):
        chunk = todo[start:start + batch]
        try:
            vectors, used = embed([t for _, _, t in chunk], embedding_model)
        except (model.TransportError, OSError) as error:
            return embedded, unchanged, tokens, str(error)[:120]
        if len(vectors) != len(chunk) or not all(usable(v) for v in vectors):
            return embedded, unchanged, tokens, 'the embedding answer did not hold one usable vector per text'
        tokens += used
        now = time.strftime('%Y-%m-%dT%H:%M:%S')
        index.executemany('insert or replace into view_vectors (view_id, text_sha256, model, vector_json, tokens, built_at) values (?,?,?,?,?,?)',
                          [(view_id, digest, embedding_model, json.dumps(vector), used // max(1, len(chunk)), now) for (view_id, digest, _), vector in zip(chunk, vectors)])
        index.commit()
        embedded += len(chunk)
    return embedded, unchanged, tokens, None


ensure_index = build_index


def usable(vector):
    """A vector the ranking can use: a non-empty list of numbers."""
    return isinstance(vector, list) and len(vector) > 0 and all(isinstance(x, (int, float)) for x in vector)


def fresh_vectors(ledger, index, embedding_model=EMBEDDING_MODEL):
    """view id → vector for every view whose stored vector was made from the view's current text and is usable; a
    view whose text changed since, was never embedded, or holds an empty vector is absent."""
    stored = {r['view_id']: (r['text_sha256'], json.loads(r['vector_json'])) for r in index.execute('select view_id, text_sha256, vector_json from view_vectors where model=?', (embedding_model,))}
    out = {}
    dims = None
    for record in ledger.execute('select * from views'):
        have = stored.get(record['view_id'])
        if have and have[0] == sha(view_text(record, store.rungs_of(ledger, record['view_id']))) and usable(have[1]) and (dims is None or len(have[1]) == dims):
            out[record['view_id']] = have[1]
            dims = len(have[1])
    return out


def query_vector(index, query, embed=openai_embeddings, embedding_model=EMBEDDING_MODEL):
    digest = sha(query)
    row = index.execute('select vector_json from query_vectors where text_sha256=? and model=?', (digest, embedding_model)).fetchone()
    if row:
        return json.loads(row['vector_json']), True
    vectors, tokens = embed([query], embedding_model)
    index.execute('insert or replace into query_vectors (text_sha256, model, vector_json, tokens, built_at) values (?,?,?,?,?)',
                  (digest, embedding_model, json.dumps(vectors[0]), tokens, time.strftime('%Y-%m-%dT%H:%M:%S')))
    index.commit()
    return vectors[0], False


def warm_queries(index, queries, embed=openai_embeddings, embedding_model=EMBEDDING_MODEL):
    """Embed every query not yet in the cache in one embeddings call, so the searches that follow find their vectors
    locally. Measured 2026-10-24: a never-seen query costs a 0.6–1.9 s round trip and an idea made seven of them in
    a row, five seconds of a fourteen-second idea. Returns the number of queries embedded."""
    wanted = {}
    for query in queries:
        digest = sha(query)
        if digest not in wanted and not index.execute('select 1 from query_vectors where text_sha256=? and model=?', (digest, embedding_model)).fetchone():
            wanted[digest] = query
    if not wanted:
        return 0
    vectors, tokens = embed(list(wanted.values()), embedding_model)
    if len(vectors) != len(wanted):
        raise model.TransportError(f'the embedding answer held {len(vectors)} vectors for {len(wanted)} queries')
    now = time.strftime('%Y-%m-%dT%H:%M:%S')
    index.executemany('insert or replace into query_vectors (text_sha256, model, vector_json, tokens, built_at) values (?,?,?,?,?)',
                      [(digest, embedding_model, json.dumps(vector), tokens // len(wanted), now) for digest, vector in zip(wanted, vectors)])
    index.commit()
    return len(wanted)


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(x * x for x in b)) or 1.0
    return dot / (na * nb)


def object_aliases(universe_path):
    """object id → the words that name it in an idea: its id, its full name and the aliases the universe lists
    (tickers, Chinese names, product names). Never the single words of a name: 'rate', 'risk', 'technology' or
    'china' hit ideas about anything (2026-10-24: 5 of 49 probes got a false object that way)."""
    aliases = {}
    with open(universe_path, encoding='utf-8') as handle:
        universe = json.load(handle)
    for kind in ('companies', 'themes'):
        for entry in universe.get(kind, []):
            words = {entry['id'].lower(), entry['name'].lower(), *(a.lower() for a in entry.get('aliases', []))}
            aliases[entry['id']] = {w for w in words if len(w) >= 3 or CJK.search(w)}
    return aliases


CJK = re.compile(r'[\u4e00-\u9fff]+')
LATIN_WORD = re.compile(r'[a-z0-9][a-z0-9.\-]{2,}', re.I)


def _names(word, text):
    """A Latin alias must stand as a word ('meta' is not in 'metadata'); a Chinese alias may stand anywhere."""
    if CJK.search(word):
        return word in text
    return re.search(r'(?<![a-z0-9])' + re.escape(word) + r'(?![a-z0-9])', text) is not None


def objects_in(query, aliases):
    text = query.lower()
    return {object_id for object_id, words in aliases.items() if any(_names(w, text) for w in words)}


def lexical_terms(query, limit=12):
    """What the ledger's trigram index is asked for: the Latin words of three characters or more, and every
    three-character window of each Chinese run (Chinese has no spaces to split on; the index matches on
    trigrams). 2026-10-24: a Chinese idea written without spaces matched nothing as one phrase."""
    terms = [m.group(0) for m in LATIN_WORD.finditer(query)]
    for run in CJK.findall(query):
        terms += [run[i:i + 3] for i in range(len(run) - 2)] or [run]
    seen, out = set(), []
    for term in terms:
        if term.lower() not in seen:
            seen.add(term.lower())
            out.append(term)
    return out[:limit]


def search(ledger, index, query, k=10, as_of=None, include_closed=False, embed=openai_embeddings, embedding_model=EMBEDDING_MODEL, aliases=None, semantic=True):
    """Top-k views for a query as of a day: cosine similarity on the view text, plus a small boost when the query
    names the view's object and when the ledger's trigram index also matches. The ranking is 'semantic' only when
    semantic ranking is allowed, every candidate has a usable vector made from its current text and the query could
    be embedded; otherwise it is 'lexical' (the trigram index's own order), and the answer says so and names the
    views without a fresh vector. `semantic=False` (a front started with --lexical) never calls the embedder.
    `results` is null when the library holds no view on anything the idea names as of that day (D91): no company
    or theme of the universe is named in it and the ledger's own text index matches no view; otherwise the ranked
    list comes back whole and the caller judges which views correspond (D76)."""
    as_of = as_of or service.default_as_of(ledger)
    candidates = service.summaries(ledger, as_of, include_closed)
    if not candidates:
        return {'query': query, 'as_of': as_of, 'mode': 'semantic' if semantic else 'lexical', 'missing_vectors': [], 'results': None}
    mentioned = objects_in(query, aliases or {})
    lexical_order = store.search_views(ledger, ' '.join(lexical_terms(query)), 50)          # the ledger's trigram index, best first
    lexical_rank = {view_id: i for i, view_id in enumerate(lexical_order)}
    vectors = fresh_vectors(ledger, index, embedding_model) if semantic else {}
    missing = [record['view_id'] for record in candidates if record['view_id'] not in vectors]
    mode, q = 'semantic', None
    if not semantic or missing:
        mode = 'lexical'
    else:
        try:
            q, _ = query_vector(index, query, embed, embedding_model)
        except (model.TransportError, OSError):
            mode = 'lexical'
    results = []
    for record in candidates:
        semantic = cosine(q, vectors[record['view_id']]) if q is not None else 0.0
        object_hit = record['object'] in mentioned
        text_hit = record['view_id'] in lexical_rank
        # with embeddings a text hit is a small nudge; without them the trigram index's own order is the ranking
        text_score = (TEXT_BOOST if mode == 'semantic' else 1.0 - lexical_rank[record['view_id']] / max(1, len(lexical_order))) if text_hit else 0.0
        score = semantic + (OBJECT_BOOST if object_hit else 0.0) + text_score
        results.append({'view_id': record['view_id'], 'object': record['object'], 'kind': record['kind'], 'looks_at': record['looks_at'], 'question': record['question'],
                        'due_day': record['due_day'], 'open': record['open'], 'dependencies': record['dependencies'], 'dependants': record['dependants'],
                        'score': round(score, 4), 'parts': {'semantic': round(semantic, 4), 'object_hit': object_hit, 'text_hit': text_hit}})
    results.sort(key=lambda r: -r['score'])
    named_or_matched = any(r['parts']['object_hit'] or r['parts']['text_hit'] for r in results)
    best = max((r['parts']['semantic'] for r in results), default=0.0)
    if not named_or_matched and (q is None or best < NULL_FLOOR):
        return {'query': query, 'as_of': as_of, 'mode': mode, 'missing_vectors': missing, 'results': None}     # no recorded view on anything the idea names
    return {'query': query, 'as_of': as_of, 'mode': mode, 'missing_vectors': missing, 'results': results[:k]}


def fake_embed(texts, embedding_model=EMBEDDING_MODEL, dims=256):
    """A deterministic stand-in for tests: a bag of character bigrams hashed into a fixed number of dimensions, so
    texts sharing words share directions. Never used for the real index."""
    out = []
    for text in texts:
        vector = [0.0] * dims
        lowered = re.sub(r'\s+', ' ', text.lower())
        for i in range(len(lowered) - 1):
            vector[int(hashlib.md5(lowered[i:i + 2].encode('utf-8')).hexdigest(), 16) % dims] += 1.0
        out.append(vector)
    return out, sum(len(t) for t in texts) // 4
