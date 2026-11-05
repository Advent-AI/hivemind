"""Write read-only Codex check prompts for one reader's records, split into N ranges balanced by the log's bytes.
usage: python3 split_verify.py <records.jsonl> <prefix> <parts>"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_verify_prompts as mv
source, prefix, count = sys.argv[1], sys.argv[2], int(sys.argv[3])
text = mv.LOG.read_text(encoding='utf-8')
heads = [(m.start(), m.group(1)) for m in re.finditer(r'^## (D\d+) ', text, re.M)]
sizes = {d: (heads[i + 1][0] if i + 1 < len(heads) else len(text)) - s for i, (s, d) in enumerate(heads)}
records = [json.loads(l) for l in Path(source).read_text(encoding='utf-8').splitlines() if l.strip()]
total = sum(sizes[r['id']] for r in records); parts, cur, acc = [], [], 0
for r in records:
    cur.append(r); acc += sizes[r['id']]
    if acc >= total / count * (len(parts) + 1) and len(parts) < count - 1:
        parts.append(cur); cur = []
parts.append(cur)
for n, part in enumerate(parts):
    name = f'verify-{prefix}{"abcdefgh"[n]}'
    Path(f'{name}.prompt.txt').write_text(mv.INSTRUCTIONS + ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in part), encoding='utf-8')
    print(f'{name}: {part[0]["id"]}..{part[-1]["id"]} ({len(part)} records, {sum(sizes[r["id"]] for r in part)/1e3:.0f} KB of log)')
