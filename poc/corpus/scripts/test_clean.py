"""Page cleaning before the pipeline reads a page (Alex, 2026-10-27: "你先清理干净html 还有一些垃圾吧 … 不要让我们的评估eval
会因为这些数据而被影响"). Three closed rules, each proven on a fixture with a positive and a negative control, and one
control on real stored pages: the three benchmark articles' hand-curated reporting lines (D338) survive cleaning.

Run: python3 -m pytest poc/corpus/scripts/test_clean.py -q
"""
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clean_pages  # noqa: E402

FROZEN = os.path.join(HERE, '..', '..', 'data', 'items-nvda-2026-07-01-10-27.sqlite')
STABILITY = os.path.join(HERE, '..', '..', 'reports', '2026-10-27-extraction-stability', 'inputs')

BODY = 'CoreWeave signed contracts for its A100 GPUs that run into 2029, chief executive Michael Intrator said on the call, and power constraints keep that capacity rented.'


def page(*lines):
    return '\n'.join(lines)


def test_a_line_repeated_in_three_pages_of_one_publisher_is_a_template_line_and_is_removed():
    rows = [{'input_id': f'p{i}', 'publisher': 'site.com', 'text': page('Join site today', f'Headline {i}', BODY + f' Page {i}.')} for i in range(3)]
    rows.append({'input_id': 'q1', 'publisher': 'other.com', 'text': page('Join site today', 'Other headline', BODY)})
    template = clean_pages.template_lines(rows)
    assert 'Join site today' in template['site.com']
    assert 'Headline 1' not in template['site.com']                 # appears on one page only
    assert 'Join site today' not in template.get('other.com', set())  # one page of another publisher
    kept = clean_pages.clean_lines(['Join site today', 'Headline 1', BODY], template['site.com'], article=True)
    assert kept == ['Headline 1', BODY]


def test_a_byline_survives_the_fragment_rule_and_a_bare_by_line_is_joined_with_its_name():
    assert clean_pages.clean_lines(['By', 'Luke James', 'Published', 'GO PREMIUM', BODY], set(), article=True) == ['By Luke James', BODY]
    assert clean_pages.clean_lines(['By Indranil Ghosh', 'Bytes and pieces', BODY], set(), article=True) == ['By Indranil Ghosh', BODY]
    assert clean_pages.clean_lines(['By', 'Luke James', BODY], {'By', 'Luke James'}, article=True) == ['By Luke James', BODY]   # a prolific author is not a template


def test_a_short_fragment_without_a_digit_or_end_punctuation_is_removed_from_an_article_only():
    lines = ['Skip to main content', 'GO PREMIUM', 'Revenue rose 56% to $46.7 billion', 'Key points:', 'By Alex Lee', BODY]
    assert clean_pages.clean_lines(lines, set(), article=True) == ['Revenue rose 56% to $46.7 billion', 'Key points:', 'By Alex Lee', BODY]
    assert clean_pages.clean_lines(lines, set(), article=False) == lines   # a filing or notice keeps its short cells


def test_a_line_without_a_letter_and_a_line_repeated_in_the_same_page_are_removed_from_an_article():
    lines = ['Nvidia stock sinks as chip sell-off deepens', '7,675.94', '+52.26 +0.69%', 'Nvidia stock sinks as chip sell-off deepens', BODY, 'Revenue rose 56% to $46.7 billion', BODY]
    assert clean_pages.clean_lines(lines, set(), article=True) == ['Nvidia stock sinks as chip sell-off deepens', BODY, 'Revenue rose 56% to $46.7 billion']
    assert clean_pages.clean_lines(['Revenue', '46,743', '46,743'], set(), article=False) == ['Revenue', '46,743', '46,743']   # a filing's table keeps its cells


