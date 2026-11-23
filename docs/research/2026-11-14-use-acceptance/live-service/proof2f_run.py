"""Proof 2f's runner (OPERATING-CONTRACT.md, row 3; council round 142): builds the two check pages with `poc/ui/verify-live-day.mjs`,
serves `poc/` on a local port and loads each page in headless Chrome, which runs its checks on load; prints each page's outcome and
exits 1 unless both passed.

  python3 proof2f_run.py [poc folder]
"""
import html
import re
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'


def free_port():
    probe = socket.socket()
    probe.bind(('127.0.0.1', 0))
    port = probe.getsockname()[1]
    probe.close()
    return port


def main(arguments):
    poc = Path(arguments[0]) if arguments else ROOT / 'poc'
    built = subprocess.run(['node', str(poc / 'ui' / 'verify-live-day.mjs')], capture_output=True, text=True)
    print(built.stdout.strip() or built.stderr.strip()[-500:])
    if built.returncode != 0:
        return 1
    port = free_port()
    server = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=poc,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    failed = False
    try:
        for name in ('a', 'b'):
            with tempfile.TemporaryDirectory() as profile:
                dom = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', f'--user-data-dir={profile}',
                                      '--virtual-time-budget=30000', '--dump-dom', f'http://127.0.0.1:{port}/ui/dist/live-day-check-{name}.html'],
                                     capture_output=True, text=True, timeout=240).stdout
            found = re.search(r'<pre id="live-day-result">(.*?)</pre>', dom, re.S)
            outcome = html.unescape(found.group(1)) if found else 'no outcome on the page'
            print(f'case {name.upper()}: {outcome}')
            failed |= not outcome.startswith('Passed')
    finally:
        server.terminate()
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
