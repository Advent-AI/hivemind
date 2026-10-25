# Research universe

> Status: first version frozen, October 18, 2026; specific themes remain a draft. English edition: October 25, 2026 (D163).
> Design page: `docs/system-design.html` → New → Research universe. Recorded decisions take precedence over this PRD.

## Purpose

Define which subjects to research and which information categories to track for each. This is the sole owner of what the system processes.

Tariff research needs government notices; company research needs news and company announcements; Bitcoin research needs on-chain data. A second global category switch would eventually conflict with this list.

## Scope

List over 500 US-listed companies, cryptocurrencies, commodities and macro themes, each with tracked categories. Supply this scope to upstream. Also supply all themes to extraction block 3 so theme candidates can select one.

The universe does not filter items inside dispatch, choose reading methods or model settings, or automatically add subjects. Extraction owns reading methods; Config owns model settings. Unresolved identifiers and proposed themes go to human review; resolvable assets merely outside the universe do not.

D155's POC entries include research references without changing this information scope. See the [improvement plan](../poc/grouping-improvement-plan.md) for their purpose and identity limits.

## Four subject kinds

<!-- generated: kinds -->
| Kind | Identifiers | Example |
|---|---|---|
| Company | Ticker, CIK or company name | Over 500 US-listed companies: Apple, Amazon, Meta… |
| Cryptocurrency | Cryptocurrency symbol | Bitcoin, Ethereum… |
| Commodity | Commodity symbol | Gold, crude oil, copper… |
| Theme | Theme ID | US inflation, US–China tariffs, Russia–Ukraine war… |
<!-- /generated: kinds -->

## Default tracked categories

<!-- generated: defaults -->
| Kind | Tracked information | Category IDs |
|---|---|---|
| Company | Company publications (earnings, periodic reports, calls, presentations and other releases), related legal and capital-markets documents regardless of filer, news, opinion and analysis, interviews, official actions, prices, holdings, calendars and third-party measurements | T1–T10, T12–T15 |
| Cryptocurrency | News, opinion and analysis, official actions (enforcement, ETF approvals), prices, flows and holdings, unlock calendars and on-chain data | T7, T8, T10, T12–T15 |
| Commodity | News, opinion and analysis, official actions (OPEC decisions, sanctions), statistics (EIA inventories), prices, holdings (CFTC), calendars, shipping and satellite data | T7, T8, T10–T15 |
| Theme | No default; define categories for each theme | — |
<!-- /generated: defaults -->

## Draft theme library: 12 groups

<!-- generated: themes -->
| Group | Theme |
|---|---|
| Money and rates | Fed policy rate · US Treasury yield curve · ECB, BOJ and PBOC policy |
| Inflation | US inflation · Wage growth · Energy price transmission |
| Growth and employment | US recession risk · Labour market · Consumer spending · Chinese economy · European economy |
| Fiscal policy | US deficits and debt issuance · Debt ceiling and government shutdowns · Tax policy |
| Trade and industrial policy | US–China tariffs · Chip export controls · Industrial subsidies (CHIPS Act, IRA) · Supply-chain shifts |
| Geopolitics and war | Russia–Ukraine war · Middle East conflict · Taiwan Strait · Sanctions |
| Politics and elections | US elections · Policy direction |
| Regulation and law | US/EU antitrust · Data and privacy · AI regulation · Financial regulation |
| Energy and commodities | Crude oil supply (OPEC) · Natural gas · Industrial metals |
| Exchange rates and capital flows | US dollar strength · Renminbi · Yen |
| Industry cycles | AI capital expenditure · Semiconductor cycle · Cloud demand |
| Market risk appetite | Credit spreads · Volatility · Liquidity |
<!-- /generated: themes -->

## Theme tracking examples

<!-- generated: examples -->
| Theme | Tracked information | Category IDs |
|---|---|---|
| US inflation | CPI, PCE and BLS releases, ISM price components and University of Michigan inflation expectations (macro statistics); related news; economist forecasts | T11, T7, T8 |
| US–China tariffs | USTR and Commerce Department announcements (official actions); related news and commentary; company reports, calls and announcements discussing tariffs | T10, T7, T8, T1–T6 |
<!-- /generated: examples -->

## Rules

<!-- generated: rules -->
1. Manage and version the research universe separately from Config. The theme library is part of it, not a separate copy.
2. The universe defines which subjects to research and which categories to track for each. It is the sole owner of what the system processes.
3. Companies, cryptocurrencies and commodities each have default categories. Every theme explicitly specifies at least one category. Categories must come from the set of 16. A universe version is invalid if a subject cannot be resolved in reference data or the theme library.
4. Upstream supplies only subjects and categories covered by the universe. Test code follows the same scope. Every supplied item is processed.
5. Adding a subject or changing tracked categories creates a new version. Upstream backfills relevant historical items under the new universe.
6. Rates, exchange rates and indices belong to themes, such as the US Treasury yield curve or US dollar strength, rather than separate subject kinds.
7. Do not add subjects automatically. Unresolved identifiers and themes outside the universe go to the human review pool. Resolvable companies, cryptocurrencies or commodities outside the universe, such as Samsung, only receive a processing-log entry.
8. Macro and geopolitical themes connect to companies through thesis dependencies. A theme thesis describes an outcome without calling it good or bad. An asset thesis records which theme theses it reads and which end of each is bullish for it. A changed conclusion triggers the library’s rejudgement rules for dependent theses.
<!-- /generated: rules -->

## Examples

- An Apple company row uses company defaults: upstream sends earnings, 10-Ks, calls, news, prices and other tracked categories.
- A US–China tariff theme can track official actions, news, opinion/analysis and company disclosures T1–T6: upstream sends USTR announcements, related reporting and commentary, and company reports, calls and releases mentioning tariffs.
- Adding a company creates a new universe version; upstream backfills its relevant historical information.

## Acceptance

- Every version lists each subject's kind, name and tracked categories.
- An invalid category, a theme with no categories, or an unresolved subject invalidates the version.
- Any change creates a new version and preserves the previous one.
- Dispatch contains no subject-based routing decision.
- Nothing outside the universe is added automatically. Unresolved identifiers and new themes enter human review; resolvable out-of-universe companies, cryptocurrencies and commodities do not.

## Open questions

- Specific themes in the draft library.
- Upstream delivery and where its universe version is recorded.
- Storage location and maintenance ownership.
- Reference data used to validate subjects belongs to upstream; coordinate that contract with upstream.

## Related decisions

- D6: separate management and versioning. D11: four subject kinds; themes are part of the universe.
- D16: unresolved identifiers go to human review. D18: the universe alone selects subjects/categories and supplies defaults.
- D19, D37: first-version freeze; changes need a decision.
- D24/D28: the earlier exclusion of financial reports was reversed; company defaults include T1, T2 and T4.
- D26/D41/D42: macro effects reach companies through dependencies; use company as the subject kind.
- D45/D46: the model selects dependency direction and code prevents cycles.
- D47: distinguish unresolved identifiers and new themes from resolvable out-of-universe assets.
- D51/D58/D60: dependent open theses follow the library's rejudgement rule; a changed conclusion is broader than a changed rung.
- D59: all themes appear in extraction block 3.
