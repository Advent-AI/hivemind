"""The MCP front of the Hivemind service (docs/poc/service.md): one tool per call, stdio transport, every answer from
src/hivemind/service.py and search.py. Hivemind is a database with a search engine on top: the caller searches,
chooses which views to keep and how to arrange them, and reads each view's state, history and evidence. Nothing
here writes to the ledger or knows who is asking.

Usage: python3 scripts/hivemind_mcp.py [--views DB] [--index DB]
Claude Code: claude mcp add hivemind -- python3 /path/to/scripts/hivemind_mcp.py
"""
import argparse
import contextlib
import os
import sys

from mcp.server.fastmcp import FastMCP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import bundle, search as search_module, service  # noqa: E402
from hivemind.views import store  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument('--views', default=os.path.join(ROOT, 'poc', 'data', 'served-2026-10-28-v34-nvda-3m-through-0828', 'views.sqlite'))
parser.add_argument('--index', default=os.path.join(ROOT, 'poc', 'data', 'service-english', 'search-index.sqlite'))
parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
parser.add_argument('--items', default=os.path.join(ROOT, 'poc', 'data', 'items-nvda-2026-07-01-10-27.sqlite'))
parser.add_argument('--lexical', action='store_true', help='no embedding at all (no network): search ranks by the trigram index and says mode lexical')
parser.add_argument('--transport', choices=['stdio', 'streamable-http'], default='stdio', help='stdio for a local agent; streamable-http to serve /mcp over HTTP (Docker)')
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('--port', type=int, default=8789)
ARGS = parser.parse_args()
ALIASES = search_module.object_aliases(ARGS.universe)

from hivemind import idea as idea_module  # noqa: E402


@contextlib.contextmanager
def connections():
    """One tool call's databases (live-service/OPERATING-CONTRACT.md, row 2): the ledger, items and index opened per call, never shared
    between calls (a search writes the index's query cache); the ledger's committed state pinned by BEGIN and a first read; every
    connection closed on every path, a failure while opening included."""
    opened = []
    try:
        ledger = service.open_pinned(ARGS.views)
        opened.append(ledger)
        index = search_module.open_index(ARGS.index)
        opened.append(index)
        items = store.open_read_only(ARGS.items) if os.path.exists(ARGS.items) else None
        if items is not None:
            opened.append(items)
        yield ledger, items, index
    finally:
        if opened and opened[0].in_transaction:
            opened[0].rollback()
        for conn in reversed(opened):
            conn.close()


def start_objects():
    """The object list for the server's instructions, computed once at start and labelled with its day; every tool reads the current
    last completed day. Start-up indexing embeds only views visible at the last completed day, and none on a first-day store (row 4a)."""
    with connections() as (ledger, _items, index):
        if not ARGS.lexical:
            try:
                embedded, _unchanged, _tokens, error = search_module.ensure_index(ledger, index)
                if error:
                    sys.stderr.write(f'hivemind: embedding stopped ({error}) after {embedded} views; search runs lexical until the rest is built\n')
            except service.FirstDayNotCompleted:
                sys.stderr.write("hivemind: index not built, the store's first day has not completed; search is lexical until a restart\n")
        try:
            day = service.resolve_bound(ledger, None)
        except service.FirstDayNotCompleted:
            return "No day of this ledger has completed yet; every tool refuses until one has."
        return (f'Objects as of {day}, when this server started; every tool reads the current last completed day. '
                + idea_module.object_list(ledger, day, ALIASES))


OBJECTS = start_objects()
mcp = FastMCP('hivemind', host=ARGS.host, port=ARGS.port, instructions=(
    'Hivemind is a ledger of research views (a dated question with a five-step ladder, judged every day on evidence) '
    'with a search engine on top. To read an idea against it: first break the idea into its parts, the one to four '
    'questions whose answers decide it (each about one concrete quantity, date or event); search with the idea and with '
    'each part (k=20); map each part to every view whose question answers it or whose outcome would move it, leaving out '
    'views that only share a company or a word; then read each mapped view (state as of a day, history, evidence) and '
    'say what the judged positions tell about each part and which parts no view covers. Say judged, never true. Every '
    'tool takes as_of, a calendar day; the default is the ledger\'s last completed day. Nothing here changes the ledger. '
    'search matches each view\'s own text (question, what it looks at, ladder conditions; Chinese, English queries work): '
    'ask for one object and one quantity or event per query; views(object) lists everything under one object. '
    + OBJECTS))


