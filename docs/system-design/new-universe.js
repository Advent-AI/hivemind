// The New design's research universe: the objects the system researches, the kinds of information tracked for each, and
// the theme library among them. Edit the data at the top; the drill-down renders it. Decisions D6, D11, D18, D26 and D28 in
// docs/DECISIONS.md. The texts are for a reader who did not follow the discussion: plain words, no field names.
(function () {
  'use strict';

  const OBJECT_KINDS = [
    { label: 'Company', identifiers: 'Ticker, CIK or company name', example: 'Over 500 US-listed companies: Apple, Amazon, Meta…' },
    { label: 'Cryptocurrency', identifiers: 'Cryptocurrency symbol', example: 'Bitcoin, Ethereum…' },
    { label: 'Commodity', identifiers: 'Commodity symbol', example: 'Gold, crude oil, copper…' },
    { label: 'Theme', identifiers: 'Theme ID', example: 'US inflation, US–China tariffs, Russia–Ukraine war…' },
  ];

  // What each kind of object looks at by default: the one place that decides which kinds of information are processed.
  const TRACKING_DEFAULTS = [
    { kind: 'Company', plain: 'Company publications (earnings, periodic reports, calls, presentations and other releases), related legal and capital-markets documents regardless of filer, news, opinion and analysis, interviews, official actions, prices, holdings, calendars and third-party measurements', codes: 'T1–T10, T12–T15' },
    { kind: 'Cryptocurrency', plain: 'News, opinion and analysis, official actions (enforcement, ETF approvals), prices, flows and holdings, unlock calendars and on-chain data', codes: 'T7, T8, T10, T12–T15' },
    { kind: 'Commodity', plain: 'News, opinion and analysis, official actions (OPEC decisions, sanctions), statistics (EIA inventories), prices, holdings (CFTC), calendars, shipping and satellite data', codes: 'T7, T8, T10–T15' },
    { kind: 'Theme', plain: 'No default; define categories for each theme', codes: '—' },
  ];

  // The theme library, first draft: the macro, political, economic and geopolitical drivers that move the objects above.
  const THEME_LIBRARY = [
    { category: 'Money and rates', themes: 'Fed policy rate · US Treasury yield curve · ECB, BOJ and PBOC policy' },
    { category: 'Inflation', themes: 'US inflation · Wage growth · Energy price transmission' },
    { category: 'Growth and employment', themes: 'US recession risk · Labour market · Consumer spending · Chinese economy · European economy' },
    { category: 'Fiscal policy', themes: 'US deficits and debt issuance · Debt ceiling and government shutdowns · Tax policy' },
    { category: 'Trade and industrial policy', themes: 'US–China tariffs · Chip export controls · Industrial subsidies (CHIPS Act, IRA) · Supply-chain shifts' },
    { category: 'Geopolitics and war', themes: 'Russia–Ukraine war · Middle East conflict · Taiwan Strait · Sanctions' },
    { category: 'Politics and elections', themes: 'US elections · Policy direction' },
    { category: 'Regulation and law', themes: 'US/EU antitrust · Data and privacy · AI regulation · Financial regulation' },
    { category: 'Energy and commodities', themes: 'Crude oil supply (OPEC) · Natural gas · Industrial metals' },
    { category: 'Exchange rates and capital flows', themes: 'US dollar strength · Renminbi · Yen' },
    { category: 'Industry cycles', themes: 'AI capital expenditure · Semiconductor cycle · Cloud demand' },
    { category: 'Market risk appetite', themes: 'Credit spreads · Volatility · Liquidity' },
  ];

  const TRACKING_EXAMPLES = [
    { theme: 'US inflation', tracked: 'CPI, PCE and BLS releases, ISM price components and University of Michigan inflation expectations (macro statistics); related news; economist forecasts', codes: 'T11, T7, T8' },
    { theme: 'US–China tariffs', tracked: 'USTR and Commerce Department announcements (official actions); related news and commentary; company reports, calls and announcements discussing tariffs', codes: 'T10, T7, T8, T1–T6' },
  ];

  const RULES = [
    'Manage and version the research universe separately from Config. The theme library is part of it, not a separate copy.',
    'The universe defines which subjects to research and which categories to track for each. It is the sole owner of what the system processes.',
    'Companies, cryptocurrencies and commodities each have default categories. Every theme explicitly specifies at least one category. Categories must come from the set of 16. A universe version is invalid if a subject cannot be resolved in reference data or the theme library.',
    'Upstream supplies only subjects and categories covered by the universe. Test code follows the same scope. Every supplied item is processed.',
    'Adding a subject or changing tracked categories creates a new version. Upstream backfills relevant historical items under the new universe.',
    'Rates, exchange rates and indices belong to themes, such as the US Treasury yield curve or US dollar strength, rather than separate subject kinds.',
    'Do not add subjects automatically. Unresolved identifiers and themes outside the universe go to the human review pool. Resolvable companies, cryptocurrencies or commodities outside the universe, such as Samsung, only receive a processing-log entry.',
    'Macro and geopolitical themes connect to companies through thesis dependencies. A theme thesis describes an outcome without calling it good or bad. An asset thesis records which theme theses it reads and which end of each is bullish for it. A changed conclusion triggers the library’s rejudgement rules for dependent theses.',
  ];

  const design = window.HIVEMIND_DESIGNS.new;
  design.drilldowns = design.drilldowns || {};
  design.drilldowns.universe = {
    button: 'Explore the universe: subjects, tracked categories and themes',
    kicker: 'Research universe · Details',
    size: 'full',
    render(container, context) {
      const escapeHtml = context.escapeHtml;
      const kindRows = OBJECT_KINDS.map((row) => `<tr><td>${escapeHtml(row.label)}</td><td>${escapeHtml(row.identifiers)}</td>`
        + `<td class="schema-table__quiet">${escapeHtml(row.example)}</td></tr>`).join('');
      const defaultRows = TRACKING_DEFAULTS.map((row) => `<tr><td>${escapeHtml(row.kind)}</td><td>${escapeHtml(row.plain)}</td>`
        + `<td class="schema-table__quiet">${escapeHtml(row.codes)}</td></tr>`).join('');
      const themeRows = THEME_LIBRARY.map((row) => `<tr><td>${escapeHtml(row.category)}</td><td>${escapeHtml(row.themes)}</td></tr>`).join('');
      const trackingRows = TRACKING_EXAMPLES.map((row) => `<tr><td>${escapeHtml(row.theme)}</td><td>${escapeHtml(row.tracked)}</td>`
        + `<td class="schema-table__quiet">${escapeHtml(row.codes)}</td></tr>`).join('');

      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">Research universe: subjects and tracked information</h2>
          <p class="drill__intro">The four subject kinds are companies (over 500 US-listed companies), cryptocurrencies, commodities, and macroeconomic, political, economic or geopolitical themes. Each specifies tracked information categories; upstream supplies only that scope.</p>
          <div class="drill__columns drill__columns--schema">
            <section>
              <h3 class="drill__heading">Four subject kinds</h3>
              <table class="schema-table schema-table--compact">
                <thead><tr><th>Kind</th><th>Identifiers</th><th>Example</th></tr></thead>
                <tbody>${kindRows}</tbody>
              </table>
              <h3 class="drill__heading drill__heading--spaced">Default categories by subject kind</h3>
              <table class="schema-table schema-table--compact">
                <thead><tr><th>Kind</th><th>Tracked information</th><th>Category IDs</th></tr></thead>
                <tbody>${defaultRows}</tbody>
              </table>
              <h3 class="drill__heading drill__heading--spaced">Draft theme library: 12 groups</h3>
              <table class="schema-table schema-table--compact">
                <thead><tr><th>Group</th><th>Theme</th></tr></thead>
                <tbody>${themeRows}</tbody>
              </table>
              <h3 class="drill__heading drill__heading--spaced">Tracked information for a theme: examples</h3>
              <table class="schema-table schema-table--compact">
                <thead><tr><th>Theme</th><th>Tracked information</th><th>Category IDs</th></tr></thead>
                <tbody>${trackingRows}</tbody>
              </table>
            </section>
            <section>
              <h3 class="drill__heading">Rules</h3>
              <ol class="drill__rules">${RULES.map((rule) => `<li>${escapeHtml(rule)}</li>`).join('')}</ol>
            </section>
          </div>
        </div>`;
    },
  };
})();
