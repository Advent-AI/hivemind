"""Build or check the "Forecast unavailable" release package (docs/research/2026-11-22-number-answers/RELEASE-BUILD.md).

    release_build.py build --ledger <views.sqlite> --items <items.sqlite> [--as-of YYYY-MM-DD] --out <folder>
    release_build.py check <folder> --ledger <views.sqlite> --items <items.sqlite>

No model or network call; both stores are read only. The package is checked in a private staging folder against the stores before
one atomic move publishes it, and neither the package nor the report ever replaces an existing path. Exit statuses: 0 done; 1
refused, with nothing published by this command; 2 the package is published (build) or passes (check) but the report name is taken
or the report could not be written.
"""
import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import release, service  # noqa: E402
from hivemind.views import store  # noqa: E402


def report_path(out):
    return out.with_name(out.name + '.report.json')


def write_report(report, path):
    """Print the report, then publish it: 0 when it is published (naming any temporary file left behind), 2 when it is not."""
    print(json.dumps(report, ensure_ascii=False, indent=1))
    try:
        leftover = release.publish_report(report, path)
    except OSError as error:
        print(f'report not written ({error}); run check to write it', file=sys.stderr)
        return 2
    print(f'report: {path}')
    if leftover:
        print(f'report published; its temporary file {leftover} could not be removed', file=sys.stderr)
    return 0


def build(args):
    out = Path(args.out).absolute()
    report = report_path(out)
    for path in (out, report):
        if os.path.lexists(path):
            print(f'refused: {path} exists', file=sys.stderr)
            return 1
    started = time.monotonic()
    staged = views_db = items_db = None
    try:
        views_db = service.open_ledger(str(release.store_path(args.ledger)))
        items_db = store.open_read_only(str(release.store_path(args.items)))
        bound = release.resolve(views_db, args.as_of)
        staged = release.stage(out)
        data = release.release_export(views_db, items_db, bound)
        export_seconds = time.monotonic() - started
        release.write_package(data, staged)
        checked = time.monotonic()
        counts, data, size = release.check_package(staged, views_db, items_db, expected_as_of=bound)
        unresolved = release.withheld_unresolved(views_db, data)
        check_seconds = time.monotonic() - checked
        release.publish(staged, out)
        staged = None                       # published: this build no longer owns the staging name
    except Exception as error:              # any failure before publication: nothing at --out from this build
        print(f'refused: {type(error).__name__}: {error}', file=sys.stderr)
        return 1
    finally:
        if staged is not None:
            shutil.rmtree(staged)
        for conn in (views_db, items_db):
            if conn is not None:
                conn.close()
    print(f'published {out}: {counts}')
    summary = {'ledger': str(args.ledger), 'items': str(args.items), 'as_of': bound, 'counts': counts,
               'withheld_unresolved': unresolved, 'data_bytes': size,
               'export_seconds': round(export_seconds, 2), 'check_seconds': round(check_seconds, 2)}
    return write_report(summary, report)


def check(args):
    out = Path(args.package).absolute()
    views_db = items_db = None
    try:
        views_db = service.open_ledger(str(release.store_path(args.ledger)))
        items_db = store.open_read_only(str(release.store_path(args.items)))
        started = time.monotonic()
        counts, data, size = release.check_package(out, views_db, items_db)
        check_seconds = time.monotonic() - started
        unresolved = release.withheld_unresolved(views_db, data)
    except Exception as error:
        print(f'refused: {type(error).__name__}: {error}', file=sys.stderr)
        return 1
    finally:
        for conn in (views_db, items_db):
            if conn is not None:
                conn.close()
    print(f'passes {out}: {counts}')
    summary = {'ledger': str(args.ledger), 'items': str(args.items), 'as_of': data['as_of'], 'counts': counts,
               'withheld_unresolved': unresolved, 'data_bytes': size,
               'export_seconds': None, 'check_seconds': round(check_seconds, 2)}
    return write_report(summary, report_path(out))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)
    make = commands.add_parser('build')
    make.add_argument('--ledger', required=True, type=Path)
    make.add_argument('--items', required=True, type=Path)
    make.add_argument('--as-of')
    make.add_argument('--out', required=True, type=Path)
    verify = commands.add_parser('check')
    verify.add_argument('package', type=Path)
    verify.add_argument('--ledger', required=True, type=Path)
    verify.add_argument('--items', required=True, type=Path)
    args = parser.parse_args(argv)
    return build(args) if args.command == 'build' else check(args)


if __name__ == '__main__':
    sys.exit(main())
