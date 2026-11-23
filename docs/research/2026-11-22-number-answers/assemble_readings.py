"""The blind reading step of the judging-v13 paid gate (PAID-GATE.md §4): split packets.md into reader batches, list the
disagreements between readers A and B for a third reader, and assemble the readings file that `paid_gate.py verdict` seals.

Usage:
  python3 assemble_readings.py split <packets.md> <out folder> <batches>
  python3 assemble_readings.py third <packets.md> <reader A json> <reader B json> <out prompt file>
  python3 assemble_readings.py assemble <packets.md> <reader A json> <reader B json> <third json or -> <out readings json>
  python3 assemble_readings.py split-exact <packets.md> <out folder> <batches> <brief.md>        # D753: the exact file in every batch
  python3 assemble_readings.py third-exact <packets.md> <reader A json> <reader B json> <out prompt file> <brief.md>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUESTIONS = ('usable', 'contradiction', 'internal_reference', 'deciding_gap')


def sections(text):
    """The packets in order: [(pid, section text)], each section starting at its '## P..' line."""
    found = list(re.finditer(r'^## (P\d+)\n', text, re.M))
    return [(m.group(1), text[m.start():(found[i + 1].start() if i + 1 < len(found) else len(text))]) for i, m in enumerate(found)]


def read_json(path):
    """A reader's answer: the outermost JSON object in the file (fences and prose around it are ignored)."""
    text = Path(path).read_text()
    start, end = text.find('{'), text.rfind('}')
    if start < 0 or end < start:
        raise SystemExit(f'{path}: no JSON object')
    return json.loads(text[start:end + 1])


def split(packets_path, out, batches):
    text = Path(packets_path).read_text()
    parts = sections(text)
    brief = (HERE / 'reader-brief-v13.md').read_text()
    out.mkdir(parents=True, exist_ok=False)
    size = -(-len(parts) // batches)
    for b in range(batches):
        chunk = parts[b * size:(b + 1) * size]
        if chunk:
            (out / f'batch-{b + 1}.md').write_text(brief + '\n\n# Packets\n\n' + ''.join(s for _, s in chunk))
            print(f'batch-{b + 1}: {", ".join(p for p, _ in chunk)} ({sum(len(s) for _, s in chunk)} chars)')


def split_exact(packets_path, out, batches, brief_path):
    """[D753, council 70] Every reader batch carries the exact packets.md, unchanged (its key-commitment line included), and names
    separately the packets that batch must answer, so the text the readers receive is the text whose sha256 the readings carry."""
    text = Path(packets_path).read_text()
    ids = [pid for pid, _ in sections(text)]
    brief = Path(brief_path).read_text()
    out.mkdir(parents=True, exist_ok=False)
    size = -(-len(ids) // batches)
    for b in range(batches):
        chunk = ids[b * size:(b + 1) * size]
        if chunk:
            (out / f'batch-{b + 1}.md').write_text(
                brief + '\n\n# Your packets\n\nAnswer only these packets, every card of each: ' + ', '.join(chunk)
                + '. The file below holds all packets; leave the others.\n\n# The packets file (exact)\n\n' + text)
            print(f'batch-{b + 1}: {", ".join(chunk)}')


def third_exact(packets_path, a_path, b_path, out, brief_path):
    """[D753, council 70] The third reading with the exact packets.md and the two readings of each disputed question."""
    text = Path(packets_path).read_text()
    a, b = read_json(a_path), read_json(b_path)
    rows = disagreements(a, b)
    lines = [Path(brief_path).read_text(), '\n# Third reading\n',
             'Two readers disagreed on the questions listed below. For each one, read that packet in the file below and both readings, '
             'and give your own answer (yes or no) with a ground naming an id of that packet. Return only JSON: '
             '{"P01": {"K1": {"usable": {"answer": "...", "ground": "..."}}}} with exactly the listed packet, card and question keys.\n']
    for pid, card, q in rows:
        lines.append(f'Disagreement: {pid} {card} {q}\n  Reader 1: {json.dumps(a[pid][card][q], ensure_ascii=False)}\n'
                     f'  Reader 2: {json.dumps(b[pid][card][q], ensure_ascii=False)}\n')
    lines.append('\n# The packets file (exact)\n\n' + text)
    Path(out).write_text('\n'.join(lines))
    print(f'{len(rows)} disagreements in {len({r[0] for r in rows})} packets')


def disagreements(a, b):
    return sorted((pid, card, q) for pid in a for card in a[pid] for q in QUESTIONS
                  if a[pid][card].get(q, {}).get('answer') != b.get(pid, {}).get(card, {}).get(q, {}).get('answer'))


def third(packets_path, a_path, b_path, out):
    text = Path(packets_path).read_text()
    by_pid = dict(sections(text))
    a, b = read_json(a_path), read_json(b_path)
    rows = disagreements(a, b)
    brief = (HERE / 'reader-brief-v13.md').read_text()
    lines = [brief, '\n# Third reading\n',
             'Two readers disagreed on the questions listed below. For each one, read the packet and both readings, and give your own '
             'answer (yes or no) with a ground naming an id of that packet. Return only JSON: '
             '{"P01": {"K1": {"usable": {"answer": "...", "ground": "..."}}}} with exactly the listed packet, card and question keys.\n']
    for pid in sorted({r[0] for r in rows}):
        lines.append(by_pid[pid])
        for _, card, q in [r for r in rows if r[0] == pid]:
            lines.append(f'Disagreement: {pid} {card} {q}\n  Reader 1: {json.dumps(a[pid][card][q], ensure_ascii=False)}\n'
                         f'  Reader 2: {json.dumps(b[pid][card][q], ensure_ascii=False)}\n')
    Path(out).write_text('\n'.join(lines))
    print(f'{len(rows)} disagreements in {len({r[0] for r in rows})} packets')


def assemble(packets_path, a_path, b_path, third_path, out):
    data = Path(packets_path).read_bytes()
    a, b = read_json(a_path), read_json(b_path)
    t = read_json(third_path) if third_path != '-' else {}
    readings = {}
    for pid in sorted(set(a) | set(b)):
        readings[pid] = {}
        for card in sorted(set(a.get(pid, {})) | set(b.get(pid, {}))):
            entry = {'A': a.get(pid, {}).get(card, {}), 'B': b.get(pid, {}).get(card, {})}
            if t.get(pid, {}).get(card):
                entry['third'] = t[pid][card]
            readings[pid][card] = entry
    Path(out).write_text(json.dumps({'packets_sha256': hashlib.sha256(data).hexdigest(), 'packets': readings}, indent=1, ensure_ascii=False))
    print(f'{len(readings)} packets assembled; {len(disagreements(a, b))} disagreements, {sum(len(v) for v in t.values())} cards with a third reading')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'split' and len(sys.argv) == 5:
        split(sys.argv[2], Path(sys.argv[3]), int(sys.argv[4]))
    elif cmd == 'third' and len(sys.argv) == 6:
        third(*sys.argv[2:6])
    elif cmd == 'split-exact' and len(sys.argv) == 6:                      # D753: the exact file, the batch's packets named
        split_exact(sys.argv[2], Path(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
    elif cmd == 'third-exact' and len(sys.argv) == 7:
        third_exact(*sys.argv[2:7])
    elif cmd == 'assemble' and len(sys.argv) == 7:
        assemble(*sys.argv[2:7])
    else:
        raise SystemExit(__doc__)
