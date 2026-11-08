"""Isolated Step 3 evidence library for the clean path (PRD §6): an in-memory logical store and its dossier text, not the live writer.

A group is one stored statement. Its original record keeps its id and fields unchanged and gives the group its id. A later record that
Step 2 judged a repeat joins the group as a member and keeps its own id, text, fields and source article. Thesis links belong to the
group and remember the record that brought each one. A revision is its own group, linked to every group it revises; a repeat that also
revises another group adds that link to its own group, naming the member that established it.

The writer refuses rather than guesses: a failed comparison, several repeat targets, an unknown group, or a replayed record whose
placement differs from the first time raise `Refused` and write nothing. Physical storage and crash recovery are not provided here.

Later linking (Alex, 2026-11-08: a material statement no thesis takes is kept and linked when a related thesis opens; design
STEP1-CONDITIONS-DESIGN.md §§11.1, 17): when a thesis opens, every group whose original arrived with no link, from an earlier article,
is judged against it in batches. Each judged (thesis, group) pair is recorded once in `judged`; a batch that fails twice stays pending,
is reported, and is judged again on the next write to that thesis, against the same opening boundary (`opened_at`)."""
import copy

RECORD_FIELDS = ('id', 'article', 'publisher', 'publication_date', 'summary', 'passages', 'original_party', 'reporting_speaker', 'tier',
                 'statement_date', 'evidence_period', 'thesis_ids')


class Refused(Exception):
    """A Step 2 outcome the library will not write; nothing was changed."""


class Library:
    def __init__(self):
        self.groups = {}       # group id → {'original': record, 'members': [record], 'links': {thesis id: record id}, 'revises': [{'group', 'by'}]}
        self.placement = {}    # record id → group id
        self.order = []        # group ids in the order they were created
        self.judged = {}       # (thesis id, group id) → True | False, the later-linking ledger
        self.later_log = []    # one entry per later-linking call: thesis, article, linked, pending, judged
        self.opened_at = {}    # thesis id → the article that opened it: the boundary of its later linking
        self.pending = {}      # thesis id → group ids whose judgement failed twice and waits for the next write to the thesis

    def apply(self, record, outcome):
        """Write one record with its Step 2 outcome: {'kind': 'new' | 'repeat' | 'revision' | 'failed', 'repeat_of': [group ids],
        'revises': [group ids], 'reason': text}. Returns the id of the group that holds the record."""
        missing = [f for f in RECORD_FIELDS if f not in record]
        if missing:
            raise Refused(f'record lacks {missing}')
        kind, repeat_of, revises = outcome['kind'], list(outcome.get('repeat_of') or []), list(outcome.get('revises') or [])
        if kind == 'failed':
            raise Refused(f"comparison failed for {record['id']}: {outcome.get('reason', 'no reason given')}")
        if kind not in ('new', 'repeat', 'revision'):
            raise Refused(f'unknown outcome {kind!r}')
        if (kind == 'repeat') != bool(repeat_of) or len(repeat_of) > 1:
            raise Refused(f"a repeat names exactly one group; got {repeat_of} for outcome {kind}")
        if kind == 'revision' and not revises:
            raise Refused('a revision names the group it revises')
        for group_id in repeat_of + revises:
            if group_id not in self.groups:
                raise Refused(f'unknown group {group_id}')
        target = repeat_of[0] if repeat_of else record['id']
        if record['id'] in self.placement:
            if self.placement[record['id']] != target:
                raise Refused(f"{record['id']} was placed in {self.placement[record['id']]}, not {target}")
            group = self.groups[target]
            stored = next(r for r in [group['original']] + group['members'] if r['id'] == record['id'])
            if {k: v for k, v in stored.items() if k != 'thesis_ids'} != {k: v for k, v in record.items() if k != 'thesis_ids'}:
                raise Refused(f"{record['id']} names a stored record with different content; a changed record needs a new id")
            self._link(group, record)
            return target
        if kind == 'repeat':
            group = self.groups[target]
            group['members'].append(copy.deepcopy(record))
        else:
            group = {'original': copy.deepcopy(record), 'members': [], 'links': {}, 'revises': []}
            self.groups[target] = group
            self.order.append(target)
        self.placement[record['id']] = target
        self._link(group, record)
        for revised in revises:
            if revised != target and not any(r['group'] == revised for r in group['revises']):
                group['revises'].append({'group': revised, 'by': record['id']})
        return target

    def link_later(self, thesis_id, judge, before_article, batch=10):
        """Judge every group whose original arrived unlinked from an article before `before_article` against a newly opened thesis.
        judge(group ids) returns {group id: True | False} or raises. Returns {'linked': [...], 'pending': [...], 'judged': n}."""
        self.opened_at.setdefault(thesis_id, before_article)
        before_article = self.opened_at[thesis_id]
        todo = [g for g in self.order if not self.groups[g]['original']['thesis_ids']
                and self.groups[g]['original']['article'] < before_article and (thesis_id, g) not in self.judged]
        linked, pending = [], []
        for start in range(0, len(todo), batch):
            ids = todo[start:start + batch]
            answers = None
            for _attempt in range(2):
                try:
                    answers = judge(ids)
                    break
                except Exception:   # tried twice, then reported as pending, never saved as a judgement
                    answers = None
            if answers is None:
                pending += ids
                continue
            for group_id in ids:
                self.judged[(thesis_id, group_id)] = bool(answers[group_id])
                if answers[group_id]:
                    self.groups[group_id]['links'].setdefault(thesis_id, self.groups[group_id]['original']['id'])
                    linked.append(group_id)
        if pending:
            self.pending[thesis_id] = pending
        else:
            self.pending.pop(thesis_id, None)
        return {'linked': linked, 'pending': pending, 'judged': len(todo) - len(pending)}

    @staticmethod
    def _link(group, record):
        for thesis_id in record['thesis_ids']:
            group['links'].setdefault(thesis_id, record['id'])

    @staticmethod
    def articles(group):
        """Distinct source articles of a group, oldest first; two records from one article count once."""
        seen = []
        for record in [group['original']] + group['members']:
            if record['article'] not in seen:
                seen.append(record['article'])
        return seen

    def dossier(self, thesis_id):
        """Group ids linked to a thesis, in creation order."""
        return [g for g in self.order if thesis_id in self.groups[g]['links']]


