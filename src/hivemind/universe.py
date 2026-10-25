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
        self.theme_names.update({t['legacy_name']: t['id'] for t in raw['themes'] if t.get('legacy_name')})

    def has(self, object_id):
        return object_id in self.companies or object_id in self.themes

    def kind(self, object_id):
        if object_id in self.companies:
            return 'company'
        if object_id in self.themes:
            return 'theme'
        return None

    def resolve(self, text):
        """An object named by ticker, theme id, theme name, company name or one of the object's aliases (a theme's
        former name is an alias); None when not on the list."""
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
        for record in list(self.themes.values()) + list(self.companies.values()):
            if any(alias.casefold() == key.casefold() for alias in record.get('aliases') or []):
                return record['id']
        return None

    def watches(self, object_id, category):
        record = self.companies.get(object_id) or self.themes.get(object_id)
        return bool(record and category in record['categories'])

    def theme_list(self, legacy=False):
        """(id, name) per theme; legacy=True gives the name a Chinese prompt version printed (legacy_name, else name), so its stored requests replay byte-identical."""
        return [(t['id'], (t.get('legacy_name') or t['name']) if legacy else t['name']) for t in self.themes.values()]

    def watch_list(self, object_id):
        """The analyst's quantities to watch for this object (keyed-views-plan.md 2.4); empty when the object has none."""
        record = self.companies.get(object_id) or self.themes.get(object_id) or {}
        return list(record.get('watch') or [])

    SCOPELESS = {'total_revenue', 'gross_margin', 'operating_margin', 'operating_expense_growth', 'total_expenses', 'operating_loss', 'tax_rate', 'capex'}

    def scope_and_source(self, object_id, measure, scope='', event_type='n/a'):
        """Use a reference name only on an exact match; preserve actual business qualifiers (D155)."""
        plain = re.sub(r'^(?:non[-_ ]?gaap|gaap)\s*', '', scope.strip(), flags=re.I)
        redundant = {'', measure.replace('_', ' ')}
        if measure in self.SCOPELESS and plain.casefold() in redundant:
            return '', 'none'
        for entry in self.watch_list(object_id):
            if (entry.get('measure') == measure and entry.get('scope')
                    and scope_key(entry['scope']) == scope_key(scope)
                    and (not entry.get('event_type') or entry['event_type'] == event_type)):
                return entry['scope'], 'watch'
        return scope, 'model'

    def fiscal_year_end_month(self, object_id):
        """12 for a theme, a company whose fiscal year is the calendar year, or an unknown object."""
        company = self.companies.get(object_id)
        return int((company or {}).get('fiscal_year_end_month') or 12)

    def fiscal_period(self, object_id, year, bare_is_calendar=False):
        """Convert an entire single-year name. Explicit calendar years stay calendar; other spans return None. A bare year
        (2026) is the company's fiscal year under the Chinese prompt versions (06-views: 公司的数按它的财年) and a calendar
        year under the English ones, whose request defines "FY2027, or 2026 for a calendar year"."""
        parsed = parse_year(year)
        if not parsed:
            return None
        kind, y = parsed
        month = 12 if kind == 'calendar' or (kind == 'bare' and bare_is_calendar) else self.fiscal_year_end_month(object_id)
        if month == 12:
            return f'{y}-01-01', f'{y}-12-31'
        start = f'{y - 1}-{month + 1:02d}-01'
        import calendar
        return start, f'{y}-{month:02d}-{calendar.monthrange(y, month)[1]:02d}'

    def canonical_year(self, object_id, year):
        """One spelling per year for the join between a view's year and a waiting dependency's year: a fiscal form
        (FY2027, fiscal year 2027, 2027财年) becomes FY2027 when the object's fiscal year differs from the calendar
        year, else 2027; a calendar form (calendar year 2026, CY2026, 2026自然年) becomes 2026; a bare year keeps its
        digits and is never reinterpreted as a fiscal year (an event dated "2026" means calendar 2026); text that is
        not one single year stays as written (a multi-year span never resolves a waiting dependency)."""
        parsed = parse_year(year)
        if not parsed:
            return (year or '').strip()
        kind, y = parsed
        if kind == 'fiscal' and self.fiscal_year_end_month(object_id) != 12:
            return f'FY{y}'
        return str(y)

    def fiscal_note(self, object_id, publication_day, english=False):
        """One line telling the model how this company's fiscal years map onto the calendar, so a number's year and
        due day are written right (NVDA's FY2027 ends in January 2027, not 2028)."""
        company = self.companies.get(object_id)
        if not company:
            return ''
        month = int(company.get('fiscal_year_end_month') or 12)
        year, pub_month = int(publication_day[:4]), int(publication_day[5:7])
        if month == 12:
            if english:
                return (f"{object_id}'s fiscal year is the calendar year and ends in December: this year is FY{year}, next year is FY{year + 1}; "
                        f'full-year figures are published in the annual report in January to March of the following year.')
            return f'{object_id} 的财年和自然年一样，12 月结束：今年是 FY{year}，明年是 FY{year + 1}；全年数在次年 1 到 3 月的年报里公布。'
        # the fiscal year is named by the calendar year in which it ends
        current = year if pub_month <= month else year + 1
        start_month = month % 12 + 1
        start_year = current - 1 if start_month > month else current
        report_month = month + 1 if month < 12 else 1
        if english:
            return (f"{object_id}'s fiscal year ends in month {month} and is named for the calendar year in which it ends: FY{current} runs from "
                    f'{start_year}-{start_month:02d} to {current}-{month:02d}; the publication day {publication_day} falls in FY{current}, so this year is FY{current} '
                    f"and next year is FY{current + 1}; FY{current}'s full-year figures are published in the annual report around {current}-{report_month:02d}; use that day as the due date.")
        return (f'{object_id} 的财年在 {month} 月结束，财年按结束的那一年命名：FY{current} 从 {start_year}-{start_month:02d} 到 {current}-{month:02d}，'
                f'发布日 {publication_day} 落在 FY{current}，所以今年是 FY{current}，明年是 FY{current + 1}；FY{current} 的全年数在 {current}-{report_month:02d} 前后的年报里公布，到期日按那天写。')


