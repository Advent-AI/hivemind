"""Run inputs through the input classification rules and report every input whose outcome is not the expected one.

The classifier below implements the rules exactly as the New tab's classification module states them
(docs/system-design/new-classification.js): first the intake resolves the author from the channel, then the tree gives
one outcome, a tag, "not an input" or a refusal. Three populations run through it:

1. the real sources stored in the old system's latest ledger (read only);
2. the TrueNorth MCP's 54 data tools, each as a structured dataset;
3. hand-written cases covering every tag and the boundaries between them, each with the outcome an analyst expects.

A check at the end compares the tags here with the page's, so the two cannot drift apart unnoticed.

    python3 docs/system-design/simulate_classification.py
"""

import collections
import json
import re
import sqlite3
import sys
from pathlib import Path
from urllib.parse import urlparse

PAGE_DIRECTORY = Path(__file__).resolve().parent
OLD_REPOSITORY = PAGE_DIRECTORY.parents[2] / "tn-hivemind"
OLD_LEDGER = OLD_REPOSITORY / ".runtime" / "v4" / "shadow-2026-10-14.sqlite3"
OLD_SOURCE_REGISTRY = OLD_REPOSITORY / "config" / "sources" / "registry-v3.json"

REFUSED = "refused"
NOT_INPUT = "not_input"

# ------------------------------------------------------------------ the rules

REQUIRED_FIELDS = ("input_id", "content_sha256", "channel", "source_uri", "publisher", "published_at", "retrieved_at",
                   "is_structured", "media_type", "language")
NON_TEXT_MEDIA = ("audio", "video", "image")

# Each filing system's closed category table: form or category code → the kind of document it is (rule 5).
FILING_GENRES = {
    "EDGAR": {
        **{form: "periodic" for form in ("10-K", "10-Q", "20-F", "40-F", "ARS")},
        **{form: "legal_capital" for form in ("DEF 14A", "DEFA14A", "DEFM14A", "DEFC14A", "DFAN14A", "PRE 14A", "PREC14A",
                                              "S-1", "S-3", "S-4", "F-1", "F-3", "F-4", "424B2", "424B3", "424B5",
                                              "SC TO-I", "SC TO-T", "SC 14D9")},
        "425": "merger_communication",
        **{form: "current" for form in ("8-K", "6-K")},
        "UPLOAD": "official_record",
        **{form: "ownership" for form in ("4", "SC 13D", "SC 13G", "13F-HR", "144")},
        **{form: "other" for form in ("CORRESP", "NT 10-K", "NT 10-Q", "11-K")},
    },
    "HKEX": {"results announcement": "results", "annual report": "periodic", "interim report": "periodic",
             "circular": "legal_capital", "prospectus": "legal_capital", "announcement": "other"},
    "TWSE": {"monthly revenue": "other", "financial report": "periodic"},
    "COURT": {"complaint": "official_record", "motion": "official_record", "opinion": "official_record"},
}
LEGAL_EXHIBIT_TYPES = ("2", "3", "4", "10")          # Item 601: acquisition, charter, instruments, material contracts
FISCAL_RESULTS = re.compile(r"\b(q[1-4]|quarter|quarterly|half|interim|annual|full[- ]year|fiscal)\b.*\bresults\b|\bresults\b.*\b(quarter|fiscal)\b",
                            re.IGNORECASE)
MONETARY_OR_STATISTICS_SERIES = ("monetary_policy", "economic_statistics")
# Rule 3: the author type a channel vouches for when the registry has no row.
CHANNEL_DEFAULT_TYPES = {"news_index": "media", "wire": "company", "data_room": "company",
                         "contributor_platform": "individual", "newsletter_platform": "individual",
                         "x": "individual", "reddit": "individual", "linkedin": "individual", "substack": "individual"}


def base_form(form):
    """An amendment has its original form's kind: '10-K/A' → '10-K'."""
    return form[:-2] if form.endswith("/A") else form


def resolve_author(raw):
    """Intake: the author is the party answerable for the content, never the channel (rules 2 and 4)."""
    envelope = dict(raw)
    organizer = envelope.get("event_organizer")
    if organizer in ("company", "investor_conference"):
        envelope["publisher"] = envelope["presenting_company"]
    elif organizer in ("media", "official", "expert_network", "user"):
        envelope["publisher"] = envelope["host"]
    if envelope.get("wire_issuer"):                        # a wire or a press-release reprint carries the issuer's release
        envelope["publisher"] = envelope["wire_issuer"]
    if envelope.get("platform_author"):                    # a platform post or article: the account or contributor
        envelope["publisher"] = envelope["platform_author"]
    return envelope


def filing_kind(envelope):
    """Rule 5: a filed document gets its kind from its filing system's table, whoever filed it."""
    system = envelope["filing_system"]
    form = base_form(envelope.get("filing_form") or "")
    genre = FILING_GENRES.get(system, {}).get(form) or FILING_GENRES.get(system, {}).get(form.lower())
    if genre is None:
        return REFUSED, "表格代码不在映射表"
    exhibit = envelope.get("exhibit") or ""
    exhibit_type = exhibit.split(".")[0] if exhibit else ""
    if form == "8-K" and exhibit and exhibit in envelope.get("item_202_exhibits", []):
        return "T1", "filing: named under Item 2.02"
    if form == "6-K" and exhibit_type == "99" and FISCAL_RESULTS.search(envelope.get("exhibit_description", "")):
        return "T1", "filing: 6-K fiscal results"
    if exhibit_type in LEGAL_EXHIBIT_TYPES:
        return "T3", "filing: legal exhibit"
    if genre == "ownership":
        return ("T8", "filing: investor letter") if envelope.get("document_format") == "letter" else ("T13", "filing: merged into its structured version")
    if genre == "merger_communication":
        return {"transcript": ("T4", "filing: 425 call"), "slides": ("T5", "filing: 425 deck")}.get(
            envelope.get("document_format"), ("T3", "filing: 425"))
    return {"results": ("T1", "filing"), "periodic": ("T2", "filing"), "legal_capital": ("T3", "filing"),
            "official_record": ("T10", "filing")}.get(genre) or \
        (("T5", "filing: deck") if envelope.get("document_format") == "slides" else ("T6", "filing: other"))


def company_kind(envelope):
    """The company branch for documents outside any filing system, in order."""
    category = envelope.get("channel_category")
    if category in ("results", "periodic", "legal"):
        return {"results": "T1", "periodic": "T2", "legal": "T3"}[category], f"company: category {category}"
    if envelope.get("document_format") == "transcript":
        return "T4", "company ④"
    if envelope.get("document_format") == "slides":
        return "T5", "company ⑤"
    return "T6", "company ⑥"


