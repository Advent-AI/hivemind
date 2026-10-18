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
  summary: '这是新系统的架构设计，每个模块都有 PRD，只有设计，没有代码。系统做的事情，就是建立、更新和关掉一个观点库。上游不断把信息推进来，每条都已经带着分类结果（多数是 16 类之一）；分发检查后，带上顺序号交给抽取。抽取只负责读：用资深对冲基金分析师的视角，按这一类的提示词把每条信息整份读完，读出观点和证据；观点库再把它们和已有的驱动对上：加证据、新建，或者送最终判定。观点分两层：主题层讲世界上会发生什么，对象层讲某家公司（或加密货币、商品）会怎样，用“前提”连起来。每条观点和证据都带出处，能顺着出处找回那条信息。观点被证伪或过期就关掉，但留在库里供查历史；关之前由最终判定把整条观点和全部证据看一遍。到期和定时的事由 Pull 模式做。没有新信息进来，信息流这一边什么都不做。查不到、拿不准的放进人工复核池。研究对象名单、分类、Config、分发、抽取、人工复核池这六块的第一版已冻结（2026-10-18），要改先记一条新决定；观点库和最终判定还在设计中，Pull 模式只定了一部分。和旧系统的区别：旧系统按日期主动拉数据、一批一批处理，还把每家公司的财报拆成一大堆数；新系统信息来了就处理，从观点出发。所有决定记在 docs/DECISIONS.md。',
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
      subtitle: '上游已经给每条信息贴好标签：分类结果（多数是 16 类之一，也可能是重复、不算材料或不合格）、是文字还是表格、讲的是谁。这里写贴标签的规则。',
      kind: 'external',
      status: '第一版已冻结 · 2026-10-18',
      from: [],
      purpose: '上游给每条信息贴好标签再推给我们：分类结果，多数是属于哪一类（业绩稿、新闻、宏观数据……一共 16 类），也可能是重复、不算材料或不合格；是文字还是表格；讲的是谁。这里写的是贴标签的规则：上游照着贴；我们不重新分一遍，只在分发时检查信息是否完整、类别是否有效。',
      inputs: '上游拿到的原始材料，以及材料自带的信息：谁发的、哪天发的、从哪个渠道来、讲的是谁。',
      outputs: '贴好标签的一条信息。或者判定为：重复的（并到原来那条）、不算材料的（比如别人算好、我们自己就能算出来的指标）、不合格的（写明原因）。',
      checks: '只按规则和对照表判断，不用模型。看的是材料是什么：同样是宏观数据，政府发的和民间机构发的归同一类。时间只看发布在纽约时间的哪一天。对照表里查不到的不猜：作者类型先用渠道默认的，其余查不到的交给人工复核池。',
      inspect: [
        '先看材料自带的信息全不全：谁发的、哪天发的、从哪来。',
        '照着分类规则走一遍，确认它只有一个分类结果；要归类的，只落到一个类别。',
        '不合格的看原因：缺信息、没有文字可读、对照表里查不到。',
      ],
      verified: [
        '用旧系统的 412 条真实材料和 161 个手写例子测过，全部分对。',
        '“讲的是谁”：24 个手写例子全对；旧数据里能独立核对的 17 条，和旧系统的结果一致。只测了公司，加密货币、商品、主题还没测。',
        '宏观类的规则（央行材料、IMF 预测、民间统计等）是逐条推演出来的，还没有跑测试。',
        'TrueNorth 的 54 个数据接口，每个都能归到类别里。',
      ],
      open: [
        '上游怎样拿到材料、怎样贴标签，以后再谈；“标识对应哪个对象”的对照表也归上游管。',
      ],
      refs: [
        { path: 'docs/system-design/new-classification.js', symbol: 'TAGS · TREE · INPUT_SCHEMA · LOOKUP_TABLES · RULES · OBJECT_RULES · TIME_RULES' },
        { path: 'docs/system-design/simulate_classification.py', symbol: 'classify · related_companies · CASES · COMPANY_CASES' },
      ],
    },
    dispatch: {
      title: '分发',
      prd: 'docs/prd/04-dispatch.md',
      subtitle: '系统入口。每条信息依次问：完整吗？处理过吗？分类结果是什么？然后退回、跳过、不处理、并到原来那条，或带上顺序号交给抽取。',
      kind: 'code',
      status: '第一版已冻结 · 2026-10-18',
      from: [],
      purpose: '系统的入口。每来一条信息，依次问三个问题：信息完整吗？以前处理过吗？分类结果是什么？最后只有一个去处：退回、跳过、不处理、并到原来那条，或者交给抽取。交给抽取时带上类别和顺序号；顺序号按到达的先后编，不用电脑时钟，后面每一步都按它排先后。',
      inputs: '上游推来的信息；以前的处理记录。',
      outputs: '每条信息的去处。有问题的（缺信息、对照表里查不到）同时放进人工复核池。',
      checks: '缺信息的退回，这是上游的问题。同一上游编号、同一版本已经处理完的，再来就跳过，不重复花钱；没做完的从记下的那一步接着做；改过的新版本照常处理。不看信息讲的是谁。没有信息进来，就什么都不做。',
      inspect: [
        '一条信息没被处理：照着上面三个问题走一遍，看它停在哪一步。',
      ],
      refs: [
        { path: 'docs/system-design/new-config.js', symbol: 'DISPATCH_TREE' },
      ],
    },
    extract: {
      title: '抽取',
      prd: 'docs/prd/05-extraction.md',
      subtitle: '只做一件事：每条信息整份交给模型，用资深对冲基金分析师的视角、按这一类的提示词，读出观点（thesis）和证据，每条带出处，交给观点库。',
      kind: 'model',
      status: '第一版已冻结 · 2026-10-18（没定的：每一类提示词的具体写法）',
      from: [],
      purpose: '系统里唯一读信息的模块，只负责读。每条信息整份交给模型（文件连同里面的表格一起读，表格数据整批读）；角色是一位资深对冲基金分析师，按这条信息的类别用这一类的提示词（每一类一份，拼法相同），读出它看到的观点，以及支持或削弱观点的证据，每条带出处。代码核对出处以后，交给观点库；怎么和已有观点对上、写进去，是观点库的事。比如 2025-04-15 NVDA 的 8-K 说 H20 出口中国要许可证、预计计提约 55 亿美元：读出主题层“未来一年美国对华 AI 芯片出口管制会收紧”，和对象层（NVDA）“一年内中国数据中心收入基本归零”，后者以前者为前提。',
      inputs: '分发交过来的信息、它的类别和顺序号；Config 里这一类读的设置；这条信息相关对象已有驱动的名字（提示词模板最后一块）。',
      outputs: '候选观点和证据，每条带出处，交给观点库；多次处理失败的信息放进人工复核池。',
      checks: '原文那一句必须在这条信息里，数字必须印在那一句或那一格里；对不上的不交出去，记下原因。',
      inspect: [
        '一条观点从哪来：看它的出处，凭上游编号回团队的库里取原文。',
      ],
      open: [
        '每一类提示词的具体写法，建的时候在存下的信息上试过再定；每一版记在 Config 里。',
      ],
      refs: [
        { path: 'docs/system-design/new-facts.js', symbol: 'TEMPLATE · PROMPT_EXAMPLE · CATEGORY_READS · EXTRACT_STEPS · SOURCE_TREE · EXTRACT_EXAMPLE_TREE' },
      ],
    },
    views: {
      title: '观点库（thesis · ladder · evidence）',
      prd: 'docs/prd/06-views.md',
      subtitle: '系统的核心：对象 → 驱动 → 观点。抽取交来的观点和证据在这里去重、对上已有的驱动、写进库。分主题层和对象层，用前提连起来；每条带出处，关掉的也留着。',
      kind: 'store',
      from: [],
      purpose: '整个系统做的事，就是建立、更新和关掉这个库里的观点。每个对象（公司、加密货币、商品、主题）下面挂几个写得具体的驱动，比如“美国对华 AI 芯片出口管制”；每个驱动下面挂观点：一句写下不改的主张、方向、期限档、利好还是利空、理由，加上支持或削弱它的证据、证实和证伪的检验条件，以及它依赖的前提。抽取交来的观点和证据，先去重，再列出候选驱动（相关对象的全部驱动，加上从全部主题驱动里搜到的几条），由模型选“属于哪个驱动”，最后代码比方向和期限档，决定挂支持证据、挂削弱证据、新建观点还是新建驱动；需要判对错的交给最终判定。观点是模型（分析师）的判断；证据是客观的：谁在哪份文件里说了什么，分四层：发生的事、当事人说的、第三方看法、传闻。观点分两层：主题层讲世界上会发生什么，对象层讲这个对象会怎样，用前提连起来，前提记着上次看过第几版。观点每变一次多一版，旧版和关掉的观点都留着。从一条观点能查到全部来源文件，从一份文件也能查到它改过的全部观点。另外还有处理记录，分发靠它判断以前处理过没有。原文不存，凭编号去团队的库里取。',
      inputs: '抽取交来的候选观点和证据；Config 里“对上”的设置；最终判定的结论；Pull 模式定期合并和拆分驱动的结果。',
      outputs: '给抽取提示词模板用的已有驱动名字；给最终判定的观点和全部证据；拿不准的、名单外的对象、建议新增的主题放进人工复核池；每只股票的全貌（它自己的观点，加上这些观点的前提）；由代码算出的共识，以及每个来源说得准不准的记录。',
      checks: '模型给的驱动和观点编号只能是候选里的；每条观点只有一个写入者；只有文件能产生证据，观点之间只传通知；检验条件只能加；只凭第三方看法和传闻不能关掉观点；前提不能绕成环。',
      open: [
        '存在哪里、用什么数据库，和建的时候一起定。',
        '名单加了新对象、上游补推它的历史时，补推的旧文件可能另建出重复的观点，靠定期合并收拾。',
        '真建之前要在存下的数据上量：每个对象挂多少驱动；两次独立标注“同一个驱动”是否一致；判“新驱动”准不准。',
      ],
      refs: [
        { path: 'docs/system-design/new-facts.js', symbol: 'WRITE_STEPS · DECIDE_TREE · WRITE_EXAMPLE_TREE · VIEW_TREE · LEVEL_TREE · VIEW_FIELDS · EVIDENCE_FIELDS · TIERS · PROPAGATION_TREE · ORDER_RULES · CONFLICT_RULES' },
      ],
    },
    verdict: {
      title: '最终判定',
      prd: 'docs/prd/07-final-verdict.md',
      subtitle: '一条观点要关之前，模型把它、它的全部证据和前提的现状完整看一遍，判关掉（证实、证伪、过期）还是留下。',
      kind: 'model',
      from: [],
      purpose: '一条观点要不要关，不由一条证据或一个条件直接决定，而是先交到这里：模型把这条观点、它的全部证据、前提的现状和这次为什么被触发一起看完，判关掉还是留下。能判成已证实或已证伪的，只有检验条件加上“发生的事”这一层的证据；只凭别人的看法和传闻不能判。到期了还没有任何能判的证据，记“没有数据可验证”，不算对也不算错。比如 2025 年 8 月据报道美国开始发 H20 许可证：主题观点“管制会收紧”判为已证伪；以它为前提的 NVDA 观点再判一次，因为据报道中国要求企业不要采购 H20，中国收入仍没回来，所以留下，前提换成一条新的主题观点。',
      inputs: '被触发的观点、它的全部证据、前提的现状；触发的原因（由代码或 Pull 模式给出）；Config 里最终判定的设置。',
      outputs: '这条观点的新版本：关掉（写明依据），或留下（可以换前提、加检验条件）。一条观点关掉时，以它为前提的观点各自再送一次。',
      checks: '判完写明依据哪几条证据和出处；关掉的观点留在库里，可以查历史。',
      refs: [
        { path: 'docs/system-design/new-facts.js', symbol: 'VERDICT_TRIGGERS · VERDICT_TREE · VERDICT_RULES' },
      ],
    },
    pull: {
      title: 'Pull 模式',
      prd: 'docs/prd/08-pull-mode.md',
      subtitle: '系统里唯一按时间做事的地方：到期的观点送最终判定，前提落后太久的兜底复核，定期合并和拆分驱动。',
      kind: 'mixed',
      from: [],
      purpose: '和信息流的方向相反：不等信息进来，而是按日期和固定时间做三件事。一是到期：观点的检验条件或期限到了，送最终判定；要等发布日不晚于期限的文件都处理完再判，免得漏掉一份晚处理的文件。二是兜底复核：前提被削弱、超过 7 天还没人看过的观点，送最终判定。三是定期合并和拆分驱动：把其实相同的驱动合并（只是改指向，可以撤回），把混在一起的拆开。Pull 模式用的“现在”从外面传进来：上线用真实时间，测试用回放的时间。检验条件用到股价、日历这类数据时，也由这里去查。',
      inputs: '观点库里的期限、检验条件和前提的版本；外面传进来的“现在”。',
      outputs: '送最终判定的观点；合并和拆分驱动的结果，写回观点库。',
      open: [
        '定期合并和拆分多久做一次、怎样做；兜底复核的 7 天是先定的数，要在数据上调。',
        '检验条件用到的股价、XBRL 等数据从哪里查（团队自己的库，还是直接去源头）；查到的要不要也走分发进来。',
      ],
    },
    review: {
      title: '人工复核池',
      prd: 'docs/prd/09-review-pool.md',
      subtitle: '查不到、判断不了的东西先放这里等人看，比如新出现的指标、名单里没有的公司或主题。人看完怎么处理，先不设计。',
      kind: 'store',
      status: '第一版已冻结 · 2026-10-18（只定了哪些东西会进来，输出先不设计）',
      from: [],
      purpose: '对照表里查不到、规则判断不了的东西，系统不猜，先放进这个池子等人来看。现在只定哪些东西会进来；人看完以后怎么处理，先不设计。',
      inputs: '新出现的申报代码或数据集；判断不了作者类型；新的指标；查不到的公司或主题标识；写进观点库时发现讲的是名单里没有的东西（比如一场新的冲突）；写进观点库时对不上驱动、拿不准的；建议新增的主题；多次处理失败的信息；信息缺东西（这是上游的问题）。',
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
      status: '第一版已冻结 · 2026-10-18（具体主题还是草稿）',
      from: [],
      purpose: '决定两件事。一是研究哪些对象：500 多只美股、加密货币、商品，还有宏观主题（比如美国通胀、中美关税）。二是每个对象要看哪几类信息：公司要看财报、新闻和公司公告，关税主题要看政府公告。上游只推这个范围内的信息，推进来的都处理。系统里只有这里决定“处理什么”。',
      inputs: '人维护的名单。',
      outputs: '名单的一个版本：每个对象一行，写明它是什么、要看哪几类信息。公司、加密货币、商品各有一套默认，主题各自写。',
      checks: '要看的类别必须是 16 类之一，主题至少写一类；名单里的对象查不到，这一版不能用。改了名单就是一个新版本，上游按新名单把以前的相关信息补推一遍。利率、汇率、指数不单独列，算在主题里（比如“美债收益率曲线”）。新出现的公司或主题不会自动加进来，先进人工复核池。',
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
      subtitle: '只管模型设置：读的时候每个类别用哪个模型、哪版提示词，再加“对上”和“最终判定”各一套。改一次就是一个新版本。',
      kind: 'control',
      status: '第一版已冻结 · 2026-10-18',
      from: ['config'],
      purpose: '只管模型设置，分三种：抽取读信息时每个类别一套（用哪个模型、哪一版提示词）；观点库“对上”一套；最终判定一套。每一类读出什么、提示词模板怎么拼，写在抽取模块里。改一次就是一个新版本；处理过的每条信息、每次判定，记录里都写下当时用的是哪个版本。',
      inputs: '由人设定。',
      outputs: '一个版本号；抽取、观点库（对上）和最终判定按它来做。',
      checks: '设定里引用了不存在的模型设置，整个版本不能用。不设预算和并发上限。',
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
      caption: '中间一行是信息走的路：上游 → 分发 → 抽取（只读）→ 观点库（对上、写进去）。下面一行：观点库里需要判对错的观点交给最终判定；到期和定时的事由 Pull 模式发起；查不到、拿不准的放进人工复核池。左边的虚线框是上游，不归这个系统管。上面一排是设置：研究对象名单交给上游，决定推什么；Config 告诉抽取、观点库和最终判定用哪版模型设置，图上只画了到抽取的那根线。',
      nodes: [['universe', 0, 0], ['config', 1, 0], ['classify', 0, 1], ['dispatch', 1, 1], ['extract', 2, 1], ['views', 3, 1], ['review', 1, 2], ['verdict', 3, 2], ['pull', 4, 2]],
      order: ['classify', 'dispatch', 'extract', 'views', 'verdict', 'pull', 'review', 'universe', 'config'],
      edges: [
        ['universe', 'classify', '推哪些对象的哪几类信息', 'control'],
        ['classify', 'dispatch', '贴好标签的信息'],
        ['config', 'extract', '用哪版模型设置', 'control'],
        ['dispatch', 'extract', '属于某一类的信息（带顺序号）'],
        ['extract', 'views', '候选观点和证据（带出处）；读已有驱动的名字'],
        ['views', 'verdict', '要判对错的观点；判完写回'],
        ['pull', 'verdict', '到期、兜底复核', 'control'],
        ['pull', 'views', '定期合并、拆分驱动', 'control'],
        ['dispatch', 'review', '查不到、有问题的'],
        { source: 'extract', target: 'review', label: '多次失败的', route: 'bottom' },
        { source: 'views', target: 'review', label: '拿不准的、名单外的', route: 'bottom' },
      ],
    },
  ],
  dropped: {},
};
