"""The topics a finished first step opened, each with the id of its opening article and that article's exposure class
(DESIGN.md section 2). The id comes from the request of the trace row that opened the topic, through the topic builder's own
function, not from matching texts. $0; reads a trace that is no longer live.

  python3 topics_with_opening_articles.py <folder holding the trace> <trace file name> <label> <output json>
"""
import json
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / 'clean-arch/step4-2026-11-10/census'), str(ROOT / 'clean-arch/step4-2026-11-10/stage_a')]
import build_cases  # noqa: E402
import build_packet  # noqa: E402


def main(folder, trace_name, label, output):
    seen_before = set(json.loads((HERE / 'exposed-2026-10-06-10-12.json').read_text())['seen_before'])
    bounds = json.loads((HERE / 'exposure-bounds.json').read_text())
    flagged = set(bounds['flagged_shown_in_source_page_review']) | {
        article for article, twins in bounds['flagged_twin_seen_before'].items()
        if any(not all('reflection-2/cold-codex' in path for path in twin['seen_in']) for twin in twins.values())}
    week = set(json.loads((HERE / 'manifest-2026-10-06-10-12.json').read_text())['item_ids'])
    opened = build_cases.opened_count(folder, [trace_name])
    topics = []
    for entry in build_packet.theses_of(label, [trace_name], draws=folder, expected=opened):
        article = entry['article']['id']
        if article not in week:
            raise SystemExit(f"{entry['id']}: its opening article {article} is not an article of the week")
        exposure = 'seen before' if article in seen_before else 'flagged' if article in flagged else 'not found in the search'
        topics.append({'case': f"{label}/{entry['id']}", 'opening_article': article, 'day': entry['article']['publication_date'],
                       'title': entry['article']['title'], 'exposure': exposure, 'description': entry['thesis']['description'],
                       'outcome': entry['thesis']['outcome']})
    counts = {name: sum(1 for topic in topics if topic['exposure'] == name) for name in ('seen before', 'flagged', 'not found in the search')}
    Path(output).write_text(json.dumps({'topics': topics, 'counts': counts, 'wider_count': counts['flagged'] + counts['not found in the search'],
                                        'strict_count': counts['not found in the search']}, indent=1, ensure_ascii=False) + '\n')
    print(f"topics {len(topics)}: {counts}; wider count {counts['flagged'] + counts['not found in the search']}, strict count {counts['not found in the search']}")
    for topic in topics:
        print(f"  {topic['case']} | {topic['day']} | {topic['exposure']} | {topic['description'][:120]}")
    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:5]))