def classify(raw, publisher_registry, dataset_map):
    """Return (outcome, reason): a tag (a copy gets its original's), NOT_INPUT or REFUSED."""
    envelope = resolve_author(raw)
    missing = [field for field in REQUIRED_FIELDS if envelope.get(field) in (None, "")]
    if missing:
        return REFUSED, "必填字段缺失：" + ", ".join(missing)
    if malformed_identifiers(envelope):
        return REFUSED, "公司标识的格式或依据不在闭集"
    if envelope.get("produced_by_system"):
        return REFUSED, "系统自己的产出"
    if envelope.get("copy_of_tag"):
        return envelope["copy_of_tag"], "并入原件"
    if envelope.get("channel") == "upload" and not (envelope.get("dataset") or envelope.get("declared")):
        return REFUSED, "上传未声明体裁或模板"
    if envelope["is_structured"]:
        outcome = dataset_map.get(envelope.get("dataset"))
        return (outcome, "dataset") if outcome else (REFUSED, "数据集未映射")
    if envelope["media_type"].split("/")[0] in NON_TEXT_MEDIA or envelope.get("has_readable_text") is False:
        return REFUSED, "没有可读文本"
    if envelope.get("filing_system"):
        return filing_kind(envelope)
    publisher_type = publisher_registry.get(envelope["publisher"]) or CHANNEL_DEFAULT_TYPES.get(envelope.get("channel"))
    if publisher_type is None:
        return REFUSED, "作者类型定不了"
    if publisher_type == "company":
        return company_kind(envelope)
    if publisher_type == "media":
        return ("T8", "media ①") if envelope.get("channel_category") in ("opinion", "analysis") else ("T7", "media ②")
    if publisher_type == "analyst":
        return ("T9", "analyst ①") if envelope.get("document_format") in ("transcript", "call_notes") else ("T8", "analyst ②")
    if publisher_type == "official":
        return ("T11", "official ①") if envelope.get("series") in MONETARY_OR_STATISTICS_SERIES else ("T10", "official ②")
    if publisher_type == "individual":
        return "T8", "individual"
    return REFUSED, "未知作者类型"


# ------------------------------------------------------------------ related companies (the page's COMPANY_RULES)

# The closed sets of a company identifier the channel adapter writes: {scheme, value, basis}.
COMPANY_SCHEMES = ("cik", "ticker", "name")
COMPANY_BASES = ("filing_subject", "filer", "record_field", "channel_tag", "query", "declared")
AUTHOR_COMPANY = "author_company"   # added by the rules, never written by the adapter

APPLE, AMAZON, META = "issuer:sec:0000320193", "issuer:sec:0001018724", "issuer:sec:0001326801"
NVIDIA, TESLA, TSMC = "issuer:sec:0001045810", "issuer:sec:0001318605", "issuer:sec:0001046179"
MICROSOFT, ACTIVISION, XIAOMI = "issuer:sec:0000789019", "issuer:sec:0000718877", "issuer:hkex:1810"

# The reference data (T16) the resolution reads: (scheme, identifier, entity id, first day, last day). A ticker names an
# entity only between its dates; a name resolves only when it is a registered alias.
REFERENCE = [
    ("cik", "0000320193", APPLE, None, None), ("ticker", "AAPL", APPLE, None, None),
    ("name", "Apple", APPLE, None, None), ("name", "Apple Inc.", APPLE, None, None),
    ("cik", "0001018724", AMAZON, None, None), ("ticker", "AMZN", AMAZON, None, None),
    ("name", "Amazon", AMAZON, None, None), ("name", "Amazon.com, Inc.", AMAZON, None, None),
    ("cik", "0001326801", META, None, None), ("ticker", "FB", META, None, "2022-06-08"),
    ("ticker", "META", META, "2022-06-09", None),
    ("name", "Meta", META, None, None), ("name", "Meta Platforms, Inc.", META, None, None),
    ("cik", "0001045810", NVIDIA, None, None), ("ticker", "NVDA", NVIDIA, None, None), ("name", "NVIDIA", NVIDIA, None, None),
    ("cik", "0001318605", TESLA, None, None), ("ticker", "TSLA", TESLA, None, None), ("name", "Tesla", TESLA, None, None),
    ("cik", "0001046179", TSMC, None, None), ("ticker", "TSM", TSMC, None, None), ("name", "TSMC", TSMC, None, None),
    ("cik", "0000789019", MICROSOFT, None, None), ("ticker", "MSFT", MICROSOFT, None, None),
    ("name", "Microsoft", MICROSOFT, None, None),
    ("cik", "0000718877", ACTIVISION, None, None), ("name", "Activision Blizzard", ACTIVISION, None, None),
    ("ticker", "1810.HK", XIAOMI, None, None), ("name", "Xiaomi", XIAOMI, None, None),
]


def malformed_identifiers(envelope):
    """The company identifiers outside the closed sets (a malformed envelope is refused, never half-read)."""
    return [identifier for identifier in envelope.get("company_identifiers") or []
            if not isinstance(identifier, dict) or identifier.get("scheme") not in COMPANY_SCHEMES
            or identifier.get("basis") not in COMPANY_BASES or not str(identifier.get("value") or "").strip()]


def normalized_identifier(scheme, value):
    """A CIK padded to ten digits, a ticker in capitals, a name as written (aliases match exactly)."""
    value = str(value).strip()
    return {"cik": value.zfill(10), "ticker": value.upper(), "name": value}[scheme]


def resolve_identifier(scheme, value, day, reference):
    """The entity id the identifier named on ``day`` (YYYY-MM-DD), or None."""
    wanted = normalized_identifier(scheme, value)
    for reference_scheme, reference_value, entity_id, first_day, last_day in reference:
        if reference_scheme == scheme and reference_value == wanted and (first_day is None or day >= first_day) \
                and (last_day is None or day <= last_day):
            return entity_id
    return None


def related_companies(raw, outcome, publisher_registry, reference):
    """({entity id: [bases]}, [unresolved identifiers]) of one input: every identifier the channel gave, and the author
    when the author is a company. A refused input or one that is not an input has none."""
    if outcome in (REFUSED, NOT_INPUT):
        return {}, []
    envelope = resolve_author(raw)
    identifiers = list(envelope.get("company_identifiers") or [])
    author_type = publisher_registry.get(envelope["publisher"]) or CHANNEL_DEFAULT_TYPES.get(envelope.get("channel"))
    if author_type == "company":
        identifiers.append({"scheme": "name", "value": envelope["publisher"], "basis": AUTHOR_COMPANY})
    day = envelope["published_at"][:10]
    companies, unresolved = {}, []
    for identifier in identifiers:
        entity_id = resolve_identifier(identifier["scheme"], identifier["value"], day, reference)
        if entity_id is None:
            unresolved.append(identifier)
        elif identifier["basis"] not in companies.setdefault(entity_id, []):
            companies[entity_id].append(identifier["basis"])
    return companies, unresolved


# ------------------------------------------------------------------ population 3: hand-written cases

PUBLISHERS = {
    "Apple": "company", "Meta": "company", "Amazon": "company", "NVIDIA": "company", "Tesla": "company",
    "TSMC": "company", "Xiaomi": "company", "Acme Robotics (private)": "company", "Rosen Law Firm": "company",
    "S&P Dow Jones Indices": "company",
    "Reuters": "media", "Benzinga": "media", "CNBC": "media", "DigiTimes": "media", "WSJ": "media",
    "@Apple": "company", "@Reuters": "media", "@federalreserve": "official", "@elonmusk": "individual",
    "Morgan Stanley": "analyst", "Goldman Sachs": "analyst", "Moody's": "analyst", "IDC": "analyst", "Brookings": "analyst",
    "Hindenburg Research": "analyst", "Elliott Management": "analyst", "Greenlight Capital": "analyst", "Tegus": "analyst",
    "Blackstone": "analyst", "User": "analyst",
    "SA contributor: Tech Bull": "individual", "Fabricated Knowledge (Substack)": "individual", "Jane Doe (CEO)": "individual",
    "Federal Reserve": "official", "BLS": "official", "European Commission": "official", "FTC": "official",
    "US District Court": "official", "BIS (Commerce)": "official", "White House": "official", "US Senate": "official",
    "NYSE": "official", "FDA": "official", "SEC": "official", "PBOC": "official",
}

