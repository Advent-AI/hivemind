"""Complete, historical DB context for steps 2a and 2b (D250, ported for D201): the catalog of open questions in scope at a
sequence number, and the complete evidence of chosen questions at that same sequence number.

Catalog selection is a semantic job outside this module. No lexical filtering,
ranking, model call or top-N truncation is performed here.
"""
import copy
import json
from .views import store


class ContextTooLarge(ValueError):
    pass


def bounded(value, limit):
    size = len(json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode())
    if size > limit:
        raise ContextTooLarge(f'complete context requires {size} bytes; limit is {limit}')
    return value


class Reader:
    """One read transaction, one explicit exclusive sequence boundary and scope."""

    def __init__(self, path, before_seq, object_ids, universe, *, catalog_limit=150000,
                 evidence_limit=1000000):
        if type(before_seq) is not int or before_seq < 1:
            raise ValueError('before_seq must be a positive owned sequence number')
        if not object_ids or any(not universe.has(x) for x in object_ids):
            raise ValueError('explicit, known research objects required')
        if catalog_limit < 1 or evidence_limit < 1:
            raise ValueError('positive context limits required')
        self.seq = before_seq
        self.scope = sorted(set(object_ids) | set(universe.themes))
        self.catalog_limit, self.evidence_limit = catalog_limit, evidence_limit
        self.db = store.open_read_only(path)
        self.db.execute('begin')
        self._catalog = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.db.close()

    def rows(self, sql, args=()):
        return [dict(r) for r in self.db.execute(sql, args)]

    def dependencies(self, vid):
        result = self.rows('select * from dependencies where view_id=? and seq<? order by seq,dependency_id', (vid,self.seq))
        for dep in result:
            res = self.rows('select * from dependency_resolutions where dependency_id=? and seq<? order by seq desc,id desc limit 1', (dep['dependency_id'],self.seq))
            dep['resolved_to'] = res[0]['resolved_to'] if res else dep['depends_on']
            dep['resolution'] = res[0] if res else None
        return result

    def question(self, row):
        vid = row['view_id']
        switches = self.rows('select * from view_switches where view_id=? and after_seq<? order by after_seq desc,id desc limit 1', (vid,self.seq))
        if not switches:
            raise ValueError('question has no historical open/closed state: ' + vid)
        keys = self.rows('select * from view_keys where view_id=? and seq<?', (vid,self.seq))
        return dict(row, open=bool(switches[0]['open']),
                    rungs=self.rows('select * from rungs where view_id=? order by position', (vid,)),
                    key=keys[0] if keys else None, dependencies=self.dependencies(vid))

    def catalog(self):
        all_rows = self.rows('select * from views where created_seq<? order by created_seq,view_id', (self.seq,))
        by_id = {r['view_id']: r for r in all_rows}
        selected = {}
        for row in all_rows:
            if row['object_id'] in self.scope:
                q = self.question(row)
                if q['open']:
                    selected[row['view_id']] = q
        for q in list(selected.values()):
            for dep in q['dependencies']:
                vid = dep['resolved_to']
                if vid and vid not in selected:
                    if vid not in by_id:
                        raise ValueError('historical dependency target missing: ' + vid)
                    selected[vid] = self.question(by_id[vid])
        payload = {'before_seq': self.seq, 'object_ids': self.scope,
                   'questions': list(selected.values()), 'complete': True}
        bounded(payload, self.catalog_limit)
        self._catalog = selected
        return copy.deepcopy(payload)

    def evidence(self, eid):
        rows = self.rows('select * from evidence where evidence_id=? and created_seq<?', (eid,self.seq))
        if not rows:
            raise ValueError('historical evidence missing: ' + eid)
        return dict(rows[0], sources=self.rows('select * from evidence_sources where evidence_id=? and seq<? order by seq,id', (eid,self.seq)))

    def expand(self, view_ids):
        if self._catalog is None:
            self.catalog()
        if len(set(view_ids)) != len(view_ids) or any(v not in self._catalog for v in view_ids):
            raise ValueError('select distinct IDs from this historical catalog')
        evidence, questions = {}, []
        for vid in view_ids:
            ids = self.rows('select distinct e.evidence_id,e.created_seq from evidence e join evidence_links l on l.evidence_id=e.evidence_id where l.view_id=? and l.seq<? and e.created_seq<? and not exists (select 1 from replacements r where r.old_evidence_id=e.evidence_id and r.seq<?) order by e.created_seq,e.evidence_id', (vid,self.seq,self.seq,self.seq))
            for row in ids:
                eid = row['evidence_id']
                if eid not in evidence:
                    record = self.evidence(eid)
                    previous = self.rows('select * from replacements where new_evidence_id=? and seq<? order by seq,id', (eid,self.seq))
                    record['replaced'] = [dict(r, evidence=self.evidence(r['old_evidence_id'])) for r in previous]
                    evidence[eid] = record
            judgements = self.rows('select * from judgements where view_id=? and seq<? order by seq desc,judgement_id desc limit 1', (vid,self.seq))
            questions.append(dict(copy.deepcopy(self._catalog[vid]), evidence_ids=[r['evidence_id'] for r in ids],
                                  latest_judgement=judgements[0] if judgements else None))
        return bounded({'before_seq': self.seq, 'questions': questions,
                        'evidence': list(evidence.values()), 'complete': True}, self.evidence_limit)