# The accepted spellings of one year (docs/research/2026-10-25-english/plan.md, "Period text"): a full match, nothing else.
FISCAL_YEAR = re.compile(r'(?:FY\s*|fiscal\s+(?:year\s+)?)(\d{4})|(\d{4})\s*财年|FY\s*(\d{2})', re.I)
CALENDAR_YEAR = re.compile(r'(?:CY\s*|calendar\s+(?:year\s+)?)(\d{4})|(\d{4})\s*自然年|(\d{4})\s*calendar\s+year', re.I)
BARE_YEAR = re.compile(r'(\d{4})\s*年?')


def parse_year(text):
    """('fiscal' | 'calendar' | 'bare', year) for text that names exactly one year, else None. A bare year takes the
    object's fiscal year when its period is computed (06-views: 公司的数按它的财年)."""
    value = (text or '').strip()
    if not value:
        return None
    m = FISCAL_YEAR.fullmatch(value)
    if m:
        year = m.group(1) or m.group(2) or m.group(3)
        return 'fiscal', int(year) if len(year) == 4 else 2000 + int(year)
    m = CALENDAR_YEAR.fullmatch(value)
    if m:
        return 'calendar', int(m.group(1) or m.group(2) or m.group(3))
    m = BARE_YEAR.fullmatch(value)
    if m:
        return 'bare', int(m.group(1))
    return None


def scope_key(scope):
    """A scope name as compared: case, spacing, dashes and the words revenue/segment do not distinguish two scopes."""
    s = re.sub(r'[\u2013\u2014]', '-', (scope or '')).replace('＋', '+').replace('&amp;', '&')
    s = re.sub(r'\b(revenue|segment|business|division)\b', '', s, flags=re.I)
    return re.sub(r'\s+', ' ', s).strip().casefold()


def load(path):
    with open(path, encoding='utf-8') as handle:
        return Universe(json.load(handle))