DATASETS = {
    "mcp:financial_statements": "T2", "mcp:financial_segmented_revenue": "T2", "sec:companyfacts": "T2",
    "company:ir_supplement": "T6",
    "mcp:historical_bars": "T12", "vendor:options_chain": "T12", "mcp:polymarket_insight": "T12",
    "mcp:financial_analyst_estimates": "T8", "vendor:credit_ratings": "T8", "upload:estimates": "T8",
    "edgar:form4": "T13", "edgar:13f": "T13", "finra:short_interest": "T13", "cftc:cot": "T13",
    "mcp:financial_earnings_calendar": "T14", "mcp:financial_economic_calendar#date": "T14",
    "mcp:financial_economic_calendar#forecast": "T8", "mcp:financial_economic_calendar#actual": "T11",
    "fred:cpi": "T11", "alfred:gdp": "T11", "vendor:card_spend": "T15", "usaspending:awards": "T10", "uspto:grants": "T10",
    "msci:gics": "T16", "mcp:technical_analysis": NOT_INPUT, "mcp:financial_metrics": NOT_INPUT,
    "edgar:filing_index": NOT_INPUT,
}


def envelope(**fields):
    """A complete envelope with the given fields; a case overrides or blanks what it probes."""
    base = {"input_id": "case", "content_sha256": "sha", "channel": "test", "source_uri": "uri", "publisher": "Apple",
            "published_at": "2026-07-30T20:30:00Z", "retrieved_at": "2026-07-30T21:00:00Z", "is_structured": False,
            "media_type": "html", "language": "en", "document_format": "article"}
    base.update(fields)
    return base


def identifier(scheme, value, basis):
    return {"scheme": scheme, "value": value, "basis": basis}


def edgar(form, items=(), exhibit="", description="", named_under_202=(), **fields):
    """An EDGAR document; its header names the filer (the envelope's publisher unless the case gives identifiers)."""
    filer = [identifier("name", fields.get("publisher", "Apple"), "filer")]
    return envelope(filing_system="EDGAR", filing_form=form, filing_items=list(items), exhibit=exhibit,
                    exhibit_description=description, item_202_exhibits=list(named_under_202), channel="edgar",
                    document_format=fields.pop("document_format", "report"),
                    company_identifiers=fields.pop("company_identifiers", filer), **fields)


def data(dataset, **fields):
    return envelope(is_structured=True, dataset=dataset, media_type=fields.pop("media_type", "json"),
                    publisher=fields.pop("publisher", "vendor"), **fields)


def spoken(organizer, **fields):
    return envelope(document_format="transcript", event_organizer=organizer, **fields)


