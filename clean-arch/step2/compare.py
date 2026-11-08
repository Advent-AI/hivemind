"""Isolated Step 2 for the clean path (PRD §5): search the entity's stored evidence for each {thesis, incoming evidence} association,
ask Jev how the incoming evidence relates to each candidate, and turn the answers into the outcome Step 3 writes.

Search: one query per association (the thesis question, then the incoming summary and passages) against each group's original record
(summary, passages, party, statement date, period), cosine similarity of embeddings, top 10; a record with no association, or one that
lists the company's figures (a condition), also gets one entity-wide query of its own text (STEP1-CONDITIONS-DESIGN.md §10.1); the union
of the results is compared. The figures never enter a search or comparison text, so a wrongly paired figure cannot change Step 2 (§14);
the comparison reads the full passages (§15). Comparison: Jev's piece question with the production criteria (views/jev_matching), the incoming piece as state, one question
per candidate. Outcome: any same_statement makes the record a repeat of the candidate with the highest same_statement probability, ties
going to the earliest group (Alex, 2026-11-08: only the group it is most like); a supersedes answer on another candidate becomes a
revision link; with no same_statement, supersedes answers make it a revision of those groups; otherwise it is new.

`forward` runs articles in order against the library as it stood after the previous article: records of one article never see each
other. A failed comparison is refused by the library, reported, and the run continues."""
import concurrent.futures
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind.views import jev_matching  # noqa: E402

TOP = 10


def stated(record):
    return record['statement_date'] or record.get('statement_date_text') or 'unknown'


def doc_text(record):
    return '\n'.join([record['summary'], ' '.join(record['passages']), f"party: {record['original_party'] or 'unknown'}",
                      f"stated: {stated(record)}", f"period: {record['evidence_period'] or 'unknown'}"])


def query_text(record, thesis_question):
    return f"thesis: {thesis_question}\n{record['summary']}\n{' '.join(record['passages'])}"


def piece_text(record, label):
    return (f"{label} [{record['tier']}; {record['reporting_speaker']}; original source {record['original_party']}, stated "
            f"{stated(record)}] {record['summary']} | quote: {' '.join(record['passages'])}")


def query_vectors(vectors, record, thesis_questions):
    """The search queries of one record, in order: one per thesis association, then its own text when it has no association or lists
    the company's figures."""
    queries = [vectors[query_text(record, thesis_questions[t])] for t in record['thesis_ids']]
    if not record['thesis_ids'] or record.get('figures'):
        queries.append(vectors[doc_text(record)])
    return queries


# Jev's piece criteria aligned with the Step 2 merge line's own test (PRD §5 line 2; AGENTS §7.1, one ruler): a repeat is a later report
# of the stored piece's main statement. Production's wording (views/jev_matching.PIECES) judged "the same evidence", so a later report of
# only a secondary statement inside a stored record (an official's denial carried in the report it denies) was merged as a repeat.
PIECES = {'same_statement': "the INCOMING PIECE reports the STORED PIECE's main statement: a retelling, another outlet carrying it, the "
                            "same number in text or a table, or the same speaker repeating it; wording, precision and extra detail may "
                            "differ. If the stored piece carries several statements and the incoming piece reports only a secondary one, "
                            "this is not it",
          'supersedes': "a later version of the stored piece's main statement, changed: the same speaker revises that guidance, "
                        "forecast or event-progress statement, an official confirms or denies that reported claim, or the original "
                        "source revises it; another statement on the same topic is not this",
          'different': "a different fact, figure or matter, a figure for another period or quantity, or only a secondary statement of "
                       "the stored piece, even if on the same topic"}


def piece_question(text):
    return {'type': 'choice', 'criteria': PIECES,
            'instructions': 'How does the INCOMING PIECE relate to the STORED PIECE below? Use only the supplied text. STORED PIECE:\n' + text}


INFORMS = {'true': "the STORED PIECE bears on the THESIS's own matter (the parties, products, policy or quantity the THESIS names) and "
                   "makes its answer more or less likely, as evidence filed under it would",
           'false': "the STORED PIECE concerns another matter, or is a company-wide result or event that does not speak to the THESIS's "
                    "own matter, or would not change its answer"}


