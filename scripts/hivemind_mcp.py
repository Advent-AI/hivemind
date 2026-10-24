"""The MCP front of the Hivemind service (docs/poc/service.md): one tool per call, stdio transport, every answer from
src/hivemind/service.py and search.py. Hivemind is a database with a search engine on top: the caller searches,
chooses which views to keep and how to arrange them, and reads each view's state, history and evidence. Nothing
here writes to the ledger or knows who is asking.

Usage: python3 scripts/hivemind_mcp.py [--views DB] [--index DB]
Claude Code: claude mcp add hivemind -- python3 /path/to/scripts/hivemind_mcp.py
"""
import argparse
import os
import sys

from mcp.server.fastmcp import FastMCP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import bundle, search as search_module, service  # noqa: E402
from hivemind.views import store  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument('--views', default=os.path.join(ROOT, 'poc', 'data', 'sealed-2026-10-24-run3-through-0815', 'views.sqlite'))
parser.add_argument('--index', default=os.path.join(ROOT, 'poc', 'data', 'search-index.sqlite'))
parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
parser.add_argument('--items', default=os.path.join(ROOT, 'poc', 'data', 'items-window.sqlite'))
parser.add_argument('--lexical', action='store_true', help='no embedding at all (no network): search ranks by the trigram index and says mode lexical')
parser.add_argument('--transport', choices=['stdio', 'streamable-http'], default='stdio', help='stdio for a local agent; streamable-http to serve /mcp over HTTP (Docker)')
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('--port', type=int, default=8789)
ARGS = parser.parse_args()
LEDGER = service.open_ledger(ARGS.views)
INDEX = search_module.open_index(ARGS.index)
ITEMS = store.open_read_only(ARGS.items) if os.path.exists(ARGS.items) else None
ALIASES = search_module.object_aliases(ARGS.universe)
if not ARGS.lexical:
    _embedded, _unchanged, _tokens, INDEX_ERROR = search_module.ensure_index(LEDGER, INDEX)
    if INDEX_ERROR:
        sys.stderr.write(f'hivemind: embedding stopped ({INDEX_ERROR}) after {_embedded} views; search runs lexical until the rest is built\n')

from hivemind import idea as idea_module  # noqa: E402

OBJECTS = idea_module.object_list(LEDGER, service.default_as_of(LEDGER), ALIASES)
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
def thesis_bundles(view_ids: list[str], as_of: str = '') -> dict:
    """Complete UI inputs for selected thesis ids: dated states, assessments, sources, evidence and relationships.
    Pass this envelope to the frontend's fromBundles adapter. Read-only; does not call a model."""
    return bundle.thesis_bundles(LEDGER, ITEMS, view_ids, as_of or None)


@mcp.tool()
def search(query: str, k: int = 10, as_of: str = '', include_closed: bool = False) -> dict:
    """Top-k views for an idea or sentence: id, object, kind, what it looks at, the question, due day, dependencies
    (the views it is judged after) and dependants, with the score and its parts. Views, never evidence: evidence is
    anchored under its view."""
    return search_module.search(LEDGER, INDEX, query, k, as_of or None, include_closed, aliases=ALIASES, semantic=not ARGS.lexical)


@mcp.tool()
def views(object: str = '', as_of: str = '', include_closed: bool = False) -> list:
    """The views of one object (a ticker like NVDA or a theme id like ai-capex), or all views, as of a day."""
    return service.views(LEDGER, object or None, as_of or None, include_closed)


@mcp.tool()
def view(view_id: str, as_of: str = '') -> dict:
    """One view as of a day: the question, the ladder (positions 1..5, position 1 the most bullish outcome; or 2 for
    yes/no), the judged position with its label and condition and since when, whether open, dependencies and
    dependants, counts of rounds, evidence and facts."""
    record = service.view(LEDGER, view_id, as_of or None)
    if record is None:
        raise ValueError(f'no view {view_id} as of {as_of or "the last completed day"}')
    return record


@mcp.tool()
def history(view_id: str, from_day: str = '', to_day: str = '') -> dict:
    """Every judgement round in the span (day, position, whether it changed, why, the cited evidence ids and the push
    each gave), evidence arrivals per day, position changes, replacements of guidance, open/close switches."""
    return service.history(LEDGER, view_id, from_day or None, to_day or None)


@mcp.tool()
def evidence(view_id: str, as_of: str = '', tier: str = '') -> list:
    """Evidence in force under the view as of a day: one line, the source's own words, tier (发生的事 fact, 当事人说的
    party statement, 第三方看法 third-party view, 传闻 rumour), speaker, when it arrived, its sources."""
    return service.evidence(LEDGER, view_id, as_of or None, tier or None)


@mcp.tool()
def record(view_id: str, as_of: str = '') -> dict:
    """The last check of the view on or before the day: when, by which round, how many items were processed that
    day and how much evidence arrived under the view."""
    return service.record(LEDGER, view_id, as_of or None)


@mcp.tool()
def changes(since_day: str, to_day: str = '') -> list:
    """Judgements that said 'changed' after since_day, each with the view, from/to position and the evidence cited."""
    return service.changes(LEDGER, since_day, to_day or None)


@mcp.tool()
def evaluate(view_id: str, comparator: str, value_usd: float, as_of: str = '') -> dict:
    """A claim against a view's ladder: 'the quantity >= / < / = value_usd'. Returns the ladder position the
    threshold sits in, the judged position, and the verdict: holds (the judged band is wholly on the claim's side),
    not_yet (wholly on the other side) or borderline (the threshold cuts through the judged band)."""
    answer = service.evaluate(LEDGER, view_id, comparator, value_usd, as_of or None)
    if answer is None:
        raise ValueError(f'no view {view_id} as of {as_of or "the last completed day"}')
    return answer


if __name__ == '__main__':
    mcp.run(transport=ARGS.transport)
