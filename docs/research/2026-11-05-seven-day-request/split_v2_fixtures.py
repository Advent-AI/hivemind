"""Saved split answers (version 1) rewritten into the version-2 answer shapes, for offline tests that replay them through the
version-2 requests. The content is unchanged: the old reason becomes what separates the question, and a free-text subject becomes a
listed id when it is one, otherwise new with that name."""
import copy


def a_v2(answer):
    out = copy.deepcopy(answer)
    for q in out['questions']:
        reason = q.pop('why_not_already_covered', '')
        q.setdefault('closest_existing_question', 'none')
        q.setdefault('what_separates_it', reason)
    return out


def meta_v2(meta, uni):
    out = copy.deepcopy(meta)
    entries = out['candidates'].values() if isinstance(out['candidates'], dict) else out['candidates']
    for c in entries:
        if 'kind' not in c:
            continue
        kind = c.pop('kind'); listed = c['object'] in uni.companies or c['object'] in uni.themes
        c.update(new_subject='' if listed else c['object'], new_subject_kind='none' if listed else ('theme' if kind == 'theme' else 'company'),
                 object=c['object'] if listed else 'new', shared_measure='none', unit='n/a')
    return out