# (case, envelope, expected outcome, what the expectation rests on)
CASES = [
    # EDGAR filings: by the filing table, whoever filed them (rule 5)
    ("10-K", edgar("10-K"), "T2", ""),
    ("10-K/A amendment", edgar("10-K/A", supersedes="10-K"), "T2", "rule 5: /A has its form's kind"),
    ("10-Q", edgar("10-Q"), "T2", ""),
    ("10-Q/A amendment", edgar("10-Q/A"), "T2", ""),
    ("20-F (TSMC)", edgar("20-F", publisher="TSMC"), "T2", ""),
    ("ARS glossy annual report", edgar("ARS"), "T2", ""),
    ("10-K EX-10.1 credit agreement", edgar("10-K", [], "10.1", "Credit Agreement"), "T3", "an exhibit has its own kind"),
    ("8-K 2.02 EX-99.1 earnings release", edgar("8-K", ["2.02", "9.01"], "99.1", named_under_202=["99.1"]), "T1", ""),
    ("8-K 2.02+7.01 EX-99.2 CFO commentary, named under 2.02", edgar("8-K", ["2.02", "7.01", "9.01"], "99.2", publisher="NVIDIA",
                                                                   named_under_202=["99.1", "99.2"]), "T1", "rule 6"),
    ("8-K 2.02+8.01 EX-99.2 dividend release, not named under 2.02", edgar("8-K", ["2.02", "8.01", "9.01"], "99.2",
                                                                          named_under_202=["99.1"]), "T6", "rule 6"),
    ("8-K 2.02+7.01 EX-99.3 investor-day deck, not named under 2.02", edgar("8-K", ["2.02", "7.01", "9.01"], "99.3",
                                                                           named_under_202=["99.1"], document_format="slides"), "T5", "rule 6"),
    ("8-K 2.02 EX-99.1 Tesla update deck", edgar("8-K", ["2.02"], "99.1", publisher="Tesla", document_format="slides",
                                                 named_under_202=["99.1"]), "T1", ""),
    ("8-K 2.02 main document (cover text)", edgar("8-K", ["2.02", "9.01"], named_under_202=["99.1"]), "T6", ""),
    ("8-K 7.01 EX-99.1 investor-day slides", edgar("8-K", ["7.01", "9.01"], "99.1", document_format="slides"), "T5", ""),
    ("8-K 8.01 EX-99.1 buyback press release", edgar("8-K", ["8.01", "9.01"], "99.1"), "T6", ""),
    ("8-K 5.02 officer departure", edgar("8-K", ["5.02"]), "T6", ""),
    ("8-K 1.01 main document", edgar("8-K", ["1.01"]), "T6", "a short notice; the contract itself is A3"),
    ("8-K 2.03 EX-4.1 indenture", edgar("8-K", ["1.01", "2.03", "9.01"], "4.1", "Indenture"), "T3", ""),
    ("8-K 1.01 EX-10.1 credit agreement", edgar("8-K", ["1.01", "9.01"], "10.1", "Credit Agreement"), "T3", ""),
    ("8-K 5.02 EX-10.1 CEO employment agreement", edgar("8-K", ["5.02", "9.01"], "10.1", "Employment Agreement"), "T3", "agreed"),
    ("8-K 2.01 EX-2.1 merger agreement", edgar("8-K", ["2.01", "9.01"], "2.1", "Agreement and Plan of Merger"), "T3", ""),
    ("8-K 5.03 EX-3.2 amended bylaws", edgar("8-K", ["5.03", "9.01"], "3.2", "Amended Bylaws"), "T3", ""),
    ("8-K 5.07 vote results", edgar("8-K", ["5.07"]), "T6", ""),
    ("6-K EX-99.1 quarterly results (TSMC)", edgar("6-K", [], "99.1", "3Q26 quarterly results", publisher="TSMC"), "T1", ""),
    ("6-K monthly revenue (TSMC)", edgar("6-K", [], "99.1", "September revenue report", publisher="TSMC"), "T6", "monthly data is A6"),
    ("DEF 14A proxy", edgar("DEF 14A"), "T3", ""),
    ("DEFA14A company fight letter", edgar("DEFA14A", document_format="letter"), "T3", ""),
    ("DEFC14A dissident proxy by an activist", edgar("DEFC14A", publisher="Elliott Management", document_format="letter"), "T3",
     "rule 5: the same genre as the company's side"),
    ("S-1/A amendment", edgar("S-1/A"), "T3", ""),
    ("424B5 notes prospectus", edgar("424B5"), "T3", ""),
    ("SC TO-T tender filed by the acquirer", edgar("SC TO-T", publisher="Amazon"), "T3", ""),
    ("SC TO-T tender filed by a PE sponsor", edgar("SC TO-T", publisher="Blackstone"), "T3", "rule 5"),
    ("425 merger call transcript", edgar("425", document_format="transcript"), "T4", ""),
    ("425 merger investor deck", edgar("425", document_format="slides"), "T5", ""),
    ("425 merger press release", edgar("425"), "T3", ""),
    ("NT 10-Q late-filing notice", edgar("NT 10-Q"), "T6", ""),
    ("CORRESP company reply to the SEC", edgar("CORRESP"), "T6", ""),
    ("SEC comment letter (UPLOAD under the company's CIK)", edgar("UPLOAD", publisher="Apple"), "T10", "rule 5"),
    ("SC 13D EX-99 letter to the board", edgar("SC 13D", [], "99.1", publisher="Elliott Management", document_format="letter"), "T8", ""),
    ("Form 4 text version", edgar("4", publisher="Jane Doe (CEO)"), "T13", "rule 7: the structured version is the input"),
    ("SC 13G main document", edgar("SC 13G", publisher="Greenlight Capital"), "T13", "rule 7"),
    ("An EDGAR form not in the table", edgar("SC 99Z"), REFUSED, "rule 5: register it first"),

    # other filing systems
    ("HKEX results announcement (Xiaomi)", envelope(publisher="Xiaomi", filing_system="HKEX", filing_form="Results announcement"), "T1", ""),
    ("HKEX annual report", envelope(publisher="Xiaomi", filing_system="HKEX", filing_form="Annual report"), "T2", ""),
    ("HKEX circular on a connected transaction", envelope(publisher="Xiaomi", filing_system="HKEX", filing_form="Circular"), "T3", ""),
    ("TWSE monthly revenue", envelope(publisher="TSMC", filing_system="TWSE", filing_form="Monthly revenue"), "T6", ""),
    ("PACER complaint by a plaintiffs' firm", envelope(publisher="Bernstein Litowitz", filing_system="COURT", filing_form="Complaint"),
     "T10", "rule 5: the docket decides, not the filer"),

    # copies, wires, data rooms and uploads
    ("Earnings release on PR Newswire after the 8-K", envelope(publisher="PR Newswire", wire_issuer="Meta", channel="wire",
                                                                copy_of_tag="T1"), "T1", "rule 8"),
    ("Earnings release on the wire before the 8-K, no category", envelope(publisher="PR Newswire", wire_issuer="Meta", channel="wire"),
     "T6", "its own facts until the 8-K arrives"),
    ("Earnings release in the wire's earnings category, before the 8-K", envelope(publisher="Business Wire", wire_issuer="Meta",
                                                                                  channel="wire", channel_category="results"), "T1", ""),
    ("Mid-quarter profit warning on the wire, before the 8-K", envelope(publisher="Business Wire", wire_issuer="Apple", channel="wire"),
     "T6", "time rule 6: the tag known at T"),
    ("The same profit warning once its 8-K 2.02 arrives (new version)", envelope(publisher="Business Wire", wire_issuer="Apple",
                                                                                 channel="wire", copy_of_tag="T1", supersedes="A6 version"), "T1", ""),
    ("Earnings release copy on the IR site", envelope(copy_of_tag="T1", channel="ir_site"), "T1", "rule 8"),
    ("High-yield issuer's results in its bond data room", envelope(publisher="Acme Holdings (144A issuer)", channel="data_room",
                                                                   channel_category="results"), "T1", "rule 3: the data room vouches 'company'"),
    ("Credit agreement in a data room", envelope(publisher="Acme Holdings (144A issuer)", channel="data_room",
                                                 channel_category="legal", media_type="pdf"), "T3", ""),
    ("Press release reprinted in Benzinga's press-release section", envelope(publisher="Benzinga", wire_issuer="Acme Robotics (private)",
                                                                           channel_category="press_release"), "T6", ""),
    ("Contract win on the wire by an unregistered private supplier", envelope(publisher="Business Wire", wire_issuer="Unlisted Optics Ltd",
                                                                              channel="wire"), "T6", "rule 3"),
    ("Law-firm wire release announcing a class-action probe", envelope(publisher="GlobeNewswire", wire_issuer="Rosen Law Firm", channel="wire"), "T6", ""),
    ("Index-change announcement (S&P DJI)", envelope(publisher="S&P Dow Jones Indices", channel="wire"), "T6", "text; the change itself is B9/B5"),
    ("Your uploaded 10-K PDF, declared", envelope(channel="upload", declared=True, filing_system="EDGAR", filing_form="10-K",
                                                document_format="report", media_type="pdf"), "T2", ""),
    ("Your uploaded PDF, nothing declared", envelope(channel="upload", publisher="User", document_format="", media_type="pdf"), REFUSED, "rule 11"),
    ("Your earnings model (upload template)", data("upload:estimates", publisher="User", channel="upload"), "T8", ""),
    ("A spreadsheet uploaded without a template", data("", publisher="User", channel="upload"), REFUSED, "rule 11"),
    ("This system's own dossier, exported and uploaded back", envelope(channel="upload", declared=True, publisher="User",
                                                                       produced_by_system=True), REFUSED, "rule 11"),
    ("IR-site XLSX of segment KPIs", data("company:ir_supplement", publisher="Apple", media_type="xlsx"), "T6", ""),

    # spoken events: the organizer decides the author (rule 4)
    ("Earnings call transcript (transcript vendor)", spoken("company", publisher="FactSet", presenting_company="Apple"), "T4", ""),
    ("Investor-day transcript", spoken("company", presenting_company="Apple"), "T4", ""),
    ("Company podcast with a journalist host", spoken("company", presenting_company="Apple", host="CNBC"), "T4", ""),
    ("NVIDIA talk at a Goldman conference", spoken("investor_conference", publisher="Goldman Sachs", presenting_company="NVIDIA"), "T4", ""),
    ("CEO on stage at WSJ Tech Live", spoken("media", host="WSJ", presenting_company="Apple"), "T7", ""),
    ("CNBC interview with the CEO", spoken("media", host="CNBC"), "T7", ""),
    ("Senate hearing with the CEO testifying", spoken("official", host="US Senate"), "T10", ""),
    ("Expert-network transcript", spoken("expert_network", host="Tegus"), "T9", ""),
    ("Your meeting with the CFO, transcribed", spoken("user", host="User", channel="upload", declared=True), "T9", ""),

    # other company documents
    ("Earnings slides on the IR site", envelope(document_format="slides", media_type="pdf"), "T5", ""),
    ("Company blog post", envelope(), "T6", ""),
    ("ESG report PDF", envelope(document_format="report", media_type="pdf"), "T6", ""),
    ("Tesla deliveries release", envelope(publisher="Tesla"), "T6", ""),
    ("Private company's annual report on its site", envelope(publisher="Acme Robotics (private)", channel_category="periodic",
                                                             document_format="report", media_type="pdf"), "T2", ""),
    ("Product page with no date", envelope(published_at=None), REFUSED, "undated"),
    ("Earnings webcast audio, no transcript", envelope(media_type="audio/mpeg", document_format=""), REFUSED, "no readable text"),
    ("Chart image", envelope(media_type="image/png", document_format=""), REFUSED, "no readable text"),

    # media
    ("Reuters article", envelope(publisher="Reuters", channel_category="news"), "T7", ""),
    ("Reuters article with no category", envelope(publisher="Reuters"), "T7", "a missing category falls to the default"),
    ("Benzinga news preview", envelope(publisher="Benzinga", channel_category="news"), "T7", ""),
    ("Benzinga story on a rating change", envelope(publisher="Benzinga", channel_category="news"), "T7", "reporting, attributed"),
    ("Benzinga opinion column", envelope(publisher="Benzinga", channel_category="opinion"), "T8", ""),
    ("DigiTimes supply-chain report", envelope(publisher="DigiTimes", channel_category="news"), "T7", ""),
    ("Reuters story, updated version", envelope(publisher="Reuters", supersedes="v1"), "T7", ""),
    ("Story from an unregistered site in the news index", envelope(publisher="tinyblog.example", channel="news_index"), "T7", "rule 3"),
    ("Story from an unregistered site, no channel default", envelope(publisher="tinyblog.example", channel="web"), REFUSED, "rule 3"),
    ("Podcast audio", envelope(publisher="CNBC", media_type="audio/mpeg", document_format=""), REFUSED, "no readable text"),

    # research, investors, individuals, the user
    ("Sell-side initiation PDF", envelope(publisher="Morgan Stanley", document_format="report", media_type="pdf"), "T8", ""),
    ("Broker morning email note", envelope(publisher="Morgan Stanley", document_format="report", channel="email"), "T8", ""),
    ("Moody's rating action", envelope(publisher="Moody's", document_format="report"), "T8", ""),
    ("IDC market-share report", envelope(publisher="IDC", document_format="report", media_type="pdf"), "T8", ""),
    ("Think-tank paper", envelope(publisher="Brookings", document_format="report"), "T8", ""),
    ("Short-seller report", envelope(publisher="Hindenburg Research", document_format="report"), "T8", ""),
    ("Hedge fund letter", envelope(publisher="Greenlight Capital", document_format="letter"), "T8", ""),
    ("Seeking Alpha contributor thesis", envelope(publisher="Seeking Alpha", platform_author="SA contributor: Tech Bull",
                                                  channel="contributor_platform", document_format="article"), "T8", ""),
    ("Unregistered Seeking Alpha contributor", envelope(publisher="Seeking Alpha", platform_author="SA contributor: New Writer",
                                                        channel="contributor_platform", document_format="article"), "T8", "rule 3"),
    ("Substack newsletter", envelope(publisher="Substack", platform_author="Fabricated Knowledge (Substack)",
                                     channel="newsletter_platform", document_format="report"), "T8", ""),
    ("Executive's LinkedIn article", envelope(publisher="LinkedIn", platform_author="Jane Doe (CEO)", channel="linkedin",
                                              document_format="article"), "T8", ""),
    ("Your management-meeting notes", envelope(publisher="User", document_format="call_notes", channel="upload", declared=True), "T9", ""),
    ("Your thesis memo", envelope(publisher="User", document_format="memo", channel="upload", declared=True), "T8", ""),
    ("OCR'd research PDF", envelope(publisher="Morgan Stanley", document_format="report", media_type="pdf", has_readable_text=True), "T8", ""),
    ("Scanned research PDF with no text layer", envelope(publisher="Morgan Stanley", document_format="report", media_type="pdf",
                                                         has_readable_text=False), REFUSED, "no readable text"),

    # social posts: like any text, by their author; length and platform are attributes
    ("CEO's personal X post", envelope(publisher="X", platform_author="@elonmusk", channel="x", document_format="post"), "T8",
     "an individual's view; is_executive is an attribute"),
    ("Company's official X account", envelope(publisher="X", platform_author="@Apple", channel="x", document_format="post"), "T6", ""),
    ("Reuters' X account", envelope(publisher="X", platform_author="@Reuters", channel="x", document_format="post"), "T7", ""),
    ("Federal Reserve's X account on policy", envelope(publisher="X", platform_author="@federalreserve", channel="x",
                                                       document_format="post", series="monetary_policy"), "T11", ""),
    ("Analyst's personal X post", envelope(publisher="X", platform_author="@some_analyst", channel="x", document_format="post"), "T8", ""),
    ("LinkedIn feed post", envelope(publisher="LinkedIn", platform_author="Jane Doe (CEO)", channel="linkedin", document_format="post"), "T8", ""),
    ("Substack Note and Substack article by the same writer", envelope(publisher="Substack", platform_author="Fabricated Knowledge (Substack)",
                                                                       channel="substack", document_format="post"), "T8",
     "the same tag as the article: length is an attribute"),
    ("Unregistered Reddit account", envelope(publisher="Reddit", platform_author="u/some_user", channel="reddit", document_format="post"), "T8", ""),
    ("Edited X post", envelope(publisher="X", platform_author="@elonmusk", channel="x", document_format="post", supersedes="first version"), "T8", ""),
    ("Post with no account", envelope(publisher=None, channel="x", document_format="post"), REFUSED, "author required"),
    ("Post with no timestamp", envelope(publisher="X", platform_author="@elonmusk", channel="x", document_format="post", published_at=None),
     REFUSED, "time required"),

    # officials
    ("FOMC statement", envelope(publisher="Federal Reserve", series="monetary_policy"), "T11", ""),
    ("Fed chair speech on policy", envelope(publisher="Federal Reserve", series="monetary_policy"), "T11", ""),
    ("Fed governor speech on supervision", envelope(publisher="Federal Reserve", series="supervision"), "T10", ""),
    ("Fed enforcement action", envelope(publisher="Federal Reserve", series="enforcement"), "T10", ""),
    ("BLS CPI release text", envelope(publisher="BLS", series="economic_statistics"), "T11", ""),
    ("EU Commission antitrust decision", envelope(publisher="European Commission", series="competition"), "T10", ""),
    ("FTC complaint", envelope(publisher="FTC", series="press_release"), "T10", ""),
    ("FTC page with no series", envelope(publisher="FTC"), "T10", "a missing series falls to the default"),
    ("Court opinion", envelope(publisher="US District Court", series="opinions"), "T10", ""),
    ("BIS export-control rule", envelope(publisher="BIS (Commerce)", series="federal_register"), "T10", ""),
    ("Tariff executive order", envelope(publisher="White House", series="executive_orders"), "T10", ""),
    ("NYSE trading-halt notice", envelope(publisher="NYSE", series="notices"), "T10", ""),
    ("FDA approval letter", envelope(publisher="FDA", series="approvals"), "T10", ""),
    ("SEC litigation release", envelope(publisher="SEC", series="litigation"), "T10", ""),
    ("PBOC statement in Chinese", envelope(publisher="PBOC", series="monetary_policy", language="zh"), "T11", ""),

    # structured datasets
    ("MCP financial statements", data("mcp:financial_statements"), "T2", ""),
    ("SEC companyfacts XBRL fact", data("sec:companyfacts", derived_from="10-Q"), "T2", ""),
    ("Daily bars", data("mcp:historical_bars"), "T12", ""),
    ("Options chain", data("vendor:options_chain"), "T12", ""),
    ("Prediction-market odds", data("mcp:polymarket_insight"), "T12", ""),
    ("Analyst estimates", data("mcp:financial_analyst_estimates"), "T8", ""),
    ("Credit-rating history", data("vendor:credit_ratings"), "T8", ""),
    ("Form 4 XML", data("edgar:form4"), "T13", ""),
    ("13F information table", data("edgar:13f"), "T13", ""),
    ("FINRA short interest", data("finra:short_interest"), "T13", ""),
    ("CFTC COT", data("cftc:cot"), "T13", ""),
    ("Earnings calendar", data("mcp:financial_earnings_calendar"), "T14", ""),
    ("Economic calendar row: the date", data("mcp:financial_economic_calendar#date"), "T14", "rule 12: split"),
    ("Economic calendar row: the forecast", data("mcp:financial_economic_calendar#forecast"), "T8", ""),
    ("Economic calendar row: the actual", data("mcp:financial_economic_calendar#actual"), "T11", ""),
    ("CPI series", data("fred:cpi"), "T11", ""),
    ("GDP vintage revision", data("alfred:gdp", supersedes="prior vintage"), "T11", ""),
    ("Card-spend panel", data("vendor:card_spend"), "T15", ""),
    ("Government contract awards", data("usaspending:awards"), "T10", ""),
    ("Patent grants", data("uspto:grants"), "T10", ""),
    ("GICS classification", data("msci:gics"), "T16", ""),
    ("Vendor technical analysis", data("mcp:technical_analysis"), NOT_INPUT, "computed analytics"),
    ("Vendor-computed ratios", data("mcp:financial_metrics"), NOT_INPUT, "computed analytics"),
    ("EDGAR filing list", data("edgar:filing_index"), NOT_INPUT, "discovery index"),
    ("An unmapped dataset", data("vendor:new_feed"), REFUSED, ""),
    ("News item with no timestamp", envelope(publisher="Reuters", published_at=None), REFUSED, "undated"),

    # company identifiers: closed sets (company rule 1)
    ("Company identifier with a basis outside the closed set", envelope(
        publisher="Reuters", company_identifiers=[identifier("ticker", "AAPL", "guess")]), REFUSED, "company rule 1"),
    ("Company identifier with an empty value", envelope(
        publisher="Reuters", company_identifiers=[identifier("ticker", " ", "channel_tag")]), REFUSED, "company rule 1"),
]

