"""The HTTP front of the Hivemind service (docs/poc/service.md, docs/poc/idea-card.md): JSON on one port, one route
per call, every answer from src/hivemind/service.py, search.py and idea.py. The web page's front; agents use MCP.

GET routes (query string parameters in brackets):
  /search          [q, k, as_of, include_closed]
  /views           [object, as_of, include_closed]
  /views/<id>      [as_of]
  /views/<id>/history   [from, to]
  /views/<id>/evidence  [as_of, tier]
  /views/<id>/record    [as_of]
  /changes         [since, to]
  /evaluate        [view_id, comparator (>=, <, =), value_usd, as_of]
  /days            the ledger's first and last completed day
  /thesis-bundles   [ids (comma-separated), as_of] complete dated frontend inputs
  /library         [as_of] all collected theses and stored groups, without a model call
POST route (JSON body):
  /ideas           {text, as_of?, k?, bundles?} → the idea card (mapping and optional analyst summary; none when no view is recorded); bundles:false leaves the
                   views' bundles out for a page that fetches /thesis-bundles itself
                   Accept: application/x-ndjson streams progress then result, or an error record

Every request opens its own connections (the server is threaded; an idea call takes seconds and must not block the
page's reads). Usage: python3 scripts/hivemind_api.py [--host 127.0.0.1] [--port 8788] [--views DB] [--items DB]
[--index DB] [--archive DB] [--config JSON] [--lexical]
"""
import argparse
import http.server
import json
import os
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import bundle, config, idea, model, search, service  # noqa: E402
from hivemind.views import store  # noqa: E402

PATHS = {}
ALIASES = {}
CFG = None
SEMANTIC = True
REQUEST_ERRORS = (KeyError, service.LedgerError, model.TransportError, model.SchemaError, config.ConfigError, ValueError, TypeError)


def error_response(error):
    if isinstance(error, KeyError):
        return 404, f'not found: {error}'
    if isinstance(error, service.LedgerError):
        return 500, str(error)
    if isinstance(error, (model.TransportError, model.SchemaError, config.ConfigError)):
        return 502, f'{type(error).__name__}: {str(error)[:200]}'
    return 400, str(error)


