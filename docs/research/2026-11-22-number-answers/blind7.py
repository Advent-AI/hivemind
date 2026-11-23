"""The D751 $0 writer test (SMALL-DESIGN.md §5 [D751]): D750's design and tally (blind5.py, with council 66's premise rules),
unchanged, on the request with council 68's line-9 wording ("weigh the plausible alternatives for any unknown fact that decides the
band. Explain whether the evidence as a whole favours one band before deciding whether or how much to adjust"). Cases S, E and P-v8;
a fresh Claude and Codex writer each; the same two reader controls. Council 67's exit rule: a settled failure or persistent split
ends this wording loop and returns the publication choice to Alex.

  python3 blind7.py build|check|packets|tally <out>
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import blind5  # noqa: E402

blind5.REQUEST_SHA256 = '080a00128c5b0106edf42fcdd6a357186276be9a074976246a6897246f3258b0'   # judging-v13s.txt as registered (D751)
blind5.READER_BRIEF = blind5.READER_BRIEF.replace('writer test, D749', 'writer test, D751')
if 'D751' not in blind5.READER_BRIEF:
    raise SystemExit('the D751 reader brief is not built')

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) == 3 else ''
    target = Path(sys.argv[2]).resolve() if len(sys.argv) == 3 else None
    {'build': blind5.build, 'check': blind5.check, 'packets': blind5.packets, 'tally': blind5.tally}.get(
        cmd, lambda _: (_ for _ in ()).throw(SystemExit(__doc__)))(target)
