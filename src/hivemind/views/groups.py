"""Research groups (D149, D165, D166): a group is one ongoing matter with a name, a scope and aliases, the names the
matter goes by (products, projects, parties). Identity and membership are decided by code from those names, the way an
object's aliases and a scope's aliases already are; the model only declares a matter that no stored group is, and may
cite groups. A declaration whose aliases hit a stored group is that group; a thesis whose own text (focus, question,
scope) carries a group's alias joins it, when the thesis itself tracks a matter; a company's own financial line joins only
by the model's citation. Company names and tickers are never aliases: a company is not a group."""
import json
import re

MIN_ALIAS = 3


def clean_aliases(aliases, name, universe=None):
    """The aliases a group may carry: its own name, the declared aliases, each at least three characters and not a
    research object's id, name or alias (the company-folder guard at the alias level)."""
    banned = set()
    if universe is not None:         # a research object's id and names; its search aliases include product names, which groups may use
        for record in list(universe.companies.values()) + list(universe.themes.values()):
            banned.update(x.casefold() for x in (record['id'], record.get('name', ''), record.get('legacy_name', '')) if x)
    out = []
    for alias in [name] + list(aliases or []):
        alias = re.sub(r'\s+', ' ', (alias or '')).strip()
        if len(alias) < MIN_ALIAS or alias.casefold() in banned or alias.casefold() in {a.casefold() for a in out}:
            continue
        out.append(alias)
    return out


def hits(aliases, text):
    """The aliases that occur in the text as whole words, case-insensitively."""
    found = []
    folded = text or ''
    for alias in aliases or []:
        if re.search(r'(?<![A-Za-z0-9])' + re.escape(alias) + r'(?![A-Za-z0-9])', folded, re.I):
            found.append(alias)
    return found


def candidate_text(c):
    return ' '.join(str(c.get(k) or '') for k in ('looks_at', 'question', 'scope'))


def stored_groups(conn):
    from . import store
    return [store._group_record(r) for r in conn.execute('select * from thesis_groups order by rowid')]


def plan(declared, existing, candidates, new_views, tracks_a_matter, universe=None):
    """Decide, before any write, which declarations become groups, which are a stored group under another name, and
    every membership of the theses being written.

    declared: the handover's new_groups [{id, name, scope, aliases}]; existing: stored_groups(conn); candidates: the
    handover's candidates; new_views: candidate id -> view id for the theses this write creates. Returns
    (creations, memberships, notes): creations = [{local_id, name, scope, aliases}] in declaration order;
    memberships = [(view_id, group_key, basis)] where group_key is a stored group_id or a local id of a creation."""
    notes = []
    alias_index = {}                                  # casefolded alias -> stored group id
    for g in existing:
        for alias in g['aliases']:
            alias_index.setdefault(alias.casefold(), g['group_id'])
    redirected, creations, created_aliases = {}, [], {}
    founders = {ref for c in candidates if c['id'] in new_views and tracks_a_matter(c) for ref in c.get('group_refs') or []}
    for d in declared or []:
        aliases = clean_aliases(d.get('aliases'), d['name'], universe)
        same = [alias_index[a.casefold()] for a in aliases if a.casefold() in alias_index]
        if same:
            redirected[d['id']] = same[0]
            notes.append(f'declared group {d["id"]} "{d["name"]}" is stored group {same[0]} by its names; not created')
            continue
        if d['id'] not in founders:
            notes.append(f'declared group {d["id"]} "{d["name"]}" is cited by no written thesis that tracks a matter; not created')
            continue
        creations.append({'local_id': d['id'], 'name': d['name'], 'scope': d['scope'], 'aliases': aliases})
        created_aliases[d['id']] = aliases
    memberships, seen = [], set()

    def add(view_id, key, basis):
        if (view_id, key) not in seen:
            seen.add((view_id, key))
            memberships.append((view_id, key, basis))

    for c in candidates:
        if c['id'] not in new_views:
            continue
        view_id = new_views[c['id']]
        for ref in c.get('group_refs') or []:
            key = redirected.get(ref, ref)
            if key in created_aliases or any(g['group_id'] == key for g in existing):
                add(view_id, key, 'model')
            else:
                notes.append(f'view {view_id}: cited group {ref} was not created; membership dropped')
        for ref in c.get('jev_group_refs') or []:         # memberships the Jev matching engine added (log row 37), stored under their own basis
            if any(g['group_id'] == ref for g in existing):
                add(view_id, ref, 'jev')
        if not tracks_a_matter(c):
            continue                 # a company's own financial line joins a group only when the model cites one; a generic alias in its question is not membership
        text = candidate_text(c)
        for g in existing:
            for alias in hits(g['aliases'], text):
                add(view_id, g['group_id'], f'alias:{alias}')
        for local_id, aliases in created_aliases.items():
            for alias in hits(aliases, text):
                add(view_id, local_id, f'alias:{alias}')
    return creations, memberships, notes
