"""The three labelling rules tightened on 2026-10-24, each proven on a real stored row of the frozen window corpus
(read-only) with a positive and a negative control. Requirements: 02-classification 作者规则 3 and 4 (the author is
the party responsible for the content, not the channel; an unidentified author keeps the channel default), the
corpus plan's noise tier (Commerce Federal Register notices carry no object), and the POC rule that certification
and policy exhibits are 不算材料 (docs/poc/pipeline-plan.md, 语料标签收紧).

Run: python3 -m pytest poc/corpus/scripts/test_labels.py -q
"""
import json
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import assemble  # noqa: E402

FROZEN = os.path.join(HERE, '..', '..', 'data', 'items-window.sqlite')


def row_where(clause, params=()):
    conn = sqlite3.connect(f'file:{os.path.abspath(FROZEN)}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    row = conn.execute(f'select * from items where {clause} limit 1', params).fetchone()
    assert row is not None, f'no stored row for: {clause}'
    return dict(row)


def test_commerce_notice_carries_no_object_but_bis_and_ustr_do():
    mattress = row_where("topic='fr-commerce' and title like 'Mattresses From the People%'")
    assert assemble.official_objects('fr-commerce', mattress['title']) == []
    assert assemble.official_objects('fr-commerce', 'Semiconductor Products; Foreign-Trade Zone 75; Intel Corporation') == []
    assert [o['value'] for o in assemble.official_objects('fr-bis', 'Additions to the Entity List')] == ['chip-export-controls']
    assert [o['value'] for o in assemble.official_objects('fr-ustr', 'Section 301 Action')] == ['us-china-tariffs']


def test_certification_exhibits_are_not_material_and_results_exhibits_still_are():
    assert assemble.exhibit_category('10-Q', 'ex311.htm', 'nvda-10q.htm', 'EX-31.1', 'Certification of CEO', '', '') == (assemble.NOT_MATERIAL, 'certification')
    assert assemble.exhibit_category('10-K', 'ex21.htm', 'nvda-10k.htm', 'EX-21.1', 'Subsidiaries', '', '')[0] == assemble.NOT_MATERIAL
    primary = 'Item 2.02 Results of Operations. The press release is furnished as Exhibit 99.1. Item 9.01 Exhibits'
    assert assemble.exhibit_category('8-K', 'q1pr.htm', 'nvda-8k.htm', 'EX-99.1', 'Press release', '2.02,9.01', primary) == ('T1', 'release')
    assert assemble.exhibit_category('8-K', 'ex101.htm', 'nvda-8k.htm', 'EX-10.1', 'Material contract', '', '') == ('T3', 'filing')
    not_material = assemble.item(input_id='x', klass='公司材料', category=assemble.NOT_MATERIAL, publication_day='2026-08-01', coverage='full', text='x' * 500)
    assert not_material['feed'] == 0
    material = assemble.item(input_id='y', klass='公司材料', category='T6', publication_day='2026-08-01', coverage='full', text='x' * 500)
    assert material['feed'] == 1


def test_results_exhibit_named_in_the_item_202_body_not_the_table_of_contents():
    # Amazon's 8-K lists Item 2.02 in a table of contents before the body; the body names exhibits 99.1 and 99.2
    primary = row_where("input_id like 'edgar:0001018724-26-000024:%' and json_extract(extra, '$.exhibit_type') not like 'EX-%'")
    exhibit = row_where("input_id='edgar:0001018724-26-000024:amzn-20260630xex991.htm'")
    primary_name = primary['input_id'].rsplit(':', 1)[-1]
    assert assemble.exhibit_category('8-K', 'amzn-20260630xex991.htm', primary_name, 'EX-99.1', '', '2.02,9.01', primary['text'], exhibit['text']) == ('T1', 'release')
    # the same filing's body does not name a 99.3, so an exhibit of that number would stay an ordinary one
    assert assemble.exhibit_category('8-K', 'x.htm', primary_name, 'EX-99.3', '', '2.02,9.01', primary['text'], '') == ('T6', 'filing')


def test_6k_exhibit_with_a_bare_number_is_read_from_its_own_cover():
    tsm = row_where("input_id='edgar:0001046179-26-000541:a2026q2consolidatedreport-.htm'")
    assert assemble.exhibit_category('6-K', 'a2026q2consolidatedreport-.htm', 'tsm-6k.htm', 'EX-99.1', 'EX-99.1', '', '', tsm['text']) == ('T1', 'release')
    assert assemble.exhibit_category('6-K', 'x.htm', 'tsm-6k.htm', 'EX-99.1', 'Monthly revenue report', '', '', '') == ('T6', 'release')
    assert assemble.exhibit_category('6-K', 'x.htm', 'tsm-6k.htm', 'EX-99.1', 'EX-99.1', '', '', 'Notice of annual general meeting agenda and venue') == ('T6', 'filing')


def test_newsroom_release_is_results_only_when_it_reports_them():
    assert assemble.newsroom_category('NVIDIA Announces Financial Results for Second Quarter Fiscal 2027') == 'T1'
    assert assemble.newsroom_category('NVIDIA Sets Conference Call for Second-Quarter Financial Results') == 'T6'


def test_video_pages_are_not_full_articles():
    page = {'file': 'nonexistent', 'coverage': 'full'}
    assert assemble.page_texts(page, 'https://www.cnbc.com/video/2026/08/04/cramers-stop-trading-nvidia.html')[2] in ('video', 'none')
    assert assemble.VIDEO_PATH.search('/video/2026/08/04/x.html') and not assemble.VIDEO_PATH.search('/2026/08/04/nvidia-earnings.html')


def test_author_table_covers_company_newsrooms_and_research_sites():
    assert assemble.author_type('newsroom.ibm.com') == 'company'
    assert assemble.author_type('news.skhynix.com') == 'company'
    assert assemble.author_type('tikr.com') == 'analyst'
    assert assemble.author_type('cnbc.com') == 'media'
    assert assemble.author_type('some-unknown-site.example') == 'media'


def test_official_publisher_is_the_issuing_agency():
    assert assemble.official_publisher('fr-bis') == 'Bureau of Industry and Security'
    assert assemble.official_publisher('fr-commerce') == 'Department of Commerce'
    assert assemble.official_publisher('fed-speeches') == 'Federal Reserve Board'


def test_peer_themes_ride_only_on_results_reports_and_calls():
    values = lambda category: [o['value'] for o in assemble.objects_for_company('MSFT', ['ai-capex'], category)]
    assert values('T4') == ['MSFT', 'ai-capex'] and values('T1') == ['MSFT', 'ai-capex'] and values('T2') == ['MSFT', 'ai-capex']
    assert values('T6') == ['MSFT'] and values('T3') == ['MSFT'] and values(assemble.NOT_MATERIAL) == ['MSFT']


def test_a_listing_of_a_company_release_is_a_copy_of_the_original():
    original = {'input_id': 'nvblog:a', 'klass': '公司材料', 'source_uri': 'https://blogs.nvidia.com/blog/a/', 'publication_day': '2026-08-01', 'published_at': None, 'title': 'A', 'content_sha256': 'x', 'copy_of': None, 'publisher': 'NVIDIA Corporation'}
    listing = {'input_id': 'gnews:a', 'klass': '新闻', 'source_uri': 'https://blogs.nvidia.com/blog/a/?utm_source=google', 'publication_day': '2026-08-01', 'published_at': None, 'title': 'A | NVIDIA Blog', 'content_sha256': 'y', 'copy_of': None, 'publisher': 'blogs.nvidia.com'}
    other = {'input_id': 'gnews:b', 'klass': '新闻', 'source_uri': 'https://cnbc.com/b', 'publication_day': '2026-08-01', 'published_at': None, 'title': 'B', 'content_sha256': 'z', 'copy_of': None, 'publisher': 'cnbc.com'}
    assemble.mark_copies([listing, original, other])
    assert listing['copy_of'] == 'nvblog:a' and original['copy_of'] is None and other['copy_of'] is None


def test_aggregator_page_author_is_the_byline_outlet():
    fool_on_yahoo = row_where("publisher='finance.yahoo.com' and feed=1 and text like '%, The Motley Fool%'")
    assert assemble.byline_outlet(fool_on_yahoo['title'], fool_on_yahoo['text']) == 'fool.com'
    assert assemble.page_author('finance.yahoo.com', fool_on_yahoo['title'], fool_on_yahoo['text']) == ('fool.com', 'analyst', True)
    republished = row_where("publisher='finance.yahoo.com' and feed=1 and text like '%first appeared on GuruFocus%'")
    assert assemble.byline_outlet(republished['title'], republished['text']) == 'gurufocus.com'
    staff = row_where("publisher='finance.yahoo.com' and feed=1 and text like '%· Senior Business Reporter%'")
    assert assemble.byline_outlet(staff['title'], staff['text']) == ''
    assert assemble.page_author('finance.yahoo.com', staff['title'], staff['text']) == ('finance.yahoo.com', 'media', False)
    # a body that merely mentions outlets after a staff byline is never credited to them
    text = 'Head Nvidia rises Head Nvidia rises Ines Ferré · Senior Business Reporter July 28, 2026 · 2 min read NVDA. Reuters reported it. The Motley Fool likes it.'
    assert assemble.byline_outlet('Head Nvidia rises', text) == ''
    # a page that is not an aggregator keeps its own domain whatever its text says
    assert assemble.page_author('cnbc.com', 'Head', 'John Ballard, The Motley Fool July 1, 2026 · 3 min read') == ('cnbc.com', 'media', True)



def test_identical_text_at_different_urls_of_one_site_is_a_shell_not_an_article():
    """2026-10-27: a cut link served an outlet's archive page for 111 headlines; whole-page texts identical across URLs of one
    domain are the site's shell. Two outlets with the same text, or one URL listed twice, are not shells."""
    def row(input_id, url, sha, klass='新闻'):
        return {'input_id': input_id, 'source_uri': url, 'content_sha256': sha, 'klass': klass, 'coverage': 'full', 'feed': 1}
    rows = [row('a', 'https://247wallst.com/investing/2026/08/21/one', 'x'), row('b', 'https://247wallst.com/investing/2026/08/21/two', 'x'),
            row('c', 'https://reuters.com/one', 'y'), row('d', 'https://cnbc.com/one', 'y'),
            row('e', 'https://pymnts.com/one', 'z'), row('f', 'https://pymnts.com/one?utm_source=x', 'z')]
    marked, shells = assemble.mark_shells(rows)
    assert shells == 2 and [r['coverage'] for r in marked] == ['shell', 'shell', 'full', 'full', 'full', 'full']
    assert [r['feed'] for r in marked] == [0, 0, 1, 1, 1, 1]


def test_a_stored_resolved_link_is_cleaned_of_the_json_tail():
    from common import clean_resolved_url
    assert clean_resolved_url('https://finance.yahoo.com/a/b",1]') == 'https://finance.yahoo.com/a/b'
    assert clean_resolved_url('https://www.cnbc.com/x",1,"https://www.cnbc.com/amp/x') == 'https://www.cnbc.com/x'
    assert clean_resolved_url('https://www.ft.com/c?syn\\u003d1",1]') == 'https://www.ft.com/c?syn=1'
    assert clean_resolved_url('https://news.skhynix.com/en/x/') == 'https://news.skhynix.com/en/x/'


def test_a_binary_body_has_no_page_text():
    """2026-10-27: 116 fed rows of the three-month window were JPEG/PNG/GIF files and 7 were gzip streams served as pages; their
    bytes decoded as text passed the stub bar and were fed as full articles. A body that is not markup has no page text."""
    from common import decode, page_text
    jpeg = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01' + bytes(range(256)) * 40
    png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' + bytes(range(256)) * 40
    gzip_stream = b'\x1f\x8b\x08\x00' + bytes(range(256)) * 40
    assert page_text(decode(jpeg)) == '' and page_text(decode(png)) == '' and page_text(decode(gzip_stream)) == ''
    assert page_text(decode(b'<html><body><p>NVIDIA reported record data center revenue.</p></body></html>')) == 'NVIDIA reported record data center revenue.'


def test_truenorth_story_topics_label_tier_and_objects_like_a_listing():
    """A TrueNorth story (harvest_truenorth.py --events) is labelled by identity only: the asset selector that found it or the
    asset ids it carries, with that topic's tier and objects like a Google News listing; a text-query hit without a listed asset is
    no item; a record without selectors (the first NVDA harvest) stays nvda/core."""
    story = {'story_id': 'story_019fa144-e165-7c82-9e62-eda545606513', 'title': 'US Navy Transits Taiwan Strait as Beijing Tracks Flight',
             'summary': 'A US destroyer transited the Taiwan Strait ahead of the Xi-Trump meeting.', 'source': 'benzinga', 'publisher': 'benzinga',
             'source_url': 'https://www.benzinga.com/news/26/08/60700000/us-navy-transits-taiwan-strait', 'published_at': 1786795200000,
             'event_type': 'geopolitical_event', 'final_rank_score': 45, 'event_count': 1}
    by_query = {'story': story, 'retrieved_at': '2026-10-27T10:00:00+00:00', 'topics': ['geo-taiwan'], 'selectors': [{'topic': 'geo-taiwan', 'query': 'Taiwan Strait'}]}
    assert assemble.truenorth_story_row(by_query, {}) is None                     # a text query alone establishes no identity
    story_with_assets = dict(story, token_addresses=['stock_tsm', 'stock_fxi'])
    row = assemble.truenorth_story_row(dict(by_query, story=story_with_assets), {})
    assert row['topic'] == 'semis-tsmc' and row['tier'] == 'industry'
    assert [o['value'] for o in json.loads(row['object_identifiers'])] == ['TSM', 'semiconductor-cycle']
    assert row['coverage'] == 'provider_summary' and row['feed'] == 0 and row['publication_day'] == '2026-08-15'
    by_asset = {'story': story, 'retrieved_at': '2026-10-27T10:00:00+00:00', 'topics': ['geo-middle-east-oil'], 'selectors': [{'topic': 'geo-middle-east-oil', 'token_address': 'comm_wti'}]}
    assert assemble.truenorth_story_row(by_asset, {})['topic'] == 'geo-middle-east-oil'
    plain = assemble.truenorth_story_row({'story': story, 'retrieved_at': '2026-10-23T09:40:00+00:00'}, {})
    assert plain['topic'] == 'nvda' and plain['tier'] == 'core' and [o['value'] for o in json.loads(plain['object_identifiers'])] == ['NVDA']