def test_a_consent_or_promotion_sentence_is_not_a_byline_and_is_removed():
    junk = ['By submitting your information you agree to the Terms & Conditions and Privacy Policy and are aged 16 or over.',
            'By subscribing, you agree to our Terms of Service and Privacy Policy.', 'By —',
            'This material may not be published, broadcast, rewritten, or redistributed. ©2026 FOX News Network, LLC. All rights reserved.',
            'Justin Pope has positions in Microsoft. The Motley Fool has positions in and recommends Microsoft and Nvidia.',
            '*Stock Advisor returns as of July 2, 2026.', 'Read more: The Sub-$1 Pre-IPO AI Stock That Could Make People "Superhuman"',
            'Johannes Neudecker | Picture Alliance | Getty Images', '(Image credit: Intel)', 'Sign up for our newsletter.',
            'Add Us On Google Add as a preferred source on Google', 'Click here to learn more about our approach to artificial intelligence.',
            'We use cookies to ensure that we give you the best experience on our website.', 'Tags:', '0 Comments', 'Link copied!', 'Loading...',
            'For premium support please call:', 'Enter your Mastodon instance URL (optional)', '800 - 290 - 4726 more ways to reach us',
            'The Motley Fool Stock Advisor analyst team just identified what they believe are the 10 best stocks for investors to buy now.', 'View all posts by William Markito Oliveira',
            'This site requires JavaScript to run correctly. Please turn on JavaScript or unblock scripts', '[email protected]', 'X (Twitter)', 'Share:', 'U.S. markets close in 1h 39m']
    assert clean_pages.clean_lines(junk + [BODY], set(), article=True) == [BODY]
    prose = ['NVIDIA has dropped the subscription requirement for Omniverse, the company said on Tuesday.',
             'Microsoft\'s impressive track record typically earns it a premium valuation, the analyst wrote.',
             'By Alex Veiga | The Associated Press •', 'By Associated Press', 'By Harsh Chauhan – Jul 14, 2026 at 9:15AM EST', BODY]
    assert clean_pages.clean_lines(prose, set(), article=True) == prose


def test_a_date_or_reading_time_line_and_a_run_of_unpunctuated_short_lines_are_removed_keeping_lines_with_digits():
    lines = ['October 26, 2026', '2 min read', '2 hours ago', 'Published Thu, Oct 22 2026 9:12 AM EDT', 'Updated on September 2, 2026 at 8:32 am', BODY]
    assert clean_pages.clean_lines(lines, set(), article=True) == [BODY]
    sidebar = ['Anthropic files for IPO as it competes for AI dominance', 'AI agents detected inside customer bank accounts, report says',
               'Anthropic previews Claude Duet personal AI agent for subscribers', 'Massive NIS 5.75m fraud uncovered by police']
    assert clean_pages.clean_lines([BODY] + sidebar + [BODY + ' Again.'], set(), article=True) == [BODY, 'Massive NIS 5.75m fraud uncovered by police', BODY + ' Again.']
    two = ['Rivals fall short of what the Gulf needs today', 'Billions are not enough to escape Nvidia now']   # two subheadings are not a list
    assert clean_pages.clean_lines([BODY] + two + [BODY + ' Again.'], set(), article=True) == [BODY] + two + [BODY + ' Again.']


def test_template_lines_are_counted_over_original_pages_not_their_copies():
    body = BODY + ' Only here.'
    rows = [{'input_id': 'a', 'publisher': 'site.com', 'copy_of': None, 'text': page('Headline', body)},
            {'input_id': 'b', 'publisher': 'site.com', 'copy_of': 'a', 'text': page('Headline', body)},
            {'input_id': 'c', 'publisher': 'site.com', 'copy_of': 'a', 'text': page('Headline', body)}]
    assert clean_pages.template_lines(rows)['site.com'] == set()


HTML = """<html><head><title>CoreWeave signs A100 contracts into 2029</title></head><body>
<nav><a href="/">Skip to main content</a><a href="/join">Join Tom's Hardware today</a></nav>
<article><h1>CoreWeave signs A100 contracts into 2029</h1><p class="byline">By Luke James</p>
<p>CoreWeave signed contracts for its A100 GPUs that run into 2029, chief executive Michael Intrator said on the call, and power constraints keep that capacity rented across the fleet.</p>
<p>The company reported quarterly revenue of $1.21 billion, up 112% from a year earlier, and a backlog of $104 billion at the end of the quarter, which it said excludes contracts signed since July.</p>
</article>
<section class="related"><h3>Related</h3><ul><li><a href="/a">Nvidia reportedly insists the RTX 5090 isn't dead despite severe shortages and rumours</a></li>
<li><a href="/b">Modder gets DLSS 5 working on AMD GPUs</a></li><li><a href="/c">Nvidia returns to selling Founders Edition cards at MSRP</a></li></ul></section>
<div class="comments"><p>I would just turn the chip off during launch and turn it back on during flight, honestly that is what I would do with it.</p></div>
<footer><p>Privacy policy</p><p>© 2026 Future US, Inc.</p></footer></body></html>"""
TAIL = 'Analysts at Morgan Stanley estimated the renewal rate at 30% of the installed base, which the company disputed on the call as too low a figure.'