class Connections:
    """The databases one request reads: opened on entry, closed on exit, never shared between threads."""

    def __init__(self, read_only=False):
        self.read_only = read_only

    def __enter__(self):
        self.ledger = service.open_ledger(PATHS['views'])
        self.index = None if self.read_only else search.open_index(PATHS['index'])
        self.items = store.open_read_only(PATHS['items']) if PATHS.get('items') and os.path.exists(PATHS['items']) else None
        self.archive = None if self.read_only else model.Archive(PATHS['archive'])
        return self

    def __exit__(self, *exc):
        for conn in (self.ledger, self.index, self.items):
            if conn is not None:
                conn.close()


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):   # one line per request, no query text or body (an idea can carry anything)
        sys.stderr.write(f'{self.address_string()} {self.command} {self.path.split("?")[0]}\n')

    def _send(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self._cors()
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):          # a browser's preflight before a JSON POST
        self.send_response(204)
        self._cors()
        self.end_headers()

    def _answer(self, work, read_only=False):
        try:
            with Connections(read_only) as db:
                self._send(200, work(db))
        except REQUEST_ERRORS as error:
            status, message = error_response(error)
            self._send(status, {'error': message})

    def _stream_answer(self, work):
        self.send_response(200)
        self.send_header('Content-Type', 'application/x-ndjson; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self._cors()
        self.end_headers()

        def emit(event):
            self.wfile.write((json.dumps(event, ensure_ascii=False) + '\n').encode('utf-8'))
            self.wfile.flush()

        try:
            with Connections() as db:
                card = work(db, lambda stage: emit({'type': 'progress', 'stage': stage}))
                emit({'type': 'result', 'data': card})
        except (BrokenPipeError, ConnectionResetError):
            return
        except REQUEST_ERRORS as error:
            status, message = error_response(error)
            try:
                emit({'type': 'error', 'status': status, 'message': message})
            except (BrokenPipeError, ConnectionResetError):
                pass

    def do_GET(self):
        url = urllib.parse.urlsplit(self.path)
        q = {k: v[0] for k, v in urllib.parse.parse_qs(url.query).items()}
        parts = [p for p in url.path.split('/') if p]
        self._answer(lambda db: route(db, parts, q), read_only=parts in (['library'], ['thesis-bundles']))

    def do_POST(self):
        parts = [p for p in urllib.parse.urlsplit(self.path).path.split('/') if p]
        length = int(self.headers.get('Content-Length') or 0)
        raw = self.rfile.read(length) if length else b''

        def work(db, on_progress=None):
            if parts != ['ideas']:
                raise KeyError('/'.join(parts))
            try:
                body = json.loads(raw or b'{}')
            except json.JSONDecodeError as error:
                raise ValueError(f'the body is not JSON: {error}')
            if not isinstance(body, dict) or not str(body.get('text') or '').strip():
                raise ValueError('POST /ideas needs a JSON body with text')
            if CFG is None:
                raise config.ConfigError('the server was started without --config, so it cannot read ideas')
            return idea.read_idea(db.ledger, db.index, db.items, db.archive, CFG, body['text'], body.get('as_of') or None,
                                  int(body.get('k') or 10), aliases=ALIASES, semantic=SEMANTIC, bundles=body.get('bundles', True) is not False,
                                  on_progress=on_progress)
        accepted = [part.split(';', 1)[0].strip() for part in self.headers.get('Accept', '').split(',')]
        if parts == ['ideas'] and 'application/x-ndjson' in accepted:
            self._stream_answer(work)
        else:
            self._answer(work)


def flag(value):
    return str(value).lower() in ('1', 'true', 'yes')


def route(db, parts, q):
    ledger, as_of = db.ledger, q.get('as_of') or None
    if parts == ['library']:
        return bundle.library(ledger, db.items, as_of)
    if parts == ['thesis-bundles']:
        return bundle.thesis_bundles(ledger, db.items, [id.strip() for id in q.get('ids', '').split(',') if id.strip()], as_of)
    if parts == ['search']:
        return search.search(ledger, db.index, q.get('q', ''), int(q.get('k', 10)), as_of, flag(q.get('include_closed', '')), aliases=ALIASES, semantic=SEMANTIC)
    if parts == ['views']:
        return service.views(ledger, q.get('object') or None, as_of, flag(q.get('include_closed', '')))
    if len(parts) == 2 and parts[0] == 'views':
        record = service.view(ledger, parts[1], as_of)
        if record is None:
            raise KeyError(parts[1])
        return record
    if len(parts) == 3 and parts[0] == 'views':
        view_id, what = parts[1], parts[2]
        if what == 'history':
            return service.history(ledger, view_id, q.get('from') or None, q.get('to') or None)
        if what == 'evidence':
            return service.evidence(ledger, view_id, as_of, q.get('tier') or None)
        if what == 'record':
            return service.record(ledger, view_id, as_of)
        raise KeyError(what)
    if parts == ['changes']:
        if not q.get('since'):
            raise ValueError('changes needs since=YYYY-MM-DD')
        return service.changes(ledger, q['since'], q.get('to') or None)
    if parts == ['evaluate']:
        if not all(k in q for k in ('view_id', 'comparator', 'value_usd')):
            raise ValueError('evaluate needs view_id, comparator and value_usd')
        answer = service.evaluate(ledger, q['view_id'], q['comparator'], float(q['value_usd']), as_of)
        if answer is None:
            raise KeyError(q['view_id'])
        return answer
    if parts == ['days']:
        row = ledger.execute('select min(day), max(day) from days_completed').fetchone()
        return {'first_day': row[0], 'last_day': row[1]}
    raise KeyError('/'.join(parts))


def main():
    global ALIASES, CFG, SEMANTIC
    parser = argparse.ArgumentParser()
    parser.add_argument('--views', default=os.path.join(ROOT, 'poc', 'data', 'english-v23-jev-2026-10-25', 'views.sqlite'))
    parser.add_argument('--items', default=os.path.join(ROOT, 'poc', 'data', 'items-window-tags2-2026-10-24.sqlite'), help='the items database, for source titles in the idea card')
    parser.add_argument('--index', default=os.path.join(ROOT, 'poc', 'data', 'service-english', 'search-index.sqlite'))
    parser.add_argument('--archive', default=os.path.join(ROOT, 'poc', 'data', 'service-english', 'idea-archive.sqlite'), help='where idea model calls are archived for replay')
    parser.add_argument('--config', default=os.path.join(ROOT, 'poc', 'config', 'poc-v32-idea.json'), help='the config whose idea settings name the mapping and final assessment models and prompts')
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8788)
    parser.add_argument('--lexical', action='store_true', help='no embedding at all (no network): search ranks by the trigram index and says mode lexical')
    args = parser.parse_args()
    PATHS.update(views=args.views, items=args.items, index=args.index, archive=args.archive)
    os.makedirs(os.path.dirname(os.path.abspath(args.archive)), exist_ok=True)
    ALIASES = search.object_aliases(args.universe)
    CFG = config.load(args.config) if args.config and os.path.exists(args.config) else None
    SEMANTIC = not args.lexical
    if not os.path.exists(args.items):
        print(f'items database not found ({args.items}): idea cards name sources by input id', flush=True)
    if CFG is None:
        print('no config: GET routes only, POST /ideas answers 502', flush=True)
    else:
        print(f'config {CFG.version}: ideas read by {CFG.idea.model} ({CFG.idea.prompt_version}, effort {CFG.idea.reasoning_effort}); archive {os.path.basename(args.archive)}', flush=True)
        if CFG.idea_summary is not None:
            print(f'analyst summary: {CFG.idea_summary.model} ({CFG.idea_summary.prompt_version}, effort {CFG.idea_summary.reasoning_effort})', flush=True)
    if args.lexical:
        print('--lexical: no embedding; every search answers in lexical mode', flush=True)
    else:
        with Connections() as db:
            embedded, unchanged, tokens, error = search.ensure_index(db.ledger, db.index)
        print(f'index: {embedded} views embedded, {unchanged} unchanged, {tokens} tokens' + (f'; embedding stopped ({error}): search runs lexical until the rest is built' if error else ''), flush=True)
    print(f'hivemind api on http://{args.host}:{args.port}  ledger {os.path.basename(os.path.dirname(args.views))}/{os.path.basename(args.views)}  index {os.path.basename(args.index)}', flush=True)
    server = http.server.ThreadingHTTPServer((args.host, args.port), Handler)
    server.daemon_threads = True
    server.serve_forever()


if __name__ == '__main__':
    main()
