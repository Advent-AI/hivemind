#!/usr/bin/env python3
"""Render completed portions of sequential trace segments as one read-only replay."""
import argparse
import json
from pathlib import Path
from render_replay import load_trace, render


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', action='append', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--annotations')
    args = parser.parse_args()
    output = Path(args.output).resolve()
    if output in [Path(p).resolve() for p in args.source]:
        raise ValueError('output must not overwrite a trace')
    items, rows = {}, []
    for index, path in enumerate(args.source):
        segment_items, segment_rows = load_trace(path)
        items.update(segment_items)
        if index:
            previous = rows[-1] if rows else None
            first = segment_rows[0]
            if not previous or previous['status'] != 'complete' or previous['after_state'] != first['before_state']:
                raise ValueError('segment does not start from the preceding completed state')
        if index < len(args.source) - 1:
            segment_rows = [r for r in segment_rows if r['status'] == 'complete']
        for row in segment_rows:
            row = dict(row)
            row['sequence'] = len(rows) + 1
            rows.append(row)
    annotations = json.loads(Path(args.annotations).read_text()) if args.annotations else {}
    output.write_text(render(items, rows, annotations), encoding='utf-8')
    print(f'Wrote {output}: {len(rows)} article traces from {len(args.source)} segments')


if __name__ == '__main__':
    main()
