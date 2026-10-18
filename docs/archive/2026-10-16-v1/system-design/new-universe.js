// The New design's research universe: the objects the system researches, the kinds of information tracked for each, and
// the theme library among them. Edit the data at the top; the drill-down renders it. Decisions D6, D11 and D18 in
// docs/DECISIONS.md. The texts are for a reader who did not follow the discussion: plain words, no field names.
(function () {
  'use strict';

  const OBJECT_KINDS = [
    { label: '公司', identifiers: '股票代码、SEC 编号或公司名', example: '500 多只美股：Apple、Amazon、Meta……' },
    { label: '加密货币', identifiers: '加密货币代码', example: '比特币、以太坊……' },
    { label: '商品', identifiers: '商品代码', example: '黄金、原油、铜……' },
    { label: '主题', identifiers: '主题库里的编号', example: '美国通胀、中美关税、俄乌战争……' },
  ];

  // What each kind of object looks at by default: the one place that decides which kinds of information are processed.
  const TRACKING_DEFAULTS = [
    { kind: '公司', plain: '公司自己发的（业绩、定期报告、法律文件、电话会、演示材料、其他发布）、新闻、观点、访谈、官方对它的行动、股价、持仓、日历、第三方数据', codes: 'T1–T10、T12–T15' },
    { kind: '加密货币', plain: '新闻、观点、官方行动（执法、ETF 审批）、价格、资金与持仓、解锁日历、链上数据', codes: 'T7、T8、T10、T12–T15' },
    { kind: '商品', plain: '新闻、观点、官方行动（OPEC 决定、制裁）、统计数据（EIA 库存）、价格、持仓（CFTC）、日历、航运和卫星数据', codes: 'T7、T8、T10–T15' },
    { kind: '主题', plain: '没有默认，每个主题自己写', codes: '—' },
  ];

  // The theme library, first draft: the macro, political, economic and geopolitical drivers that move the objects above.
  const THEME_LIBRARY = [
    { category: '货币与利率', themes: '美联储政策利率 · 美债收益率曲线 · 欧央行、日本央行、人民银行政策' },
    { category: '通胀', themes: '美国通胀 · 工资增长 · 能源价格传导' },
    { category: '增长与就业', themes: '美国衰退风险 · 就业市场 · 消费支出 · 中国经济 · 欧洲经济' },
    { category: '财政', themes: '美国赤字与发债 · 债务上限与政府停摆 · 税收政策' },
    { category: '贸易与产业政策', themes: '中美关税 · 芯片出口管制 · 产业补贴（CHIPS 法案、IRA）· 供应链转移' },
    { category: '地缘政治与战争', themes: '俄乌战争 · 中东冲突 · 台海局势 · 制裁' },
    { category: '政治与选举', themes: '美国大选 · 政策走向' },
    { category: '监管与法律', themes: '美欧反垄断 · 数据与隐私 · AI 监管 · 金融监管' },
    { category: '能源与大宗', themes: '原油供给（OPEC）· 天然气 · 工业金属' },
    { category: '汇率与资本流动', themes: '美元强弱 · 人民币 · 日元' },
    { category: '产业周期', themes: 'AI 资本开支 · 半导体周期 · 云计算需求' },
    { category: '市场风险偏好', themes: '信用利差 · 波动率 · 流动性' },
  ];

  const TRACKING_EXAMPLES = [
    { theme: '美国通胀', tracked: 'CPI、PCE 数据和 BLS 的发布稿，ISM 的物价分项，密歇根大学的通胀预期（宏观统计）；相关新闻；经济学家的预测', codes: 'T11、T7、T8' },
    { theme: '中美关税', tracked: 'USTR、商务部的公告（官方行动）；相关新闻和评论；公司财报和电话会里提到关税的部分', codes: 'T10、T7、T8、T1–T6' },
  ];

  const RULES = [
    '名单单独管理、单独出版本，不放在 Config 里。主题库是名单的一部分，不另外建一份。',
    '名单决定两件事：研究哪些对象，以及每个对象要看哪几类信息。系统里只有这里决定“处理什么”。',
    '公司、加密货币、商品各有一套默认要看的类别；主题没有默认，每个主题自己写，至少写一类。要看的类别必须是 16 类之一；名单里的对象在参照数据或主题库里查不到，这一版不能用。',
    '上游只推名单范围内的信息，也就是“名单里的对象 × 它要看的类别”；测试程序也按这个范围推。推进来的都处理。',
    '名单加了对象或改了要看的类别，就是一个新版本；上游按新名单把以前的相关信息补推一遍。',
    '利率、汇率、指数不单独列，算在主题里（比如“美债收益率曲线”“美元强弱”）。',
    '新出现的公司或主题不会自动加进名单，先放进人工复核池，由人决定。',
    '宏观、地缘政治怎么连到个股：靠研究结论。每只股票的结论写明它依赖哪些因素，可以是公司自己的，也可以是主题；某个主题有了新事实，就找出依赖它的结论（研究结论还没设计）。',
  ];

  const design = window.HIVEMIND_DESIGNS.new;
  design.drilldowns = design.drilldowns || {};
  design.drilldowns.universe = {
    button: '展开名单：有哪些对象、各看哪几类信息、主题库',
    kicker: '研究对象名单 · 详细说明',
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
          <h2 class="drill__title">研究对象名单：研究什么，每样要看哪几类信息</h2>
          <p class="drill__intro">研究的对象有四种：公司（500 多只美股）、加密货币、商品，以及宏观、政治、经济、地缘政治的主题。每个对象还写明要看哪几类信息，上游只推这个范围内的信息。</p>
          <div class="drill__columns drill__columns--schema">
            <section>
              <h3 class="drill__heading">对象有四种</h3>
              <table class="schema-table schema-table--compact">
                <thead><tr><th>种类</th><th>用什么认出它</th><th>例子</th></tr></thead>
                <tbody>${kindRows}</tbody>
              </table>
              <h3 class="drill__heading drill__heading--spaced">每种对象默认要看哪几类信息</h3>
              <table class="schema-table schema-table--compact">
                <thead><tr><th>种类</th><th>要看的信息</th><th>类别编号</th></tr></thead>
                <tbody>${defaultRows}</tbody>
              </table>
              <h3 class="drill__heading drill__heading--spaced">主题库草稿：12 个大类</h3>
              <table class="schema-table schema-table--compact">
                <thead><tr><th>大类</th><th>主题</th></tr></thead>
                <tbody>${themeRows}</tbody>
              </table>
              <h3 class="drill__heading drill__heading--spaced">一个主题要看什么（例子）</h3>
              <table class="schema-table schema-table--compact">
                <thead><tr><th>主题</th><th>要看的信息</th><th>类别编号</th></tr></thead>
                <tbody>${trackingRows}</tbody>
              </table>
            </section>
            <section>
              <h3 class="drill__heading">规则</h3>
              <ol class="drill__rules">${RULES.map((rule) => `<li>${escapeHtml(rule)}</li>`).join('')}</ol>
            </section>
          </div>
        </div>`;
    },
  };
})();
