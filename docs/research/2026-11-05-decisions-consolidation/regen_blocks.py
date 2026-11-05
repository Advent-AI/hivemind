"""Rewrite every PRD block marked `generated` from the design page data, using docs/check.py's own renderer (run after editing
docs/system-design/new-*.js; then run python3 docs/check.py). Prints the blocks it changed."""
import sys
from pathlib import Path
sys.path.insert(0, '/Users/lchingen/hivemind/docs')
import check  # noqa: E402

data = check.run_node(check.EXTRACT)
changed = []
for (file, name), body in check.blocks(data).items():
    path = check.PRD / file
    text = path.read_text(encoding='utf-8')
    new = check.replace_block(text, name, body)
    if new is None:
        raise SystemExit(f'{file}: block {name} missing or doubled')
    if new != text:
        path.write_text(new, encoding='utf-8')
        changed.append(f'{file}#{name}')
print('rewritten:', changed or 'none')