# (case, envelope, expected related entity ids, expected unresolved identifier values, what the expectation rests on)
COMPANY_CASES = [
    ("10-K: the filer", edgar("10-K"), {APPLE}, set(), "company rule 1"),
    ("8-K filed through a filing agent: the URL and accession carry the agent's CIK",
     edgar("8-K", ["8.01"], publisher="Amazon", source_uri="https://www.sec.gov/Archives/edgar/data/1104659/000110465926107526/",
           company_identifiers=[identifier("cik", "1018724", "filer")]), {AMAZON}, set(), "company rule 2: the URL is never read"),
    ("SC 13D by an activist: the subject company and the filer",
     edgar("SC 13D", [], "99.1", publisher="Elliott Management", document_format="letter",
           company_identifiers=[identifier("cik", "320193", "filing_subject"), identifier("name", "Elliott Management", "filer")]),
     {APPLE}, {"Elliott Management"}, "both kept with their basis; an unregistered filer stays unresolved"),
    ("425 filed by the acquirer: both parties",
     edgar("425", publisher="Microsoft", company_identifiers=[identifier("name", "Activision Blizzard", "filing_subject"),
                                                             identifier("cik", "789019", "filer")]),
     {MICROSOFT, ACTIVISION}, set(), "company rule 1"),
    ("HKEX results: the filer by its exchange ticker",
     envelope(publisher="Xiaomi", filing_system="HKEX", filing_form="Results announcement",
              company_identifiers=[identifier("ticker", "1810.hk", "filer")]), {XIAOMI}, set(), "tickers compare in capitals"),
    ("Form 4 XML: the issuer in the record", data("edgar:form4", company_identifiers=[identifier("cik", "1318605", "record_field")]),
     {TESLA}, set(), "company rule 1"),
    ("13F holding row: each split record names its own issuer",
     data("edgar:13f", company_identifiers=[identifier("ticker", "NVDA", "record_field")]), {NVIDIA}, set(), "rule 12 split"),
    ("Daily bars for AAPL", data("mcp:historical_bars", company_identifiers=[identifier("ticker", "aapl", "record_field")]),
     {APPLE}, set(), ""),
    ("S&P 500 index daily bars: no company", data("mcp:historical_bars"), set(), set(), "company rule 4: may be empty"),
    ("CPI series: no company", data("fred:cpi"), set(), set(), "company rule 4"),
    ("FOMC statement: no company", envelope(publisher="Federal Reserve", series="monetary_policy"), set(), set(), "company rule 4"),
    ("IR-site XLSX of segment KPIs: the company is the author", data("company:ir_supplement", publisher="Apple", media_type="xlsx"),
     {APPLE}, set(), "company rule 1: an author that is a company"),
    ("Earnings release on the wire: the issuer is the author", envelope(publisher="PR Newswire", wire_issuer="Meta", channel="wire"),
     {META}, set(), "company rule 1"),
    ("Earnings call transcript from a vendor: the presenting company and the channel's ticker",
     spoken("company", publisher="FactSet", presenting_company="Apple", company_identifiers=[identifier("ticker", "AAPL", "channel_tag")]),
     {APPLE}, set(), "the vendor is a channel"),
    ("NVIDIA at a Goldman conference: the presenting company", spoken("investor_conference", publisher="Goldman Sachs",
                                                                       presenting_company="NVIDIA"), {NVIDIA}, set(), ""),
    ("Sell-side report on Tesla: the broker is the author, not a related company",
     envelope(publisher="Morgan Stanley", document_format="report", company_identifiers=[identifier("ticker", "TSLA", "channel_tag")]),
     {TESLA}, set(), "company rule 1: only a company author counts"),
    ("Reuters story fetched for Apple, tagged AAPL and Samsung by the channel",
     envelope(publisher="Reuters", channel_category="news",
              company_identifiers=[identifier("cik", "320193", "query"), identifier("ticker", "AAPL", "channel_tag"),
                                   identifier("name", "Samsung Electronics", "channel_tag")]),
     {APPLE}, {"Samsung Electronics"}, "company rule 3: unresolved is kept, the input is not refused"),
    ("A name that is not a registered alias", envelope(publisher="Reuters", company_identifiers=[identifier("name", "Apple Computer",
                                                                                                         "channel_tag")]),
     set(), {"Apple Computer"}, "company rule 3: names match registered aliases exactly"),
    ("2021 story tagged FB: Meta's ticker then",
     envelope(publisher="Reuters", published_at="2021-10-28T12:00:00Z", retrieved_at="2021-10-28T12:05:00Z",
              company_identifiers=[identifier("ticker", "FB", "channel_tag")]), {META}, set(), "company rule 3: the ticker on its day"),
    ("2021 story tagged META: not Meta's ticker before 2022-06-09",
     envelope(publisher="Reuters", published_at="2021-10-28T12:00:00Z", retrieved_at="2021-10-28T12:05:00Z",
              company_identifiers=[identifier("ticker", "META", "channel_tag")]), set(), {"META"}, "company rule 3"),
    ("2026 story tagged FB: no longer a ticker of Meta",
     envelope(publisher="Reuters", company_identifiers=[identifier("ticker", "FB", "channel_tag")]), set(), {"FB"}, "company rule 3"),
    ("EU decision on Apple and Meta, fetched for both",
     envelope(publisher="European Commission", series="competition",
              company_identifiers=[identifier("cik", "320193", "query"), identifier("cik", "1326801", "query")]),
     {APPLE, META}, set(), ""),
    ("Your thesis memo, declared about Amazon",
     envelope(publisher="User", document_format="memo", channel="upload", declared=True,
              company_identifiers=[identifier("ticker", "AMZN", "declared")]), {AMAZON}, set(), ""),
    ("A refused input has no companies", envelope(publisher="Reuters", published_at=None,
                                                  company_identifiers=[identifier("ticker", "AAPL", "channel_tag")]),
     set(), set(), "company rule 4"),
]

