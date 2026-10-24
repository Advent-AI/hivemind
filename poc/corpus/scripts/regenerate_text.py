"""Rebuild the whole-page text (<name>.full.txt) from every raw HTML file already on disk, offline, so the test
database carries the original page as text with nothing cut. Run after the harvesters, or any time page_text changes.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import RAW, decode, page_text, log, main_guard  # noqa: E402

FOLDERS = ('pages', 'nvidianews', 'nvblog', 'extra')


def run():
    counts = {}
    for folder in FOLDERS:
        base = os.path.join(RAW, folder)
        if not os.path.isdir(base):
            continue
        n = 0
        for name in os.listdir(base):
            if not name.endswith('.html'):
                continue
            path = os.path.join(base, name)
            with open(path, 'rb') as handle:
                markup = decode(handle.read())
            with open(path[:-5] + '.full.txt', 'w', encoding='utf-8') as handle:
                handle.write(page_text(markup))
            n += 1
        counts[folder] = n
    edgar = os.path.join(RAW, 'edgar')
    n = 0
    if os.path.isdir(edgar):
        for accession in os.listdir(edgar):
            folder = os.path.join(edgar, accession)
            if not os.path.isdir(folder):
                continue
            for name in os.listdir(folder):
                if name.lower().endswith(('.htm', '.html')):
                    with open(os.path.join(folder, name), 'rb') as handle:
                        markup = decode(handle.read())
                    with open(os.path.join(folder, name + '.full.txt'), 'w', encoding='utf-8') as handle:
                        handle.write(page_text(markup))
                    n += 1
    counts['edgar'] = n
    log('full text regenerated:', counts)


if __name__ == '__main__':
    main_guard(run)
