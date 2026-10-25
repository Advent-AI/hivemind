"""The canonical English values of every closed field the pipeline reads (D163, docs/research/2026-10-25-english/plan.md,
"Canonical vocabulary"), and the exact legacy-to-canonical conversion of the values the Chinese prompt versions wrote.

A value is converted only where an answer or a stored record is read for comparison; prose is never touched, rows are
never rewritten, and an unknown value passes through unchanged so that the schema or the code check that owns the
field refuses it as before."""

KINDS = ['asset', 'theme']
TIERS = ['fact', 'party_statement', 'third_party_view', 'rumour']
CANDIDATE_OUTCOMES = ['merge', 'succession', 'new', 'skip']
EVIDENCE_OUTCOMES = ['repeat', 'replace', 'new']
PUSHES = ['toward_first', 'toward_last', 'none']
DIRECTIONS = ['first_is_bullish', 'last_is_bullish', 'same', 'opposite']
ASSET_LABELS = ['Strongly bullish', 'Bullish', 'Neutral', 'Bearish', 'Strongly bearish']
YES_NO = ['Yes', 'No']

LEGACY = {
    'kind': {'对象观点': 'asset', '主题观点': 'theme'},
    'tier': {'发生的事': 'fact', '当事人说的': 'party_statement', '第三方看法': 'third_party_view', '传闻': 'rumour'},
    'candidate_outcome': {'归入已有的': 'merge', '接续': 'succession', '新观点': 'new', '不开': 'skip'},
    'evidence_outcome': {'重复': 'repeat', '替代': 'replace', '新证据': 'new'},
    'push': {'推向第一格': 'toward_first', '推向最后一格': 'toward_last', '不推': 'none'},
    'direction': {'对方第一格是看多': 'first_is_bullish', '对方最后一格是看多': 'last_is_bullish', '同向': 'same', '反向': 'opposite'},
    'label': {'强烈看多': 'Strongly bullish', '看多': 'Bullish', '中性': 'Neutral', '看空': 'Bearish', '强烈看空': 'Strongly bearish', '是': 'Yes', '否': 'No'},
}


def canonical(field, value):
    """The canonical value of a closed field: a legacy value converted, a canonical one kept, anything else unchanged."""
    if not isinstance(value, str):
        return value
    return LEGACY[field].get(value.strip(), value)


def legacy(field, value):
    """The Chinese spelling of a canonical value, for a request built for a Chinese prompt version."""
    for old, new in LEGACY[field].items():
        if new == value:
            return old
    return value


def extraction_answer(data):
    """An extraction answer with canonical kind, tier and standard rung labels; other fields untouched."""
    out = dict(data)
    out['candidates'] = [dict(c, kind=canonical('kind', c.get('kind')),
                              rungs=[dict(r, label=canonical('label', r.get('label'))) for r in c.get('rungs', [])]) for c in data.get('candidates', [])]
    out['evidence'] = [dict(e, tier=canonical('tier', e.get('tier'))) for e in data.get('evidence', [])]
    return out


def candidate(c):
    """A handover candidate (fresh or saved) with canonical kind and labels."""
    return dict(c, kind=canonical('kind', c.get('kind')), rungs=[dict(r, label=canonical('label', r.get('label'))) for r in c.get('rungs', [])])


def matching_answer(data):
    """A matching answer with canonical candidate outcomes, evidence outcomes and dependency directions."""
    out = dict(data)
    out['candidates'] = [dict(d, outcome=canonical('candidate_outcome', d.get('outcome')),
                              dependencies=[dict(dep, direction=canonical('direction', dep.get('direction'))) for dep in d.get('dependencies', [])])
                         for d in data.get('candidates', [])]
    out['evidence'] = [dict(d, outcome=canonical('evidence_outcome', d.get('outcome'))) for d in data.get('evidence', [])]
    return out


def judgement_answer(data):
    """A judgement answer with canonical pushes."""
    return dict(data, pushes=[dict(p, push=canonical('push', p.get('push'))) for p in data.get('pushes', [])])
