"""The takes lines (D259, D268, D274): what each open question collects, written by code from its key and its research group, beside the
question in the extraction request. A numeric line names only its quantity, scope and period; what makes the figure more or less likely
(the four paths) and the other-period allowance are stated once, in the links field's rule. The fixtures here are one real news item and
two of its statements, shared by the extraction tests. The universe file the pipeline reads."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import placement, universe  # noqa: E402

UNI = universe.load(os.path.join(ROOT, 'poc', 'universe.json'))
TEXT = ('Nvidia said on Aug 10 it has partnered six major financial institutions to launch compute financing platforms aimed at raising more than '
        'US$500 billion in third-party capital for AI infrastructure. In May, Nvidia chief financial officer Colette Kress said the H200 chips had yet to '
        'generate any revenue for the company in China. Nvidia shares climbed 3.7 per cent on July 8.')
ITEM = {'input_id': 'gnews:deb37e6ad15fb74d545ca368', 'category': 'T7', 'publication_day': '2026-08-10', 'publisher': 'straitstimes.com', 'publisher_type': 'media',
        'title': 'Nvidia partners Wall Street giants to raise $640 billion for AI infrastructure', 'object_identifiers': [{'kind': 'ticker', 'value': 'NVDA'}], 'text': TEXT}
PLATFORM = {'id': 'e1', 'quote': 'Nvidia said on Aug 10 it has partnered six major financial institutions to launch compute financing platforms aimed at raising more than US$500 billion in third-party capital for AI infrastructure.',
            'one_line': 'NVIDIA partnered six institutions to raise over $500bn for AI infrastructure.', 'speaker': 'NVIDIA', 'original_who': 'NVIDIA', 'original_day': '2026-08-10', 'tier': 'party_statement', 'event_time': '', 'links': []}
KRESS = {'id': 'e2', 'quote': 'Nvidia chief financial officer Colette Kress said the H200 chips had yet to generate any revenue for the company in China.',
         'one_line': 'CFO Kress said H200 had generated no China revenue as of May.', 'speaker': 'Colette Kress', 'original_who': 'NVIDIA CFO Colette Kress', 'original_day': '', 'tier': 'party_statement', 'event_time': '', 'links': ['v9']}


def test_d259_a_file_takes_the_evidence_that_bears_on_its_answer_not_only_its_own_figures():
    """D259 (Alex, 2026-11-02: 先放宽 takes，辅助是中间地带，给点 leeway): what makes a figure more or less likely (demand, supply, competition,
    pricing, D250 item 2's four paths) is filed under it, with no size required; D274 states that once, in the links field's rule, so a figure
    question's line names its quantity, scope and period only; an event file takes the event's variants and stopgaps or its counterparties'
    plans; a policy file takes enforcement, evasion and the affected parties' plans."""
    figure = placement.takes({'view_id': 'v1', 'kind': 'asset', 'key': {'measure': 'total_revenue', 'scope': 'FY2027 total revenue', 'period_start': '2026-02-01', 'period_end': '2027-01-31'}})
    assert figure == "takes: total_revenue figures, guidance, estimates and revisions for FY2027 total revenue, this question's period 2026-02-01..2027-01-31"
    assert 'the demand, supply, competition or pricing behind its answer' in placement.FILING_RULE_ROOT_FALLBACK
    assert 'an estimate for another period or population of a question\'s quantity is filed under it' in placement.FILING_RULE_ROOT_FALLBACK
    assert 'variants and stopgaps' in placement.takes({'view_id': 'v2', 'key': {'measure': 'event', 'event_type': 'shipment', 'scope': 'Rubin Ultra'}})
    assert "counterparties' own plans, financing and demand" in placement.takes({'view_id': 'v3', 'key': {'measure': 'event', 'event_type': 'signing', 'scope': 'Ohio lease guarantee'}})
    policy = placement.takes({'view_id': 'v4', 'key': {'measure': 'policy_event', 'scope': 'H200 import authorization'}})
    assert 'its enforcement and evasion' in policy and "the affected parties' own plans and statements about it" in policy
