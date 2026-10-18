// The new system design, built one piece at a time from the Old tab. Edit, save, refresh the page.
//
// nodes:   id → { title, kind, from, subtitle?, status?, purpose?, inputs?, outputs?, checks?, inspect?, verified?,
//          open?, refs? }
//          kind is one of control, external, model, code, mixed, store. `from` lists the Old node ids this node
//          carries over or replaces. `status` marks a decided piece. Only the fields present are shown, so a node can
//          start as a title and its open questions.
// views:   [{ id, title, kind?, caption?, nodes: [[nodeId, column, row]], edges: [[from, to, label?, style?]] }]
//          style is '' (data), 'control' (control / feedback) or 'candidate' (local only). An edge written as an
//          object may also name a route (bottom, left, right, down). The inspection order is the node list's order
//          unless `order` is given; the canvas sizes itself.
// dropped: Old node id → why it does not come over.
//
// Every Old node is then carried over (named by a `from`), dropped, or not yet decided; the migration list shows which.
// The texts are for a reader who has not followed the discussion: plain words and an example, no field names; the
// decision behind each text is in docs/DECISIONS.md.
window.HIVEMIND_DESIGNS = window.HIVEMIND_DESIGNS || {};
window.HIVEMIND_DESIGNS.new = {
  id: 'new',
  title: 'New',
  heading: '新系统设计',
  summary: '这是写 PRD 之前的架构草图，只有设计，没有代码。系统怎么工作：上游不断把信息推进来，每条都已经贴好了类别标签；系统决定每条交给谁，表格类的数据交给程序直接读，文字类的材料交给模型读；读出来的事实存进研究库，再推动研究结论更新。没有新信息进来，系统就什么都不做。另一种方式是到了约定日期或定时，系统主动去查证（Pull 模式），以后设计。查不到、判断不了的东西，放进人工复核池等人看。研究对象名单、分类、Config、分发、人工复核池这五块已经冻结第一版，以后要改，先记一条新决定。和旧系统的区别：旧系统按日期主动去拉数据、一批一批处理；新系统是信息来了就处理。测试时，用一个测试程序把测试库里的旧数据按日期顺序推进来，走同一条路。所有决定记在 docs/DECISIONS.md。',
  repositoryRoot: '../',
  prd: 'docs/prd/00-system.md',
  prdTitle: '系统总览',
  nodeHeight: 200,
  gridRowStep: 235,
  subtitleLines: 6,
  documents: [
    { label: 'Working rules (AGENTS.md)', path: 'AGENTS.md' },
    { label: 'Decisions (DECISIONS.md)', path: 'docs/DECISIONS.md' },
    { label: 'Current state (CURRENT_STATE.md)', path: 'docs/CURRENT_STATE.md' },
  ],
  nodes: {
    classify: {
      title: '分类（上游完成）',
      prd: 'docs/prd/02-classification.md',
      subtitle: '上游已经给每条信息贴好标签：属于哪一类（共 16 类）、是文字还是表格、讲的是哪家公司或哪个主题。这里写贴标签的规则，我们照着检查。',
      kind: 'external',
      status: '第一版已冻结 · 2026-10-16',
      from: [],
      purpose: '上游给每条信息贴好标签再推给我们：它属于哪一类（业绩稿、新闻、宏观数据……一共 16 类），是文字还是表格，讲的是哪家公司或哪个主题。这里写的是贴标签的规则：上游照着贴，我们照着检查。',
      inputs: '上游拿到的原始材料，以及材料自带的信息：谁发的、哪天发的、从哪个渠道来、讲的是哪些公司或主题。',
      outputs: '贴好标签的一条信息。或者判定为：重复的（并到原来那条）、不算材料的（比如别人已经算好的指标）、不合格的（写明原因）。',
      checks: '只按规则和对照表判断，不用模型。看的是材料是什么，不看谁发的：同样是宏观数据，政府发的和民间机构发的归同一类。时间只看发布在纽约时间的哪一天。对照表里查不到的不猜，交给人工复核池。',
      inspect: [
        '先看材料自带的信息全不全：谁发的、哪天发的、从哪来。',
        '照着分类规则走一遍，确认它只落到一个类别。',
        '被拒的看原因：缺信息、没有文字可读、对照表里查不到。',
      ],
      verified: [
        '用旧系统的 412 条真实材料和 161 个手写例子测过，全部分对。',
        '“讲的是哪家公司”：24 个手写例子全对；旧数据里能独立核对的 17 条，和旧系统的结果一致。只测了公司，加密、商品、主题还没测。',
        '宏观类的规则（央行材料、IMF 预测、民间统计等）是逐条推演出来的，还没有跑测试。',
        'TrueNorth 的 54 个数据接口，每个都能归到类别里。',
      ],
      open: [
        '上游怎样拿到材料、怎样贴标签，以后再谈；“代码对应哪家公司”的对照表也归上游管。',
      ],
      refs: [
        { path: 'docs/system-design/new-classification.js', symbol: 'TAGS · TREE · INPUT_SCHEMA · LOOKUP_TABLES · RULES · OBJECT_RULES · TIME_RULES' },
        { path: 'docs/system-design/simulate_classification.py', symbol: 'classify · related_companies · CASES · COMPANY_CASES' },
      ],
    },
    dispatch: {
      title: '分发',
      prd: 'docs/prd/04-dispatch.md',
      subtitle: '系统入口。每条信息依次问：完整吗？处理过吗？分类结果是什么？文字还是表格？然后退回、跳过、不处理，或交给程序、交给模型。',
      kind: 'code',
      status: '第一版已冻结 · 2026-10-16',
      from: [],
      purpose: '系统的入口。每来一条信息，依次问四个问题：信息完整吗？以前处理过吗？分类结果是什么？是文字还是表格？最后只有一个去处：退回、跳过、不处理，或者交给程序、交给模型。',
      inputs: '上游推来的信息；Config 里的模型设置；以前的处理记录。',
      outputs: '每条信息的去处。有问题的（缺信息、对照表里查不到）同时放进人工复核池。',
      checks: '缺信息的退回，这是上游的问题。同一条信息再来一次就跳过，不重复花钱；改过的新版本照常处理。不看信息讲的是哪家公司或哪个主题。没有信息进来，就什么都不做。',
      inspect: [
        '一条信息没被处理：照着上面四个问题走一遍，看它停在哪一步。',
      ],
      refs: [
        { path: 'docs/system-design/new-config.js', symbol: 'DISPATCH_TREE' },
      ],
    },
    code: {
      title: '代码处理',
      prd: 'docs/prd/05-code-processing.md',
      subtitle: '股价、财报、CPI 这类整齐的表格，程序直接读出数字。不用模型，不花钱，结果每次都一样。',
      kind: 'code',
      from: [],
      purpose: '股价、财务报表、CPI 这类数据本身就是整齐的表格，程序直接读出数字，不用模型，不花钱，每次结果都一样。',
      inputs: '分发交过来的表格类数据。',
      outputs: '读出来的数字和事实，存进研究库。',
      open: [
        '读出来的东西长什么样，还没设计。',
      ],
    },
    extract: {
      title: '模型抽取',
      prd: 'docs/prd/06-model-extraction.md',
      subtitle: '业绩稿、新闻、公告这类文字交给模型读，整理成一条条事实，比如“iPhone 收入 462 亿美元”，并写明讲的是谁。',
      kind: 'model',
      from: [],
      purpose: '业绩稿、新闻、公告这类文字，交给模型读懂，整理成一条条事实，比如“Apple 第三季度 iPhone 收入 462 亿美元”。每条事实都写明讲的是哪家公司或哪个主题。如果讲的是名单里没有的东西（比如一场新的冲突），交给人工复核池。',
      inputs: '分发交过来的文字材料；Config 里的模型设置。',
      outputs: '整理出来的事实，存进研究库。',
      open: [
        '整理出来的事实长什么样，还没设计。',
        '不同类别的材料要不要用不同的模型设置，以后再谈。',
      ],
    },
    store: {
      title: '研究库',
      prd: 'docs/prd/07-research-store.md',
      subtitle: '系统自己的库：存读出来的事实（写明讲的是谁）和每条信息的处理记录。原文不存，留在上游的库里。',
      kind: 'store',
      from: [],
      purpose: '存两样东西：读出来的事实（每条都写明讲的是谁），以及每条信息的处理记录（处理过没有、怎么处理的）。原始材料不存在这里，留在上游的库里，要看原文就去那里查。',
      inputs: '程序和模型读出来的结果。',
      outputs: '事实，以后用来推动研究结论；处理记录，分发用它判断“以前处理过没有”。',
      open: [
        '事实长什么样，还没设计。',
        '新事实怎样推动研究结论更新，等设计研究结论时再定。',
      ],
    },
    thesis: {
      title: 'thesis · ladder · evidence',
      prd: 'docs/prd/08-thesis.md',
      subtitle: '研究结论，以后设计。新事实进来时跟着更新；也可以到期或定时，由 Pull 模式主动查证。',
      kind: 'model',
      from: [],
      purpose: '以后设计。研究结论有两种方式更新：一是新事实进来，相关的结论跟着更新；二是到了约定日期或定时，系统主动去查证（Pull 模式）。',
      open: [
        'thesis、ladder、evidence 各是什么、怎么定义。',
        '哪些结论需要到期检查或定时检查。',
      ],
    },
    pull: {
      title: 'Pull 模式',
      prd: 'docs/prd/09-pull-mode.md',
      subtitle: '以后设计。不等信息进来，到了约定日期或按固定时间，系统主动去查某个结论的条件满足了没有。',
      kind: 'mixed',
      from: [],
      purpose: '和信息流的方向相反：不等信息进来，而是到了某个日期，或者按固定时间，系统主动去查某个结论的条件满足了没有。这是系统里唯一按时间触发的地方。',
      open: [
        '哪些结论需要到期检查，由研究结论的设计决定。',
        '主动查到的信息，要不要也走分发进来。',
        '它和上游推送是两回事：上游推送只负责把信息送进来。',
      ],
    },
    review: {
      title: '人工复核池',
      prd: 'docs/prd/10-review-pool.md',
      subtitle: '查不到、判断不了的东西先放这里等人看，比如新出现的指标、名单里没有的公司或主题。人看完怎么处理，先不设计。',
      kind: 'store',
      status: '第一版已冻结 · 2026-10-16（只定了哪些东西会进来）',
      from: [],
      purpose: '对照表里查不到、规则判断不了的东西，系统不猜，先放进这个池子等人来看。现在只定哪些东西会进来；人看完以后怎么处理，先不设计。',
      inputs: '新出现的表格代码或数据集；判断不了是谁发的；新的指标；查不到的公司或主题代码；模型读材料时发现讲的是名单里没有的东西（比如一场新的冲突）；信息缺东西（这是上游的问题）。',
      outputs: '先不设计。',
      checks: '只放真正查不到的。比如 Apple 的新闻里提到三星，三星查得到，只是不在我们的名单里，这不算。同一个问题只记一条，附上出现了几次、举几个例子。',
      open: [
        '人看完以后怎样更新对照表或名单、怎样生效（以后设计）。',
        '怎样通知、由谁来看（以后设计）。',
      ],
    },
    universe: {
      title: '研究对象名单',
      prd: 'docs/prd/01-universe.md',
      subtitle: '研究哪些对象：500 多只美股、加密货币、商品、宏观主题；以及每个对象要看哪几类信息。上游只推这个范围。',
      kind: 'control',
      status: '第一版已冻结 · 2026-10-16（具体主题还是草稿）',
      from: [],
      purpose: '决定两件事。一是研究哪些对象：500 多只美股、加密货币、商品，还有宏观主题（比如美国通胀、中美关税）。二是每个对象要看哪几类信息：股票要看财报和新闻，关税主题要看政府公告。上游只推这个范围内的信息，推进来的都处理。系统里只有这里决定“处理什么”。',
      inputs: '人维护的名单。',
      outputs: '名单的一个版本：每个对象一行，写明它是什么、要看哪几类信息。股票、加密、商品各有一套默认，主题各自写。',
      checks: '要看的类别必须是 16 类之一，主题至少写一类；名单里的对象查不到，这一版不能用。改了名单就是一个新版本，上游按新名单把以前的相关信息补推一遍。利率、汇率、指数不单独列，算在主题里（比如“美债利率”）。新出现的公司或主题不会自动加进来，先进人工复核池。',
      open: [
        '主题库里具体有哪些主题，还是草稿。',
        '上游怎样按名单推送，以后再谈。',
        '名单存在哪里、由谁维护。',
      ],
      refs: [
        { path: 'docs/system-design/new-universe.js', symbol: 'OBJECT_KINDS · TRACKING_DEFAULTS · THEME_LIBRARY · TRACKING_EXAMPLES' },
      ],
    },
    config: {
      title: 'Config',
      prd: 'docs/prd/03-config.md',
      subtitle: '只管一件事：模型读文字材料时，用哪个模型、哪一版提示词。改一次就是一个新版本。',
      kind: 'control',
      status: '第一版已冻结 · 2026-10-16（要不要每类一套，还没定）',
      from: ['config'],
      purpose: '只管一件事：模型读文字材料时，用哪个模型、哪一版提示词。改一次就是一个新版本，每条处理记录都会写下当时用的是哪个版本。',
      inputs: '由人设定。',
      outputs: '一个版本号；模型抽取按它来读。',
      checks: '设定里引用了不存在的模型设置，整个版本不能用。不设预算和并发上限。',
      open: [
        '所有类别共用一套模型设置，还是每类各一套（以后再谈）。',
      ],
      refs: [
        { path: 'docs/system-design/new-config.js', symbol: 'CONFIG_SCHEMA · RULES' },
      ],
    },
  },
  views: [
    {
      id: 'system',
      title: 'System overview',
      kind: 'Component handoffs',
      caption: '中间一行是信息走的路：上游 → 分发 → 程序读或模型读 → 研究库 → 研究结论。左边的虚线框是上游，不归这个系统管。上面一排是设置：研究对象名单交给上游，决定推什么；Config 告诉模型怎么读。右上的 Pull 模式和下面的人工复核池，以后再细化。',
      nodes: [['universe', 0, 0], ['config', 1, 0], ['pull', 4, 0], ['classify', 0, 1], ['dispatch', 1, 1], ['code', 2, 1], ['extract', 2, 2], ['store', 3, 1], ['thesis', 4, 1], ['review', 1, 2]],
      order: ['classify', 'dispatch', 'code', 'extract', 'store', 'thesis', 'pull', 'review', 'universe', 'config'],
      edges: [
        ['universe', 'classify', '推哪些对象的哪几类信息', 'control'],
        ['classify', 'dispatch', '贴好标签的信息'],
        ['config', 'dispatch', '模型设置', 'control'],
        ['dispatch', 'code', '表格类'],
        ['dispatch', 'extract', '文字类'],
        ['code', 'store', '读出的事实'],
        ['extract', 'store', '读出的事实'],
        ['store', 'thesis', '新事实推动更新'],
        ['pull', 'thesis', '到期或定时去查', 'control'],
        ['dispatch', 'review', '查不到、有问题的'],
        { source: 'extract', target: 'review', label: '名单里没有的东西', route: 'bottom' },
      ],
    },
  ],
  dropped: {},
};
