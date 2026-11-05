"""Controls for the per-question reading's code check (baseline_read.kept_figures, on the release's real page text) and its decision
(baseline_read_measure.delivered), $0: every case states the outcome it must have, including the cases the independent reader raised.

usage: python3 baseline_controls.py
"""
import sqlite3
import sys

HERE = '/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end'
sys.path[:0] = ['/Users/lchingen/hivemind/src', HERE]
import baseline_read as br  # noqa: E402
import baseline_read_measure as brm  # noqa: E402

PAGES = sqlite3.connect(f'file:{br.PAGES}?mode=ro', uri=True)
TEXT = PAGES.execute('select text from items where input_id=?', (br.RELEASE,)).fetchone()[0]
CFO = PAGES.execute('select text from items where input_id=?', ('edgar:NVDA:0001045810-26-000051:q1fy27cfocommentary.htm',)).fetchone()[0]
LABEL = 'Purchases related to property and equipment and intangible assets'
CHECK_CASES = [   # (case, quote, value, kept), on the release unless the case names the CFO commentary
    ('summary-table row, GAAP operating income', 'Operating income $53,536', '53,536', True),
    ('reconciliation row whose "$" sits on its own line', 'Non-GAAP operating income* $53,783', '$53,783', True),
    ('free cash flow, "$" on its own line', 'Free cash flow $48,554', '48,554', True),
    ('percent cell split from its number', 'Gross margin 74.9%', '74.9%', True),
    ('cash-flow row in parentheses', f'{LABEL} (1,757)', '(1,757)', True),
    ('revenue row', 'Revenue $81,615', '81,615', True),
    ('row quoted past the figure reported: the value is printed in it, the column is the reader\'s to check', 'Operating income $53,536 $44,299', '53,536', True),
    ('whole summary row, the reported figure first (pilot v10 send 3)', 'Operating income $53,783 $44,474 $21,801 21% 147%', '$53,783', True),
    ('previous-quarter column, the row ending on it', 'Operating income $53,536 $44,299', '44,299', True),
    ('value is part of the printed number', f'{LABEL} (1,757)', '757', False),
    ('bare number, no label', '(1,757)', '1,757', False),
    ('value at another scale than printed', f'{LABEL} (1,757)', '1.757', False),
    ('label with its footnote mark left off: the report\'s row span is stored', 'Non-GAAP operating income $53,783', '53,783', True),
    ('label not the report\'s (a word changed)', 'Non-GAAP operating profit $53,783', '53,783', False),
    ('a cell left out: the figure is in that row', 'Purchases related to property and equipment and intangible assets (1,227)', '(1,227)', True),
    ('a cell left out: the figure is not in that row', 'Purchases related to property and equipment and intangible assets (1,894)', '(1,894)', False),
    ('a sentence with a word changed is not repaired', 'Record Data Center revenue of $75.2 billion, up 93% from a year ago', '$75.2 billion', False),
    ('figure not in the report', 'Operating income $53,000', '53,000', False),
    ('headline bullet copied whole, more numbers after the figure', 'Record Data Center revenue of $75.2 billion, up 92% from a year ago', '$75.2 billion', True),
    ('two figures written as one value', 'For the quarter, GAAP and non-GAAP earnings per diluted share were $2.39 and $1.87, respectively.', '$2.39 and $1.87', False),
    ('digits inside a product name are not a figure (v7 send 1)', 'Expanded collaboration with Google Cloud to advance agentic and physical AI, including new NVIDIA Vera Rubin-powered A5X instances and a preview of Google Gemini models on Google Distributed Cloud running on NVIDIA Blackwell and Blackwell Ultra GPUs.', 'new NVIDIA Vera Rubin-powered A5X instances', False),
]
CFO_CASES = [   # (case, quote, value, kept), on the CFO commentary
    ('sentence copied whole, the figure mid-sentence', 'Data Center revenue for the first quarter was a record $75.2 billion, up 92% from a year ago and up 21% sequentially, driven by the ramp of our Blackwell 300 products and demand for our InfiniBand, Spectrum-X™ Ethernet, and NVLink™ solutions.', '75.2', True),
    ('commitments sentence copied whole (whose quantity it is, is the reader\'s to check)', 'Multi-year cloud service commitments were $30.0 billion, up from $27.0 billion sequentially, to support the growing needs of our research and development efforts.', '30.0', True),
    ('market-platform table row', 'Data Center $75,246', '$75,246', True),
    ('value not printed in the quote', 'Data Center revenue for the first quarter was a record $75.2 billion', '75.25', False),
]


def figure(quote, value, period, one_line='', kept=True, basis='GAAP'):
    return {'quote': quote, 'value': value, 'unit': 'USD millions', 'period': period, 'one_line': one_line, 'basis': basis, 'kept': kept,
            'in_report': kept, 'labelled': kept, 'value_in_quote': kept}


OP, REV = figure('Operating income $53,783', '53,783', 'Q1 FY27', basis='non-GAAP'), figure('Revenue $81,615', '81,615', 'Q1 FY27')
CAPEX = figure(f'{LABEL} (1,757)', '(1,757)', 'Three months ended April 26, 2026')
DECISION_CASES = [   # (case, question, figures, delivered)
    ('v10 both lines', 'v10', [OP, REV], True),
    ('v10 operating income only', 'v10', [OP], False),
    ('v10 previous quarter labelled Q1 FY27 (misread column)', 'v10', [OP, REV, figure('Operating income $53,783 $44,474', '44,474', 'Q1 FY27')], False),
    ('v10 previous quarter labelled Q4 FY26', 'v10', [OP, REV, figure('Operating income $53,783 $44,474', '44,474', 'Q4 FY26')], True),
    ('v10 operating income refused by the check', 'v10', [figure('Operating income $53,783', '53,783', 'Q1 FY27', kept=False), REV], False),
    ('v10 operating income labelled FY26', 'v10', [figure('Operating income $53,783', '53,783', 'Q1 FY26'), REV], False),
    ('v10 plus non-GAAP net income 45,548 (2.4% from 44,474)', 'v10', [OP, REV, figure('Net income $45,548', '45,548', 'Q1 FY27')], True),
    ('v12 cash-flow row', 'v12', [CAPEX], True),
    ('v12 label only in the quote', 'v12', [figure(LABEL, '1,757', 'Q1 FY27')], False),
    ('v12 year-ago column labelled Q1 FY27', 'v12', [figure(f'{LABEL} (1,757) (1,227)', '(1,227)', 'Q1 FY27')], False),
    ('v12 plus other long-term liabilities 1,217', 'v12', [CAPEX, figure('Other long-term liabilities 1,217', '1,217', 'Q1 FY27')], True),
]


def main():
    wrong = 0
    for text, cases in ((TEXT, CHECK_CASES), (CFO, CFO_CASES)):
        for case, quote, value, expected in cases:
            got = br.kept_figures({'figures': [{'quote': quote, 'value': value}]}, text)[0]['kept']
            wrong += got != expected
            print(f'{"ok " if got == expected else "BAD"} check    {case}: kept {got}, must be {expected}')
    for case, view_id, figures, expected in DECISION_CASES:
        got = brm.delivered(view_id, figures)
        wrong += got != expected
        print(f'{"ok " if got == expected else "BAD"} decision {case}: delivered {got}, must be {expected}')
    total = len(CHECK_CASES) + len(CFO_CASES) + len(DECISION_CASES)
    print(f'\n{total} cases judged, {wrong} wrong')
    sys.exit(1 if wrong else 0)


if __name__ == '__main__':
    main()
