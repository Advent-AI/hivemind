"""The D750 $0 writer test (SMALL-DESIGN.md §5 [D750]): blind5's design, unchanged, on the request with council 65's bullet-2 sentence
("it remains a forecast when reaffirmed, and is taken in full only when you show what evidence puts the required volume in hand for the
period"). Cases S, E and P-v8; a fresh Claude and Codex writer each; the same two reader controls; the same tally.

  python3 blind6.py build|check|packets|tally <out>
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import blind5  # noqa: E402

blind5.REQUEST_SHA256 = '54f5847d715caec159e6509b7966c13df4d4af0756953d206fefa1347879f397'   # judging-v13s.txt as registered (D750)
blind5.READER_BRIEF = blind5.READER_BRIEF.replace('writer test, D749', 'writer test, D750')
if 'D750' not in blind5.READER_BRIEF:
    raise SystemExit('the D750 reader brief is not built')

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) == 3 else ''
    target = Path(sys.argv[2]).resolve() if len(sys.argv) == 3 else None
    {'build': blind5.build, 'check': blind5.check, 'packets': blind5.packets, 'tally': blind5.tally}.get(
        cmd, lambda _: (_ for _ in ()).throw(SystemExit(__doc__)))(target)
