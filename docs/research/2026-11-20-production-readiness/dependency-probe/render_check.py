"""$0 check (Alex's A, 2026-11-20): what a Data Center question's judging request would show if it read the total-revenue
question's conclusion through a dependency. Works on scratch copies; the finished stores are opened read-only and never written."""
import json, sqlite3, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / 'src'))
from hivemind.views import judging

PAIRS = {'old-1': ('v8', 'v4'), 'old-2': ('v9', 'v14'), 'old-3': ('v35', 'v3')}  # (Data Center FY2027, total revenue FY2027)
scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
report = {}
for draw, (data_center, total) in PAIRS.items():
    source = sqlite3.connect(f'file:{REPO}/poc/data/comparison-2026-11-17/run/{draw}/prod/views.sqlite?mode=ro', uri=True)
    copy_path = scratch / f'{draw}-views.sqlite'
    copy_path.unlink(missing_ok=True)
    copy = sqlite3.connect(copy_path)
    source.backup(copy)
    source.close()
    copy.row_factory = sqlite3.Row
    last_seq = copy.execute('select max(seq) from judgements').fetchone()[0]
    copy.execute("insert into dependencies(view_id, depends_on, wait_chain_view_id, wait_year, direction, seq) values (?, ?, '', '', 'first_is_bullish', ?)",
                 (data_center, total, last_seq))
    copy.commit()
    _system, user = judging.build_prompt(copy, data_center, 'judging-v7')
    block = user.split('[Current conclusions of the theses it depends on]')[1].split('\n\n')[0].strip()
    total_reasons = copy.execute('select reasons from judgements where view_id=? order by judgement_id desc limit 1', (total,)).fetchone()[0]
    report[draw] = {'data_center': data_center, 'total': total, 'block_chars': len(block), 'total_reasons_chars': len(total_reasons),
                    'cut_at_600': len(total_reasons) > 600, 'shown': block, 'cut_off': total_reasons[600:]}
    copy.close()
print(json.dumps(report, indent=1, ensure_ascii=False))
