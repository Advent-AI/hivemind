// The New design's extraction module, the views database and the final verdict (decisions D26-D42). Extraction reads
// every item whole, by its category, as a senior hedge fund analyst, with cards of the views already open, and hands
// over two things with their sources: evidence attached to a card or to a candidate view, and candidate views for what
// no card covers. There a view is a question with a ladder and a due date; candidates are matched to the views already
// open (attach, succeed, new, or not opened), each piece of evidence is matched to the evidence its view already holds
// (repeat, replacement, or new evidence), evidence pushes the view's state, and views are linked by dependencies and
// chained by succession (D38-D40, D42). The final verdict is still the old draft and is to be redone (D41). Edit the
// data at the top; the three drill-downs render it. The texts are for a reader who did not follow the discussion: plain
// words and an example, no field names.
(function () {
  'use strict';

  // ------------------------------------------------------------------ extraction

  // The template prompt of the read step: the same parts for every category, in this order.
  const TEMPLATE = [
    { part: '角色', content: '你是一位资深对冲基金分析师。读这条信息，是为了检验和形成观点：把支持或削弱已有观点的话和数挑出来，作为证据挂到那条观点上；已有观点管不到、又要紧的事，写成候选观点，带上提出它的证据。观点照观点库的写法：一个观点只看一件东西；数字写明哪一年和判卷来源；主题观点的范围按管它的那条规定或那个决定来写。', source: '所有类别一样' },
    { part: '这一类是什么、怎么读', content: '这一类的定义和读法，比如“看法和估计算作者说的，不当成已经发生的事”。', source: '取自分类规则，这里不另写' },
    { part: '讲的是谁', content: '这条信息的相关对象。', source: '这条信息的标签' },
    { part: '这一类要读出什么', content: '见下面的表，每类一行。', source: '抽取模块' },
    { part: '这些对象已有的观点', content: '这条信息相关对象开着的观点，加上它们依赖的观点；只给问题和看的是什么，不给状态和证据：让模型把证据挂到这些观点上，又不被已有的判断带着走。', source: '观点库' },
  ];

  // What each category should yield, and in which tier its evidence usually sits. The category's own definition and
  // reading rule come from the classification page and are not repeated here.
  const CATEGORY_READS = {
    T1: { read: '实际数、指引、管理层的解释；判卷要用的数', tier: '实际数是发生的事；指引和解释是当事人说的' },
    T2: { read: '实际数、分部数；风险因素和业务描述里讲到的风险和变化', tier: '数是发生的事；风险和变化是当事人说的' },
    T3: { read: '交易条款（价格、对价、交割条件、时间表）；各方的说法和诉求', tier: '条款是发生的事；说法是当事人说的' },
    T4: { read: '管理层对关键问题的回答、口径的变化；分析师追问的焦点', tier: '回答是当事人说的；追问是第三方看法' },
    T5: { read: '管理层给的中长期目标、资本配置的框架、新业务的规模', tier: '当事人说的' },
    T6: { read: '发生了什么事（高管变动、并购、新产品、回购）；公布的经营数字（比如交付量）', tier: '发生的事' },
    T7: { read: '发生了什么事、什么时候、涉及谁；消息从哪来，原始来源是谁', tier: '官方确认的算发生的事；“知情人士称”算传闻' },
    T8: { read: '作者的看法、论据、预测、评级和目标价，以及它们的变化（用来算共识）', tier: '第三方看法' },
    T9: { read: '说话人讲的经营情况（订单、价格、份额、库存）；他凭什么知道', tier: '第三方看法' },
    T10: { read: '决定或行动本身、什么时候生效、影响谁；后面的程序（上诉、截止日），可以用作到期日', tier: '发生的事' },
    T11: { read: '公布的数字和政策决定，和上一次比差多少；官方措辞的变化', tier: '数和决定是发生的事；措辞是当事人说的' },
    T12: { read: '价格和成交的变化', tier: '发生的事' },
    T13: { read: '谁在买、谁在卖、规模多大', tier: '发生的事' },
    T14: { read: '排定的日期，用作到期日或催化剂', tier: '发生的事' },
    T15: { read: '测到的经营数据，作为量化证据', tier: '发生的事（注明是第三方测的）' },
    T16: { read: '研究对象默认不看', tier: '—' },
  };

  const CATEGORY_NOTE = '每份文件都整份交给模型，里面的表格一起读；表格数据一次发布算一条，也整批交给模型。申报里的 XBRL 数字不另外推，文件本身已经有这些数；判卷要准确的数时，由 Pull 模式去查。';

  // Every category has its own prompt: the same template with that category's parts. One assembled example.
  const PROMPT_EXAMPLE = {
    label: 'T7 新闻的提示词', note: '同一个提示词模板，第 2、4 块换成新闻这一类的',
    children: [
      { answer: '1 角色', label: '资深对冲基金分析师', note: '读这条信息，是为了检验和形成观点：证据挂到已有观点上；已有观点管不到的要紧事，写成候选观点' },
      { answer: '2 这一类怎么读', label: '媒体的报道', note: '取自分类规则：媒体发的内容，除了评论和分析（那归 T8）；媒体登记过的发布系列按系列归类' },
      { answer: '3 讲的是谁', label: '这篇报道的相关对象', note: '由代码填，比如 NVDA、AMD' },
      { answer: '4 要读出什么', label: '发生了什么事、什么时候、涉及谁；消息从哪来，原始来源是谁', note: '官方确认的算发生的事；“知情人士称”算传闻' },
      { answer: '5 已有的观点', label: '这篇报道相关对象开着的观点，加上它们依赖的观点', note: '由代码填，只给问题和看的是什么；比如“NVDA FY27 全年中国区收入，比 FY26 会怎样？”，和它依赖的“这一档芯片对华出口许可”' },
    ],
  };

  const PROMPT_NOTES = [
    '每一类都有自己的提示词：同一个提示词模板，第 2 块（这一类怎么读）和第 4 块（要读出什么）换成这一类的；第 1 块所有类别一样；第 3、5 块由代码按这条信息填进去。',
    '研究对象会看的 15 类（T1–T15）各一份；T16 研究对象默认不看，用到时再写。',
    '输出的格式（证据、候选观点、出处各有哪些格子）由代码规定和检查，不写进提示词。',
    '每一类提示词的具体写法，建的时候在存下的信息上试过再定；每一版记在 Config 里，改一次就是一个新版本。',
  ];

  // Extraction, step by step: it only reads; matching and writing happen in the views database.
  const EXTRACT_STEPS = [
    { code: '1', name: '拼提示词', who: '代码', does: '按这条信息的类别，用同一个提示词模板拼出这一类的提示词；第 5 块由观点库给：相关对象开着的观点，加上它们依赖的观点' },
    { code: '2', name: '读', who: '模型', does: '整份读完，交出两样：证据，挂到第 5 块里的观点上，或挂到这次的候选观点上；候选观点，第 5 块里没有一条观点管、又要紧的事，带上提出它的证据。每条带出处' },
    { code: '3', name: '核对出处', who: '代码', does: '原文那一句在不在这条信息里、数字在不在那一句或那一格里；证据挂的必须是第 5 块里的观点或这次的候选观点；对不上的不要，记下原因' },
    { code: '4', name: '交给观点库', who: '代码', does: '带着顺序号，交给观点库去对上、写进去' },
  ];

  // The two things one read hands over, side by side.
  const EXTRACT_TWO = [
    { aspect: '是什么', evidence: '信息里的一句话或一个数：谁说了什么、发生了什么', candidate: '我们要盯的一个问题：一把梯子、一个到期日' },
    { aspect: '多不多', evidence: '几乎每条信息都有', candidate: '少：第 5 块里没有一条观点管、又要紧的事' },
    { aspect: '挂在哪', evidence: '第 5 块里的观点（可以挂几条），或者这次的候选观点', candidate: '带着提出它的证据' },
    { aspect: '到了观点库', evidence: '和它那条观点下已有的证据比：重复、替代还是新证据', candidate: '和开着的观点比：挂到已有的、接续、新观点、不开，还是拿不准' },
    { aspect: '例子', evidence: '8-K 里的“H20 出口中国要许可证”', candidate: '2025-04 那条规定管的这一档芯片对华出口许可，到 2026-04-15 处在哪一格？' },
  ];

  // How the model sorts what it reads: against the cards.
  const EXTRACT_SORT_TREE = {
    label: '读到一句话或一个数', question: '它和哪条观点有关？',
    children: [
      { answer: '第 5 块里的观点', label: '证据：挂到那条观点上', act: true },
      { answer: '第 5 块里没有，但要紧', label: '候选观点：这句话是它的证据', note: '值不值得开一条新观点，由观点库定', act: true },
      { answer: '都没关系', label: '不抽', note: '背景、套话' },
    ],
  };

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
    '每条观点、每条证据、每一次变化都带出处；状态的每次变化写明依据哪几条证据。',
    '抽取核对：原文那一句不在这条信息里、数字不在那一句或那一格里的，证据挂的不是第 5 块里的观点或这次候选观点的，不交出去；观点库核对：出处在处理记录里查不到的，不写进库。都记下原因。',
    '两头都能查：从一条观点查到它的全部来源信息，从一条信息查到它产生和改动过的全部观点和证据。',
    '原文不存，凭上游编号去团队的库里取。',
    '同一条信息里说同一件事的几处（正文和表格里的同一个数），交成一条证据，带几个出处。',
  ];

  const EXTRACT_EXAMPLE_TREE = {
    label: '两条信息读出什么', note: '示意',
    children: [
      {
        answer: '2025-04-15 NVDA 的 8-K', label: '库是空的，第 5 块里没有观点', question: '读出两条候选观点',
        note: 'T6 公司其他发布：H20 出口中国要许可证，预计最多约 55 亿美元的费用',
        children: [
          { answer: '候选观点（主题观点）', label: '2025-04 那条规定管的这一档芯片（H20、MI308 等）对华出口许可，到 2026-04-15 处在哪一格？', note: '事件；五格从“全面禁止”到“不再要许可”；证据：原文“…requires a license for export to China … of the Company’s H20 integrated circuits…”（发生的事，NVDA 披露：H20 出口中国要许可证）；到了观点库，开成 #1', act: true },
          { answer: '候选观点（对象观点 NVDA）', label: 'NVDA FY26 全年中国区收入，比 FY25 会怎样？', note: '数字，一段时间的数；到期 = FY26 年报的财报日；判卷看年报里按地区分的收入（NVDA 只公布中国区含香港的总数）；证据：原文“…charges of up to approximately $5.5 billion…”（当事人说的：公司预计最多约 55 亿美元的费用）；到了观点库，开成 #2，依赖 #1', act: true },
        ],
      },
      {
        answer: '2025-07-14 NVDA 的声明', label: '第 5 块：#2 和它依赖的 #1', question: '读出一条证据，没有候选观点',
        children: [
          { answer: '证据', label: '挂到 #1', note: '当事人说的；一句话说清：NVDA 称美国政府已保证会批准 H20 对华出口的许可（2025-07-14）', act: true },
        ],
      },
    ],
  };

  const EXAMPLE_NOTE = '出处：每条证据都记上游编号和版本、所在段落和原文那一句（英文原句，中文只是说明）；代码核对“$5.5 billion”确实在那一句里。第一条信息进来时库是空的，第 5 块里没有观点，读到的要紧事只能写成候选观点；第二条信息进来时，第 5 块里已经有出口许可那条，NVDA 的声明就直接挂上去。到了观点库，候选观点去对上开着的观点，证据去和它那条观点下已有的证据比，见观点库。例子用 NVDA，美股、期货、加密货币都走同一套。';

  const EXTRACT_OPEN = [
    '每一类提示词的具体写法，建的时候在存下的信息上试过再定；每一版记在 Config 里。',
    '已有观点里放了依赖的主题观点以后，几家公司对宏观的看法会一起挂到主题观点上，可人多不等于信息多：主题观点要不要只收新的观察（发生的事、公司自己看到的订单和价格）。',
    '抽取挂错、漏抽的证据，对上标注看不到：要不要另外按信息抽样，对着当时给的已有观点读原文核查。',
  ];

  // ------------------------------------------------------------------ views database (D38–D40)

  // What the views database holds.
  const VIEW_TREE = {
    label: '观点库',
    children: [
      {
        answer: '对象', label: '名单里的公司、加密货币、商品、主题',
        children: [
          {
            answer: '观点', label: '一个问题 + 一把梯子 + 一个到期日', note: '写下不改；梯子五格，只有是或否的问题两格；对象观点的身份是“对象 + 看的是什么”，主题观点的身份只看“看的是什么”',
            children: [
              { answer: '两个位置', label: '现在在哪一格、状态', note: '前者是事实，后者是我们的判断', act: true },
              { answer: '连线', label: '证据', note: '证据只存一次，带出处和层；往哪边推记在连线上；被替代的证据留在历史里，不再算数', act: true },
              { answer: '依赖', label: '别的观点', note: '它的答案要用到对方的答案；箭头带一个方向：对方的哪一头对它是看多', act: true },
              { answer: '接续', label: '上一期的观点', note: '同一样东西一期接一期，连成一条链', act: true },
            ],
          },
        ],
      },
      { answer: '只追加的记录', label: '对上记录、重判记录、关掉记录、标注', note: '每一步都新加一条，不改不删；想知道某天当时怎么判，就翻那天以前的记录' },
    ],
  };

  // The two kinds of view: the same structure, rungs that mean different things.
  const VIEW_KINDS = [
    { kind: '对象观点', on: '能交易的对象：公司、加密货币、商品', rungs: '五格：强烈看多、看多、中性、看空、强烈看空；只有是或否的问题两格：看多、看空。说的是对业务好还是坏，建的时候定，以后不变', example: 'NVDA FY27 全年中国区收入，比 FY26 会怎样？' },
    { kind: '主题观点', on: '主题：宏观、政策、行业', rungs: '一条轴上的几种结果（五格；只有是或否的问题两格），用结果命名，不说好坏；好坏由依赖它的对象观点各自的箭头说', example: '美联储 2026 年最后一次议息后的目标利率上限，比现在会怎样？（大幅降息……大幅加息）' },
  ];

  const KIND_NOTE = '同一件世界上的事，对不同的对象可能好坏相反：降息对以太坊是看多，对 JPM 的净利息收入是看空。所以主题观点不说好坏。对股价的看法，是我们的状态和共识（市场押在哪一格）差多少；共识怎么记还没定。';

  // Two ladders, one of each kind (ranges are illustrative).
  const LADDER_EXAMPLES = {
    label: '两种梯子', note: '区间示意',
    children: [
      {
        answer: '数字的梯子', label: 'NVDA FY27 全年中国区收入，比 FY26', question: '代码拿公布的数比区间',
        note: '一段时间的数；到期 = FY27 年报的财报日；判卷看年报里按地区分的收入（NVDA 只公布中国区含香港的总数）',
        children: [
          { answer: '强烈看多', label: '涨 50% 及以上' },
          { answer: '看多', label: '涨 10% 及以上，不到 50%' },
          { answer: '中性', label: '涨不到 10%，或降不到 10%' },
          { answer: '看空', label: '降 10% 及以上，不到 80%' },
          { answer: '强烈看空', label: '降 80% 及以上', note: '基本归零' },
        ],
      },
      {
        answer: '事件的梯子', label: '2025-04 那条规定管的这一档芯片（H20、MI308 等）对华出口许可，到 2026-04-15 处在哪一格',
        question: '模型只看“发生的事”判，写明依据', note: '以那天已经生效的规定为准',
        children: [
          { answer: '第 1 格', label: '全面禁止，不再受理许可' },
          { answer: '第 2 格', label: '要许可，实际不发', note: '2025-04 现在在这一格' },
          { answer: '第 3 格', label: '要许可，发的时候附条件', note: '2025-08 现在在这一格（据报道发许可，上缴 15% 的中国收入）', act: true },
          { answer: '第 4 格', label: '要许可，发的时候不附条件' },
          { answer: '第 5 格', label: '不再要许可' },
        ],
      },
    ],
  };

  const LADDER_RULES = [
    '每把梯子五格：对象观点是强烈看多到强烈看空，主题观点是一条轴上的五种结果，用结果命名。只有是或否的问题用两格，不硬分五格：对象观点的两格是看多、看空；主题观点的两格用结果命名，比如“到期前签署了”“没签署”。',
    '每一格是一个看得见的、是或否的条件；各格不重叠，盖住所有可能，到期时正好一格成立。没有“部分”：部分做到的单独写成一格。分得出程度的事按程度分五格，比如“12 月 FOMC 会怎样”：降 50 个基点以上、降 25 个基点、不动、加 25 个基点、加 50 个基点以上。',
    '一把梯子只放一种东西。数字的梯子是同一个数在写明那一年的几段区间，由代码判；事件的梯子是同一件事到期那天可能处在的几种状态，写清是哪个阶段（宣布、签署、生效、执行），由模型只看“发生的事”判，写明依据。',
    '一个观点只看一件东西。既要数字又要事件的，拆成两条，用依赖连起来（NVDA 中国区收入依赖出口许可）；两部分可能往相反方向走的（H20 这一档和 Blackwell 这一档），拆成两条，有真实的依赖才连箭头。',
    '梯子由模型在建观点时定，定了到期以前不改；后来合并进来的候选观点带的梯子一律不要。中性跟什么比，写在那一格的条件里，比如“比去年同期变动在 10% 以内”。',
    '数字的观点写明三件事：哪一年（公司按财年，其他按自然年）；是一段时间的数（收入）还是时点的数（政策利率）；判卷来源（公司写财报里的哪一项，宏观写哪个官方数据序列）。到期日就是这个数公布的那天。“今年”“明年”按已经处理过的信息里最晚的发布日算（只往前走，不看电脑时钟）；期末已过的年份不再新开观点。',
    '到期日定在这个争论见分晓的那天，一般 6–12 个月；中间的季报是证据，不另开观点。',
  ];

  // The two positions on one ladder.
  const POSITIONS = [
    { position: '现在在哪一格', means: '事实：现在落在哪一格；到期那天就是答案', moves: '只有“发生的事”能动它。事件的观点由模型判；时点的数由代码按最近公布的值定，记下是哪天的值；一段时间的数在答案公布前没有这个位置', example: '2025-08：要许可，发的时候附条件' },
    { position: '状态', means: '判断：我们认为到期会落在哪一格', moves: '四层证据都能推它。每次由模型从这条观点下没被替代的全部证据（每条带上它替掉的那条，看得到变化）、加上它依赖的观点的现状重新判，不在上一次的基础上加减；写明依据哪几条证据，代码核对它们确实连在这条观点上。这一轮只多了重复的证据、依赖也没变，就不重判。回放靠存下来的重判记录，不靠重新调用模型', example: '看到 8-K 以后：强烈看空' },
  ];

  const TIERS = [
    { tier: '发生的事', examples: '官方动作、公布的数、已经完成的交易', counts: '能动“现在在哪一格”，也能推状态' },
    { tier: '当事人说的', examples: '公司指引、管理层表态、官员讲话', counts: '只能推状态' },
    { tier: '第三方看法', examples: '卖方、媒体分析、专家', counts: '只能推状态' },
    { tier: '传闻', examples: '“知情人士称”、没有出处的消息', counts: '只能推状态' },
  ];

  const TIER_RULES = [
    '推多远由模型判，写明依据；层不给固定分数。',
    '独立来源按原始来源数：二十家媒体转述同一条独家，是同一条证据的二十个出处，算一份。',
    '层看是谁确认的：“知情人士称商务部开始发许可证”是传闻；商务部或公司确认以后，确认的那条是发生的事，替代那条传闻；传闻还是传闻，留在历史里。',
    '证据只存一次，本身不带方向；往哪边推记在证据和每条观点之间的连线上，由每次重判写。同一句话可以连几条观点，各推各的。',
  ];

  // How B reads A when B depends on A.
  const DEPENDENCY_TREE = {
    label: 'B 依赖 A', question: 'A 是哪一种观点？', note: '箭头带一个方向：A 的哪一头对 B 是看多；两条主题观点之间是同向或反向',
    children: [
      {
        answer: '数字的观点', label: '钉住年份', note: '例：JPM 2027 全年净利息收入 → 美联储 2027 年末利率',
        children: [
          { answer: 'A 开着', label: '读 A 的现状', act: true },
          { answer: 'A 出了答案', label: '读 A 的答案', note: '答案本来就是 B 要的输入，不算断', act: true },
          { answer: 'A 答不出', label: '标“缺这个输入”', note: '不能把没有答案当成中性' },
          { answer: 'A 还没建', label: '箭头先等着', note: 'A 建出来时自动连上，B 重判一次' },
        ],
      },
      {
        answer: '事件的观点', label: '顺着接续往下走', note: '例：NVDA FY27 全年中国区收入 → 这一档芯片对华出口许可',
        children: [
          { answer: 'A 开着', label: '读 A 的现状', act: true },
          { answer: 'A 关了，有接续的', label: '读接续的那条', note: '记一笔，B 重判一次', act: true },
          { answer: 'A 关了，没有接续', label: '读 A 的答案，标“只是历史”', note: 'A 答不出的，标“缺这个输入”' },
        ],
      },
    ],
  };

  const DEPENDENCY_RULES = [
    '依赖只连输入：B 的答案要用到 A 的答案，才连 B → A。对方对已经发生的事做出的反应，是证据，不是依赖：OPEC+ 看着已经发生的油价定产量，每天的油价是“OPEC+ 配额”这条观点的证据；“原油年均价”这条观点要用到 OPEC+ 配额的答案，才依赖它。',
    '主题观点不说好坏，好坏由每个依赖它的对象观点自己的箭头说：降息那头对以太坊是看多，对 JPM 是看空。',
    '箭头只有一个方向。看起来要“先好后坏”，说明中间还有一条观点没写出来，要拆出来：钢铁关税抬高国内钢价是一条路，拖垮下游用钢需求是另一条路。',
    '只传通知，不搬证据：A 的证据不复制到 B，B 重判时把 A 的现状当背景读。B 重判时，代码把同时连在 A 上的证据标出来：“这条已经算进 A 了”。',
    '什么时候通知 B：A 的“现在在哪一格”或状态换了格；B 读的那条换了（顺着接续换到下一条、等着的箭头连上了）；A 答不出。没换格就不通知。B 每次读的是哪一条、哪一版，记在 B 的重判记录里。',
    '不能绕成环。两个问题互为输入（同一时期一起决定），说明问题没起好：合成一个问题，或者只留对投资判断有用的那个方向，另一个方向的影响走证据。代码不收会绕成环的箭头，退回给模型改写，留记录；加箭头、顺着接续换下一条时都查。',
    '建一条新观点时，模型挑它依赖哪几条：开着的主题观点（用检索找几条来挑），或别的对象的观点（比如供应链）；数字的依赖也可以指向还没建的那一年，写明哪个对象、看的是什么、哪一年，箭头先等着。每条写方向和一句怎么影响；代码核对被依赖的观点确实存在，或者写明了要等的那一年。接续的新一期，照上一期的依赖挪一年，由模型确认。',
    '真正新的一条主题观点（不接续谁）建出来时，把全部开着的观点分批过一遍，由模型挑出该依赖它的，补上箭头，这些观点各重判一次。新主题很少，全过一遍花得起；只取检索的前几名会漏掉排在后面的。',
  ];

  // Succession: the same thing, period after period.
  const CHAIN_RULES = [
    '同一样东西的下一条观点接着上一条，连成一条链：美联储 2026 年末利率 → 2027 年末利率 → 2028 年末利率。链存的是血缘，箭头怎么读见上面。',
    '一条最多被接续一次，不能分叉。一条写坏了要拆成两条时不算接续；依赖它的箭头收到通知，重判时重新挑。',
    '接续的那条，梯子的方向和上一条一样（第一格永远是同一头），门槛可以重定。所以箭头只按“哪一头”读，不按“第几格”。',
    '接错了，追加一条“撤销接续”，不改原来的记录。',
    '接续、并入、依赖是三种关系，分开记：接续是下一期，并入是重复，依赖是箭头。',
  ];

  // Writing what extraction hands over, one item per round: candidate views first, then evidence.
  const INTAKE_STEPS = [
    { code: '1', name: '核对出处', who: '代码', does: '出处在处理记录里查不到的不要，记下原因' },
    { code: '2', name: '收证据', who: '代码', does: '重试不重复存；上游修正版只换它自己那一处出处：它只是转载的，不动原来那条证据；它本身是原始来源的，新版的句子照常对上，改了的就替代原句' },
    { code: '3', name: '拉清单', who: '代码', does: '候选观点讲的每个对象开着的观点，加上每条链最近关掉的那条；讲的是主题时，再从全部开着的主题观点里检索补 5 条；超出今年、明年的数字候选观点先筛掉；清单是空的，也照样交给第 4 步，只判新观点还是不开' },
    { code: '4', name: '对上', who: '模型', does: '一次调用，不读原文：每个候选观点挂到哪一条、接续哪一条、新观点、不开，还是拿不准，写理由；每条证据和它那条观点下没被替代的证据比，是重复、替代还是新证据' },
    { code: '5', name: '核对', who: '代码', does: '编号必须在清单里，或者是那条观点下的证据；接续合规矩' },
    { code: '6', name: '写进库', who: '代码', does: '各对象自己的队列写，先写主题，再写对象；重复只多一个出处；替代按说的时间排（这句话是哪天说的），后说的算数，先说的标“被替代”，晚到的旧说法直接进历史；被替代的证据还连着别的观点，新的那条也连过去；原始来源自己的修正版里找不到、也没被新句替代的原句，算删了，标“被替代”；对上那一刻看到的变了，这部分重新对上' },
    { code: '7', name: '连依赖', who: '模型', does: '新观点挑它依赖哪几条；新的主题观点反过来补箭头；代码查环' },
    { code: '8', name: '重判一轮', who: '模型', does: '这一轮有新证据或替代、或者依赖变了的观点，按依赖先后各判一次；只多了重复的不判；换了格的再往下通知' },
  ];

  // Two lanes, one shape: a candidate view and a piece of evidence are each compared with what is already there.
  const INTAKE_SHAPE = [
    { aspect: '去哪比', views: '这个对象开着的观点（主题观点用检索找几条）', evidence: '它那条观点下已有的证据' },
    { aspect: '判什么', views: '挂到已有的、接续、新观点、不开、拿不准', evidence: '重复、替代、新证据' },
    { aspect: '链', views: '接续：美联储 2026 年末利率 → 2027 → 2028', evidence: '替代：AMZN 资本开支指引涨 12% → 25%' },
    { aspect: '什么算现在', views: '链上开着的那条', evidence: '没被替代的那些' },
    { aspect: '搜全库吗', views: '公司不搜；主题只在主题观点里检索', evidence: '不搜' },
  ];

  // Step 4: where a candidate goes.
  const MATCH_OUTCOMES = [
    { outcome: '挂到已有的', when: '候选观点看的就是那条观点看的东西，或者是它的一部分：“H20 在中国的收入”是“中国区收入”的一部分', writes: '只挂证据，证据再和那条观点下的证据比；候选观点的问题、梯子、到期日都不要，用已有的' },
    { outcome: '接续', when: '同一样东西的下一年（数字）；或者那条已经关了，要接着看（事件）', writes: '建新观点，记接续；依赖照上一期挪一年' },
    { outcome: '新观点', when: '另一样东西，会和已有的各走各的：Blackwell 这一档对华许可，不是 H20 这一档', writes: '建新观点，梯子和到期日从此定死' },
    { outcome: '不开', when: '候选观点太宽，捆了几样东西，比如“美国对华芯片管制”', writes: '不建；只挂在它上面的证据不存' },
    { outcome: '拿不准', when: '说不清', writes: '还没定：先建新的、由查重来并，还是先并进最像的那条' },
  ];

  const MATCH_NOTES = [
    '对上问的是“挂到哪”，不只是“是不是同一条”：只要属于已有的争论，就挂过去；只有确实是另一样东西，才开新观点。分析师不会为“H20 在中国的收入”单开一个争论，它是“中国区收入”这个争论的证据。',
    '拉清单靠对象：公司观点把这家公司开着的观点全拿出来就行，不用搜，也不会漏。主题观点的身份只看“看的是什么”，主题只是放它的地方，所以要跨全部主题比；主题标得模糊、条数多，这里和定期查重才用检索。相似度只用来拉清单，当不了裁判：“H20 对华许可”和“Blackwell 对华许可”很像，却是两条；看多和看空的两种说法，是同一条。',
    '主题观点的范围按管它的那条规定或那个决定来写：写成“2025-04 那条规定管的这一档芯片（H20、MI308 等）”，AMD 的 MI308 就会挂上去，不会另开一条。',
    '抽取只交挂在观点上的证据；候选观点不开、证据又没挂在别的观点上的，不存，只在处理记录里留一笔。',
  ];

  // Step 4: where a piece of evidence goes, against the evidence its view already holds.
  const EVIDENCE_OUTCOMES = [
    { outcome: '重复', when: '说的就是那条观点下已有的一条：转载；正文和表格里的同一个数；同一个人把同样的话再说一遍', writes: '那一条多记一个出处；证据不多一条，不重判' },
    { outcome: '替代', when: '和已有的一条是同一件事的前后两个说法：同一个人后来改了说法或数（指引、预测、状态）；官方证实或否认了一条传闻；原始来源自己出了修正版，改了原句', writes: '按说的时间排（这句话是哪天说的），后说的算数，先说的标“被替代”，留在历史里；晚到的旧说法直接进历史；重判' },
    { outcome: '新证据', when: '别的都是：新的事、另一期的数、另一个人的说法（说法相反的也是）；拿不准也算新证据', writes: '加进来，和别的一起算数；重判' },
  ];

  const EVIDENCE_NOTES = [
    '证据只和它那条观点下的证据比，不拿证据去搜全库：观点先定好（抽取时挂上的，或者候选观点对上的那条），再看这条观点自己已经有什么。和观点一个形状：候选观点比的是这个对象开着的观点，证据比的是这条观点下的证据。',
    '一条证据挂几条观点，也只存一条：和这几条观点下的证据一起比一次。',
    '被替代的证据还连着别的观点，新的那条也连过去，那些观点也重判；不然那条观点手里只剩一个过时的说法。',
    '证据是一句话或一个数，替掉的只是那一句：卖方新报告改了收入预测，替掉的是它上一份里的那个预测，别的论据照样算数。',
    '对上不读原文，比的是证据里“一句话说清”的那句；拿不准算新证据，最坏也就是两条都算数，由重判自己看。',
  ];

  // The three merges, at different times.
  const MERGE_KINDS = [
    { merge: '挂到已有的', when: '每条信息对上时', does: '只加证据和连线' },
    { merge: '接续', when: '对上时，同一样东西的下一期', does: '建新观点，记接续' },
    { merge: '并入', when: '定期查重：Pull 模式每天发起一次；同一对象开着的观点两两比，主题观点跨全部主题用检索找相像的', does: '后建的那条关掉，记“并入 X”；它的连线加到 X 上；指向它的箭头顺着“并入”读到 X，方向按 X 的梯子重新核对，代码查环；X 重判一次' },
  ];

  const INTAKE_EXAMPLE_TREE = {
    label: '三条信息，库从空的开始', note: '示意',
    children: [
      {
        answer: '2025-04-15 NVDA 的 8-K', label: '库是空的，交来两个候选观点', question: '对上：都开新观点',
        children: [
          { answer: '#1 主题观点', label: '这一档芯片对华出口许可（事件）', note: '证据：H20 出口中国要许可证（发生的事）；现在在第 2 格', act: true },
          { answer: '#2 对象观点（NVDA）', label: 'FY26 全年中国区收入（数字）', note: '证据：预计最多约 55 亿美元的费用（当事人说的）；依赖 #1，放松那头看多', act: true },
        ],
      },
      {
        answer: '2025-04-16 AMD 的 8-K', label: '标到 AMD，AMD 还没有观点，交来两个候选观点', question: '对上',
        children: [
          { answer: '候选观点“MI308 对华许可”', label: '挂到 #1', note: '清单里检索到 #1：同一条规定管的同一档，会一起动；它的证据再和 #1 下的证据比：AMD 说的是 MI308，是新证据；#1 重判，没换格，不通知 #2', act: true },
          { answer: '候选观点“AMD 2025 全年中国区收入”', label: '新观点 #3', note: 'AMD 还没有开着的观点；证据：预计最多约 8 亿美元的费用（当事人说的）', act: true },
        ],
      },
      {
        answer: '2025-04-16 路透转载 NVDA 的 8-K', label: '已有的观点：#2 和它依赖的 #1', question: '对上',
        children: [
          { answer: '证据挂到 #1 和 #2', label: '都是重复', note: '原始来源同是 NVDA 的 8-K，说的就是 #1、#2 下已有的那两条：各多记一个出处；#1、#2 都不重判', act: true },
        ],
      },
    ],
  };

  // One view's evidence over half a year: how repeats and replacements keep it current (numbers illustrative).
  const EVIDENCE_EXAMPLE = [
    { item: '2-05 电话会：资本开支指引涨 12%', matched: '新证据（这条观点下还没有证据）', store: '加 g1', rejudge: '判' },
    { item: '2-06 路透转载', matched: '重复 g1', store: 'g1 多一个出处', rejudge: '不判' },
    { item: '3-10 MS：预计涨 18%', matched: '新证据（另一个人说的）', store: '加 m1', rejudge: '判' },
    { item: '4-30 电话会：指引改成涨 25%', matched: '替代 g1', store: 'g2 算数，g1 被替代', rejudge: '判，读到“12% → 25%”' },
    { item: '5-02 MS：改成涨 27%', matched: '替代 m1', store: 'm2 算数，m1 被替代', rejudge: '判' },
    { item: '5-20 一份 2 月的 MS 报告晚到', matched: '替代：和 m2 是同一个人说同一件事，它更早', store: '排进历史，m2 照旧算数', rejudge: '不判' },
    { item: '6-10 会上重申“还是 25% 左右”', matched: '重复 g2', store: 'g2 多一个出处（最近一次 6-10）', rejudge: '不判' },
  ];

  const EVIDENCE_EXAMPLE_NOTE = '半年后这条观点下可能有几十条证据，重判读的只是没被替代的那几条：公司指引涨 25%（2 月是 12%），MS 预计涨 27%（3 月是 18%），加上别的人、别的事。';

  // The judge of step 4, its records, and the labels that will train a faster model.
  const JUDGE_STEPS = [
    { code: '1', name: '大模型对上', who: '模型', does: '第一版用通用大模型做对上（Config 里的“对上”设置），先让系统跑起来' },
    { code: '2', name: '每次都记', who: '代码', does: '每次对上留一条对上记录：给模型看了什么、按什么顺序、它答了什么、最后写进库的是什么' },
    { code: '3', name: '挑一部分', who: '代码', does: '拿不准的；后来被查重并掉的；被代码拒绝过的；再由 Pull 模式每周随机抽一些' },
    { code: '4', name: '人来标', who: '人', does: '看候选观点和清单，选出正确的去向；看证据和它那条观点下的证据，选重复、替代还是新证据；写一句理由' },
    { code: '5', name: '量', who: '代码', does: '拿人标的量对上准不准：新观点判得准不准、挂错多少、替代判错多少、换个顺序答案变不变' },
    { code: '6', name: '训练小模型', who: '代码', does: '攒够了，用大模型的判断和人标的一起，训练一个小的匹配模型' },
    { code: '7', name: '小模型接手', who: '代码', does: '它在考试集上和人标的一致率过了 Alex 定的线，又对这一条有把握，就由它定；其余照旧交大模型' },
  ];

  const TRACE_FIELDS = [
    { part: '哪条信息', meaning: '上游编号和版本、顺序号' },
    { part: '交来的', meaning: '抽取交来的候选观点和证据，原样' },
    { part: '给模型看的', meaning: '候选观点比的是清单：每条观点按给的顺序，每条是怎么进来的（这个对象开着的、检索第几名、某条链最近关掉的）；证据比的是它那条观点下没被替代的证据' },
    { part: '谁定的', meaning: '大模型、以后的小模型，或人' },
    { part: '请求和返回', meaning: '实际发出的请求、原始返回、Config 版本（模型、提示词版本、温度）' },
    { part: '决定', meaning: '每个候选观点的去向和理由；每条证据是重复、替代还是新证据；代码核对的结果和拒绝的原因' },
    { part: '写进库的', meaning: '最后写进库的结果' },
    { part: '后来', meaning: '查重把它并掉了、人标的和它不一样：都作为新记录指回这一条' },
  ];

  const LABEL_RULES = [
    '标注不挡流程：系统照常跑，标注是事后做的。',
    '人标的选项和模型的一样：候选观点是挂到哪一条、接续哪一条、新观点、不开；证据是重复、替代、新证据；都另加“说不清”；写一句理由。',
    '标准由 Alex 定：先标一批，大家对齐“同一样东西”“一部分”和“替代”的边界，再往下标。',
    '用来考试的那一份，标的人看不到模型的答案；考试集固定，只在换裁判（换模型、换提示词、换上小模型）时评一次；平时调提示词只用另一份。',
    '标注不直接改库：人标出来的重复观点，交给查重并入；证据的标注和其余的先记着。',
    '这里用的是人工标注加监督训练：训练一个分“是不是同一样东西”的小模型，用不到强化学习。',
    '同样的请求和返回也给连依赖、重判和查重记着（重判记录里本来就有）；第一版只标对上。',
  ];

  // How a view ends.
  const LIFECYCLE_TREE = {
    label: '一条观点', question: '到哪一步了？',
    children: [
      { answer: '开着', label: '没被替代的证据变了、或者依赖变了，就重判一次', note: '名额：事件同一件事一条；数字同一个数今年、明年两条' },
      { answer: '期末已过，答案没出', label: '等答案', note: '数字的观点；不占今年、明年的名额' },
      {
        answer: '关掉', label: '三种方式', question: '为什么关？',
        children: [
          { answer: '出答案', label: '记答案和出处', note: '按梯子写明的判卷来源，用第一次公布的值；拿答案对的，是带来答案的那条信息进来之前最后的状态', act: true },
          { answer: '答不出', label: '记原因，不算准不准', note: '不再披露这个数、事情本身没了；对象退出名单也先这样关，算不算成绩还没定；下载或解析失败是故障，要重试，不算答不出', act: true },
          { answer: '并入', label: '记“并入 X”', note: '查重发现重复', act: true },
        ],
      },
    ],
  };

  const LIFECYCLE_NOTES = [
    '到期由 Pull 模式发起，等发布日不晚于到期日的信息都处理完再定答案。事件观点的答案由谁来定、要不要先经最终判定，等最终判定按新设计重做时定。',
    '答案出来以后，后来的修订记下来，但不改这条观点的答案。要接着看，就开一条新观点接续它。',
  ];

  const VIEW_FIELDS = [
    { part: '对象', meaning: '名单里的哪个对象', example: 'NVDA' },
    { part: '种类', meaning: '对象观点或主题观点', example: '对象观点' },
    { part: '看的是什么', meaning: '数字：哪个数、哪一年、一段时间的数还是时点的数、判卷来源；事件：哪件事、范围、阶段', example: 'FY27 全年中国区收入；判卷看年报里按地区分的收入' },
    { part: '问题', meaning: '一句话，写下不改', example: 'NVDA FY27 全年中国区收入，比 FY26 会怎样？' },
    { part: '梯子', meaning: '五格（只有是或否的问题两格），每格一个是或否的条件，写下不改', example: '涨 50% 及以上……降 80% 及以上' },
    { part: '到期日', meaning: '争论见分晓的那天；数字就是它公布的那天', example: 'FY27 年报的财报日' },
    { part: '现在在哪一格、状态', meaning: '两个位置，每次重判各记一版，写明依据', example: '状态：强烈看空' },
    { part: '依赖', meaning: '指向哪几条观点，各带一个方向', example: '→ 这一档芯片对华出口许可：放松那头看多' },
    { part: '接续', meaning: '接着哪一条；可以没有', example: '接着 FY26 那条' },
    { part: '从哪来', meaning: '从哪条信息建的', example: '2025-04-15 NVDA 的 8-K' },
    { part: '结束', meaning: '开着、等答案，或者关掉（出答案、答不出、并入）', example: '开着' },
  ];

  const EVIDENCE_FIELDS = [
    { part: '原文', meaning: '信息里的那一句，或表里的那一格' },
    { part: '一句话说清', meaning: '离开原文也看得懂的一句：谁、做了什么、多少、哪一期；对上和重判读这一句' },
    { part: '出处', meaning: '上游编号和版本、类别、发布日、在信息里的位置；重复的（转载、同一条信息的正文和表格、同一个人再说一遍）记成这条证据的又一个出处' },
    { part: '谁说的', meaning: '说这句话的人或机构' },
    { part: '原始来源', meaning: '转述的，指向最初说这句话的人和那一次（哪天）；按它数独立来源，替代也按这一天排先后' },
    { part: '哪一层', meaning: '发生的事、当事人说的、第三方看法、传闻' },
    { part: '事情发生的时间', meaning: '事情什么时候发生或生效；数字写它属于哪一期' },
    { part: '被替代', meaning: '指向替代它的那一条：同一个人后来改了说法或数、官方证实或否认了这条传闻；或者原始来源自己出了修正版，把这句改了、删了（删了的没有后继）；被替代的不再算数，留在历史里' },
  ];

  const ORDER_RULES = [
    '只有信息能产生证据；观点之间只传通知，不传证据，所以观点不会自己证明自己。',
    '每条观点只有一个写入者：主题观点由主题的队列写，对象观点由对象的队列写；同一条信息先写主题，再写对象。',
    '先后按顺序号排，不用电脑时钟。一条信息只读顺序号比它小的信息留下的状态，加上这一轮里它自己已经写下的（比如上游这一轮刚判完的状态）；并行时读到的东西在提交前变了，就重新做一次。',
    '一条信息引起的变化算一轮：先做完挂证据、建观点、接续和补箭头，再按依赖先后重判，上游这一轮判完，下游才判，每条观点每轮只提交一次；上游没换格，这条路就停。',
    '只追加：观点的问题、梯子和到期日写下就不动；对上、重判、接续、关掉、并入、标注都是新加的记录，带顺序号。',
    '晚到的信息：收到时重判，不倒回去改过去的状态；证据记它真实的发布日；晚到的旧说法（和现在算数的某一条是同一件事的前后两个说法，又说得早）直接进历史。',
    '同一条信息的修正版只换它自己那一处出处：它只是转载的，不动原来那条证据；它本身是原始来源的，改了的原句由新句替代，删了的标“被替代”。连着变了的证据的观点各重判一次；过去的重判记录不改。',
    '失败：每条信息记下做到哪一步，从失败的那一步重试，重试只替换自己上次的结果；多次失败的放进人工复核池。',
    '对象被移出名单：它开着的观点关掉，记“答不出（不再跟踪）”；算不算成绩还没定。',
    '两头都能查：从一条观点查到推过它的全部信息；从一条信息查到它建过的观点，和它作为出处的全部证据（重复的也查得到）。',
  ];

  const STORE_NOTE = '存在哪：一个关系数据库就够，记录都是只追加的表；全文检索和向量检索建在同一个库里，是随时能重建的索引，不是原始记录；依赖的箭头用表和递归查询，不需要单独的向量库或图数据库。具体用哪个产品，建的时候定。规模（估算）：约 1,400 条开着的观点，一年约 180 万条证据。';

  const VIEWS_OPEN = [
    '“今年”“明年”按已经处理过的信息里最晚的发布日算：这是 Claude 的读法，等 Alex 确认。',
    '拿不准是同一条还是新的时，先建新的、由查重来并，还是先并进最像的那条。',
    '共识：市场押在哪一格（同一把梯子上的第三个位置）；对股价的看法就是我们的状态和共识的差距。',
    '什么样的问题算关键问题，每个对象几条（现实里每家公司只盯 2–3 个）；去重管不住“问太多不同的小问题”。',
    '事件的“同一件事”边界：什么算接续、什么算新的，要拿真实案例定。',
    '事件观点到期以前的中间日期（规定的生效日、征求意见截止日）放在哪。',
    '对象退出名单的观点算不算成绩。',
    '利率、汇率、指数的期货能交易，但名单把它们放在主题下（D11），它们价格的看多看空没有地方放。',
    '标注：谁来标、每周抽多少、用什么界面；小模型接手的门槛由 Alex 定。',
    '建之前要在存下的信息上量：每个对象开着几条观点；“新观点”判得准不准；清单顺序打乱后答案变不变；“替代”和“新证据”分得准不准；热点观点半年积累多少条没被替代的证据；没被点名的对象漏掉多少证据。',
    '到期时谁定事件观点的答案、要不要先经最终判定：最终判定和 Pull 模式按新设计重做时定。',
    '开题：系统一上线，每个对象都是空的，观点只能由先到的信息一条条建，留下的是先到的话题，梯子也照第一份材料切。要不要单独一步：开始覆盖一个对象时，先读一批材料，定下两三个关键争论。',
    '格内的大变化不通知下游：只在换格时通知，AMZN 资本开支指引从涨 12% 改成 25%，都在同一格里，依赖它的 NVDA 那条观点听不到。',
  ];

  // ------------------------------------------------------------------ final verdict (old draft, to be redone: D41)

  const VERDICT_EXAMPLE_NOTE = '到 7 月证据两边都有：NVDA 的声明（当事人说的）削弱，卖方 A（第三方看法）支持。两条不在同一层，也没有“发生的事”来削弱，不触发最终判定；观点留着，两边的证据都展示出来。能一锤定音的，就是证伪条件里写的那件事：美国会不会真的批准 H20 对华出口。8 月据报道商务部开始发许可证，证伪条件满足，送最终判定，主题观点“管制会收紧”判为已证伪。以它为前提的 NVDA 观点再判一次：据报道中国要求企业不要采购 H20，中国收入仍没回来，所以留下，前提换成一条新的主题观点。';


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
    button: '展开抽取：每一类信息怎么读成证据和候选观点',
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
          <h2 class="drill__title">抽取：每一类信息怎么读成证据和候选观点</h2>
          <p class="drill__intro">抽取只做一件事：每条信息整份交给模型，用资深对冲基金分析师的视角、按这一类的提示词，对着这些对象已有的观点读完，交出两样东西。一是证据：支持或削弱已有观点的话和数，挂到那条观点上。二是候选观点：已有观点管不到、又要紧的事，带着提出它的证据。每条带出处，交给观点库；怎么和库里已有的比、写进去，是观点库的事。</p>
          <p class="drill__status"><span class="pill pill--strong">第一版已冻结 · 2026-10-18</span>定下：整份交给模型；每一类一份提示词，拼法相同；观点是模型的判断，证据是客观的；每条都带出处；抽取只读。2026-10-20 按 D41、D42 改了交给观点库的东西：证据挂到已有观点上，和候选观点分开交。没定：每一类提示词的具体写法，建的时候试过再定。</p>
          <h3 class="drill__heading drill__heading--spaced">一条信息，一步一步</h3>
          <p class="flow-legend">黑框是模型做的，灰框是代码做的。</p>
          ${flow(stepCards, '→', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">读出两样东西：证据和候选观点</h3>
          ${table(['', '证据', '候选观点（thesis）'], EXTRACT_TWO.map((row) => [row.aspect, row.evidence, row.candidate]), escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">读到一句话或一个数，它算什么</h3>
          ${tree(EXTRACT_SORT_TREE, escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">第 1 步：每一类的提示词，都由同一个提示词模板的这五块拼起来</h3>
          ${flow(templateCards, '+', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">每一类有自己的提示词：拼出来长这样（T7 新闻）</h3>
          ${tree(PROMPT_EXAMPLE, escapeHtml)}
          <ul class="drill__rules">${listItems(PROMPT_NOTES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">16 个类别：每一类读出什么（第 4 块）</h3>
          ${table(['类别', '这一类要读出什么', '证据一般在哪一层'], categoryRows, escapeHtml)}
          <p class="drill__footnote">${escapeHtml(CATEGORY_NOTE)}</p>
          <h3 class="drill__heading drill__heading--spaced">例子：两条信息读出什么</h3>
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
    button: '展开观点库：观点长什么样、证据和候选观点怎么写进库、怎么连、怎么标注',
    kicker: '观点库 · 详细说明',
    size: 'full',
    render(container, context) {
      const escapeHtml = context.escapeHtml;
      const stepCards = (steps) => steps.map((step) => ({ code: step.code, title: step.name, who: step.who, note: step.does, strong: step.who === '模型' }));
      const tierCards = TIERS.map((tier, index) => ({ code: String(index + 1), title: tier.tier, note: `${tier.examples}。${tier.counts}`, strong: index === 0 }));
      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">观点库（thesis · ladder · evidence）</h2>
          <p class="drill__intro">系统做的事，就是建立、更新和关掉这里的观点。一条观点是一个问题、一把梯子和一个到期日：证据把我们的判断往两头推，到期拿答案对一下，就知道判得准不准。抽取交来两样东西，在这里各走一条线、走法一样：候选观点和这个对象开着的观点比，挂上去、接续、开新的，或者不开；证据和它那条观点下已有的证据比，是重复、替代还是新证据；只是重复的，不重判。每条证据都带出处，所有记录只追加。</p>
          ${status('设计中 · 2026-10-20', '已定（D38–D40、D42）：观点的结构、两种观点、梯子、两个位置、证据和层、依赖和接续、候选观点和证据怎么写进库、对上的裁判和标注。还没定的见最后。', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">结构</h3>
          ${tree(VIEW_TREE, escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">两种观点：结构一样，梯子的格意思不一样</h3>
          ${table(['种类', '挂在哪', '梯子的格', '例子'], VIEW_KINDS.map((row) => [row.kind, row.on, row.rungs, row.example]), escapeHtml)}
          <p class="drill__footnote">${escapeHtml(KIND_NOTE)}</p>
          <h3 class="drill__heading drill__heading--spaced">梯子：五格（只有是或否的问题两格），每格是一个看得见的条件</h3>
          ${tree(LADDER_EXAMPLES, escapeHtml)}
          <ol class="drill__rules">${listItems(LADDER_RULES, escapeHtml)}</ol>
          <h3 class="drill__heading drill__heading--spaced">一把梯子上的两个位置</h3>
          ${table(['位置', '是什么', '谁能动它', '例子'], POSITIONS.map((row) => [row.position, row.means, row.moves, row.example]), escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">证据分四层</h3>
          ${flow(tierCards, '·', escapeHtml)}
          <ul class="drill__rules">${listItems(TIER_RULES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">依赖：箭头怎么读</h3>
          ${tree(DEPENDENCY_TREE, escapeHtml)}
          <ul class="drill__rules">${listItems(DEPENDENCY_RULES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">接续：同一样东西一期接一期</h3>
          <ul class="drill__rules">${listItems(CHAIN_RULES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">进库：候选观点和证据各走一条线，走法一样</h3>
          ${table(['', '候选观点', '证据'], INTAKE_SHAPE.map((row) => [row.aspect, row.views, row.evidence]), escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">一条信息进来，怎么写进库（一轮）</h3>
          <p class="flow-legend">黑框是模型做的，灰框是代码做的。</p>
          ${flow(stepCards(INTAKE_STEPS), '→', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">第 4 步对上：候选观点的去向</h3>
          ${table(['去向', '什么时候', '写什么'], MATCH_OUTCOMES.map((row) => [row.outcome, row.when, row.writes]), escapeHtml)}
          <ul class="drill__rules">${listItems(MATCH_NOTES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">第 4 步对上：证据的去向</h3>
          ${table(['去向', '什么时候', '写什么'], EVIDENCE_OUTCOMES.map((row) => [row.outcome, row.when, row.writes]), escapeHtml)}
          <ul class="drill__rules">${listItems(EVIDENCE_NOTES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">合并有三种，发生在不同的时候</h3>
          ${table(['合并', '什么时候', '做什么'], MERGE_KINDS.map((row) => [row.merge, row.when, row.does]), escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">例子：三条信息怎么写进库</h3>
          ${tree(INTAKE_EXAMPLE_TREE, escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">例子：一条观点下的证据怎么跟着更新（AMZN 2026 全年资本开支，示意）</h3>
          ${table(['信息', '对上证据', '库里', '重判'], EVIDENCE_EXAMPLE.map((row) => [row.item, row.matched, row.store, row.rejudge]), escapeHtml)}
          <p class="drill__footnote">${escapeHtml(EVIDENCE_EXAMPLE_NOTE)}</p>
          <h3 class="drill__heading drill__heading--spaced">对上的裁判和标注：先用大模型跑起来，攒下标注，以后交给小模型</h3>
          <p class="flow-legend">黑框是模型做的，灰框是代码或人做的。</p>
          ${flow(stepCards(JUDGE_STEPS), '→', escapeHtml)}
          <div class="drill__columns">
            <section>
              <h3 class="drill__heading drill__heading--spaced">一条对上记录记什么</h3>
              ${table(['部分', '记什么'], TRACE_FIELDS.map((row) => [row.part, row.meaning]), escapeHtml)}
            </section>
            <section>
              <h3 class="drill__heading drill__heading--spaced">标注的规矩</h3>
              <ul class="drill__rules">${listItems(LABEL_RULES, escapeHtml)}</ul>
            </section>
          </div>
          <h3 class="drill__heading drill__heading--spaced">一条观点怎么结束</h3>
          ${tree(LIFECYCLE_TREE, escapeHtml)}
          <ul class="drill__rules">${listItems(LIFECYCLE_NOTES, escapeHtml)}</ul>
          <div class="drill__columns">
            <section>
              <h3 class="drill__heading drill__heading--spaced">一条观点有哪些部分</h3>
              ${table(['部分', '写什么', '例子'], VIEW_FIELDS.map((row) => [row.part, row.meaning, row.example]), escapeHtml)}
            </section>
            <section>
              <h3 class="drill__heading drill__heading--spaced">一条证据记什么</h3>
              ${table(['部分', '写什么'], EVIDENCE_FIELDS.map((row) => [row.part, row.meaning]), escapeHtml)}
              <h3 class="drill__heading drill__heading--spaced">先后、同步和血缘</h3>
              <ul class="drill__rules">${listItems(ORDER_RULES, escapeHtml)}</ul>
              <p class="drill__footnote">${escapeHtml(STORE_NOTE)}</p>
            </section>
          </div>
          <h3 class="drill__heading drill__heading--spaced">还没定的</h3>
          <ul class="drill__rules">${listItems(VIEWS_OPEN, escapeHtml)}</ul>
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
          ${status('旧稿 · 要重做', '观点库已按 D38–D40 重建，这里写的检验条件、证实和证伪、前提都不再用；关掉之前要不要经过这里，重做时定（D41）。', escapeHtml)}
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
              <p class="drill__footnote">${escapeHtml(VERDICT_EXAMPLE_NOTE)}</p>
            </section>
          </div>
        </div>`;
      keepFitted(container);
    },
  };
})();
