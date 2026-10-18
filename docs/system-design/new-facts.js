// The New design's extraction module, the views database and the final verdict (decisions D26-D35). Extraction reads
// every item whole, by its category, as a senior hedge fund analyst, and hands views and evidence with their sources to
// the views database, which matches them against the drivers already held and keeps them in two levels linked by
// premises; the final verdict decides whether a view still stands. Edit the data at the top; the three drill-downs render it. The
// texts are for a reader who did not follow the discussion: plain words and an example, no field names.
(function () {
  'use strict';

  // ------------------------------------------------------------------ extraction

  // The template prompt of the read step: the same parts for every category, in this order.
  const TEMPLATE = [
    { part: '角色', content: '你是一位资深对冲基金分析师。读这条信息，是为了形成和检验对公司、资产和主题的观点：写出你的观点，以及支持或削弱它的证据。', source: '所有类别一样' },
    { part: '这一类是什么、怎么读', content: '这一类的定义和读法，比如“看法和估计算作者说的，不当成已经发生的事”。', source: '取自分类规则，这里不另写' },
    { part: '讲的是谁', content: '这条信息的相关对象。', source: '这条信息的标签' },
    { part: '这一类要读出什么', content: '见下面的表，每类一行。', source: '抽取模块' },
    { part: '这些对象已有的驱动', content: '只给驱动的名字，不给观点的方向和证据：让模型知道该注意什么，又不被已有的观点带着走。', source: '观点库' },
  ];

  // What each category should yield, and in which tier its evidence usually sits. The category's own definition and
  // reading rule come from the classification page and are not repeated here.
  const CATEGORY_READS = {
    T1: { read: '实际数、指引、管理层的解释；检验条件要用的数', tier: '实际数是发生的事；指引和解释是当事人说的' },
    T2: { read: '实际数、分部数；风险因素和业务描述里讲到的风险和变化', tier: '数是发生的事；风险和变化是当事人说的' },
    T3: { read: '交易条款（价格、对价、交割条件、时间表）；各方的说法和诉求', tier: '条款是发生的事；说法是当事人说的' },
    T4: { read: '管理层对关键问题的回答、口径的变化；分析师追问的焦点', tier: '回答是当事人说的；追问是第三方看法' },
    T5: { read: '管理层给的中长期目标、资本配置的框架、新业务的规模', tier: '当事人说的' },
    T6: { read: '发生了什么事（高管变动、并购、新产品、回购）；公布的经营数字（比如交付量）', tier: '发生的事' },
    T7: { read: '发生了什么事、什么时候、涉及谁；消息从哪来，原始来源是谁', tier: '官方确认的算发生的事；“知情人士称”算传闻' },
    T8: { read: '作者的看法、论据、预测、评级和目标价，以及它们的变化（用来算共识）', tier: '第三方看法' },
    T9: { read: '说话人讲的经营情况（订单、价格、份额、库存）；他凭什么知道', tier: '第三方看法' },
    T10: { read: '决定或行动本身、什么时候生效、影响谁；后面的程序（上诉、截止日），适合写成检验条件', tier: '发生的事' },
    T11: { read: '公布的数字和政策决定，和上一次比差多少；官方措辞的变化', tier: '数和决定是发生的事；措辞是当事人说的' },
    T12: { read: '价格和成交的变化，对着检验条件看', tier: '发生的事' },
    T13: { read: '谁在买、谁在卖、规模多大', tier: '发生的事' },
    T14: { read: '排定的日期，用作检验条件的期限或催化剂', tier: '发生的事' },
    T15: { read: '测到的经营数据，作为量化证据', tier: '发生的事（注明是第三方测的）' },
    T16: { read: '研究对象默认不看', tier: '—' },
  };

  const CATEGORY_NOTE = '每份文件都整份交给模型，里面的表格一起读；表格数据一次发布算一条，也整批交给模型。申报里的 XBRL 数字不另外推，文件本身已经有这些数；检验条件要准确的数时，由 Pull 模式去查。';

  // Every category has its own prompt: the same template with that category's parts. One assembled example.
  const PROMPT_EXAMPLE = {
    label: 'T7 新闻的提示词', note: '同一个提示词模板，第 2、4 块换成新闻这一类的',
    children: [
      { answer: '1 角色', label: '资深对冲基金分析师', note: '读这条信息，是为了形成和检验观点：写出你的观点，以及支持或削弱它的证据' },
      { answer: '2 这一类怎么读', label: '媒体的报道', note: '取自分类规则：媒体发的内容，除了评论和分析（那归 T8）；媒体登记过的发布系列按系列归类' },
      { answer: '3 讲的是谁', label: '这篇报道的相关对象', note: '由代码填，比如 NVDA、AMD' },
      { answer: '4 要读出什么', label: '发生了什么事、什么时候、涉及谁；消息从哪来，原始来源是谁', note: '官方确认的算发生的事；“知情人士称”算传闻' },
      { answer: '5 已有的驱动', label: '这些对象已有驱动的名字', note: '由代码填，比如“美国对华 AI 芯片出口管制”' },
    ],
  };

  const PROMPT_NOTES = [
    '每一类都有自己的提示词：同一个提示词模板，第 2 块（这一类怎么读）和第 4 块（要读出什么）换成这一类的；第 1 块所有类别一样；第 3、5 块由代码按这条信息填进去。',
    '研究对象会看的 15 类（T1–T15）各一份；T16 研究对象默认不看，用到时再写。',
    '输出的格式（候选观点、证据、出处各有哪些格子）由代码规定和检查，不写进提示词。',
    '每一类提示词的具体写法，建的时候在存下的信息上试过再定；每一版记在 Config 里，改一次就是一个新版本。',
  ];

  // Extraction, step by step: it only reads; matching and writing happen in the views database.
  const EXTRACT_STEPS = [
    { code: '1', name: '拼提示词', who: '代码', does: '按这条信息的类别，用同一个提示词模板拼出这一类的提示词' },
    { code: '2', name: '读', who: '模型', does: '整份读完，写出候选观点（主张、主题层还是对象层、讲的是谁、驱动、方向、期限档、利好还是利空、理由、前提、检验条件）和证据（原文、谁说的、原始来源、哪一层），每条带出处' },
    { code: '3', name: '核对出处', who: '代码', does: '原文那一句在不在这条信息里、数字在不在那一句或那一格里；对不上的不要，记下原因' },
    { code: '4', name: '交给观点库', who: '代码', does: '带着顺序号，交给观点库去对上、写进去' },
  ];

  // The views database, writing what extraction hands over.
  const WRITE_STEPS = [
    { code: '1', name: '证据去重', who: '代码', does: '原始来源、讲的事或指标、日期或财期都一样：只多记一个出处' },
    { code: '2', name: '找候选驱动', who: '代码', does: '这份文件相关对象的全部驱动，加上从全部主题驱动里用关键词和 embedding 搜到的几条' },
    { code: '3', name: '对上', who: '模型', does: '短调用，不带全文：属于哪个驱动、新驱动还是拿不准；前提是哪条；有没有重复的证据' },
    { code: '4', name: '定', who: '代码', does: '按下面的判断树：加证据、新建观点或新建驱动' },
    { code: '5', name: '查要不要判', who: '代码', does: '符合触发条件的观点，交给最终判定' },
  ];

  // Step 4 of writing into the views database, as a decision tree. A branch asks one question; each child is one answer. A child without children is where
  // the candidate ends up: `act` marks the ones written into the views database.
  const DECIDE_TREE = {
    label: '一条候选观点', question: '模型说它属于哪个驱动？', note: '驱动和观点的编号只能是候选里的，越界由代码拒绝',
    children: [
      {
        answer: '已有的驱动', label: '找同一期限档的有效观点', question: '有吗？', note: '同一个驱动、同一个期限档只有一条有效观点',
        children: [
          {
            answer: '有', label: '比方向', question: '方向一样吗？',
            children: [
              { answer: '一样', label: '挂成支持证据', act: true },
              { answer: '相反', label: '挂成削弱证据', note: '不另建一条反方向的观点', act: true },
            ],
          },
          { answer: '没有', label: '在这个驱动下新建观点', act: true },
        ],
      },
      { answer: '新驱动', label: '新建驱动和观点', note: 'Pull 模式定期合并驱动时会再看到它', act: true },
      { answer: '拿不准', label: '照样新建，标“待复核”', note: '同时放进人工复核池', act: true },
      { answer: '名单外的对象', label: '放进人工复核池', note: '观点和证据先挂“未知对象”' },
    ],
  };

  const DECIDE_NOTES = [
    '同一份文件，先写主题层，再写对象层，对象层看到的是刚更新过的前提。',
    '数字类的检验条件用固定格式写：指标、哪段时间、怎么算、怎么比、门槛多少，全系统一段代码来判；需要新的写法，就加一种格式。',
  ];

  // What one source records; every view, piece of evidence and change carries one.
  const SOURCE_TREE = {
    label: '一条出处',
    children: [
      { answer: '哪条信息', label: '上游编号和版本', note: '凭它去团队的库里取原文' },
      { answer: '哪一类、哪天', label: '类别、发布日' },
      { answer: '哪一处', label: '第几节第几段、表里哪一格', note: '表格数据写数据集和记录编号' },
      { answer: '哪一句', label: '原文那一句', note: '代码核对它真的在这条信息里，数字真的印在那一句或那一格里', act: true },
    ],
  };

  const SOURCE_NOTES = [
    '每条观点、每条证据、每一次变化都带出处；观点的主张和理由写明依据哪几条证据。',
    '抽取核对：原文那一句不在这条信息里、数字不在那一句或那一格里的，不交出去；观点库核对：出处在处理记录里查不到的，不写进库。都记下原因。',
    '两头都能查：从一条观点查到它的全部来源信息，从一条信息查到它产生和改动过的全部观点和证据。',
    '原文不存，凭上游编号去团队的库里取。',
  ];

  const EXTRACT_EXAMPLE_TREE = {
    label: 'NVDA 的 8-K · 2025-04-15', question: '读出两条候选观点', note: 'T6 公司其他发布：H20 出口中国要许可证，预计计提约 55 亿美元',
    children: [
      { answer: '主题层', label: '未来一年美国对华 AI 芯片出口管制会收紧', note: '证据：“H20 出口中国要许可证”（发生的事，NVDA 披露）；证伪条件：美国批准 H20 对华出口', act: true },
      { answer: '对象层（NVDA）', label: '一年内中国数据中心收入基本归零（利空）', note: '前提：上一条；证据：“预计计提约 55 亿美元”（当事人说的，公司自己的预计）；检验条件：中国区收入同比降 50% 以上（NVDA 只公布中国区总收入，用它来量）', act: true },
    ],
  };

  const WRITE_EXAMPLE_TREE = {
    label: '抽取交来的两条候选观点', note: '来自 NVDA 的 8-K · 2025-04-15',
    children: [
      {
        answer: '主题层', label: '未来一年美国对华 AI 芯片出口管制会收紧', question: '对上：主题“芯片出口管制”下的驱动“美国对华 AI 芯片出口管制”',
        children: [{ answer: '定', label: '新建主题观点（第 1 版）', note: '这个驱动下还没有观点', act: true }],
      },
      {
        answer: 'NVDA 层', label: '一年内中国数据中心收入基本归零（利空）', question: '对上：新驱动“中国区数据中心收入”',
        children: [{ answer: '定', label: '新建 NVDA 观点', note: '前提指向左边的主题观点，记“看过第 1 版”', act: true }],
      },
    ],
  };

  const EXAMPLE_NOTE = '出处：两条证据都记 8-K 的上游编号和版本、所在段落和原文那一句；代码核对“55 亿美元”确实在那一句里。读完就交给观点库，怎么对上、写进去，见观点库。例子用 NVDA，美股、期货、加密货币都走同一套。';

  const EXTRACT_OPEN = [
    '每一类提示词的具体写法，建的时候在存下的信息上试过再定；每一版记在 Config 里。',
  ];

  // ------------------------------------------------------------------ views database

  const VIEW_TREE = {
    label: '观点库',
    children: [
      {
        answer: '对象', label: '公司、加密货币、商品、主题', note: '都来自研究对象名单',
        children: [
          {
            answer: '驱动', label: '写得具体：谁、做什么、对哪儿', note: '例：美国对华 AI 芯片出口管制。定义写下不改，要改就新建，旧的指过去',
            children: [
              {
                answer: '观点', label: '一句主张，加方向和期限', note: '主张写下不改；要改就新建一条，接替旧的',
                children: [
                  { answer: '挂着', label: '证据', note: '原文、出处、谁说的、原始来源、哪一层、支持还是削弱', act: true },
                  { answer: '挂着', label: '检验条件（ladder）', note: '证实和证伪，各带期限；只能加，不能删也不能放宽', act: true },
                  { answer: '可以有', label: '前提', note: '指向另一条观点，记着上次看过它第几版', act: true },
                ],
              },
            ],
          },
        ],
      },
      { answer: '另记', label: '处理记录', note: '每份文件处理到哪一步；分发靠它判断以前处理过没有' },
    ],
  };

  // The same structure on every kind of object (illustrative cases, not real calls).
  const OBJECT_EXAMPLES = [
    { kind: '美股', theme: '主题“芯片出口管制”，驱动“美国对华 AI 芯片出口管制”：未来一年会收紧', object: 'NVDA，驱动“中国区数据中心收入”：一年内基本归零（利空），以左边为前提', evidence: '8-K 和业绩稿（T1、T6）、商务部的规定（T10）、新闻（T7）' },
    { kind: '期货（商品）', theme: '主题“原油供给（OPEC）”，驱动“OPEC+ 的产量配额”：未来半年会继续增产', object: '原油，驱动“全球原油库存”：未来半年油价承压（利空），以左边为前提', evidence: 'OPEC+ 会议声明（T10）、EIA 库存（T11）、CFTC 持仓（T13）、航运数据（T15）' },
    { kind: '加密货币', theme: '主题“美联储政策利率”，驱动“联邦基金利率路径”：年内会降息', object: '以太坊，驱动“美国现货 ETF 的资金流”：未来三个月持续净流入（利好），以左边为前提', evidence: 'ETF 资金流（T13）、SEC 的审批（T10）、链上活动（T15）、FOMC 声明（T11）' },
    { kind: '利率、指数期货', theme: '不单独算对象，观点挂在主题上，比如主题“美债收益率曲线”', object: '—', evidence: '宏观统计和政策利率（T11）、市场价格（T12）' },
  ];

  const VIEW_FIELDS = [
    { part: '层', meaning: '主题层讲世界上会发生什么；对象层讲这个对象（公司、加密货币、商品）会怎样', example: '主题层' },
    { part: '主张', meaning: '一句话，写下不改', example: '未来一年美国对华 AI 芯片出口管制会收紧' },
    { part: '方向和期限', meaning: '上升或下降；期限档（短期或长期），加到期日。同一个驱动下，同一个期限档只有一条有效观点', example: '上升；短期，到 2026-04-15' },
    { part: '利好还是利空', meaning: '只有对象层有：这个驱动对这个对象的影响方向，不是买卖立场', example: 'NVDA 那条：利空' },
    { part: '理由', meaning: '为什么这么看，写明依据哪几条证据', example: 'H20 出口要许可证，公司预计计提约 55 亿美元' },
    { part: '前提', meaning: '指向另一条观点（通常是主题观点），同时记着上次看过它第几版', example: 'NVDA 那条：以管制会收紧为前提，看过第 1 版' },
    { part: '检验条件（ladder）', meaning: '证实条件和证伪条件，各带期限；数字的由代码判，事件的由模型判；只能加，不能删也不能放宽', example: '主题观点的证伪条件：美国批准 H20 对华出口' },
    { part: '我们和共识哪里不同', meaning: '可以空着；共识由代码算', example: '—' },
    { part: '状态', meaning: '有效、已证实、已证伪、已过期、已并入、被接替、不再跟踪', example: '有效' },
    { part: '历史', meaning: '每变一次多一版，记下哪天、因为哪份文件；旧版都留着', example: '2025-04-15 新建' },
  ];

  const EVIDENCE_FIELDS = [
    { part: '原文', meaning: '文件里的那一句，或表里的那一格' },
    { part: '出处', meaning: '上游编号和版本、类别、发布日、在文件里的位置' },
    { part: '谁说的', meaning: '说这句话的人或机构' },
    { part: '原始来源', meaning: '转述的，指向最初说这句话的人；按它数独立来源' },
    { part: '哪一层', meaning: '发生的事、当事人说的、第三方看法、传闻' },
    { part: '支持还是削弱', meaning: '对这条观点' },
    { part: '对着哪条检验条件', meaning: '在回答哪个关键问题；没有就不填' },
    { part: '后来的结果', meaning: '关键问题被事实回答以后，代码标上“后来被证实”或“后来被否认”' },
  ];

  const TIERS = [
    { tier: '发生的事', examples: '官方动作、公布的数字、已经发生的交易', counts: '能满足检验条件' },
    { tier: '当事人说的', examples: '公司指引、管理层表态、官员讲话', counts: '只能让观点变强或变弱' },
    { tier: '第三方看法', examples: '卖方、媒体分析、专家、经济学家的预测', counts: '只能让观点变强或变弱；用来算共识' },
    { tier: '传闻', examples: '“知情人士称”、没有出处的消息', counts: '只能让观点变强或变弱' },
  ];

  const LEVEL_RULES = [
    '驱动是世界上的事（政府政策、宏观数据、整个行业的供需），而且名单里有对应的主题：观点挂在主题层。',
    '驱动是这个对象自己的事：观点挂在对象层。',
    '是世界上的事，但名单里还没有这个主题：先挂在对象层，同时放进人工复核池，建议新增主题。主题只能来自名单，系统不自己造主题。',
    '世界上发生了什么，证据挂在主题观点上；公司自己的数字和说法（包括“如果……我们会……”）挂在对象观点上；一份文件可以两层都挂。',
    '一条主题观点影响哪些对象，不另存名单，查“哪些观点以它为前提”就有。一只股票的全貌，就是它自己的观点加上这些观点的前提，同一个宏观因素只算一次。',
    '前提也可以指向别家公司的观点（比如供应链）；代码检查不能绕成环。',
  ];

  // The two levels on one example: a theme view and the object views that rest on it.
  const LEVEL_TREE = {
    label: '主题“芯片出口管制”',
    children: [
      {
        answer: '驱动', label: '美国对华 AI 芯片出口管制',
        children: [
          {
            answer: '主题观点', label: '未来一年管制会收紧', note: '证据：商务部规定、官方表态、关于这件事的新闻',
            children: [
              { answer: '以它为前提', label: 'NVDA：一年内中国数据中心收入基本归零', note: '利空 · 证据：NVDA 自己的 8-K、业绩稿', act: true },
              { answer: '以它为前提', label: 'AMD：MI308 对华收入受损', note: '利空 · 证据：AMD 自己的 8-K', act: true },
              { answer: '以它为前提', label: 'TSM：来自中国客户的收入下降', note: '利空 · 证据：管理层说“如果……会……”', act: true },
            ],
          },
        ],
      },
    ],
  };

  // What a view does when the view it rests on changes.
  const PROPAGATION_TREE = {
    label: '前提观点变了', question: '变的是什么？', note: '前提记着上次看过第几版；新版本出来，就是落后了',
    children: [
      { answer: '状态变了', label: '马上送最终判定', note: '证伪、过期、证实、被接替、不再跟踪：“前提变了，这条还成立吗？”', act: true },
      { answer: '被合并', label: '代码改指向', note: '标“前提有更新”' },
      { answer: '被削弱', label: '送最终判定', note: '这个对象下一份文件进来时；最迟 7 天，由 Pull 模式兜底', act: true },
      { answer: '被支持', label: '不处理', note: '只多一个版本号' },
    ],
  };

  const ORDER_RULES = [
    '只有文件能产生证据；观点之间只传通知，不传证据，所以观点不会自己证明自己。',
    '每条观点只有一个写入者：主题观点由主题的队列写，对象观点由对象的队列写。别的文件给它的证据，带着那份文件的顺序号，作为一条消息交给它的队列。',
    '一份文件只读顺序号比它小、而且发布日不晚于它的文件留下的状态，加上它自己已经写下的；同一天的文件按顺序号排，不看几点几分。结果必须和一份一份按顺序处理完全一样，并行只是为了快；并行时读到的观点在提交前变了，就重新判断一次。',
    '晚到的文件（发布日比已经处理过的还早）：读它发布那天的版本，不偷看以后；写的时候排在最后，证据上记它真实的发布日。',
    '同一份文件的修正版：新版的证据替换旧版的，旧版留在历史里；修正后某条观点没了依据，送最终判定。',
    '失败：每份文件记下做到了哪一步；从失败的那一步重试，重试只替换自己上次的结果；多次失败的放进人工复核池。',
    '对象被移出名单：它的观点保留，标“不再跟踪”，到期不判。',
  ];

  // Conflicting sources are normal; how a view weighs them.
  const CONFLICT_RULES = [
    '不投票：上层说了算。只凭第三方看法和传闻，不能把观点关掉。',
    '数独立来源，不数条数：按原始来源数，20 家媒体转述同一条独家算 1 家。',
    '出现分歧（同一层里，独立来源有的支持、有的削弱）：送最终判定，把能一锤定音的事实写成新的检验条件：什么事实，什么时候能知道。',
    '检验条件只能加，不能删，也不能放宽，防止事后挪球门。',
    '关键问题被事实回答以后，代码把早先对着它的说法标成“后来被证实”或“后来被否认”。每个来源说得准不准，就攒成了记录；这份记录先只展示，不用来给证据加权。',
    '共识由代码算：对每条观点，每个独立的第三方来源只取它最新的立场，汇总成分布，就是“市场怎么看”。我们读到的来源只是市场的一部分。',
  ];

  const CONFLICT_EXAMPLE = [
    { when: '2025-04-15', who: 'NVDA 8-K', tier: '发生的事', said: 'H20 出口要许可证', effect: '支持' },
    { when: '2025-04-16', who: 'AMD 8-K', tier: '发生的事', said: 'MI308 也要许可证', effect: '支持' },
    { when: '2025-04', who: '20 家媒体', tier: '发生的事', said: '同上（转述，原始来源都是 NVDA 的 8-K）', effect: '不另算' },
    { when: '2025-07 中', who: 'NVDA 声明', tier: '当事人说的', said: '美国政府保证会批准 H20 许可证', effect: '削弱' },
    { when: '2025-07（示意）', who: '卖方 A', tier: '第三方看法', said: '许可只是谈判筹码，管制的大方向不变', effect: '支持' },
    { when: '2025-08（据报道）', who: '报道官方动作', tier: '发生的事', said: '商务部开始发 H20 许可证，条件是上缴 15% 的中国收入', effect: '削弱，满足证伪条件' },
  ];

  const CONFLICT_EXAMPLE_NOTE = '到 7 月证据两边都有：NVDA 的声明（当事人说的）削弱，卖方 A（第三方看法）支持。两条不在同一层，也没有“发生的事”来削弱，不触发最终判定；观点留着，两边的证据都展示出来。能一锤定音的，就是证伪条件里写的那件事：美国会不会真的批准 H20 对华出口。8 月据报道商务部开始发许可证，证伪条件满足，送最终判定，主题观点“管制会收紧”判为已证伪。以它为前提的 NVDA 观点再判一次：据报道中国要求企业不要采购 H20，中国收入仍没回来，所以留下，前提换成一条新的主题观点。';

  const VIEWS_OPEN = [
    '驱动目录怎样维护：Pull 模式定期合并和拆分的具体做法；新驱动由一处写入，避免两个对象的队列同时建出同一个驱动。',
    '名单加了新对象、上游补推它的历史时，补推的旧文件可能另建出重复的观点，靠定期合并收拾。',
    '存在哪里、用什么数据库，和建的时候一起定。',
    '真建之前要在存下的数据上量：每个对象挂多少驱动和观点；两次独立标注“是不是同一个驱动”的一致度；判“新驱动”准不准；候选清单换个顺序，答案会不会变。',
  ];

  // ------------------------------------------------------------------ final verdict

  const VERDICT_TRIGGERS = [
    { trigger: '证实条件或证伪条件满足', who: '代码' },
    { trigger: '到了期限', who: 'Pull 模式；要等发布日不晚于期限的文件都处理完再判' },
    { trigger: '前提的状态变了（证伪、过期、证实、被接替、不再跟踪）', who: '代码，马上' },
    { trigger: '前提被削弱', who: '这个对象下一份文件进来时；最迟 7 天，由 Pull 模式兜底' },
    { trigger: '“发生的事”这一层来了削弱证据', who: '代码' },
    { trigger: '出现分歧：同一层里，独立来源有的支持、有的削弱', who: '代码' },
    { trigger: '同一份文件出了修正版，观点没了依据', who: '代码' },
  ];

  const VERDICT_TREE = {
    label: '最终判定', question: '这条观点还成立吗？', note: '模型看：这条观点、全部证据、前提的现状、这次为什么被送来',
    children: [
      { answer: '证实条件满足，有“发生的事”', label: '关掉：已证实', note: '写明依据哪几条证据', act: true },
      { answer: '证伪条件满足，有“发生的事”', label: '关掉：已证伪', note: '写明依据哪几条证据', act: true },
      { answer: '到期，没有能判的证据', label: '关掉：已过期', note: '记“没有数据可验证”，不算对也不算错', act: true },
      { answer: '其余情况', label: '留下', note: '可以去掉或换掉前提；可以加检验条件，写下“什么事实能定、什么时候能知道”', act: true },
    ],
  };

  const VERDICT_RULES = [
    '模型把这条观点、它的全部证据、前提的现状和这次为什么被触发一起看完，一次判完。',
    '能判成已证实或已证伪的，只有检验条件加上“发生的事”这一层的证据；只凭第三方看法和传闻不能判。已过期不算判对错。',
    '判完写成这条观点的新版本，写明依据哪几条证据和出处；关掉的观点留在库里，可以查历史。',
    '一条观点关掉以后，以它为前提的观点各自再送一次最终判定。',
    'Pull 模式用的“现在”从外面传进来：上线用真实时间，测试用回放的时间。系统里没有自己的钟。',
  ];

  // ------------------------------------------------------------------ rendering

  function listItems(items, escapeHtml) {
    return items.map((item) => `<li>${escapeHtml(item)}</li>`).join('');
  }

  function table(headers, rows, escapeHtml) {
    return '<table class="schema-table schema-table--compact">'
      + `<thead><tr>${headers.map((header) => `<th>${escapeHtml(header)}</th>`).join('')}</tr></thead>`
      + `<tbody>${rows.map((row) => `<tr>${row.map((cell) => `<td>${escapeHtml(cell)}</td>`).join('')}</tr>`).join('')}</tbody>`
      + '</table>';
  }

  function status(pill, note, escapeHtml) {
    return `<p class="drill__status"><span class="pill pill--mixed">${escapeHtml(pill)}</span>${escapeHtml(note)}</p>`;
  }

  // A row of cards joined by a separator; a card is { code?, title, who?, note?, strong? }.
  function flow(cards, separator, escapeHtml) {
    return '<div class="flow">' + cards.map((card) => `<div class="flow__card${card.strong ? ' flow__card--strong' : ''}">`
      + '<div class="flow__top">'
      + (card.code !== undefined ? `<span class="org-tag__code">${escapeHtml(card.code)}</span>` : '')
      + `<span class="flow__title">${escapeHtml(card.title)}</span></div>`
      + (card.who ? `<span class="flow__who">${escapeHtml(card.who)}</span>` : '')
      + (card.note ? `<span class="flow__note">${escapeHtml(card.note)}</span>` : '')
      + '</div>').join(`<span class="flow__arrow">${escapeHtml(separator)}</span>`) + '</div>';
  }

  function renderBranch(branch, escapeHtml, isRoot) {
    const isOutcome = !branch.children;
    const classes = ['org-node', isRoot ? 'org-node--root' : '', isOutcome ? (branch.act ? 'org-node--act' : 'org-node--leaf') : '']
      .filter(Boolean).join(' ');
    const box = `<div class="${classes}">`
      + (branch.answer ? `<span class="org-node__family">${escapeHtml(branch.answer)}</span>` : '')
      + `<span class="org-node__label">${escapeHtml(branch.label)}</span>`
      + (branch.question ? `<span class="org-node__question">${escapeHtml(branch.question)}</span>` : '')
      + (branch.note ? `<span class="org-node__note">${escapeHtml(branch.note)}</span>` : '')
      + '</div>';
    const below = isOutcome ? ''
      : `<ul>${branch.children.map((child) => `<li>${renderBranch(child, escapeHtml, false)}</li>`).join('')}</ul>`;
    return box + below;
  }

  function tree(root, escapeHtml) {
    return `<div class="org"><div class="org-tree"><ul><li>${renderBranch(root, escapeHtml, true)}</li></ul></div></div>`;
  }

  // Scale each tree down, never up, so the whole of it is in view.
  function fitTrees(container) {
    container.querySelectorAll('.org').forEach((frame) => {
      const inner = frame.querySelector('.org-tree');
      if (!inner) return;
      inner.style.zoom = '1';
      inner.style.zoom = String(Math.min(1, (frame.clientWidth - 8) / inner.scrollWidth));
    });
  }

  function keepFitted(container) {
    requestAnimationFrame(() => fitTrees(container));
    window.addEventListener('resize', () => { if (container.isConnected) fitTrees(container); });
  }

  const design = window.HIVEMIND_DESIGNS.new;
  design.drilldowns = design.drilldowns || {};

  design.drilldowns.extract = {
    button: '展开抽取：每一类信息怎么读成观点',
    kicker: '抽取 · 详细说明',
    size: 'full',
    render(container, context) {
      const escapeHtml = context.escapeHtml;
      const tags = (design.classification || {}).TAGS || {};
      const categoryRows = Object.keys(CATEGORY_READS)
        .sort((first, second) => Number(first.slice(1)) - Number(second.slice(1)))
        .map((code) => [`${code} ${(tags[code] || {}).label || ''}`, CATEGORY_READS[code].read, CATEGORY_READS[code].tier]);
      const stepCards = EXTRACT_STEPS.map((step) => ({ code: step.code, title: step.name, who: step.who, note: step.does, strong: step.who === '模型' }));
      const templateCards = TEMPLATE.map((part, index) => ({ code: String(index + 1), title: part.part, who: part.source, note: part.content }));
      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">抽取：每一类信息怎么读成观点</h2>
          <p class="drill__intro">抽取只做一件事：每条信息整份交给模型，用资深对冲基金分析师的视角、按这一类的提示词，读出观点（thesis）和证据，每条带出处，交给观点库。怎么和已有观点对上、写进去，是观点库的事。</p>
          <p class="drill__status"><span class="pill pill--strong">第一版已冻结 · 2026-10-18</span>定下：整份交给模型；每一类一份提示词，拼法相同；观点是模型的判断，证据是客观的；每条都带出处；抽取只读。没定：每一类提示词的具体写法，建的时候试过再定。</p>
          <h3 class="drill__heading drill__heading--spaced">一条信息，一步一步</h3>
          <p class="flow-legend">黑框是模型做的，灰框是代码做的。</p>
          ${flow(stepCards, '→', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">第 1 步：每一类的提示词，都由同一个提示词模板的这五块拼起来</h3>
          ${flow(templateCards, '+', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">每一类有自己的提示词：拼出来长这样（T7 新闻）</h3>
          ${tree(PROMPT_EXAMPLE, escapeHtml)}
          <ul class="drill__rules">${listItems(PROMPT_NOTES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">16 个类别：每一类读出什么（第 4 块）</h3>
          ${table(['类别', '这一类要读出什么', '证据一般在哪一层'], categoryRows, escapeHtml)}
          <p class="drill__footnote">${escapeHtml(CATEGORY_NOTE)}</p>
          <h3 class="drill__heading drill__heading--spaced">一个例子：NVDA 的 8-K 读出什么</h3>
          ${tree(EXTRACT_EXAMPLE_TREE, escapeHtml)}
          <p class="drill__footnote">${escapeHtml(EXAMPLE_NOTE)}</p>
          <div class="drill__columns">
            <section>
              <h3 class="drill__heading drill__heading--spaced">出处记什么</h3>
              ${tree(SOURCE_TREE, escapeHtml)}
              <ul class="drill__rules">${listItems(SOURCE_NOTES, escapeHtml)}</ul>
            </section>
            <section>
              <h3 class="drill__heading drill__heading--spaced">还没定的</h3>
              <ul class="drill__rules">${listItems(EXTRACT_OPEN, escapeHtml)}</ul>
            </section>
          </div>
        </div>`;
      keepFitted(container);
    },
  };

  design.drilldowns.views = {
    button: '展开观点库：怎么写进库、观点长什么样、两层怎么连',
    kicker: '观点库 · 详细说明',
    size: 'full',
    render(container, context) {
      const escapeHtml = context.escapeHtml;
      const writeCards = WRITE_STEPS.map((step) => ({ code: step.code, title: step.name, who: step.who, note: step.does, strong: step.who === '模型' }));
      const tierCards = TIERS.map((tier, index) => ({ code: String(index + 1), title: tier.tier, note: `${tier.examples}。${tier.counts}`, strong: index === 0 }));
      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">观点库（thesis · ladder · evidence）</h2>
          <p class="drill__intro">系统做的事，就是建立、更新和关掉这里的观点。抽取读出来的观点和证据交到这里：先去重、对上已有的驱动，再由代码决定挂证据还是新建。观点是模型（分析师）的判断；证据是客观的：谁在哪份文件里说了什么。关掉的观点和旧版本都留着，每一条都带出处。</p>
          ${status('设计中 · 2026-10-18', '已定：一个格式、两层、一种线（前提）；只有文件能产生证据；检验条件只能加；只凭第三方看法和传闻不能关掉观点。', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">结构：对象 → 驱动 → 观点</h3>
          ${tree(VIEW_TREE, escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">抽取交来的观点和证据，怎么写进库</h3>
          <p class="flow-legend">黑框是模型做的，灰框是代码做的。</p>
          ${flow(writeCards, '→', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">第 4 步：代码怎么定</h3>
          ${tree(DECIDE_TREE, escapeHtml)}
          <p class="flow-legend">黑框：写进观点库。灰框：放进人工复核池。</p>
          <ul class="drill__rules">${listItems(DECIDE_NOTES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">例子：NVDA 的 8-K 读出的两条怎么写进库</h3>
          ${tree(WRITE_EXAMPLE_TREE, escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">两层：主题观点在上，对象观点以它为前提</h3>
          ${tree(LEVEL_TREE, escapeHtml)}
          <ul class="drill__rules">${listItems(LEVEL_RULES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">同一套结构，用在每一种对象上（示意）</h3>
          ${table(['对象', '主题层观点', '对象层观点', '证据从哪来'], OBJECT_EXAMPLES.map((row) => [row.kind, row.theme, row.object, row.evidence]), escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">前提变了，靠它的观点怎么办</h3>
          ${tree(PROPAGATION_TREE, escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">证据分四层，上层说了算</h3>
          ${flow(tierCards, '＞', escapeHtml)}
          <div class="drill__columns">
            <section>
              <h3 class="drill__heading drill__heading--spaced">说法互相矛盾时</h3>
              <ul class="drill__rules">${listItems(CONFLICT_RULES, escapeHtml)}</ul>
            </section>
            <section>
              <h3 class="drill__heading drill__heading--spaced">例子：主题观点“未来一年美国对华 AI 芯片出口管制会收紧”</h3>
              ${table(['时间', '谁说的', '哪一层', '说了什么', '对这条观点'], CONFLICT_EXAMPLE.map((row) => [row.when, row.who, row.tier, row.said, row.effect]), escapeHtml)}
              <p class="drill__footnote">${escapeHtml(CONFLICT_EXAMPLE_NOTE)}</p>
            </section>
          </div>
          <div class="drill__columns">
            <section>
              <h3 class="drill__heading drill__heading--spaced">一条观点有哪些部分</h3>
              ${table(['部分', '写什么', '例子'], VIEW_FIELDS.map((row) => [row.part, row.meaning, row.example]), escapeHtml)}
            </section>
            <section>
              <h3 class="drill__heading drill__heading--spaced">一条证据记什么</h3>
              ${table(['部分', '写什么'], EVIDENCE_FIELDS.map((row) => [row.part, row.meaning]), escapeHtml)}
              <h3 class="drill__heading drill__heading--spaced">先后和同步</h3>
              <ul class="drill__rules">${listItems(ORDER_RULES, escapeHtml)}</ul>
              <h3 class="drill__heading drill__heading--spaced">还没定的</h3>
              <ul class="drill__rules">${listItems(VIEWS_OPEN, escapeHtml)}</ul>
            </section>
          </div>
        </div>`;
      keepFitted(container);
    },
  };

  design.drilldowns.verdict = {
    button: '展开最终判定：什么时候判、判出什么',
    kicker: '最终判定 · 详细说明',
    size: 'full',
    render(container, context) {
      const escapeHtml = context.escapeHtml;
      const triggerCards = VERDICT_TRIGGERS.map((trigger) => ({ title: trigger.trigger, who: trigger.who }));
      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">最终判定：一条观点还成立吗</h2>
          <p class="drill__intro">一条观点要不要关，不由一条证据或一个条件直接决定，而是先送到这里，由模型把整条观点和它的全部证据完整看一遍再判。</p>
          ${status('设计中 · 2026-10-18', '已定：关掉之前一定经过这里；关掉的观点留在库里。', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">这些情况会把观点送来</h3>
          ${flow(triggerCards, '·', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">判出什么</h3>
          ${tree(VERDICT_TREE, escapeHtml)}
          <div class="drill__columns">
            <section>
              <h3 class="drill__heading drill__heading--spaced">规则</h3>
              <ol class="drill__rules">${listItems(VERDICT_RULES, escapeHtml)}</ol>
            </section>
            <section>
              <h3 class="drill__heading drill__heading--spaced">例子</h3>
              <p class="drill__footnote">${escapeHtml(CONFLICT_EXAMPLE_NOTE)}</p>
            </section>
          </div>
        </div>`;
      keepFitted(container);
    },
  };
})();
