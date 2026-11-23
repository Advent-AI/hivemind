"""Rows written before a kind was stored, as the product's readers show them ($0; council round 32).

For every stored ledger that holds dependency rows: what the service (`service.dependencies`, `service.dependants`, which the
library bundle, the search records and the idea route are built on) shows for each question, beside the reading relation of the
separation candidate (`separated_edges`). For a `reads` row the two must agree: the product's "depends on" is the reading. For a
`supports` row they are opposite: the service shows the driver as depending on the root, the candidate has the root read the driver.

  python3 old_rows_readers.py
"""
import collections
import json
import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).parent
sys.path[:0] = [str(ROOT / 'src'), str(HERE)]
from hivemind import service  # noqa: E402
from hivemind.views import store  # noqa: E402
import separated_edges  # noqa: E402


def main():
    counts, ledgers = collections.Counter(), collections.Counter()
    separated_edges._ORIGINAL.update(dependencies_of=store.dependencies_of, dependants_of=store.dependants_of, direct_parents=store.direct_parents)   # the seam's own readers, nothing installed
    for folder, _, files in os.walk(ROOT / 'poc/data'):
        for name in files:
            if not (name.endswith('.sqlite') and 'views' in name):
                continue
            conn = sqlite3.connect(f'file:{Path(folder) / name}?mode=ro', uri=True)
            conn.row_factory = sqlite3.Row
            if not conn.execute("select 1 from sqlite_master where name = 'dependencies'").fetchone() or not conn.execute('select 1 from dependencies limit 1').fetchone():
                continue
            kinds = {separated_edges.kind_of(conn, dict(row)) for row in conn.execute('select * from dependencies')}
            ledgers['+'.join(sorted(kinds))] += 1
            for (view,) in conn.execute('select view_id from views').fetchall():
                shown = sorted(dep['view_id'] for dep in service.dependencies(conn, view, '2099-12-31') if dep['view_id'])
                shown_back = service.dependants(conn, view, '2099-12-31')
                reads = sorted(dep['resolved_to'] for dep in separated_edges.reading_dependencies_of(conn, view) if dep['resolved_to'])
                read_by = separated_edges.reading_dependants_of(conn, view)
                if not shown and not shown_back and not reads and not read_by:
                    continue
                family = 'reads' if kinds == {'reads'} else 'supports' if kinds == {'supports'} else 'mixed'
                counts[(family, 'the service shows what the candidate reads' if (shown, shown_back) == (reads, read_by) else
                        'the service shows the opposite of what the candidate reads' if (shown, shown_back) == (read_by, reads) else 'neither')] += 1
    out = {'ledgers_by_kinds_held': dict(ledgers), 'questions_with_an_edge': {f'{family}: {verdict}': count for (family, verdict), count in sorted(counts.items())}}
    (HERE / 'old-rows-readers.json').write_text(json.dumps(out, indent=1) + '\n')
    print(out)


if __name__ == '__main__':
    main()
