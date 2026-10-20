// The New design's extraction module, the views database and the final verdict (decisions D26-D45). Extraction reads
// every item whole, by its category, as a senior hedge fund analyst, with the open views of the item's objects and the
// views they depend on (prompt part 5), and hands over two things with their sources: evidence attached to one of those
// views or to a candidate view, and candidate views for what none of them covers. There a view is a question with a
// ladder and a due date; the model matches each candidate to views found by search (the same view, its next period, or
// a new view) and each piece of evidence to the evidence its view already holds (repeat, replacement, or new evidence);
// evidence pushes the view's state, and views are linked by dependencies and chained by succession. Only what Alex said
// or decided is written as decided (D45); Claude's proposals he has not decided are kept apart in VIEWS_PROPOSED. The
// final verdict is still the old draft and is to be redone (D41). Edit the data at the top; the three drill-downs
// render it. The texts are for a reader who did not follow the discussion: plain words and an example, no field names.
(function () {
  'use strict';

  // ------------------------------------------------------------------ extraction

  // The template prompt of the read step: the same parts for every category, in this order.
  const TEMPLATE = [
    { part: '角色', content: '你是一位资深对冲基金分析师。读这条信息，是为了检验和形成观点：把支持或削弱已有观点的话和数挑出来，作为证据连到那条观点上；已有观点管不到、又要紧的事，写成候选观点，当场写全：问题、梯子、到期日，带上提出它的证据。观点照观点库的写法：一个观点只看一件东西；数字写明哪一年。', source: '所有类别一样' },
    { part: '这一类是什么、怎么读', content: '这一类的定义和读法，比如“看法和估计算作者说的，不当成已经发生的事”。', source: '取自分类规则，这里不另写' },
    { part: '讲的是谁', content: '这条信息的相关对象。', source: '这条信息的标签' },
    { part: '这一类要读出什么', content: '见下面的表，每类一行。', source: '抽取模块' },
    { part: '这些对象已有的观点', content: '这条信息相关对象开着的观点，加上它们依赖的观点，写明谁依赖谁；只给问题和看的是什么，不给状态和证据：让模型把证据连到这些观点上，又不被已有的判断带着走。', source: '观点库' },
  ];

  // What each category should yield, and in which tier its evidence usually sits. The category's own definition and
  // reading rule come from the classification page and are not repeated here.
  const CATEGORY_READS = {
    T1: { read: '实际数、指引、管理层的解释', tier: '实际数是发生的事；指引和解释是当事人说的' },
    T2: { read: '实际数、分部数；风险因素和业务描述里讲到的风险和变化', tier: '数是发生的事；风险和变化是当事人说的' },
    T3: { read: '交易条款（价格、对价、交割条件、时间表）；各方的说法和诉求', tier: '条款是发生的事；说法是当事人说的' },
    T4: { read: '管理层对关键问题的回答、口径的变化；分析师追问的焦点', tier: '回答是当事人说的；追问是第三方看法' },
    T5: { read: '管理层给的中长期目标、资本配置的框架、新业务的规模', tier: '当事人说的' },
    T6: { read: '发生了什么事（高管变动、并购、新产品、回购）；公布的经营数字（比如交付量）', tier: '发生的事' },
    T7: { read: '发生了什么事、什么时候、涉及谁；说法从哪来，原始来源是谁', tier: '官方确认的算发生的事；“知情人士称”算传闻' },
    T8: { read: '作者的看法、论据、预测、评级和目标价，以及它们的变化（用来算共识）', tier: '第三方看法' },
    T9: { read: '说话人讲的经营情况（订单、价格、份额、库存）；他凭什么知道', tier: '第三方看法' },
    T10: { read: '决定或行动本身、什么时候生效、影响谁；后面的程序（上诉、截止日），可以用作到期日', tier: '发生的事' },
    T11: { read: '公布的数字和政策决定，和上一次比差多少；官方措辞的变化', tier: '数和决定是发生的事；措辞是当事人说的' },
    T12: { read: '价格和成交的变化', tier: '发生的事' },
    T13: { read: '谁在买、谁在卖、规模多大', tier: '发生的事' },
    T14: { read: '排定的日期，用作到期日', tier: '发生的事' },
    T15: { read: '测到的经营数据，作为量化证据', tier: '发生的事（注明是第三方测的）' },
    T16: { read: '研究对象默认不看', tier: '—' },
  };

  const CATEGORY_NOTE = '每份文件都整份交给模型，里面的表格一起读；表格数据一次发布算一条，也整批交给模型。申报里的 XBRL 数字不另外推，文件本身已经有这些数。到期时要不要另外去查准确的数，等 Pull 模式按新设计重做时定。';

  // Every category has its own prompt: the same template with that category's parts. One assembled example.
  const PROMPT_EXAMPLE = {
    label: 'T7 新闻的提示词', note: '同一个提示词模板，第 2、4 块换成新闻这一类的',
    children: [
      { answer: '1 角色', label: '资深对冲基金分析师', note: '读这条信息，是为了检验和形成观点：证据连到已有观点上；已有观点管不到的要紧事，写成候选观点，当场写全问题、梯子、到期日' },
      { answer: '2 这一类怎么读', label: '媒体的报道', note: '取自分类规则：媒体发的内容，除了评论和分析（那归 T8）；媒体登记过的发布系列按系列归类' },
      { answer: '3 讲的是谁', label: '这篇报道的相关对象', note: '由代码填，比如 NVDA、AMD' },
      { answer: '4 要读出什么', label: '发生了什么事、什么时候、涉及谁；说法从哪来，原始来源是谁', note: '官方确认的算发生的事；“知情人士称”算传闻' },
      { answer: '5 已有的观点', label: '这篇报道相关对象开着的观点，加上它们依赖的观点', note: '由代码填，写明谁依赖谁，只给问题和看的是什么；比如“NVDA FY27 全年中国区收入，比 FY26 会怎样？”，和它依赖的“这一档芯片对华出口许可”' },
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
    { code: '2', name: '读', who: '模型', does: '整份读完，交出两样：证据，连到第 5 块里的观点上，或连到这次的候选观点上；候选观点，第 5 块里没有一条观点管、又要紧的事，带上提出它的证据。每条带出处' },
    { code: '3', name: '核对出处', who: '代码', does: '原文那一句在不在这条信息里、数字在不在那一句或那一格里；证据连的必须是第 5 块里的观点或这次的候选观点；对不上的不要，记下原因' },
    { code: '4', name: '交给观点库', who: '代码', does: '带着顺序号，交给观点库去对上、写进去' },
  ];

  // The two things one read hands over, side by side.
  const EXTRACT_TWO = [
    { aspect: '是什么', evidence: '信息里的一句话或一个数：谁说了什么、发生了什么', candidate: '一个要盯的问题（thesis），当场写全：问题、梯子、到期日' },
    { aspect: '多不多', evidence: '几乎每条信息都有', candidate: '少：第 5 块里没有一条观点管、又要紧的事' },
    { aspect: '连到哪', evidence: '第 5 块里的观点（可以连几条），或者这次的候选观点', candidate: '带着提出它的证据' },
    { aspect: '到了观点库', evidence: '和它那条观点下已有的证据比：重复、替代还是新证据', candidate: '和搜出来的几条已有观点比：是哪一条（或它的一部分）、接续、新观点，还是不开' },
    { aspect: '例子', evidence: '8-K 里的“H20 出口中国要许可证”', candidate: '2025-04 那条规定管的这一档芯片对华出口许可，到 2026-04-15 处在哪一格？' },
  ];

  // How the model sorts what it reads: against the open views in prompt part 5.
  const EXTRACT_SORT_TREE = {
    label: '读到一句话或一个数', question: '它和哪条观点有关？',
    children: [
      { answer: '第 5 块里的观点', label: '证据：连到那条观点上', note: '连在它直接讲的那条上；另一条依赖那条的，不再连给它', act: true },
      { answer: '第 5 块里没有，但要紧', label: '候选观点：这句话是它的证据', note: '是已有的哪一条，还是新观点，由观点库对上时定', act: true },
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
    '每条观点、每条证据、每一次变化都带出处；状态的每次变化写明依据哪几条证据（因为依赖的观点变了而重判的，也写那几条观点）。',
    '抽取核对：原文那一句不在这条信息里、数字不在那一句或那一格里的，证据连的不是第 5 块里的观点或这次候选观点的，不交出去；观点库核对：出处在处理记录里查不到的，不写进库。都记下原因。',
    '两头都能查：从一条观点查到它的全部来源信息，从一条信息查到它产生和改动过的全部观点和证据。',
    '整份信息不存，凭上游编号去团队的库里取；证据只存原文那一句。',
    '同一条信息里说同一件事的几处（正文和表格里的同一个数），交成一条证据，带几个出处。',
  ];

  const EXTRACT_EXAMPLE_TREE = {
    label: '两条信息读出什么', note: '示意',
    children: [
      {
        answer: '2025-04-15 NVDA 的 8-K', label: '库是空的，第 5 块里没有观点', question: '读出两条候选观点',
        note: 'T6 公司其他发布：H20 出口中国要许可证，预计最多约 55 亿美元的费用',
        children: [
          { answer: '候选观点（主题观点）', label: '2025-04 那条规定管的这一档芯片（H20、MI308 等）对华出口许可，到 2026-04-15 处在哪一格？', note: '事件；五格：全面禁止／要许可，一个都不发／要许可，发了，但有附条件的／要许可，发了，都不附条件／不再要许可；到期 = 2026-04-15；证据：原文“…requires a license for export to China … of the Company’s H20 integrated circuits…”（发生的事，NVDA 披露：H20 出口中国要许可证）；到了观点库，开成 #1', act: true },
          { answer: '候选观点（对象观点 NVDA）', label: 'NVDA FY26 全年中国区收入，比 FY25 会怎样？', note: '数字；五格：涨 50% 及以上／涨 10% 及以上不到 50%／涨跌都不到 10%／降 10% 及以上不到 80%／降 80% 及以上；到期 = FY26 年报的财报日；证据：原文“…charges of up to approximately $5.5 billion…”（当事人说的：公司预计最多约 55 亿美元的费用）；到了观点库，开成 #2，依赖 #1', act: true },
        ],
      },
      {
        answer: '2025-07-14 NVDA 的声明', label: '第 5 块：#2 和它依赖的 #1', question: '读出一条证据，没有候选观点',
        children: [
          { answer: '证据', label: '连到 #1', note: '当事人说的；一句话说清：NVDA 称美国政府已保证会批准 H20 对华出口的许可（2025-07-14）', act: true },
        ],
      },
    ],
  };

  const EXAMPLE_NOTE = '出处：每条证据都记上游编号和版本、所在段落和原文那一句（英文原句，中文只是说明）；代码核对“$5.5 billion”确实在那一句里。第一条信息进来时库是空的，第 5 块里没有观点，读到的要紧事只能写成候选观点；第二条信息进来时，第 5 块里已经有出口许可那条，NVDA 的声明就直接连上去。到了观点库，候选观点去和搜出来的已有观点比，证据去和它那条观点下已有的证据比，见观点库。例子用 NVDA，美股、期货、加密货币都走同一套。';

  const EXTRACT_OPEN = [
    '每一类提示词的具体写法，建的时候在存下的信息上试过再定；每一版记在 Config 里。',
    '候选观点的颗粒度（见观点库还没定的）：提示词要让模型知道，观点全抽成财务指标、抽得太粗或太细都不对；等调研完再写。',
    '已有观点里放了依赖的主题观点以后，几家公司对宏观的看法会一起连到主题观点上，可人多不等于信息多：主题观点要不要只收新的观察（发生的事、公司自己看到的订单和价格）。',
    '抽取连错、漏抽的证据，对上标注看不到：要不要另外按信息抽样，对着当时给的已有观点读原文核查。',
  ];

  // ------------------------------------------------------------------ views database (D38–D45)

  // What the views database holds.
  const VIEW_TREE = {
    label: '观点库',
    children: [
      {
        answer: '对象', label: '名单里的公司、加密货币、商品、主题',
        children: [
          {
            answer: '观点', label: '一个问题 + 一把梯子 + 一个到期日', note: '写下不改；梯子五格，只有是或否的问题两格；同一个对象、看同一样东西，同一时间只开一条',
            children: [
              { answer: '状态', label: '这条观点处在梯子的哪一格', note: '证据把它往梯子的一头或另一头推，模型按事实判', act: true },
              { answer: '连线', label: '证据', note: '证据只存一次，带出处和层；往哪边推记在连线上；被替代的证据留在历史里，不再算数', act: true },
              { answer: '依赖', label: '别的观点', note: '箭头带一个方向：对方的哪一头对它是看多', act: true },
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
        answer: '对象观点（数字）', label: 'NVDA FY27 全年中国区收入，比 FY26', question: '五格：对 NVDA 的业务是好是坏',
        note: '到期 = FY27 年报的财报日',
        children: [
          { answer: '强烈看多', label: '涨 50% 及以上' },
          { answer: '看多', label: '涨 10% 及以上，不到 50%' },
          { answer: '中性', label: '涨不到 10%，或降不到 10%' },
          { answer: '看空', label: '降 10% 及以上，不到 80%' },
          { answer: '强烈看空', label: '降 80% 及以上', note: '基本归零' },
        ],
      },
      {
        answer: '主题观点（事件）', label: '2025-04 那条规定管的这一档芯片（H20、MI308 等）对华出口许可，到 2026-04-15 处在哪一格',
        question: '五格：一条轴上的结果，不说好坏', note: '以那天已经生效的规定为准',
        children: [
          { answer: '第 1 格', label: '全面禁止，不再受理许可' },
          { answer: '第 2 格', label: '要许可，一个都不发' },
          { answer: '第 3 格', label: '要许可，发了，但有附条件的' },
          { answer: '第 4 格', label: '要许可，发了，都不附条件' },
          { answer: '第 5 格', label: '不再要许可' },
        ],
      },
    ],
  };

  const LADDER_RULES = [
    '每把梯子五格：对象观点是强烈看多到强烈看空，说的是对业务好还是坏；主题观点是一条轴上的五种结果，用结果命名，不说好坏。只有是或否的问题用两格，不硬分五格：对象观点的两格是看多、看空；主题观点的两格用结果命名，比如“到期前签署了”“没签署”。',
    '每一格写成一个能核对的结果：可以是一个数落在哪段区间，也可以是一件事到了哪一步。格和格不重叠、不留空，到期时正好一格成立：涨 50% 及以上、涨 10% 及以上不到 50%、涨跌都不到 10%、降 10% 及以上不到 80%、降 80% 及以上，每个边界只属于一格，到期拿到实际数，一定落进其中一格；写成“涨很多、涨一点”就对不出来。没有含糊的“部分”：部分做到的，写清楚是什么，单独成一格（“发许可，但附条件”）。中性跟什么比，写在那一格的条件里。',
    '一把梯子只放一种东西，一个观点只看一件东西：既要数字又要事件的，拆成两条，用依赖连起来；两部分可能往相反方向走的（H20 这一档和 Blackwell 这一档），也是两条观点。',
    '梯子由模型在建观点时定，定了到期以前不改；后来并进来的候选观点，梯子和到期日都用已有的。',
    '数字的观点写明哪一年。今年就是这条信息进来那年，到 12 月 31 日；明年是下一年，到 12 月 31 日。公司的数按它的财年：信息进来时所在的那个财年是今年，下一个是明年。同一个数，今年、明年最多各开一条，超出的不开；到期日就是这个数公布的那天。',
    '到期日定在这个争论见分晓的那天，一般 6–12 个月；中间的季报是证据，不另开观点。',
  ];

  // The state on a ladder (D45: where it is now is a proposal, in VIEWS_PROPOSED).
  const POSITIONS = [
    { position: '状态', means: '这条观点处在梯子的哪一格：我们的判断，证据把它往梯子的一头或另一头推', moves: '模型判，温度调低，只按事实。每次从这条观点下没被替代的全部证据（每条带上它替掉的那条，看得到变化）、加上它依赖的观点现在的状态和理由重新判，不在上一次的基础上加减；写明依据哪几条证据。这一轮只多了重复的证据、依赖也没变，就不重判', example: '看到 8-K 以后：强烈看空' },
  ];

  // How a judgement shows its sources and how code checks them (D46).
  const STATE_RULES = [
    '每次判断都写明依据：模型按固定格式交回判断，其中一栏写它根据的是哪几条证据，写证据的编号，比如“依据：e12、e15”；因为它依赖的观点变了而重判的，也写那几条观点的编号，比如“依赖：#1”。',
    '代码查表核对：每条证据存进库时有一个编号；库里记着每个观点下有哪些证据、每条有没有被后来的说法换掉。代码拿依据里的编号去查：证据是不是这个观点下的、有没有被换掉；观点是不是它依赖的那几条。都对，这次判断写进去；有一个不对，这次判断不收，记下原因，让模型重判一次。只查有没有，不管判得对不对，就像查脚注里的页码书里有没有。',
    '想知道某天当时怎么判，就翻那天存下的判断记录，不重新问模型；再问一次，模型可能答得不一样。',
  ];

  const TIERS = [
    { tier: '发生的事', examples: '官方动作、公布的数、已经完成的交易', counts: '能定哪一格成立，也能推状态' },
    { tier: '当事人说的', examples: '公司指引、管理层表态、官员讲话', counts: '只能推状态' },
    { tier: '第三方看法', examples: '卖方、媒体分析、专家', counts: '只能推状态' },
    { tier: '传闻', examples: '“知情人士称”、没有出处的说法', counts: '只能推状态' },
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
          { answer: 'A 开着', label: '读 A 的状态和理由', act: true },
          { answer: 'A 出了答案', label: '读 A 的答案', note: '答案本来就是 B 要的输入，不算断', act: true },
          { answer: 'A 还没建', label: '箭头先等着', note: 'A 建出来时连上，B 重判一次' },
        ],
      },
      {
        answer: '事件的观点', label: '顺着接续往下走', note: '例：NVDA FY27 全年中国区收入 → 这一档芯片对华出口许可',
        children: [
          { answer: 'A 开着', label: '读 A 的状态和理由', act: true },
          { answer: 'A 关了，有接续的', label: '读接续的那条', note: '记一笔', act: true },
          { answer: 'A 关了，没有接续', label: '读 A 的答案，标“只是历史”' },
        ],
      },
    ],
  };

  const DEPENDENCY_RULES = [
    '主题观点不说好坏，好坏由每个依赖它的对象观点自己的箭头说：降息那头对以太坊是看多，对 JPM 是看空。',
    '箭头只有一个方向。看起来要“先好后坏”，说明中间还有一条观点没写出来，要拆出来：钢铁关税抬高国内钢价是一条路，拖垮下游用钢需求是另一条路。',
    '观点和观点之间只有一种关联：依赖。B 依赖 A，就是 B 判断时要看 A 的结论。B 判断时看两样，分开放：直接讲 B 的证据；它依赖的观点现在的状态和理由。A 的结论对 B 起的作用像证据，但不当证据存：证据是外面发生的事、别人说的话，A 的结论是我们自己的判断，当成证据，系统会自己说服自己。',
    '一句话只算一次：讲 A 的话只算 A 的证据（同一条信息里新提的两条候选观点也一样，一句话只连到它直接讲的那条），B 通过 A 的结论知道这件事；直接讲 B 的，才算 B 的证据；B 不依赖 A 的，讲 A 的话也直接算 B 的证据。依赖谁只在建 B 的时候定，所以不会出现先算给 B、后来又通过 A 再算一次。',
    '什么时候通知 B：A 的状态换了格，或者 B 等着的 A 刚建出来、箭头连上了。别的时候不通知。',
    '连不连依赖，由模型判，像分析师一样：写出这条观点的结果要靠哪几条观点的结果，各往哪个方向推。已经发生的事是证据，不连：OPEC 看着今天的油价定产量，今天的油价是“OPEC 产量”这条观点的证据，不是依赖。',
    '防绕圈：每加一条箭头，或者一条箭头顺着接续换到下一期，代码先查会不会绕成圈（A 靠 B，B 又靠 A）；会的话这条不收，退回给模型改。看起来互相依赖的两个问题，是观点没起好。',
  ];

  // Succession: the same thing, period after period.
  const CHAIN_RULES = [
    '同一样东西的下一条观点接着上一条，连成一条链：美联储 2026 年末利率 → 2027 年末利率 → 2028 年末利率。链存的是血缘，箭头怎么读见上面。',
    '一条只能有一个下一期：FY26 后面只接一条 FY27，不能冒出两条。',
    '下一期的梯子方向不变：上一期第一格是“强烈看多”，下一期也是；每一格的门槛可以重新定。依赖它的观点认的是“哪一头对我是看多”，方向一反就乱了。',
  ];

  // Writing what extraction hands over, one item per round: candidate views first, then evidence.
  const INTAKE_STEPS = [
    { code: '1', name: '核对出处', who: '代码', does: '出处在处理记录里查不到的不要，记下原因' },
    { code: '2', name: '收证据', who: '代码', does: '重试不重复存；上游修正版只换它自己那一处出处：它只是转述的，不动原来那条证据；它本身是原始来源的，新版的句子照常对上，改了的就替代原句' },
    { code: '3', name: '搜索', who: '代码', does: '搜索引擎叠在观点库上（像 Elasticsearch，语义搜索或关键词，怎么搜还没定）。候选观点搜整个观点库，开着的、关掉的都搜，取前 N 条（N 写在 Config，先定 10）；证据只在它连到的那条观点下的证据里搜，取前 N 条；连在候选观点上的，等候选观点有了去向再搜。搜出来是空的，也照样交给第 4 步' },
    { code: '4', name: '对上', who: '模型', does: '模型不读原文，先判每个候选观点是清单里的哪一条（或者它的一部分）、接续哪一条，还是新观点（对不上，或者只是有点像，就开新的），太大太杂的、超出今年和明年的数字观点不开，写理由；每条证据和它那条观点下搜出来的证据比，是重复、替代还是新证据。这些在同一次调用里判完。候选观点并进了已有的那条，它带的证据接着在那条观点下搜，为它再叫一次模型比' },
    { code: '5', name: '核对', who: '代码', does: '编号必须在清单里，或者是那条观点下的证据' },
    { code: '6', name: '写进库', who: '代码', does: '各对象自己的队列写，先写主题，再写对象；重复只多一个出处；替代按说的时间排（这句话是哪天说的），后说的算数，先说的标“被替代”，晚到的旧说法不加进来，只在处理记录里写一笔；被替代的证据还连着别的观点，新的那条也连过去；原始来源自己的修正版里找不到、也没被新句替代的原句，算删了，标“被替代”；对上那一刻看到的变了，这部分重新对上' },
    { code: '7', name: '连依赖', who: '模型', does: '新观点挑它依赖哪几条，写明方向；代码先查会不会绕成圈，会就退回给模型改' },
    { code: '8', name: '重判一轮', who: '模型', does: '这一轮有新证据或替代、它依赖的观点换了格、或者它等着的观点刚建出来，重判：先判上游，再判下游，每条这一轮只判一次；只多了重复的不判；换了格的再往下通知' },
  ];

  // Two lanes, one shape: a candidate view and a piece of evidence are each compared with what is already there.
  const INTAKE_SHAPE = [
    { aspect: '去哪比', views: '搜索引擎从整个观点库搜出的前 N 条', evidence: '在它那条观点下的证据里搜出的前 N 条' },
    { aspect: '判什么', views: '是哪一条（或它的一部分）、接续、新观点，还是不开', evidence: '重复、替代、新证据' },
    { aspect: '链', views: '接续：美联储 2026 年末利率 → 2027 → 2028', evidence: '替代：AMZN 资本开支指引涨 12% → 25%' },
    { aspect: '什么算现在', views: '链上开着的那条（数字可以今年、明年各开一条）', evidence: '没被替代的那些（证据的替代也连成一条链）' },
    { aspect: '搜什么', views: '整个观点库，开着的、关掉的都搜', evidence: '只搜它那条观点下的，不搜全库' },
  ];

  // Step 4: where a candidate goes.
  const MATCH_OUTCOMES = [
    { outcome: '并进已有的', when: '候选观点看的就是那条观点看的东西，或者是它的一部分（“H20 在中国的收入”是“中国区收入”的一部分）', writes: '只连证据，证据再和那条观点下的证据比；梯子和到期日用已有的' },
    { outcome: '接续', when: '同一样东西的下一期：数字的下一年；事件的那条已经关了，要接着看', writes: '建新观点，记接续' },
    { outcome: '新观点', when: '对不上，或者只是有点像：Blackwell 这一档对华许可，不是 H20 这一档', writes: '建新观点，梯子和到期日从此定死' },
    { outcome: '不开', when: '太大太杂，一条里捆了几件可能往相反方向走的事：“美国对华芯片管制会怎样”；或者数字的观点超出了今年、明年', writes: '不建；它的证据如果也连在具体的那条上，照常算数；只连在它身上的不存' },
  ];

  const MATCH_NOTES = [
    '搜只用来找出前几条可能的，是不是同一条由模型判：“H20 对华许可”和“Blackwell 对华许可”很像，却是两条；看多和看空的两种说法，是同一条。',
    '关掉的观点也搜得到：FY26 那条关了，FY27 的候选观点进来照样搜到它，模型判成接续。',
  ];

  // Step 4: where a piece of evidence goes, against the evidence its view already holds.
  const EVIDENCE_OUTCOMES = [
    { outcome: '重复', when: '说的就是那条观点下已有的一条：别人转述；正文和表格里的同一个数；同一个人把同样的话再说一遍', writes: '那一条多记一个出处；证据不多一条，不重判' },
    { outcome: '替代', when: '和已有的一条是同一件事的前后两个说法：同一个人后来改了说法或数（指引、预测、状态）；官方证实或否认了一条传闻；原始来源自己出了修正版，改了原句', writes: '按说的时间排（这句话是哪天说的），后说的算数，先说的标“被替代”，留在历史里，重判；晚到的旧说法（同一件事已经有更新的）不加进来，只在处理记录里写一笔，不重判' },
    { outcome: '新证据', when: '别的都是：新的事、另一期的数、另一个人的说法（说法相反的也是）；拿不准也算新证据', writes: '加进来，和别的一起算数；重判' },
  ];

  const EVIDENCE_NOTES = [
    '证据只和它那条观点下的证据比，不拿证据去搜全库：观点先定好（抽取时连上的，或者候选观点对上的那条），再在这条观点下没被替代的证据里搜前 N 条，交给模型比。和观点一个形状：候选观点比的是从整个观点库搜出来的，证据比的是从它那条观点下搜出来的。',
    '一条证据连几条观点，也只存一条：和这几条观点下的证据一起比一次。',
    '被替代的证据还连着别的观点，新的那条也连过去，那些观点也重判；不然那条观点手里只剩一个过时的说法。',
    '证据是一句话或一个数，替掉的只是那一句：卖方新报告改了收入预测，替掉的是它上一份里的那个预测，别的论据照样算数。',
    '对上不读原文，比的是证据里“一句话说清”的那句；拿不准算新证据，最坏也就是两条都算数，由重判自己看。',
  ];


  const INTAKE_EXAMPLE_TREE = {
    label: '三条信息，库从空的开始', note: '示意',
    children: [
      {
        answer: '2025-04-15 NVDA 的 8-K', label: '库是空的，交来两个候选观点', question: '对上：清单是空的，都开新观点',
        children: [
          { answer: '#1 主题观点', label: '这一档芯片对华出口许可（事件）', note: '证据：H20 出口中国要许可证（发生的事）', act: true },
          { answer: '#2 对象观点（NVDA）', label: 'FY26 全年中国区收入（数字）', note: '证据：预计最多约 55 亿美元的费用（当事人说的）；依赖 #1，放松那头看多', act: true },
        ],
      },
      {
        answer: '2025-04-16 AMD 的 8-K', label: '讲的是 AMD，AMD 还没有观点，交来两个候选观点', question: '对上',
        children: [
          { answer: '候选观点“MI308 对华许可”', label: '并进 #1', note: '搜到 #1，模型判是同一件事（同一条规定管的同一档芯片）；它的证据再和 #1 下的证据比：AMD 说的是 MI308，是新证据；#1 重判，没换格，不通知 #2', act: true },
          { answer: '候选观点“AMD 2025 全年中国区收入”', label: '新观点 #3', note: 'AMD 还没有开着的观点；证据：预计最多约 8 亿美元的费用（当事人说的）', act: true },
        ],
      },
      {
        answer: '2025-04-16 路透的报道，转述 NVDA 的 8-K', label: '已有的观点：#2 和它依赖的 #1', question: '对上',
        children: [
          { answer: '证据连到 #1 和 #2', label: '都是重复', note: '原始来源同是 NVDA 的 8-K，说的就是 #1、#2 下已有的那两条：各多记一个出处；#1、#2 都不重判', act: true },
        ],
      },
    ],
  };

  // One view's evidence over half a year: how repeats and replacements keep it current (numbers illustrative).
  const EVIDENCE_EXAMPLE = [
    { item: '2-05 电话会：资本开支指引涨 12%', matched: '新证据（这条观点下还没有证据）', store: '加 g1', rejudge: '判' },
    { item: '2-06 路透的报道，转述指引', matched: '重复 g1', store: 'g1 多一个出处', rejudge: '不判' },
    { item: '3-10 MS：预计涨 18%', matched: '新证据（另一个人说的）', store: '加 m1', rejudge: '判' },
    { item: '4-30 电话会：指引改成涨 25%', matched: '替代 g1', store: 'g2 算数，g1 被替代', rejudge: '判，读到“12% → 25%”' },
    { item: '5-02 MS：改成涨 27%', matched: '替代 m1', store: 'm2 算数，m1 被替代', rejudge: '判' },
    { item: '5-20 一份 2 月的 MS 报告晚到', matched: '晚到的旧说法：MS 后来已经改过两次（3 月 m1、5 月 m2）', store: '不加进来，处理记录里写一笔“过时，没用”；m2 照旧算数', rejudge: '不判' },
    { item: '6-10 会上重申“还是 25% 左右”', matched: '重复 g2', store: 'g2 多一个出处（最近一次 6-10）', rejudge: '不判' },
  ];

  const EVIDENCE_EXAMPLE_NOTE = '半年后这条观点下可能有几十条证据，重判读的只是没被替代的那几条：公司指引涨 25%（2 月是 12%），MS 预计涨 27%（3 月是 18%），加上别的人、别的事。';

  // The judge of step 4, its records, and the labels that will train a faster model.
  const JUDGE_STEPS = [
    { code: '1', name: '大模型对上', who: '模型', does: '第一版用通用大模型做对上（Config 里的“对上”设置），先让系统跑起来' },
    { code: '2', name: '每次都记', who: '代码', does: '每次对上留一条对上记录：给模型看了什么、它答了什么、最后写进库的是什么' },
    { code: '3', name: '人来标', who: '人', does: '挑两种给人标：被代码退回的（模型写的依据不对），和隔一段时间随机抽的几条；人标出正确的结果' },
    { code: '4', name: '训练小模型', who: '代码', does: '用人标的结果，训练一个更快的小模型' },
    { code: '5', name: '小模型接手', who: '代码', does: '以后由小模型做对上；什么时候接手还没定' },
  ];

  const TRACE_FIELDS = [
    { part: '哪条信息', meaning: '上游编号和版本、顺序号' },
    { part: '交来的', meaning: '抽取交来的候选观点和证据，原样' },
    { part: '给模型看的', meaning: '候选观点比的是搜出来的前 N 条（带名次）；证据比的是它那条观点下搜出来的前 N 条' },
    { part: '谁定的', meaning: '大模型、以后的小模型，或人' },
    { part: '请求和返回', meaning: '实际发出的请求、原始返回、Config 版本（模型、提示词版本、温度）' },
    { part: '决定', meaning: '每个候选观点的去向和理由；每条证据是重复、替代还是新证据；代码核对的结果和拒绝的原因' },
    { part: '写进库的', meaning: '最后写进库的结果' },
  ];


  // How a view ends.
  const LIFECYCLE_TREE = {
    label: '一条观点', question: '到哪一步了？',
    children: [
      { answer: '开着', label: '证据变了、或者依赖换了格，就重判一次', note: '同一样东西同时只开一条；数字的同一个数，今年、明年各一条' },
      { answer: '到期，出了答案', label: '关掉', note: '答案怎么定，等最终判定按新设计重做时定；要接着看，就开一条新观点接续它', act: true },
      { answer: '对象被移出名单', label: '留着，标“不再跟踪”', note: '到期不判，D31' },
    ],
  };

  const LIFECYCLE_NOTES = [
    '到期由 Pull 模式发起（D14）；事件观点的答案由谁来定、要不要先经最终判定，等最终判定按新设计重做时定。',
  ];

  const VIEW_FIELDS = [
    { part: '对象', meaning: '名单里的哪个对象', example: 'NVDA' },
    { part: '种类', meaning: '对象观点或主题观点', example: '对象观点' },
    { part: '看的是什么', meaning: '数字：哪个数、哪一年；事件：哪件事', example: 'FY27 全年中国区收入' },
    { part: '问题', meaning: '一句话，写下不改', example: 'NVDA FY27 全年中国区收入，比 FY26 会怎样？' },
    { part: '梯子', meaning: '五格（只有是或否的问题两格），每格一个能核对的结果，写下不改', example: '涨 50% 及以上……降 80% 及以上' },
    { part: '到期日', meaning: '争论见分晓的那天；数字就是它公布的那天', example: 'FY27 年报的财报日' },
    { part: '状态', meaning: '每次重判记一版，写明依据', example: '强烈看空' },
    { part: '依赖', meaning: '指向哪几条观点，各带一个方向', example: '→ 这一档芯片对华出口许可：放松那头看多' },
    { part: '接续', meaning: '接着哪一条；可以没有', example: '接着 FY26 那条' },
    { part: '从哪来', meaning: '从哪条信息建的', example: '2025-04-15 NVDA 的 8-K' },
    { part: '开着还是关了', meaning: '开着，或者到期出了答案关掉；对象移出名单的，标“不再跟踪”', example: '开着' },
  ];

  const EVIDENCE_FIELDS = [
    { part: '原文', meaning: '信息里的那一句，或表里的那一格' },
    { part: '一句话说清', meaning: '离开原文也看得懂的一句：谁、做了什么、多少、哪一期；对上和重判读这一句' },
    { part: '出处', meaning: '上游编号和版本、类别、发布日、在信息里的位置；重复的（别人转述、同一条信息的正文和表格、同一个人再说一遍）记成这条证据的又一个出处' },
    { part: '谁说的', meaning: '说这句话的人或机构' },
    { part: '原始来源', meaning: '转述的，指向最初说这句话的人和那一次（哪天）；按它数独立来源，替代也按这一天排先后' },
    { part: '哪一层', meaning: '发生的事、当事人说的、第三方看法、传闻' },
    { part: '事情发生的时间', meaning: '事情什么时候发生或生效；数字写它属于哪一期' },
    { part: '被替代', meaning: '指向替代它的那一条：同一个人后来改了说法或数、官方证实或否认了这条传闻；或者原始来源自己出了修正版，把这句改了、删了（删了的没有后继）；被替代的不再算数，留在历史里' },
  ];

  const ORDER_RULES = [
    '只有信息能产生证据；观点之间只传通知，不传证据，所以观点不会自己证明自己。',
    '每条观点只有一个写入者：主题观点由主题的队列写，对象观点由对象的队列写；同一条信息先写主题，再写对象。',
    '先后按顺序号排，不用电脑时钟。一条信息只读顺序号比它小的信息留下的状态，加上这一轮里它自己已经写下的；结果要和一条一条按顺序处理完全一样；并行时读到的东西在提交前变了，就重新做一次（D31）。',
    '一条信息引起的变化算一轮：先做完连证据、建观点、接续和连依赖，再按依赖先后重判。上游判完才判下游，下游读的是上游这一轮刚判完的状态；每条观点这一轮只判一次。全局的观点（比如美联储）连着很多观点，它先变，跟着它的再各判一次。',
    '只追加：观点的问题、梯子和到期日写下就不动；对上、重判、接续、关掉、标注都是新加的记录，带顺序号。',
    '时间线只往后加，不回头改：观点的每一次变化，按我们什么时候知道的往后记。晚到的信息，同一件事已经有更新的说法，它就不算数，不加进观点，只在处理记录里写一笔“过时，没用”；讲的是我们不知道的事，照常算，记上它真实的日期。分这两种由模型比证据时一起判，不另加规矩。',
    '同一条信息的修正版只换它自己那一处出处：它只是转述的，不动原来那条证据；它本身是原始来源的，改了的原句由新句替代，删了的标“被替代”。连着变了的证据的观点各重判一次；过去的重判记录不改。',
    '失败：每条信息记下做到哪一步，从失败的那一步重试，重试只替换自己上次的结果；多次失败的放进人工复核池。',
    '两头都能查：从一条观点查到推过它的全部信息；从一条信息查到它建过的观点，和它作为出处的全部证据（重复的也查得到）。',
  ];

  const STORE_NOTE = '存在哪、用什么数据库，建的时候定。';

  const VIEWS_OPEN = [
    '搜索怎么搜：用语义搜索、关键词还是两样一起，怎么排先后；建的时候在存下的信息上试过再定。前几条先定 10，试的时候再调。',
    '共识：市场押在哪一格；对股价的看法就是我们的状态和共识的差距。共识怎么记还没定（D30 原来定的是由代码按每个独立第三方来源最新的立场算）。',
    '观点的颗粒度还没定，要专门定：一部分就并进大的那条，太大太杂的不开，可到底多大算一条，现在说不清。要紧的那一块要单独成一条（NV 中国区收入很关键，不能并进总收入）；太粗的话，观点会全变成财务指标，这不行。要让模型清楚知道这种抽法和颗粒度是错的。先做一次完整的调研：从对冲基金的角度看，一条观点到底长什么样，什么该合、什么该拆。',
    '什么样的问题算关键问题，每个对象几条（现实里每家公司只盯 2–3 个）；去重管不住“问太多不同的小问题”。',
    '事件的“同一件事”边界：什么算接续、什么算新的，要拿真实案例定。',
    '事件观点到期以前的中间日期（规定的生效日、征求意见截止日）放在哪。',
    '利率、汇率、指数的期货能交易，但名单把它们放在主题下（D11），它们价格的看多看空没有地方放。',
    '标注的细节以后再补：谁来标、标多少、用什么界面；怎么考小模型准不准、训练怎么用标好的数据；小模型什么时候接手。',
    '建之前要在存下的信息上量：每个对象开着几条观点；“新观点”判得准不准；清单顺序打乱后判断变不变；“替代”和“新证据”分得准不准；热点观点半年积累多少条没被替代的证据；没被点名的对象漏掉多少证据。',
    '到期时谁定事件观点的答案、要不要先经最终判定：最终判定和 Pull 模式按新设计重做时定。',
    '开题：系统一上线，每个对象都是空的，观点只能由先到的信息一条条建，留下的是先到的话题，梯子也照第一份材料切。要不要单独一步：开始覆盖一个对象时，先读一批材料，定下两三个关键争论。',
    '格内的大变化不通知下游：只在换格时通知，AMZN 资本开支指引从涨 12% 改成 25%，都在同一格里，依赖它的 NVDA 那条观点听不到。',
  ];

  // Claude's proposals that Alex has not decided (D45). None of them is built until he decides it.
  const VIEWS_PROPOSED = [
    'Pull 模式的事，设计 Pull 模式时再谈：结束的另外两种，答不出（不再披露这个数、事情本身没了，不算准不准；依赖它的观点标“缺这个输入”）和等答案（数字的观点期末已过、答案还没公布）。',
    'Pull 模式的事，设计 Pull 模式时再谈：每天查重，Pull 模式每天发起，同一对象开着的观点两两比；后建的并入先建的，连线和箭头搬过去，查环，重判；Config 里多一套“查重”的设置。',
    'Pull 模式的事，设计 Pull 模式时再谈：到期怎么定答案，用第一次公布的值，后来的修订不改；拿来打分的，是带来答案的那条信息进来之前的最后状态；等发布日不晚于到期日的信息都处理完再定。',
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
          <p class="drill__intro">抽取只做一件事：每条信息整份交给模型，用资深对冲基金分析师的视角、按这一类的提示词，对着这些对象已有的观点读完，交出两样东西。一是证据：支持或削弱已有观点的话和数，连到那条观点上。二是候选观点：已有观点管不到、又要紧的事，带着提出它的证据。每条带出处，交给观点库；怎么和库里已有的比、写进去，是观点库的事。</p>
          <p class="drill__status"><span class="pill pill--strong">第一版已冻结 · 2026-10-18</span>定下：整份交给模型；每一类一份提示词，拼法相同；观点是模型的判断，证据是客观的；每条都带出处；抽取只读。2026-10-20 按 D41、D42、D45–D47 改了交给观点库的东西：证据连到已有观点上，和候选观点分开交；候选观点当场写全。没定：每一类提示词的具体写法，建的时候试过再定。</p>
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
          <p class="drill__intro">系统做的事，就是建立、更新和关掉这里的观点。一条观点是一个问题、一把梯子和一个到期日：证据把我们的判断往两头推，到期拿答案对一下，就知道判得准不准。抽取交来两样东西，在这里各走一条线、走法一样：候选观点和搜出来的几条已有观点比，由模型判是哪一条、接续，还是开新的；证据和它那条观点下已有的证据比，是重复、替代还是新证据；只是重复的，不重判。每条证据都带出处，所有记录只追加。</p>
          <p class="drill__status"><span class="pill pill--strong">第一版已冻结 · 2026-10-20</span>只写 Alex 说过或定过的（D45、D46）；要改，先记一条新决定（D48）。还没定的、和 3 条 Pull 模式的事，单列在最后。</p>
          <h3 class="drill__heading drill__heading--spaced">结构</h3>
          ${tree(VIEW_TREE, escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">两种观点：结构一样，梯子的格意思不一样</h3>
          ${table(['种类', '属于什么', '梯子的格', '例子'], VIEW_KINDS.map((row) => [row.kind, row.on, row.rungs, row.example]), escapeHtml)}
          <p class="drill__footnote">${escapeHtml(KIND_NOTE)}</p>
          <h3 class="drill__heading drill__heading--spaced">梯子：五格（只有是或否的问题两格），每格是一个能核对的结果</h3>
          ${tree(LADDER_EXAMPLES, escapeHtml)}
          <ol class="drill__rules">${listItems(LADDER_RULES, escapeHtml)}</ol>
          <h3 class="drill__heading drill__heading--spaced">状态：这条观点处在梯子的哪一格</h3>
          ${table(['', '是什么', '谁来判', '例子'], POSITIONS.map((row) => [row.position, row.means, row.moves, row.example]), escapeHtml)}
          <ul class="drill__rules">${listItems(STATE_RULES, escapeHtml)}</ul>
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
          <h3 class="drill__heading drill__heading--spaced">例子：三条信息怎么写进库</h3>
          ${tree(INTAKE_EXAMPLE_TREE, escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">例子：一条观点下的证据怎么跟着更新（AMZN 2026 全年资本开支，示意）</h3>
          ${table(['信息', '对上证据', '库里', '重判'], EVIDENCE_EXAMPLE.map((row) => [row.item, row.matched, row.store, row.rejudge]), escapeHtml)}
          <p class="drill__footnote">${escapeHtml(EVIDENCE_EXAMPLE_NOTE)}</p>
          <h3 class="drill__heading drill__heading--spaced">对上的裁判和标注：先用大模型跑起来，攒下标注，以后交给小模型</h3>
          <p class="flow-legend">黑框是模型做的，灰框是代码或人做的。</p>
          ${flow(stepCards(JUDGE_STEPS), '→', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">一条对上记录记什么</h3>
          ${table(['部分', '记什么'], TRACE_FIELDS.map((row) => [row.part, row.meaning]), escapeHtml)}
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
          <h3 class="drill__heading drill__heading--spaced">Claude 提的、Alex 还没定的（定了才算数）</h3>
          <ol class="drill__rules">${listItems(VIEWS_PROPOSED, escapeHtml)}</ol>
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
