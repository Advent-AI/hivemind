"""Which later week of news has never been sent by any run or probe? ($0; D549.) For each candidate week the articles are listed
through both systems' own entries, as `fresh_week_inputs.py` does for the fresh week (the production replay's routing on an empty
store, and the clean runner's selection rule; the two lists must be the same). Then every stored file under the data, clean-path
and research folders is searched for each article id. A file that is a copy of the source articles, or a list of ids written by
this census or by the fresh-week preparation, is not a send; anything else is counted as one and named.

  python3 exposure_census.py
"""
import collections
import json
import mmap
import re
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).parent
sys.path[:0] = [str(HERE.parent)]
import fresh_week_inputs as week_inputs  # noqa: E402

WEEKS = [('2026-09-29', '2026-10-05'), ('2026-10-06', '2026-10-12'), ('2026-10-13', '2026-10-19'), ('2026-10-20', '2026-10-26')]
SEARCHED = ['poc/data', 'clean-arch', 'docs/research']
NOT_A_SEND = ('poc/data/items-', '.page.sqlite', 'docs/research/2026-11-14-use-acceptance/fresh-articles-2026-09-22-10-05', 'docs/research/2026-11-14-use-acceptance/second-week/',
              'fresh-week-manifest.json')


def week_list(start, end):
    week_inputs.FROM, week_inputs.UNTIL = start, end
    return week_inputs.production_list()


def main():
    lists = {week: week_list(*week) for week in WEEKS}
    ids = sorted({article for articles in lists.values() for article in articles})
    wanted = {article.encode() for article in ids}
    prefixes = sorted({article.split(':', 1)[0] for article in ids})
    shape = re.compile(b'(?:' + b'|'.join(re.escape(prefix.encode()) for prefix in prefixes) + rb'):[0-9A-Za-z_\-\.]{6,120}')
    found, files, scanned_bytes = collections.defaultdict(set), 0, 0
    for folder in SEARCHED:
        for path in (ROOT / folder).rglob('*'):
            relative = str(path.relative_to(ROOT))
            if not path.is_file() or path.is_symlink() or any(mark in relative for mark in NOT_A_SEND) or path.stat().st_size == 0:
                continue
            files += 1
            scanned_bytes += path.stat().st_size
            with open(path, 'rb') as handle, mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as data:
                for match in shape.finditer(data):
                    token = match.group(0)
                    if token in wanted:
                        found[token.decode()].add(relative)
                    elif token[:30] in wanted or any(token.startswith(candidate) for candidate in ()):      # an id followed by more id-like characters: not a match
                        pass
    print(f'files searched: {files}; {scanned_bytes / 1e9:.1f} GB; id prefixes: {prefixes}')
    out = {'searched': SEARCHED, 'not_counted_as_a_send': list(NOT_A_SEND), 'weeks': {}}
    for week, articles in lists.items():
        sent = {article: sorted(found[article]) for article in articles if found[article]}
        senders = collections.Counter(path.split('/')[2] if path.startswith('poc/data/') else '/'.join(path.split('/')[:3]) for paths in sent.values() for path in paths)
        out['weeks']['..'.join(week)] = {'eligible_articles': len(articles), 'never_sent': len(articles) - len(sent), 'sent_before': len(sent), 'sent_by': dict(senders.most_common(8)),
                                         'articles_in_order': articles, 'sent_articles': sent}
        print(f"{week[0]}..{week[1]}: eligible {len(articles)}, never sent {len(articles) - len(sent)}, sent before {len(sent)}; by {dict(senders.most_common(5))}")
    (HERE / 'exposure-census.json').write_text(json.dumps(out, indent=1) + '\n')


def lists_index(ids, _cache={}):
    if 'set' not in _cache:
        _cache['set'] = set(ids)
    return _cache['set']


if __name__ == '__main__':
    main()