def test_the_article_body_comes_from_the_html_extractor_and_a_dropped_tail_paragraph_is_re_added_from_the_page_text():
    page_lines = ['CoreWeave signs A100 contracts into 2029', 'Skip to main content', "Join Tom's Hardware today", 'By Luke James',
                  'CoreWeave signed contracts for its A100 GPUs that run into 2029, chief executive Michael Intrator said on the call, and power constraints keep that capacity rented across the fleet.',
                  'The company reported quarterly revenue of $1.21 billion, up 112% from a year earlier, and a backlog of $104 billion at the end of the quarter, which it said excludes contracts signed since July.',
                  TAIL, 'Related', "Nvidia reportedly insists the RTX 5090 isn't dead despite severe shortages and rumours", 'Modder gets DLSS 5 working on AMD GPUs',
                  'Nvidia returns to selling Founders Edition cards at MSRP', 'I would just turn the chip off during launch and turn it back on during flight, honestly that is what I would do with it.',
                  'Privacy policy', '© 2026 Future US, Inc.']
    kept = clean_pages.clean_article(page_lines, HTML, set())
    text = '\n'.join(kept)
    assert 'CoreWeave signed contracts for its A100 GPUs' in text and 'backlog of $104 billion' in text
    assert TAIL in text                                                        # on the page, missing from the extractor: re-added
    assert 'Skip to main content' not in text and 'Privacy policy' not in text and '© 2026' not in text
    assert 'RTX 5090' not in text                                              # a related headline is not in the article element
    assert 'Analysts' in text and kept.index(TAIL) > kept.index('The company reported quarterly revenue of $1.21 billion, up 112% from a year earlier, and a backlog of $104 billion at the end of the quarter, which it said excludes contracts signed since July.')


def test_a_forward_looking_statement_paragraph_and_a_read_also_link_are_removed_from_an_article():
    fls = 'Statements in this release that are not strictly historical, including statements regarding the collaboration, are forward-looking statements within the meaning of the federal securities laws and involve risks and uncertainties that could cause actual results to differ materially from those expressed or implied by such statements, including the risks described in the filings. ' * 2
    lines = [BODY, fls.strip(), 'READ ALSO: Nvidia Is Backing This AI IPO Candidate. It Lost $1 Billion in Just 6 Months', "Also read: Nvidia RTX Spark laptops offer another approach to local AI.", BODY + ' Again.']
    assert clean_pages.clean_lines(lines, set(), article=True) == [BODY, BODY + ' Again.']
    assert clean_pages.clean_lines([fls.strip()], set(), article=False) == [fls.strip()]      # a release keeps its legal paragraph


def test_a_page_left_without_a_body_is_not_fed():
    assert clean_pages.has_body(['Important disclaimers apply to everything on this site, which is operated by a company registered abroad and so on.'] * 2) is False
    assert clean_pages.has_body([BODY, BODY + ' Again.', BODY + ' And again.']) is True


