"""The research list (docs/prd/01-universe.md): which objects exist and which categories each is watched in. The
only place that decides what is processed. Loaded from poc/universe.json."""
import json
import re


class Universe:
    def __init__(self, raw):
        self.version = raw['version']
        self.companies = {c['id']: c for c in raw['companies']}
        self.themes = {t['id']: t for t in raw['themes']}
        self.theme_names = {t['name']: t['id'] for t in raw['themes']}

    def has(self, object_id):
        return object_id in self.companies or object_id in self.themes

    def kind(self, object_id):
        if object_id in self.companies:
            return 'company'
        if object_id in self.themes:
            return 'theme'
        return None

    def resolve(self, text):
        """An object named by ticker, theme id, theme name or company name; None when not on the list."""
        if not text:
            return None
        key = text.strip()
        if key in self.companies or key in self.themes:
            return key
        if key in self.theme_names:
            return self.theme_names[key]
        upper = key.upper()
        if upper in self.companies:
            return upper
        for company in self.companies.values():
            if company['name'].lower() == key.lower():
                return company['id']
        return None

    def watches(self, object_id, category):
        record = self.companies.get(object_id) or self.themes.get(object_id)
        return bool(record and category in record['categories'])

    def theme_list(self):
        return [(t['id'], t['name']) for t in self.themes.values()]

    def watch_list(self, object_id):
        """The analyst's quantities to watch for this object (keyed-views-plan.md 2.4); empty when the object has none."""
        record = self.companies.get(object_id) or self.themes.get(object_id) or {}
        return list(record.get('watch') or [])

    SCOPELESS = {'total_revenue', 'gross_margin', 'operating_margin', 'operating_expense_growth', 'total_expenses', 'operating_loss', 'tax_rate', 'capex'}

    def canonical_scope(self, object_id, measure, scope='', event_type='n/a'):
        """The scope the key carries (keyed-views-plan.md 2.1, after T2): a measure that has no scope by nature carries none
        (the basis field holds GAAP / non-GAAP; T2 wrote 'GAAP', 'GAAP tax rate', 'non-GAAP tax rate' as scopes and opened
        the tax rate four times); a measure whose watch entry names a scope carries that entry's spelling; otherwise
        the model's scope stands."""
        return self.scope_and_source(object_id, measure, scope, event_type)[0]

    def scope_and_source(self, object_id, measure, scope='', event_type='n/a'):
        """(scope, source): source is 'none' for a scope-less measure, 'watch' when the list's spelling applies, 'model' when
        the model's own scope stands (keyed-views-plan.md 2.5: identity is code's when the scope is code's)."""
        if measure in self.SCOPELESS:
            return '', 'none'
        for entry in self.watch_list(object_id):
            if entry.get('measure') == measure and entry.get('scope') and scope_hits(entry, scope) and (not entry.get('event_type') or entry['event_type'] == event_type):
                return entry['scope'], 'watch'
        return scope, 'model'

    def fiscal_period(self, object_id, year):
        """The calendar span of a company's fiscal year named 'FY2027' or '2027' (a theme's or an unknown object's year
        is the calendar year): (start, end) ISO dates, or None when the year cannot be read. Code owns the conversion:
        T2 wrote FY2027 as 2027-02-01..2028-01-31 on the Compute & Networking view."""
        m = re.search(r'(\d{4})', year or '')
        if not m:
            return None
        y = int(m.group(1))
        company = self.companies.get(object_id)
        month = int((company or {}).get('fiscal_year_end_month') or 12)
        if month == 12:
            return f'{y}-01-01', f'{y}-12-31'
        start = f'{y - 1}-{month + 1:02d}-01'
        import calendar
        return start, f'{y}-{month:02d}-{calendar.monthrange(y, month)[1]:02d}'

    def watch_allows(self, object_id, measure, scope='', event_type='n/a'):
        """Whether a candidate view with this key opens: its measure is on the object's list, and when the entry names a
        scope or an event type they match after normalisation. `other` never opens. No list → nothing opens for that object."""
        if measure == 'other':
            return False
        for entry in self.watch_list(object_id):
            if entry.get('measure') != measure:
                continue
            if entry.get('scope') and not scope_hits(entry, scope):
                continue
            if entry.get('event_type') and entry['event_type'] != event_type:
                continue
            return True
        return False

    def fiscal_note(self, object_id, publication_day):
        """One line telling the model how this company's fiscal years map onto the calendar, so a number's year and
        due day are written right (NVDA's FY2027 ends in January 2027, not 2028)."""
        company = self.companies.get(object_id)
        if not company:
            return ''
        month = int(company.get('fiscal_year_end_month') or 12)
        year, pub_month = int(publication_day[:4]), int(publication_day[5:7])
        if month == 12:
            return f'{object_id} 的财年和自然年一样，12 月结束：今年是 FY{year}，明年是 FY{year + 1}；全年数在次年 1 到 3 月的年报里公布。'
        # the fiscal year is named by the calendar year in which it ends
        current = year if pub_month <= month else year + 1
        start_month = month % 12 + 1
        return (f'{object_id} 的财年在 {month} 月结束，财年按结束的那一年命名：FY{current} 从 {current - 1 if start_month > month else current}-{start_month:02d} 到 {current}-{month:02d}，'
                f'发布日 {publication_day} 落在 FY{current}，所以今年是 FY{current}，明年是 FY{current + 1}；FY{current} 的全年数在 {current}-{month + 1 if month < 12 else 1:02d} 前后的年报里公布，到期日按那天写。')


def scope_hits(entry, scope):
    """A watch entry's scope matches the model's scope when the names are equal after normalisation or one of the entry's
    aliases occurs inside the model's scope (keyed-views-plan.md 2.3/2.6: the model writes, code binds by alias; T2b
    refused 'top 5 cloud providers and hyperscalers CapEx' against 'five hyperscalers' on spelling alone)."""
    mine = scope_key(scope)
    if not mine:
        return False
    if scope_key(entry['scope']) == mine:
        return True
    return any(scope_key(alias) and scope_key(alias) in mine for alias in entry.get('aliases', []))


def scope_key(scope):
    """A scope name as compared: case, spacing, dashes and the words revenue/segment do not distinguish two scopes."""
    s = re.sub(r'[\u2013\u2014]', '-', (scope or '')).replace('＋', '+').replace('&amp;', '&')
    s = re.sub(r'\b(revenue|segment|business|division)\b', '', s, flags=re.I)
    return re.sub(r'\s+', ' ', s).strip().casefold()


def load(path):
    with open(path, encoding='utf-8') as handle:
        return Universe(json.load(handle))