def informs_question(text):
    return {'type': 'noul', 'criteria': INFORMS,
            'instructions': 'Does the STORED PIECE below inform the THESIS stated above? Use only the supplied text; a shared company, '
                            'product family or word is not enough, and the company\'s overall results, guidance and estimates inform a '
                            'thesis about its revenue or earnings path, not one about a competitor, a supplier or a policy unless they '
                            'speak to it. STORED PIECE:\n' + text}


def later_link_judge(library, thesis_question, ask):
    """The judge `Library.link_later` calls: one Jev request per batch, the thesis as state, one yes/no question per stored group."""
    def judge(group_ids):
        questions = {f'q{i}': informs_question(piece_text(library.groups[g]['original'], 'STORED PIECE')) for i, g in enumerate(group_ids)}
        raw = ask(f'THESIS: {thesis_question}', questions)
        return {g: raw[f'q{i}']['noul'] >= jev_matching.THRESHOLD for i, g in enumerate(group_ids)}
    return judge


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)) or 1)


def search(library, vectors, record, thesis_questions):
    """Candidate group ids: each query's top 10 by cosine against the groups' original records, merged in rank order."""
    candidates = []
    for query in query_vectors(vectors, record, thesis_questions):
        ranked = sorted(library.order, key=lambda g: -cosine(query, vectors[doc_text(library.groups[g]['original'])]))[:TOP]
        candidates += [g for g in ranked if g not in candidates]
    return candidates


def outcome(answers, order):
    """answers: {group id: {'choice', 'probabilities'}}; order: group ids in creation order."""
    same = [g for g, a in answers.items() if a['choice'] == 'same_statement']
    later = [g for g, a in answers.items() if a['choice'] == 'supersedes']
    if same:
        best = max(same, key=lambda g: (answers[g]['probabilities']['same_statement'], -order.index(g)))
        return {'kind': 'repeat', 'repeat_of': [best], 'revises': later}
    if later:
        return {'kind': 'revision', 'revises': later}
    return {'kind': 'new'}


def forward(articles, library, vectors, thesis_questions, ask, workers=8, opened=None):
    """articles: lists of Step 3 records in article order. ask(state, questions) returns Jev's answers by question id, or raises.
    opened: per article, the thesis ids it opened; after the article's records are written, each is linked later to the stored groups
    that arrived unlinked from earlier articles (`Library.link_later`). A thesis written to with pairs still pending is judged again,
    against its opening boundary. Returns one decision per record."""
    decisions = []
    for index, records in enumerate(articles):
        def decide(record):
            candidates = search(library, vectors, record, thesis_questions)
            if not candidates:
                return record, candidates, {}, {'kind': 'new'}
            questions = {f'q{i}': piece_question(piece_text(library.groups[g]['original'], 'STORED PIECE'))
                         for i, g in enumerate(candidates)}
            incoming = piece_text(record, 'INCOMING PIECE')
            try:
                raw = ask(incoming, questions)
            except Exception as first:   # retried once; a second failure is reported, never silently saved as new
                try:
                    raw = ask(incoming, questions)
                except Exception as error:
                    return record, candidates, {}, {'kind': 'failed', 'reason': f'{type(first).__name__}: {first}; retry: {type(error).__name__}: {error}'}
            answers = {g: {'choice': raw[f'q{i}']['choice'], 'probabilities': raw[f'q{i}']['probabilities']} for i, g in enumerate(candidates)}
            return record, candidates, answers, outcome(answers, library.order)
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(decide, records))
        for record, candidates, answers, result in results:
            entry = {'id': record['id'], 'candidates': candidates, 'answers': answers, 'outcome': result}
            try:
                entry['group'] = library.apply(record, result)
            except Exception as error:
                entry['refused'] = f'{type(error).__name__}: {error}'
            decisions.append(entry)
        article = records[0]['article'] if records else None
        if article is None:
            continue
        written = {t for r in records for t in r['thesis_ids']}
        retry = [t for t in written if t in library.pending and t not in (opened[index] if opened else [])]
        for thesis_id in list(opened[index] if opened else []) + retry:   # opened here, or written to with pairs still pending
            result = library.link_later(thesis_id, later_link_judge(library, thesis_questions[thesis_id], ask), article)
            library.later_log.append({'thesis': thesis_id, 'article': article, **result})
    return decisions