def test_cleaning_a_database_writes_a_dated_copy_with_the_page_kept_and_the_feed_flag_updated(tmp_path):
    src = tmp_path / 'items.sqlite'
    conn = sqlite3.connect(str(src))
    conn.execute('create table items (input_id text primary key, publisher text, document_format text, feed integer, coverage text, text text, text_chars integer, title text, category text)')
    for i in range(3):
        conn.execute('insert into items values (?,?,?,?,?,?,?,?,?)', (f'p{i}', 'site.com', 'article', 1, 'full', page('Join site today', f'Headline {i}', BODY + f' Page {i}.', BODY + f' Again on page {i}.', BODY + f' And again on page {i}.'), 0, f'Headline {i}', 'T7'))
    conn.execute('insert into items values (?,?,?,?,?,?,?,?,?)', ('shell', 'site.com', 'article', 1, 'full', page('Join site today', 'Headline', 'Subscribe to read the full story and more from our premium service team today'), 0, 'Headline', 'T7'))
    conn.execute('insert into items values (?,?,?,?,?,?,?,?,?)', ('filing', 'EDGAR', 'filing', 1, 'full', page('Item 1.', 'Revenue', '46,743'), 0, '10-Q', 'T2'))
    conn.commit(); conn.close()
    dst = tmp_path / 'items-cleaned.sqlite'
    census = clean_pages.clean_database(str(src), str(dst), raw_root=str(tmp_path))
    out = sqlite3.connect(str(dst)); out.row_factory = sqlite3.Row
    p0 = out.execute("select * from items where input_id='p0'").fetchone()
    assert p0['text'] == page('Headline 0', BODY + ' Page 0.', BODY + ' Again on page 0.', BODY + ' And again on page 0.') and p0['text_chars'] == len(p0['text'])
    assert p0['text_page'].startswith('Join site today') and p0['feed'] == 1
    shell = out.execute("select * from items where input_id='shell'").fetchone()
    assert shell['feed'] == 0 and shell['coverage'] == 'none'
    filing = out.execute("select * from items where input_id='filing'").fetchone()
    assert filing['text'] == page('Item 1.', 'Revenue', '46,743') and filing['feed'] == 1
    assert census['pages'] == 5 and census['unfed'] == 1
    assert sqlite3.connect(str(src)).execute("select text from items where input_id='p0'").fetchone()[0].startswith('Join site today')   # the source is untouched


def test_the_benchmark_articles_keep_every_curated_reporting_line_after_cleaning():
    conn = sqlite3.connect(f'file:{os.path.abspath(FROZEN)}?mode=ro', uri=True); conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute('select input_id, publisher, document_format, copy_of, source_uri, coalesce(text_page, text) as text from items')]   # the page, whether the database is cleaned or not
    template = clean_pages.template_lines(rows)
    pages = {r['input_id']: r for r in rows}
    index = clean_pages.pages_index(os.path.join(HERE, '..', 'raw'))
    norm = lambda s: re.sub(r'\s+', ' ', s).strip()
    for name, input_id in [('coreweave', 'gnews:011203b517e045ffe773b1fb'), ('motley', 'gnews:dadd84590540a466aea01b3c'), ('restofworld', 'gnews:01a49ffd41f6abe24538da65')]:
        row = pages[input_id]
        html = clean_pages.html_of(row, index)
        assert html, f'{name}: stored html not found'
        kept = clean_pages.clean_article(row['text'].split('\n'), html, template[row['publisher']])
        cleaned = norm('\n'.join(kept))
        curated = [norm(l) for l in open(os.path.join(STABILITY, f'{name}.clean.txt'), encoding='utf-8') if l.strip()]
        # the reporting lines and the byline must survive; the curated files also hold subheadings ("Rivals fall short"),
        # captions ("Data by YCharts") and the bare date line, which the fragment and template rules remove knowingly
        # the page's headline line goes with the page-top run (the item header carries the title)
        reporting = [l for l in curated if (len(l) >= 40 or l.startswith('By')) and l != norm(row['text'].split('\n')[0])]
        missing = [l for l in reporting if l not in cleaned and not (l == 'By' and 'By ' in cleaned)]
        assert missing == [], f'{name}: {len(missing)} reporting lines lost, first: {missing[0][:80]}'
        assert re.search(r'(^|\n)By [A-Z]', '\n'.join(kept)), f'{name}: byline lost'
        assert clean_pages.has_body(kept)
        junk = {'coreweave': 'Skip to main content', 'motley': 'Data by YCharts', 'restofworld': 'Skip to content'}[name]
        assert junk in clean_pages.lines_of(row['text']) and junk not in kept, f'{name}: {junk!r} survived'