def labelled_passages(record):
    """Each passage as a reader sees it: the source text Step 1 found, labelled 'Quote', or, when Step 1 did not find it (verified
    value None), the model's text labelled 'Unverified quote'. The model's own text stays in the record's `passages`. A record stored
    before verification was carried shows its passages as 'Quote'."""
    verified = record.get('verified_passages') or record['passages']
    return [('Quote', found) if found is not None else ('Unverified quote', passage) for passage, found in zip(record['passages'], verified)]


def record_text(record, label):
    attribution = record['original_party'] or 'unknown party'
    if record['reporting_speaker'] and record['reporting_speaker'] != record['original_party']:
        attribution += f", reported by {record['reporting_speaker']}"
    head = (f"[{label}] {record['publication_date']} · {record['publisher'] or 'unknown publisher'} · {attribution} · tier {record['tier']}"
            f" · stated {record['statement_date'] or 'unknown'} · period {record['evidence_period'] or 'unknown'}")
    quotes = '\n'.join(f'  {label_of}: "{p}"' for label_of, p in labelled_passages(record))
    return f"{head}\n  {record['summary']}\n{quotes}"


def group_text(library, group_id, label, labels, member_text=True, notes=()):
    """A group as a reader sees it: the original record, then each later report of the same statement in arrival order, with its own
    text when `member_text` is set and as a source line otherwise. Distinct articles are counted; repeats are not called confirmation."""
    group = library.groups[group_id]
    lines = [record_text(group['original'], label)]
    if group['members']:
        articles = library.articles(group)
        publishers = {r['publisher'] for r in [group['original']] + group['members']}
        lines.append(f'  Later reports of the same statement: {len(group["members"])} records from {len(articles) - 1} further articles '
                     f'({len(publishers)} publishers in all). Articles repeating a statement do not by themselves confirm it independently.')
        for member in group['members']:
            if member_text:
                party = '' if member['original_party'] == group['original']['original_party'] else f" · {member['original_party']}"
                quotes = ' '.join(f'"{p}"' if kind == 'Quote' else f'"{p}" (unverified)' for kind, p in labelled_passages(member))
                lines.append(f"    - {member['publication_date']} · {member['publisher']}{party}: {member['summary']}\n      Quote: {quotes}")
            else:
                lines.append(f"    - {member['publication_date']} · {member['publisher']}")
    for revised in group['revises']:
        lines.append(f"  Revises [{labels[revised['group']]}]." if revised['group'] in labels else '  Revises an entry outside this dossier.')
    lines += [f'  {note}' for note in notes]
    return '\n'.join(lines)
