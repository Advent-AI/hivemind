"""D130: the agent's read-only HTTP/MCP bundle is the complete Thesis UI input."""
import asyncio
import json
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import bundle, service  # noqa: E402
from hivemind.views import store  # noqa: E402

LEDGER = ROOT / 'poc/data/sealed-2026-10-24-run3-through-0815/views.sqlite'
ITEMS = ROOT / 'poc/data/items-window.sqlite'


def assert_payload(payload):
    assert payload['as_of'] == '2026-08-15'
    assert payload['days'][-1] == '2026-08-15'
    assert [view['view_id'] for view in payload['views']] == ['v3', 'v1']
    for view in payload['views']:
        assert all(j['id'] and j['day'] <= payload['as_of'] for j in view['judgements'])
        assert all(e['arrival_day'] <= payload['as_of'] for e in view['evidence'])
        assert all(s['day'] <= payload['as_of'] for s in view['switches'])


def test_bundle_selection_is_dated_deduplicated_and_read_only():
    ledger, items = service.open_ledger(str(LEDGER)), store.open_read_only(str(ITEMS))
    try:
        assert_payload(bundle.thesis_bundles(ledger, items, ['v3', 'v1', 'v3'], '2026-08-15'))
        assert ledger.total_changes == 0
        with pytest.raises(KeyError):
            bundle.thesis_bundles(ledger, items, ['v16'], '2026-07-23')
        with pytest.raises(ValueError):
            bundle.thesis_bundles(ledger, items, [], '2026-08-15')
        with pytest.raises(ValueError):
            bundle.thesis_bundles(ledger, items, ['v3'], '2026-02-30')
    finally:
        items.close()
        ledger.close()


def test_http_bundle_endpoint_as_the_agent_calls_it(tmp_path):
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    process = subprocess.Popen(
        [sys.executable, str(ROOT / 'scripts/hivemind_api.py'), '--port', str(port), '--lexical',
         '--config', '', '--index', str(tmp_path / 'index.sqlite'), '--archive', str(tmp_path / 'archive.sqlite')],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        url = f'http://127.0.0.1:{port}/thesis-bundles?ids=v3,v1&as_of=2026-08-15'
        for attempt in range(40):
            try:
                with urllib.request.urlopen(url, timeout=5) as response:
                    assert_payload(json.load(response))
                break
            except (urllib.error.URLError, ConnectionError):
                if attempt == 39:
                    raise
                time.sleep(0.05)
        with pytest.raises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(f'http://127.0.0.1:{port}/thesis-bundles?ids=missing', timeout=5)
        assert error.value.code == 404
    finally:
        process.terminate()
        process.wait(timeout=10)


def test_mcp_bundle_tool_as_the_agent_calls_it(tmp_path):
    async def run():
        params = StdioServerParameters(command=sys.executable, args=[
            str(ROOT / 'scripts/hivemind_mcp.py'), '--lexical', '--index', str(tmp_path / 'index.sqlite'),
        ])
        async with stdio_client(params) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                await session.initialize()
                result = await session.call_tool('thesis_bundles', {'view_ids': ['v3', 'v1'], 'as_of': '2026-08-15'})
                assert not result.isError
                payload = result.structuredContent or json.loads(result.content[0].text)
                assert_payload(payload)
    asyncio.run(run())