@mcp.tool()
def thesis_library(as_of: str = '') -> dict:
    """All collected theses and their stored research groups, including ungrouped and closed theses.
    Membership is not a dependency or a parent-child relationship. No model call or ledger write."""
    with connections() as (ledger, items, _index):
        return bundle.library(ledger, items, as_of or None)


@mcp.tool()
def thesis_bundles(view_ids: list[str], as_of: str = '') -> dict:
    """Complete UI inputs for selected thesis ids: dated states, assessments, sources, evidence and relationships.
    Pass this envelope to the frontend's fromBundles adapter. Read-only; does not call a model."""
    with connections() as (ledger, items, _index):
        return bundle.thesis_bundles(ledger, items, view_ids, as_of or None)


@mcp.tool()
def search(query: str, k: int = 10, as_of: str = '', include_closed: bool = False) -> dict:
    """Top-k views for an idea or sentence: id, object, kind, what it looks at, the question, due day, dependencies
    (the views it is judged after) and dependants, with the score and its parts. Views, never evidence: evidence is
    anchored under its view."""
    with connections() as (ledger, _items, index):
        return search_module.search(ledger, index, query, k, as_of or None, include_closed, aliases=ALIASES, semantic=not ARGS.lexical)


@mcp.tool()
def views(object: str = '', as_of: str = '', include_closed: bool = False) -> list:
    """The views of one object (a ticker like NVDA or a theme id like ai-capex), or all views, as of a day."""
    with connections() as (ledger, _items, _index):
        return service.views(ledger, object or None, as_of or None, include_closed)


@mcp.tool()
def view(view_id: str, as_of: str = '') -> dict:
    """One view as of a day: the question, the ladder (positions 1..5, position 1 the most bullish outcome; or 2 for
    yes/no), the judged position with its label and condition and since when, whether open, dependencies and
    dependants, counts of rounds, evidence and facts."""
    with connections() as (ledger, _items, _index):
        record = service.view(ledger, view_id, as_of or None)
    if record is None:
        raise ValueError(f'no view {view_id} as of {as_of or "the last completed day"}')
    return record


@mcp.tool()
def history(view_id: str, from_day: str = '', to_day: str = '') -> dict:
    """Every judgement round in the span (day, position, whether it changed, why, the cited evidence ids and the push
    each gave), evidence arrivals per day, position changes, replacements of guidance, open/close switches."""
    with connections() as (ledger, _items, _index):
        return service.history(ledger, view_id, from_day or None, to_day or None)


@mcp.tool()
def evidence(view_id: str, as_of: str = '', tier: str = '') -> list:
    """Evidence in force under the view as of a day: one line, the source's own words, tier (发生的事 fact, 当事人说的
    party statement, 第三方看法 third-party view, 传闻 rumour), speaker, when it arrived, its sources."""
    with connections() as (ledger, _items, _index):
        return service.evidence(ledger, view_id, as_of or None, tier or None)


@mcp.tool()
def record(view_id: str, as_of: str = '') -> dict:
    """The last check of the view on or before the day: when, by which round, how many items were processed that
    day and how much evidence arrived under the view."""
    with connections() as (ledger, _items, _index):
        return service.record(ledger, view_id, as_of or None)


@mcp.tool()
def changes(since_day: str, to_day: str = '') -> list:
    """Judgements that said 'changed' after since_day, each with the view, from/to position and the evidence cited."""
    with connections() as (ledger, _items, _index):
        return service.changes(ledger, since_day, to_day or None)


@mcp.tool()
def evaluate(view_id: str, comparator: str, value_usd: float, as_of: str = '') -> dict:
    """A claim against a view's ladder: 'the quantity >= / < / = value_usd'. Returns the ladder position the
    threshold sits in, the judged position, and the verdict: holds (the judged band is wholly on the claim's side),
    not_yet (wholly on the other side) or borderline (the threshold cuts through the judged band)."""
    with connections() as (ledger, _items, _index):
        answer = service.evaluate(ledger, view_id, comparator, value_usd, as_of or None)
    if answer is None:
        raise ValueError(f'no view {view_id} as of {as_of or "the last completed day"}')
    return answer


if __name__ == '__main__':
    mcp.run(transport=ARGS.transport)
