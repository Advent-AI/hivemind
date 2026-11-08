"""Forward simulation of Step 2 over the stored Step 1 items, in article order, with the library each decision would really see.

For each article, every item searches the library as it stands after all earlier articles (records merged away are gone; a record
keeps its first item's text): R1, one query per {thesis, evidence} association, top 10, union of the associations. Jev answers the
production question (J0) for each candidate. Precedence: any same_statement → the item is merged away, its source and any missing thesis
link added to every matched record; else any supersedes → a new record linked as a later version; else a new record. Items of one
article never see each other.

Usage: forward_sim.py <folder> [--dry-run]"""
import concurrent.futures, hashlib, json, math, sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jev_compare  # noqa: E402
from jev_compare import jev, model  # noqa: E402

TOP = 10


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)) or 1)


def main():
    folder = Path(sys.argv[1])
    dry = '--dry-run' in sys.argv
    items = json.loads((folder / 'items.json').read_text())
    by_key = {it['key']: it for it in items}
    cache = json.loads((folder / 'embeddings.json').read_text())
    articles = sorted({it['article'] for it in items})
    library = {}   # record key (its first item) → {'sources': [...], 'theses': [...], 'later_version_of': [...]}
    decisions = []
    archive = None if dry else model.Archive(str(folder / 'forward-sim.sqlite'))
    cfg = SimpleNamespace(provider='jev', version='step2-forward-J0', checksum=hashlib.sha256(b'forward-J0').hexdigest()[:16])
    questions_sent = 0
    for article in articles:
        incoming = [it for it in items if it['article'] == article]
        jobs = []
        for it in incoming:
            candidates = []
            for thesis in it['theses']:
                ranked = sorted(library, key=lambda k: -cosine(cache[f"q1:{it['key']}:{thesis['id']}"], cache[f"doc:{k}"]))[:TOP]
                candidates += [k for k in ranked if k not in candidates]
            jobs.append((it, candidates))
        def ask(job):
            it, candidates = job
            if not candidates or dry:
                return it, candidates, {}
            questions = {f'q{i}': jev_compare.question('J0', by_key[k]) for i, k in enumerate(candidates)}
            answer = jev.ask(archive, cfg, jev_compare.SETTING, jev_compare.j0_state(it), questions, 'step2_forward_J0')
            return it, candidates, {k: answer.data[f'q{i}']['choice'] for i, k in enumerate(candidates)}
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(ask, jobs))
        for it, candidates, choices in results:
            questions_sent += len(candidates)
            same = [k for k in candidates if choices.get(k) == 'same_statement']
            later = [k for k in candidates if choices.get(k) == 'supersedes']
            thesis_ids = [t['id'] for t in it['theses']]
            if same:
                for k in same:
                    library[k]['sources'].append(it['key'])
                    library[k]['theses'] += [t for t in thesis_ids if t not in library[k]['theses']]
                outcome = 'merged'
            else:
                library[it['key']] = {'sources': [it['key']], 'theses': thesis_ids, 'later_version_of': later}
                outcome = 'later_version' if later else 'new'
            decisions.append({'key': it['key'], 'article': article, 'outcome': outcome, 'candidates': candidates, 'choices': choices,
                              'merged_into': same, 'later_version_of': later})
    print(f'items {len(items)}; questions {questions_sent}; about ${questions_sent * 450 / 1e6 * model.PRICES[jev_compare.SETTING.model][0]:.3f} at the Jev rate'
          if dry else f'items {len(items)}; library records {len(library)}; merged {sum(d["outcome"] == "merged" for d in decisions)}; '
          f'later versions {sum(d["outcome"] == "later_version" for d in decisions)}; questions {questions_sent}')
    if not dry:
        (folder / 'forward-sim.json').write_text(json.dumps({'decisions': decisions, 'library': library}, indent=1))


if __name__ == '__main__':
    main()