# ------------------------------------------------------------------ population 2: the MCP's data tools

# What each tool returns, by measured object. Several B objects: split (rule 10); text: an A input, not a dataset;
# derived or discovery: not an input.
MCP_TOOL_OBJECTS = {
    "basic_market_info": ["T12"], "coinbase_premium": ["T12"], "company_sector_facts": ["T16"], "derivatives_analysis": ["derived"],
    "etf_flow": ["T13"], "event_v2": ["text", "discovery"], "fear_greed": ["derived"], "financial_analyst_estimates": ["T8"],
    "financial_commodity_snapshot": ["T12"], "financial_company_facts": ["T16"], "financial_earnings_calendar": ["T14"],
    "financial_earnings_data": ["T8", "T1"], "financial_earnings_transcript": ["text"],
    "financial_economic_calendar": ["T14", "T8", "T11"], "financial_etf_exposure": ["T13"], "financial_etf_holdings": ["T13"],
    "financial_etf_overview": ["T16", "text"], "financial_etf_profile": ["T16"], "financial_fundamental_graph": ["derived"],
    "financial_fx_rates": ["T12"], "financial_insider_trades": ["T13"], "financial_institutional_ownership": ["T13"],
    "financial_investor_portfolio": ["T13"], "financial_macro_data": ["T11", "T12"], "financial_metrics": ["derived"],
    "financial_resolve_stock_ticker": ["T16"], "financial_sec_filing_items": ["text"], "financial_sec_filings": ["discovery"],
    "financial_segmented_revenue": ["T2"], "financial_statements": ["T2"], "financial_stock_dividends": ["T12"],
    "financial_stock_splits": ["T12"], "historical_bars": ["T12"], "hyperliquid_smart_money": ["T13"], "kline_analysis": ["derived"],
    "liquidation_risk": ["derived"], "macro_market_context": ["derived"], "market_derivatives_series": ["T12"],
    "market_klines_multi": ["T12"], "market_session": ["T14"], "market_ticker24h": ["T12"], "market_universe": ["T16"],
    "market_whale_positions": ["T13"], "mvrv": ["derived"], "options_report": ["derived"], "performance_scanner": ["derived"],
    "polymarket_insight": ["T12"], "query_chains": ["T15"], "query_protocols": ["T15"], "resolve_asset": ["T16"],
    "technical_analysis": ["derived"], "token_unlock": ["T14"], "trending_discovery": ["derived"], "venue_costs": ["T12"],
}

