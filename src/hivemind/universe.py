"""The research list (docs/prd/01-universe.md): which objects exist and which categories each is watched in. The
only place that decides what is processed. Loaded from poc/universe.json."""
import json


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


def load(path):
    with open(path, encoding='utf-8') as handle:
        return Universe(json.load(handle))
