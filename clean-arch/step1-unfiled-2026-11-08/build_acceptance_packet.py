"""Write the readers' source packet for the acceptance set (no model calls): every article of the manifest, in manifest order, with
its id, title, publisher, publication day and the exact text the runner sends. The packet holds no system output.

Usage: build_acceptance_packet.py <manifest.json> <packet.json>"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/step1')]
import runner  # noqa: E402


def main():
    manifest = json.loads(Path(sys.argv[1]).read_text())
    items = runner.selected_items(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite', manifest)
    packet = [{'id': item['input_id'], 'title': item['title'], 'publisher': item['publisher'],
               'publication_date': item['publication_day'], 'text': item['text']} for item in items]
    Path(sys.argv[2]).write_text(json.dumps(packet, ensure_ascii=False, indent=1))
    print(f'{len(packet)} articles, {sum(len(a["text"]) for a in packet)} characters of text')


if __name__ == '__main__':
    main()