# ------------------------------------------------------------------ population 1: the old ledger's real sources

REAL_PUBLISHERS = {"Apple Inc.": "company", "Amazon.com, Inc.": "company", "Meta Platforms, Inc.": "company",
                   "European Commission": "official", "US Federal Trade Commission": "official"}
WIRE_HOSTS = ("prnewswire.com", "businesswire.com", "globenewswire.com")
# The news channel's category table, kept to sections that are unambiguously argument (a column). Benzinga's
# trading-ideas sections mix argued pieces with market round-ups, so they stay news.
CATEGORY_TABLE = {"opinion": "opinion"}
COMPANY_NAMES = {"Meta": "Meta Platforms, Inc.", "Apple": "Apple Inc.", "Amazon": "Amazon.com, Inc."}


def named_company(title):
    return next(full for short, full in COMPANY_NAMES.items() if short.lower() in title.lower())


def real_envelope(source, edgar_releases):
    """The envelope a channel adapter builds from an old source record."""
    uri = source["canonical_uri"]
    host = urlparse(uri).netloc.replace("www.", "")
    path = urlparse(uri).path.lower().strip("/")
    document_type = source["document_type"]
    fields = {"input_id": source["origin_id"], "content_sha256": source["content_sha256"], "channel": "news_index",
              "source_uri": uri, "publisher": source["publisher"], "published_at": source.get("published_at"),
              "retrieved_at": source.get("first_seen_at"), "is_structured": False, "media_type": "html", "language": "en",
              "document_format": "article"}
    if document_type == "earnings_release":
        fields.update(channel="edgar", filing_system="EDGAR", filing_form="8-K", filing_items=["2.02"], exhibit="99.1",
                      item_202_exhibits=["99.1"])
    elif document_type == "annual_report":
        fields.update(channel="edgar", filing_system="EDGAR", filing_form="10-K")
    elif document_type == "earnings_transcript":
        fields.update(channel="mcp", document_format="transcript", event_organizer="company", presenting_company=source["publisher"])
    elif document_type == "regulatory_release" and "sec.gov" in uri:
        fields.update(channel="edgar", filing_system="EDGAR", filing_form="8-K",
                      filing_items=["5.02"] if "item-5" in source["origin_id"] else ["8.01"])
    elif document_type == "regulatory_release":
        fields.update(channel="official_site", series="press_release")
    elif host.endswith(WIRE_HOSTS):
        issuer = named_company(source["title"])
        day = (source.get("published_at") or "")[:10]
        fields.update(publisher=host, wire_issuer=issuer, channel="wire",
                      copy_of_tag="T1" if (issuer, day) in edgar_releases else None)
    elif "earnings call transcript" in source["title"].lower():
        fields.update(publisher=host, document_format="transcript", event_organizer="company",
                      presenting_company=named_company(source["title"]))
    else:
        category = next((value for key, value in CATEGORY_TABLE.items() if path.startswith(key)), "news")
        fields.update(publisher=host, channel_category=category)
    fields["company_identifiers"] = real_company_identifiers(source, fields)
    return fields


# Old document types whose companies the adapter derives from the document itself, independently of the old tags: the
# EDGAR header's filer and the transcript channel's ticker. Every other old source's companies came from the company
# its fetch queried, so those inputs only show that the identifiers flow through.
INDEPENDENT_TYPES = ("annual_report", "earnings_release", "earnings_transcript")


def independent(source):
    return source["document_type"] in INDEPENDENT_TYPES or (
        source["document_type"] == "regulatory_release" and "sec.gov" in source["canonical_uri"])


def real_company_identifiers(source, fields):
    """The identifiers a channel adapter writes for an old source (never read from the URL path)."""
    if fields.get("filing_system"):
        return [identifier("name", source["publisher"], "filer")]
    if source["document_type"] == "earnings_transcript":
        return [identifier("ticker", source["canonical_uri"].split("/")[-2], "channel_tag")]
    return [identifier("cik", reference["id"].rsplit(":", 1)[-1], "query") for reference in source["target_refs"]]


def run_real_companies():
    """[(group, compared, matched, [mismatch lines])] of the old sources' resolved companies against their old tags."""
    connection = sqlite3.connect(f"file:{OLD_LEDGER}?mode=ro", uri=True)
    sources = [json.loads(row[0]) for row in connection.execute("select payload from research_records where kind='source'")]
    edgar_releases = {(source["publisher"], (source.get("published_at") or "")[:10])
                      for source in sources if source["document_type"] == "earnings_release"}
    groups = {"independent": [0, 0, []], "flow-through": [0, 0, []]}
    for source in sources:
        fields = real_envelope(source, edgar_releases)
        outcome, _ = classify(fields, REAL_PUBLISHERS, {})
        if outcome in (REFUSED, NOT_INPUT):
            continue
        companies, unresolved = related_companies(fields, outcome, REAL_PUBLISHERS, REFERENCE)
        expected = {reference["id"] for reference in source["target_refs"]}
        group = groups["independent" if independent(source) else "flow-through"]
        group[0] += 1
        if set(companies) == expected and not unresolved:
            group[1] += 1
        else:
            group[2].append(f"{source['title'][:60]} | expected {sorted(expected)}, got {sorted(companies)}, "
                            f"unresolved {[item['value'] for item in unresolved]}")
    return [(name, compared, matched, mismatches) for name, (compared, matched, mismatches) in groups.items()]


def run_company_cases():
    """[(case, expected ids, got ids, expected unresolved, got unresolved, why)] of the company cases that fail, and the
    number of tag cases with at least one related company (every tag case also runs through the company rules)."""
    failures = []
    for name, case_envelope, expected_ids, expected_unresolved, why in COMPANY_CASES:
        outcome, _ = classify(case_envelope, PUBLISHERS, DATASETS)
        companies, unresolved = related_companies(case_envelope, outcome, PUBLISHERS, REFERENCE)
        got_unresolved = {item["value"] for item in unresolved}
        if set(companies) != expected_ids or got_unresolved != expected_unresolved:
            failures.append((name, expected_ids, set(companies), expected_unresolved, got_unresolved, why))
    with_companies = 0
    for _, case_envelope, _, _ in CASES:
        outcome, _ = classify(case_envelope, PUBLISHERS, DATASETS)
        with_companies += bool(related_companies(case_envelope, outcome, PUBLISHERS, REFERENCE)[0])
    return failures, with_companies


def expected_real(source, edgar_releases):
    """The outcome an analyst gives the old record, read from what the document is."""
    title = source["title"].lower()
    document_type = source["document_type"]
    if not source.get("published_at"):
        return REFUSED
    if document_type == "earnings_release":
        return "T1"
    if any(host in source["canonical_uri"] for host in WIRE_HOSTS):
        return "T1" if (named_company(source["title"]), source["published_at"][:10]) in edgar_releases else "T6"
    if document_type == "annual_report":
        return "T2"
    if document_type == "earnings_transcript" or "earnings call transcript" in title:
        return "T4"
    if document_type == "regulatory_release":
        return "T6" if "sec.gov" in source["canonical_uri"] else "T10"
    if source["canonical_uri"].split("benzinga.com/")[-1].lower().startswith("opinion"):
        return "T8"
    return "T7"


def run_real():
    connection = sqlite3.connect(f"file:{OLD_LEDGER}?mode=ro", uri=True)
    sources = [json.loads(row[0]) for row in connection.execute("select payload from research_records where kind='source'")]
    edgar_releases = {(source["publisher"], (source.get("published_at") or "")[:10])
                      for source in sources if source["document_type"] == "earnings_release"}
    registry = dict(REAL_PUBLISHERS)
    outcomes = collections.Counter()
    misses = collections.defaultdict(list)
    argued = []
    for source in sources:
        fields = real_envelope(source, edgar_releases)
        outcome, reason = classify(fields, registry, {})
        expected = expected_real(source, edgar_releases)
        outcomes[outcome] += 1
        if outcome == "T8" and not source.get("document_type", "").startswith("earnings"):
            argued.append(source["title"][:90])
        if outcome != expected:
            misses[(expected, outcome, reason)].append(f"{source['title'][:70]} | {source['canonical_uri'][:80]}")
    return len(sources), outcomes, misses, argued


def run_cases():
    failures = []
    reached = collections.Counter()
    for name, case_envelope, expected, why in CASES:
        outcome, reason = classify(case_envelope, PUBLISHERS, DATASETS)
        reached[outcome] += 1
        if outcome != expected:
            failures.append((name, expected, outcome, reason, why))
    return failures, reached


def page_tags():
    """The tag codes and names the page defines."""
    text = (PAGE_DIRECTORY / "new-classification.js").read_text(encoding="utf-8")
    return dict(re.findall(r"^\s{4}(T\d+): \{ name: '([a-z_]+)'", text, re.MULTILINE))


def main():
    tags_on_page = page_tags()
    simulated_tags = {f"T{number}" for number in range(1, 17)}
    failed = False

    total, outcomes, real_misses, argued = run_real()
    real_failures = sum(len(titles) for titles in real_misses.values())
    print(f"=== 1. old ledger: {total} real sources; {total - real_failures} as expected, {real_failures} not")
    print("  outcomes:", dict(sorted(outcomes.items())))
    for (expected, outcome, reason), titles in sorted(real_misses.items(), key=lambda item: -len(item[1])):
        print(f"  ✗ expected {expected}, got {outcome} ({reason}): {len(titles)}")
        for title in titles[:3]:
            print(f"      {title}")
    print(f"  the {len(argued)} real inputs classified A8 (read them: are they argued analysis?):")
    for title in argued:
        print(f"      {title}")

    listed = json.loads(OLD_SOURCE_REGISTRY.read_text())["tool_inventory"]["names"]
    unknown = sorted(set(listed) - set(MCP_TOOL_OBJECTS))
    by_shape = collections.defaultdict(list)
    for tool, objects in MCP_TOOL_OBJECTS.items():
        data_objects = [o for o in objects if o.startswith("T")]
        shape = ("one tag" if len(data_objects) == 1 and len(objects) == 1 else
                 "several tags → split" if len(data_objects) > 1 else
                 "data plus text → split" if data_objects else
                 "text → a document input" if objects == ["text"] else "not an input")
        by_shape[shape].append(tool)
    print(f"\n=== 2. MCP tools: {len(listed)} listed, {len(listed) - len(unknown)} mapped, unknown: {unknown or 'none'}")
    for shape, tools in sorted(by_shape.items()):
        print(f"  {shape} ({len(tools)}): {', '.join(sorted(tools))}")

    failures, reached = run_cases()
    print(f"\n=== 3. hand-written cases: {len(CASES)}; {len(CASES) - len(failures)} as expected, {len(failures)} not")
    for name, expected, outcome, reason, why in failures:
        print(f"  ✗ {name}\n      expected {expected}, got {outcome} ({reason}) {why}")
    uncovered = sorted(simulated_tags - set(reached), key=lambda code: int(code[1:]))
    print(f"  outcomes reached: {dict(sorted(reached.items()))}")
    print(f"  tags no case reaches: {uncovered or 'none'}")

    company_failures, tag_cases_with_companies = run_company_cases()
    print(f"\n=== 4. related companies: {len(COMPANY_CASES)} company cases; {len(COMPANY_CASES) - len(company_failures)} "
          f"as expected, {len(company_failures)} not")
    for name, expected_ids, got_ids, expected_unresolved, got_unresolved, why in company_failures:
        print(f"  ✗ {name}\n      expected {sorted(expected_ids)} + unresolved {sorted(expected_unresolved)}, "
              f"got {sorted(got_ids)} + unresolved {sorted(got_unresolved)} {why}")
    print(f"  the {len(CASES)} tag cases also ran through the company rules; {tag_cases_with_companies} have a related company")
    real_company_misses = 0
    for group, compared, matched, mismatches in run_real_companies():
        print(f"  old ledger, {group}: {compared} compared with their old company tags; {matched} equal, "
              f"{compared - matched} not")
        real_company_misses += compared - matched
        for line in mismatches[:5]:
            print(f"      ✗ {line}")
        if compared == 0:
            print(f"  ✗ the {group} group is empty: nothing was judged")
            real_company_misses += 1

    print("\n=== consistency with the page")
    if set(tags_on_page) != simulated_tags:
        print(f"  ✗ page tags {sorted(tags_on_page)} differ from the simulated tags")
        failed = True
    else:
        print(f"  page defines the same {len(tags_on_page)} tags the simulation emits")

    failed = failed or bool(failures) or bool(real_misses) or bool(uncovered) or bool(unknown) or bool(company_failures) \
        or bool(real_company_misses)
    print("\nRESULT:", "FAIL" if failed else "PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
