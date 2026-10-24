// The New design's extraction module, the views database and the final verdict (decisions D26-D45). Extraction reads
// every item whole, by its category, as a senior hedge fund analyst, with the open views of the item's objects and the
// views they depend on (prompt part 5), and hands over two things with their sources: evidence attached to one of those
// views or to a candidate view, and candidate views with extraction-owned subject memberships (D149). A view is a question with a
// ladder and a due date; the model matches each candidate to views found by search (the same view, its next period, or
// a new view) and each piece of evidence to the evidence its view already holds (repeat, replacement, or new evidence);
// evidence pushes the view's state, which is frozen at the due date (D54), and views are linked by dependencies and
// chained by succession. Only what Alex said or decided is written as decided (D45); Claude's proposals he has not
// decided are kept apart in VIEWS_PROPOSED. The final verdict is still the old draft and is to be redone with pull mode
// (D41, D54). Edit the data at the top; the three drill-downs render it. The texts are for a reader who did not follow
// the discussion: plain words and an example, no field names.
(function () {
  'use strict';

  // ------------------------------------------------------------------ extraction

  // The template prompt of the read step: the same parts for every category, in this order.
  const TEMPLATE = [
    { part: '角色', content: '你是一位资深对冲基金分析师。读这条信息，是为了检验和形成观点：把支持或削弱已有观点的话和数挑出来，作为证据连到那条观点上；已有观点管不到、又要紧的事，写成候选观点，当场写全：问题、梯子、到期日和研究归属，带上提出它的证据。你自己的备忘录里的判断，都交成候选观点，可以不带证据，不当作证据。写观点的规矩：一个观点只看一件东西；梯子五格（只有是或否的问题两格），每格是一个能核对的结果，格和格不重叠、不留空，没有含糊的“部分”；到期日定在争论见分晓的那天，数字的观点就是这个数公布的那天；数字写明哪一年：今年、明年按这条信息的发布日算，公司的数按它的财年。', source: '所有类别一样；写观点的规矩原样取自观点库' },
    { part: '这一类是什么、怎么读', content: '这一类的定义和读法，比如“看法和估计都算作者说的，不当成已经发生的事”。', source: '取自分类规则，这里不另写' },
    { part: '讲的是谁', content: '这条信息的相关对象；另附研究对象名单里的全部主题，候选观点讲的是主题时，名单里有的从里面挑，没有的写清是什么事。', source: '这条信息的标签；主题取自研究对象名单' },
    { part: '这一类要读出什么', content: '见下面的表，每类一行。', source: '抽取模块' },
    { part: '已有观点与研究主线', content: '这条信息相关对象开着的观点，加上它们依赖的观点，写明谁依赖谁；只给问题、看的是什么和到期日，不给状态和证据；同一块另附可用的研究主线，内容按观点库的归组规矩提供。', source: '观点库' },
  ];

  // D149 requires extraction-owned membership; D147/D148 remain isolated implementations and measurements.
  const EXTRACT_RELATIONS = [
    "D149 已定要求：读全文时就决定候选观点属于哪个持续业务过程，称为研究主线。例如 Rubin 出货和 SK 工厂上线各有自己的问题，同时属于 Rubin 推出这条主线。归组随抽取完成，不留给前端或事后全库聚类。",
    "证据和候选观点仍分开交；每个候选观点同时带结构化归属，需要新主线时附上名称和范围。只在解释里提到相关、没有可保存的引用，不算交完。抽取只读不落库，完整交接和保存规矩由观点库的“研究主线：抽取时归组”一节规定。",
    "这是目标要求，不是已上线的能力。正式管线还没有归组交接，D147 原型及 D148、D150 一致性结果见 docs/poc/pipeline-plan.md 的“抽取时归组：目标与当前实现”。"
];

  const GROUP_RELATIONS = [
    "D149 已定要求：把观点按所谈的持续业务过程组织成研究主线。例如 Vera Rubin 从产品准备到客户落地；出货时间、SK 工厂上线、OpenAI 部署仍各有问题、梯子和到期日。主线可从一条观点开始，一个观点可属于多条主线。它没有状态或梯子，不自动产生依赖，也不等于给 agent 的上层投资论点。",
    "归属按业务过程判断，可以跨公司、跨行业，不按同一家公司判断。明确使用 Rubin 的客户部署可以跨公司归在 Rubin 下；NVIDIA 的 PC 芯片不能仅因同公司归入 Rubin，OpenAI 部署不能因同属 Rubin 就归入 SK 专属主线。研究主线也不代替研究对象名单里的主题。",
    "读全文前，代码给抽取提供可用的已有主线名称、范围和编号；搜索范围不按公司隔开。抽取在这次读全文的调用里决定归属：引用展示过的主线，或声明有名称和范围的新主线。每个候选观点必须有非空、不重复的归属引用，不能指向未展示、未声明的主线；代码检查完整引用，不合格的交接不进入写入。没有合适的旧主线就声明新的，不硬塞进近似的。",
    "比对仍只判断观点和证据身份、依赖，不读归属字段来重判分组。候选观点新建、接续或归入已有观点后，写入器把候选观点编号解析为最终观点编号，把新主线编号解析为库内编号，再保存成员关系；未通过原出处检查或最终不开的候选观点不成为成员。未使用的新主线声明不建空主线，也不因此拒绝其他有效归属。",
    "同一主线的同一成员只存一次；归属带输入编号和顺序号，遵守本库的先后与历史读取规则。主线和成员在观点、证据写入那一步一起提交，失败一起回滚，处理记录不能把半次写入记成完成。重送不重复增加成员，继续用原分发和恢复流程。",
    "主线不复制证据。详情沿成员观点的真实证据连线读来源，按所看顺序号过滤，并排除当时已被替代的证据；没有连线就返回空证据。新成员或原观点写入的变化标记使主线更新；重复原话只多出处不触发。只有证据、没有新候选观点的文章沿既有成员关系更新，不重新造观点或主线。",
    "验收看原文支持的成员关系和证据能否保留，不要求名称、编号、组数每次完全一样。分别报告没抽出、检查拒绝、漏归和错归，不能混成一个一致性数字。Rubin 出货与客户部署的核心联系要保留，无关产品和其他客户专属主线的错归也要检查；多公司、大库尚未验证。",
    "实现参考仍是隔离实验：D147 用 existing_subjects 给出已有主线，threads 声明 id、name、scope，candidates[].thread_ids 写引用；新编号用 t 加正整数，库内编号用 g 加正整数。搜索暂用标题和全文词在全局名称、范围索引取前 N 条，N 来自原配置。这些是原型的字段和搜索做法，不是已接入正式管线的能力，也不证明大库召回。",
    "当前差距见 docs/poc/pipeline-plan.md 的“抽取时归组：目标与当前实现”。D148 补已有成员上下文的变体未采用；D150 每条归属先写短依据也未解决错归和漏抽，未采用。历次原答与结果保留，上层投资论点生成、MCP 展示及旧数据回填不在本次实现范围。"
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
    T8: { read: '作者的看法、论据、预测、评级和目标价，以及它们的变化', tier: '第三方看法' },
    T9: { read: '说话人讲的经营情况（订单、价格、份额、库存）；他凭什么知道', tier: '第三方看法' },
    T10: { read: '决定或行动本身、什么时候生效、影响谁；后面的程序（上诉、截止日），可以用作到期日', tier: '发生的事' },
    T11: { read: '公布的数字和政策决定，和上一次比差多少；官方措辞的变化', tier: '数和决定是发生的事；措辞是当事人说的' },
    T12: { read: '价格和成交的变化', tier: '发生的事' },
    T13: { read: '谁在买、谁在卖、规模多大', tier: '发生的事' },
    T14: { read: '排定的日期，用作到期日', tier: '发生的事' },
    T15: { read: '测到的经营数据，作为量化证据', tier: '发生的事（注明是第三方测的）' },
    T16: { read: '研究对象默认不看', tier: '—' },
  };

  const CATEGORY_NOTE = '每份文件都整份交给模型，里面的表格一起读；表格数据一次发布算一条，也整批交给模型。申报里的 XBRL 数字不另外推，文件本身已经有这些数。到期时要不要另外去查准确的数，等以后设计 Pull 模式时定。';

  // Every category has its own prompt: the same template with that category's parts. One assembled example.
  const PROMPT_EXAMPLE = {
    label: 'T7 新闻的提示词', note: '同一个提示词模板，第 2、4 块换成新闻这一类的',
    children: [
      { answer: '1 角色', label: '资深对冲基金分析师', note: '读这条信息，是为了检验和形成观点：证据连到已有观点上；已有观点管不到的要紧事，写成候选观点，当场写全问题、梯子、到期日和研究归属' },
      { answer: '2 这一类怎么读', label: '媒体的报道', note: '取自分类规则：媒体发的内容里，评论和分析归 T8，登记过的发布系列按系列归类，其余归这一类' },
      { answer: '3 讲的是谁', label: '这篇报道的相关对象', note: '由代码填，比如 NVDA、AMD；另附名单里的全部主题' },
      { answer: '4 要读出什么', label: '发生了什么事、什么时候、涉及谁；说法从哪来，原始来源是谁', note: '官方确认的算发生的事；“知情人士称”算传闻' },
      { answer: '5 已有观点与研究主线', label: '这篇报道相关对象开着的观点，加上它们依赖的观点', note: '由代码填，写明谁依赖谁，只给问题、看的是什么和到期日；比如“NVDA FY27 全年中国区收入，比 FY26 会怎样？”，和它依赖的“这一档芯片对华出口许可”；另附可用的研究主线' },
    ],
  };

  const PROMPT_NOTES = [
    '每一类都有自己的提示词：同一个提示词模板，第 2 块（这一类怎么读）和第 4 块（要读出什么）换成这一类的；第 1 块所有类别一样；第 3、5 块由代码按这条信息填进去。',
    '研究对象会看的 15 类（T1–T15）各一份；T16 研究对象默认不看，用到时再写。',
    '候选观点讲的是谁：主题从第 3 块附的主题里挑，名单里没有的写清是什么事；公司、加密货币、商品写代码（股票代码、加密货币代码、商品代码）或名字，由代码去参照数据里查，名字只认登记过的，和分类查公司名一样。',
    '你自己的备忘录（作者是你的 T8）：里面的判断读成候选观点，不当作证据；这样的候选观点可以不带证据，开成观点以后，第一次连上证据以前，状态写“还没判”。',
    '输出的格式（证据、候选观点及其归属、必要的新主线定义、出处各有哪几栏）由代码规定和检查，不写进提示词。',
    '每一类提示词的具体写法，建的时候在存下的信息上试过再定；每一版记在 Config 里，改一次就是一个新版本。',
  ];

  // Extraction, step by step: it only reads; matching and writing happen in the views database.
  const EXTRACT_STEPS = [
    { code: '1', name: '拼提示词', who: '代码', does: '按这条信息的类别，用同一个提示词模板拼出这一类的提示词；第 5 块由观点库给：相关对象开着的观点、它们依赖的观点，以及归组所需的已有主线' },
    { code: '2', name: '读', who: '模型', does: '整份读完，交出两样：证据，连到第 5 块里的观点上，或连到这次的候选观点上；候选观点，第 5 块里没有一条观点管、又要紧的事，带上提出它的证据；你自己的备忘录照提示词说明处理。每个候选观点同时确定研究归属，按观点库的归组规矩交出引用；每条带出处' },
    { code: '3', name: '核对出处与归属引用', who: '代码', does: '引用的原文（那一句，或表里那个单元格）在不在这条信息里、数字在不在引用的地方；证据连的必须是第 5 块里的观点或这次的候选观点；出处对不上的不要，记下原因；归属引用按观点库的完整交接规矩检查' },
    { code: '4', name: '交给观点库', who: '代码', does: '证据、候选观点连同归属和必要的新主线定义，带着顺序号一起交给观点库；比对定观点身份，写入保留归属' },
  ];

  // The two things one read hands over, side by side.
  const EXTRACT_TWO = [
    { aspect: '是什么', evidence: '信息里的一句话或一个数：谁说了什么、发生了什么', candidate: '一个要盯的问题，当场写全：讲的是谁、问题、梯子、到期日和研究归属' },
    { aspect: '多不多', evidence: '几乎每条信息都有', candidate: '少：第 5 块里没有一条观点管、又要紧的事；你自己的备忘录里的判断都算' },
    { aspect: '连到哪', evidence: '第 5 块里的观点（可以连几条），或者这次的候选观点', candidate: '带着提出它的证据（你自己的备忘录读出的可以没有）' },
    { aspect: '到了观点库', evidence: '和它那条观点下已有的证据比：重复、替代还是新证据', candidate: '先定是哪一条（或它的一部分）、接续、新观点，还是不开；归属随最终观点保存，不再由比对重判' },
    { aspect: '例子', evidence: '8-K 里的“H20 出口中国要许可证”', candidate: '2025-04 那条规定管的这一档芯片对华出口许可，到 2026-04-15 处在哪一格？' },
  ];

  // How the model sorts what it reads: against the open views in prompt part 5.
  const EXTRACT_SORT_TREE = {
    label: '读到一句话或一个数', question: '它和哪条观点有关？', note: '你自己的备忘录里的判断不走这棵树：都写成候选观点，可以不带证据',
    children: [
      { answer: '第 5 块里的观点', label: '证据：连到那条观点上', note: '连在它直接讲的那条上；另一条依赖那条的，不再连给它', act: true },
      { answer: '第 5 块里没有，但要紧', label: '候选观点：这句话是它的证据', note: '先在抽取时交研究归属；是已有的哪一条，还是新观点，由观点库比对时定；一条观点只管到它的到期日，到期以后才发生的事也算这里', act: true },
      { answer: '都没关系', label: '不抽', note: '背景、套话' },
    ],
  };

  // What one source records; every view, piece of evidence and change carries one.
  const SOURCE_TREE = {
    label: '一条出处',
    children: [
      { answer: '哪条信息', label: '上游编号', note: '每个版本有自己的编号；凭它去团队的库里取原文' },
      { answer: '哪一类、哪天', label: '类别、发布日' },
      { answer: '哪一处', label: '第几节第几段、表里哪个单元格', note: '表格数据写数据集和记录编号' },
      { answer: '哪一句', label: '原文那一句，或表里那个单元格', note: '代码核对它真的在这条信息里，数字真的印在引用的地方', act: true },
    ],
  };

  const SOURCE_NOTES = [
    '每条观点、每条证据、每一次由信息引起的变化都带出处；状态的每次变化写明依据哪几条证据（因为依赖的观点变了而重判的，也写那几条观点）。',
    '抽取核对三件事：引用的原文（那一句，或表里那个单元格）在这条信息里；数字在引用的地方；证据连的是第 5 块里的观点，或者这次的候选观点。有一件不对，就不交出去。观点库核对：出处在处理记录里查不到的，不写进库。都记下原因。',
    '两头都能查：从一条观点查到它的全部来源信息，从一条信息查到它产生和改动过的全部观点和证据。',
    '整份信息不存，要看原文就凭上游编号去团队的库里取；原文里只存观点或证据的出处引用的那一句，或表里那个单元格。',
    '同一条信息里说同一件事的几处（正文和表格里的同一个数），交成一条证据，带几个出处。',
  ];

  const EXTRACT_EXAMPLE_TREE = {
    label: '两条信息读出什么', note: '示意',
    children: [
      {
        answer: '2025-04-15 NVDA 的 8-K', label: '库是空的，第 5 块里没有观点', question: '读出两条候选观点',
        note: 'T6 公司其他发布：H20 出口中国要许可证，预计最多约 55 亿美元的费用',
        children: [
          { answer: '候选观点（主题观点）', label: '2025-04 那条规定管的这一档芯片（H20、MI308 等）对华出口许可，到 2026-04-15 处在哪一格？', note: '事件观点。五格：全面禁止；要许可，一个都不发；要许可，发了，但有附条件的；要许可，发了，都不附条件；不再要许可。到期日：2026-04-15。证据原文：“…requires a license for export to China … of the Company’s H20 integrated circuits…”，意思是 NVDA 披露 H20 出口中国要许可证，算发生的事。到了观点库，开成 #1', act: true },
          { answer: '候选观点（对象观点 NVDA）', label: 'NVDA FY26 全年中国区收入，比 FY25 会怎样？', note: '数字观点。五格：涨 50% 及以上；涨 10% 及以上不到 50%；涨跌都不到 10%；降 10% 及以上不到 80%；降 80% 及以上。到期日：FY26 年报的财报日。证据原文：“…up to approximately $5.5 billion of charges…”，意思是公司预计最多约 55 亿美元的费用，算当事人说的。到了观点库，开成 #2，依赖 #1', act: true },
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

  const EXAMPLE_NOTE = '出处：每条证据都记上游编号、所在段落和原文那一句（英文原句，中文只是说明）；代码核对“$5.5 billion”确实在那一句里。第一条信息进来时库是空的，第 5 块里没有观点，读到的要紧事只能写成候选观点；第二条信息进来时，第 5 块里已经有出口许可那条，NVDA 的声明就直接连上去。到了观点库，候选观点去和搜出来的已有观点比，证据去和它那条观点下已有的证据比，见观点库。两条候选观点同时归在“这一档芯片的对华许可与中国业务”主线下；第二篇只有证据，沿已有成员关系更新。归属不代替 #2 依赖 #1 的判断。例子用 NVDA，美股、期货、加密货币都走同一套。';

  const EXTRACT_OPEN = [
    '每一类提示词的具体写法，建的时候在存下的信息上试过再定；每一版记在 Config 里。',
    '候选观点的颗粒度，也就是一条观点管多大的范围（见观点库还没定的）：要让模型知道，观点不能全是财务指标，也不能把几件事捆成一条，或者把一件事拆得太碎；等调研完再写进提示词。',
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
            answer: '观点', label: '一个问题 + 一把梯子 + 一个到期日', note: '写下不改；梯子五格，只有是或否的问题两格；比对开观点时，同一个对象、看同一样东西，同一时间只开一条',
            children: [
              { answer: '状态', label: '这条观点处在梯子的哪一格', note: '证据把它往梯子的一头或另一头推，模型按事实判；你自己的备忘录开的观点，第一次连上证据以前是“还没判”', act: true },
              { answer: '连线', label: '证据', note: '证据只存一次，带出处和层；往哪边推记在连线上；被替代的证据留在历史里，不再算数', act: true },
              { answer: '依赖', label: '别的观点', note: '箭头带一个方向：对象观点写明对方的哪一头对它是看多，主题观点写明两把梯子同向还是反向', act: true },
              { answer: '接续', label: '上一期的观点', note: '同一样东西一期接一期，连成一条链', act: true },
            ],
          },
        ],
      },
      { answer: '研究主线', label: '按持续业务过程组织观点', note: '抽取时归组；完整规矩见“研究主线：抽取时归组”' },
      { answer: '只加不改的记录', label: '比对记录、重判记录、接续、关掉和重新打开的记录、标注', note: '每一步都新加一条，不改不删；想知道某天当时怎么判，就翻那天以前的记录' },
    ],
  };

  // The two kinds of view: the same structure, rungs that mean different things.
  const VIEW_KINDS = [
    { kind: '对象观点', on: '能交易的对象：公司、加密货币、商品', rungs: '五格：强烈看多、看多、中性、看空、强烈看空；只有是或否的问题两格：看多、看空。说的是对业务好还是坏，建的时候定，以后不变', example: 'NVDA FY27 全年中国区收入，比 FY26 会怎样？' },
    { kind: '主题观点', on: '主题：宏观、政策、行业', rungs: '从一头排到另一头的几种结果（五格；只有是或否的问题两格），用结果命名，不说好坏；对谁是好是坏，由依赖它的对象观点各自写明', example: '美联储 2026 年最后一次议息后的目标利率上限，比现在会怎样？（大幅降息……大幅加息）' },
  ];

  const KIND_NOTE = '同一件世界上的事，对不同的对象可能好坏相反：降息对以太坊是看多，对 JPM 的净利息收入是看空。所以主题观点不说好坏。';

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
          { answer: '强烈看空', label: '降 80% 及以上', note: '最多剩两成' },
        ],
      },
      {
        answer: '主题观点（事件）', label: '2025-04 那条规定管的这一档芯片（H20、MI308 等）对华出口许可，到 2026-04-15 处在哪一格',
        question: '五格：从一头排到另一头的结果，不说好坏', note: '以那天已经生效的规定为准',
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
    '每把梯子五格：对象观点是强烈看多到强烈看空，说的是对业务好还是坏；主题观点是从一头排到另一头的五种结果，用结果命名，不说好坏。只有是或否的问题用两格，不硬分五格：对象观点的两格是看多、看空；主题观点的两格用结果命名，比如“到期前签署了”“没签署”。',
    '每一格写成一个能核对的结果：可以是一个数落在哪段区间，也可以是一件事到了哪一步。格和格不重叠、不留空，到期时正好一格成立：涨 50% 及以上、涨 10% 及以上不到 50%、涨跌都不到 10%、降 10% 及以上不到 80%、降 80% 及以上，每个边界只属于一格，到期拿到实际数，一定落进其中一格；写成“涨很多、涨一点”就对不出来。没有含糊的“部分”：部分做到的，写清楚是什么，单独成一格（“发许可，但附条件”）。中性跟什么比，写在那一格的条件里。',
    '一把梯子只放一种东西，一个观点只看一件东西：既要数字又要事件的，拆成两条，用依赖连起来；两部分可能往相反方向走的（H20 这一档和 Blackwell 这一档），也是两条观点。',
    '梯子由模型在抽取时写进候选观点，开成新观点就用这把，到期以前不改；后来归入的候选观点，梯子和到期日都用已有的。',
    '数字的观点写明哪一年。不是公司的数，按自然年：这条信息发布那年是今年，下一年是明年，各到 12 月 31 日。公司的数按它的财年：发布日所在的财年是今年，下一个财年是明年。都按信息的发布日算，不看电脑时钟。同一个数，今年、明年最多各开一条，超出的不开；到期日就是这个数公布的那天。',
    '到期日定在这个争论见分晓的那天，一般 6–12 个月；中间的季报是证据，不另开观点。',
  ];

  // The state on a ladder (D45: where it is now is a proposal, in VIEWS_PROPOSED).
  const POSITIONS = [
    { position: '状态', means: '这条观点处在梯子的哪一格：我们的判断，证据把它往梯子的一头或另一头推', moves: '模型判，温度调低，只按事实。每次从这条观点下没被替代的全部证据（每条带上它替掉的那条，看得到变化）、加上它依赖的观点现在的状态和理由重新判，不在上一次的基础上加减；写明依据哪几条证据；再和这条观点在这一轮之前的结论比，写明结论变不变。读的东西没变（连着的证据只多了出处，依赖的观点结论也没变），就不重判', example: '看到 8-K 以后：强烈看空' },
  ];

  // How a judgement shows its sources and how code checks them (D46).
  const STATE_RULES = [
    '每次判断都写明依据：模型按固定格式交回判断，其中一栏写它根据的是哪几条证据，写证据的编号，比如“依据：e12、e15”；因为它依赖的观点变了而重判的，也写那几条观点的编号，比如“依赖：#1”。',
    '代码查表核对：每条证据存进库时有一个编号；库里记着每个观点下有哪些证据、每条有没有标“被替代”。代码拿依据里的编号去查：证据是不是这个观点下的、有没有标“被替代”；观点是不是它依赖的那几条。都对，这次判断写进去；有一个不对，这次判断不收，记下原因，让模型重判一次；再不对，这一步算失败，照失败的规矩处理（从这一步重试，多次失败的放进人工复核池）。只核对引用合不合上面这几条，不管判得对不对，就像核对脚注里写的页码，书里到底有没有那一页。',
    '每次判断还交一栏“结论变不变”：模型拿这次的判断和这条观点在这一轮之前的结论（状态和理由）比（这一轮里重试也一样），写“变了”或“没变”，加一句为什么；这一轮之前的结论只拿来比，不在它的基础上加减。换了一格，或者撑着这个状态的关键事实、关键数字变了，算变了：AMZN 资本开支指引从涨 12% 改成 25%，还在同一格，也是变了；同样的话再说一遍，是没变。写了“变了”，依赖它的观点读的东西就变了，这一轮接着重判。代码只核对一件事：换了一格的、第一次判的，必须写“变了”；写成“没变”的不收，照上一条查表不对的规矩处理。',
    '想知道某天当时怎么判，就翻那天存下的判断记录，不重新问模型；再问一次，模型可能答得不一样。',
  ];

  const TIERS = [
    { tier: '发生的事', examples: '官方行动、公布的数、已经完成的交易', counts: '能定哪一格成立，也能推状态' },
    { tier: '当事人说的', examples: '公司指引、管理层表态、官员讲话', counts: '只能推状态' },
    { tier: '第三方看法', examples: '卖方、媒体分析、专家', counts: '只能推状态' },
    { tier: '传闻', examples: '“知情人士称”、没有出处的说法', counts: '只能推状态' },
  ];

  const TIER_RULES = [
    '推多远由模型判，写明依据；哪一层都不给固定分数。',
    '独立来源按原始来源数：二十家媒体转述同一条独家，是同一条证据的二十个出处，算一份。',
    '层看是谁确认的：“知情人士称商务部开始发许可证”是传闻；商务部或公司确认以后，确认的那条是发生的事，替代那条传闻；传闻还是传闻，留在历史里。',
    '证据只存一次，本身不带方向；往哪边推记在证据和每条观点之间的连线上，由每次重判写。同一句话可以连几条观点，各推各的。',
  ];

  // How B reads A when B depends on A.
  const DEPENDENCY_TREE = {
    label: 'B 依赖 A', question: 'A 是哪一种观点？', note: '箭头带一个方向：B 是对象观点，写明 A 的哪一头对 B 是看多；B 是主题观点，写明两把梯子同向还是反向',
    children: [
      {
        answer: '数字的观点', label: '读那一年的那条', note: '例：JPM 2027 全年净利息收入 → 美联储 2027 年末利率',
        children: [
          { answer: 'A 开着', label: '读 A 的状态和理由', act: true },
          { answer: 'A 关了', label: '读 A 关掉时的状态和理由', note: '到期定格的，这就是 B 要用的，B 接着读它', act: true },
          { answer: 'A 还没建', label: '箭头先等着', note: '记下等的是哪条链上的哪一年（链是模型面前那条观点所在的链）；那一年的观点在链上接续出来时连上，B 重判一次' },
        ],
      },
      {
        answer: '事件的观点', label: '顺着接续往下走', note: '例：NVDA FY27 全年中国区收入 → 这一档芯片对华出口许可',
        children: [
          { answer: 'A 开着', label: '读 A 的状态和理由', act: true },
          { answer: 'A 关了，有接续的', label: '读接续的那条', note: '记一笔；接续的那条建出来，B 读的东西变了，重判一次', act: true },
          { answer: 'A 关了，没有接续', label: '读 A 关掉时的状态和理由，标“只是历史”' },
        ],
      },
    ],
  };

  const DEPENDENCY_RULES = [
    '主题观点不说好坏；对谁是好是坏，由依赖它的对象观点在箭头上写明：降息那头对以太坊是看多，对 JPM 是看空。',
    '箭头只有一个方向。看起来要“先好后坏”，说明中间还有一条观点没写出来，要拆出来：钢铁关税抬高国内钢价是一条路，拖垮下游用钢需求是另一条路。',
    '观点之间互相影响只有一种方式：依赖（接续只记哪一期接着哪一期）。B 依赖 A，就是 B 判断时要看 A 的结论。B 判断时看两样，分开放：直接讲 B 的证据；它依赖的观点现在的状态和理由。A 的结论对 B 起的作用像证据，但不当证据存：证据是外面发生的事、别人说的话，A 的结论是我们自己的判断，当成证据，系统会自己说服自己。',
    '一句话只算一次：讲 A 的话只算 A 的证据（同一条信息里新提的两条候选观点也一样，一句话只连到它直接讲的那条），B 通过 A 的结论知道这件事；直接讲 B 的，才算 B 的证据；B 不依赖 A 的，讲 A 的话也直接算 B 的证据。依赖谁只在建 B 的时候定。',
    '什么时候重判：一条观点读的东西变了，就重判。读的东西有两样：它自己的证据，和它依赖的观点的结论（状态和理由）。自己的证据变了，是来了新证据、有证据被替代，或者新连上了一条库里已有的证据；连着的证据只多了出处，不算。依赖的观点结论变了，是那条观点这次判完写了“变了”。B 等着的 A 刚建出来、B 读的那条换成了接续的下一期，也都是 B 读的东西变了。只重判开着的观点，关了的不再更新。你自己的备忘录开的观点，第一次连上证据时才第一次判；在那以前状态是“还没判”，依赖它的观点读到的也是“还没判”。',
    '新观点连不连依赖、连哪几条，由模型在比对的那一次一起判，像分析师一样：写出这条观点的结果要靠哪几条观点的结果，各往哪个方向推。从模型面前已有的观点里挑：搜出来的前 N 条、抽取时第 5 块列的、同一条信息里新建的；不另外搜。已经发生的事是证据，不连：OPEC 看着今天的油价定产量，今天的油价是“OPEC 产量”这条观点的证据，不是依赖。',
    '防绕圈：每加一条箭头，或者一条箭头顺着接续换到下一期，代码先查会不会绕成圈（A 靠 B，B 又靠 A）；会的话这条不收，退回给模型改；改了还绕圈，照失败的规矩处理。看起来互相依赖的两个问题，是观点没起好。',
  ];

  // Succession: the same thing, period after period.
  const CHAIN_RULES = [
    '同一样东西的下一条观点接着上一条，连成一条链：美联储 2026 年末利率 → 2027 年末利率 → 2028 年末利率。这条链记下各期观点的前后关系；依赖的箭头怎么顺着链走，见上面。',
    '一条只能有一个下一期：FY26 后面只接一条 FY27，不能冒出两条。',
    '下一期的梯子方向不变：上一期第一格是“强烈看多”，下一期也是；每一格的门槛可以重新定。依赖它的观点沿用原来的方向，梯子两头一反就乱了。',
  ];

  // Writing what extraction hands over, one item per round: candidate views first, then evidence.
  const INTAKE_STEPS = [
    { code: '1', name: '核对出处', who: '代码', does: '出处在处理记录里查不到的不要，记下原因' },
    { code: '2', name: '收证据', who: '代码', does: '重试不重复存；一条信息出了修正版，只换它自己那一处出处：修正版只是转述别人的，不动原来那条证据；修正版本身就是原始来源的，新版里的句子照常比对，改了的替代原句' },
    { code: '3', name: '搜索', who: '代码', does: '用搜索引擎在观点库里搜（像 Elasticsearch，语义搜索或关键词，怎么搜还没定）。候选观点搜整个观点库，开着的、关掉的都搜，取前 N 条（N 写在 Config，先定 10）；证据只在它连到的那条观点下的证据里搜，取前 N 条；连在候选观点上的（哪怕也连着已有观点），等候选观点有了去向再一起搜。搜出来是空的，也照样交给第 4 步' },
    { code: '4', name: '比对', who: '模型', does: '模型不读原文，在同一次调用里判三件事；给它看的每条已有观点，都有属于哪个对象、问题、看的是什么、梯子、到期日和开着还是关了。一是每个候选观点：是清单里的哪一条（或者它的一部分）、接续哪一条（接续的，梯子按上一期的方向排，门槛照候选观点写的），还是新观点（对不上，或者只是有点像，就开新的）；太大太杂的、超出今年和明年的数字观点、和一条关了的观点是同一样东西的同一期的，都不开；都写理由。二是要开的新观点依赖哪几条观点、各往哪个方向推，从模型面前已有的观点里挑：搜出来的、抽取时第 5 块列的、同一条信息里新建的。三是只连在已有观点上的每条证据，和那条观点下搜出来的证据比，是重复、替代还是新证据。连在候选观点上的证据，等候选观点有了去向再比：到它连着的每条已有观点下（包括候选观点归入的那条）一起搜，另叫一次模型一起比；只连在新观点上的，就是新证据' },
    { code: '5', name: '核对', who: '代码', does: '候选观点和证据的去向，编号必须在清单里，或者是那条观点下的证据；候选观点要归入的那条已有观点，必须还开着；新观点讲的对象必须在研究对象名单里（照分类查对象标识的办法查），不在的照“不开”处理；新观点依赖的，必须是这一次给模型看过的观点（或者写明了要等它那条链上的哪一年），连上以后不绕成圈，不对的退回给模型改' },
    { code: '6', name: '写进库', who: '代码', does: '按归组规矩把抽取交来的归属连到最终观点，和本步一起保存；各对象自己的队列写，先写主题观点，再写对象观点；新观点和它的依赖箭头一起写；重复只给那一条多一个出处，这次新连上它的观点也连过去；替代按说的时间排（这句话是哪天说的），后说的算数，先说的标“被替代”，晚到的旧说法不加进来，只在处理记录里写一笔；被替代的证据还连着别的观点，新的那条也连过去；原始来源自己的修正版里找不到、也没被新句替代的原句，算删了，标“被替代”；比对时读到的东西在写进库之前变了，就把受影响的部分重新比对' },
    { code: '7', name: '重判一轮', who: '模型', does: '读的东西变了的观点重判，只判开着的（关了的不判）：这一轮来了新证据、有证据被替代、新连上了一条已有的证据，或者它依赖的观点这一轮判完写了“变了”（刚建出来的、换成接续的下一期的，都算变了）。先判被依赖的观点，再判依赖它的，每条这一轮只判一次；连着的证据只多了出处，本身不触发重判；你自己的备忘录开的、还没连上证据的观点不判，状态写“还没判”；每条判完写明结论变不变，变了的，依赖它的接着判' },
  ];

  // Two lanes, one shape: a candidate view and a piece of evidence are each compared with what is already there.
  const INTAKE_SHAPE = [
    { aspect: '去哪比', views: '搜索引擎从整个观点库搜出的前 N 条', evidence: '在它那条观点下的证据里搜出的前 N 条' },
    { aspect: '判什么', views: '是哪一条（或它的一部分）、接续、新观点，还是不开', evidence: '重复、替代、新证据' },
    { aspect: '链', views: '接续：美联储 2026 年末利率 → 2027 → 2028', evidence: '替代：AMZN 资本开支指引涨 12% → 25%' },
    { aspect: '什么算现在', views: '链上开着的（数字可以今年、明年各开一条）', evidence: '没被替代的那些（证据的替代也连成一条链）' },
    { aspect: '搜什么', views: '整个观点库，开着的、关掉的都搜', evidence: '只搜它那条观点下的，不搜全库' },
  ];

  // Step 4: where a candidate goes.
  const MATCH_OUTCOMES = [
    { outcome: '归入已有的', when: '候选观点看的就是那条观点看的东西，或者是它的一部分（“H20 在中国的收入”是“中国区收入”的一部分）；只能归入开着的，关掉的只能接续', writes: '证据再和那条观点下的证据比，研究归属按本节归组规矩保留；梯子和到期日用已有的' },
    { outcome: '接续', when: '同一样东西的下一期：数字的下一年；事件的那条已经关了，要接着看', writes: '建新观点，记接续' },
    { outcome: '新观点', when: '对不上，或者只是有点像：Blackwell 这一档对华许可，不是 H20 这一档', writes: '建新观点，梯子和到期日从此定死' },
    { outcome: '不开', when: '太大太杂，一条里捆了几件可能往相反方向走的事：“美国对华芯片管制会怎样”；或者数字的观点超出了今年、明年；或者和一条关了的观点是同一样东西的同一期（关掉的只能接续）；或者讲的对象不在研究对象名单里（名单里没有的主题，交人工复核池当建议新增的主题；名单外的公司只在处理记录里留一笔）', writes: '不建；它的证据如果也连在具体的那条上，照常算数；只连在它身上的不存' },
  ];

  const MATCH_NOTES = [
    '搜只用来找出前几条可能的，是不是同一条由模型判：“H20 对华许可”和“Blackwell 对华许可”很像，却是两条；看多和看空的两种说法，是同一条。',
    '关掉的观点也搜得到：FY26 那条关了，FY27 的候选观点进来照样搜到它，模型判成接续。',
  ];

  // Step 4: where a piece of evidence goes, against the evidence its view already holds.
  const EVIDENCE_OUTCOMES = [
    { outcome: '重复', when: '说的就是那条观点下已有的一条：别人转述；正文和表格里的同一个数；同一个人把同样的话再说一遍', writes: '那一条多记一个出处；证据不多一条。对已经连着它的观点，这本身不触发重判；这次新连上它的观点，读的东西变了，照常重判' },
    { outcome: '替代', when: '和已有的一条是同一件事的前后两个说法：同一个人后来改了说法或数（指引、预测、某件事办到了哪一步）；官方证实或否认了一条传闻；原始来源自己出了修正版，改了原句', writes: '按说的时间排（这句话是哪天说的），后说的算数，先说的标“被替代”，留在历史里，重判；晚到的旧说法（同一件事已经有更新的）不加进来，只在处理记录里写一笔，不重判' },
    { outcome: '新证据', when: '别的都是：新的事、另一期的数、另一个人的说法（说法相反的也是）；拿不准也算新证据', writes: '加进来，和别的一起算数；重判' },
  ];

  const EVIDENCE_NOTES = [
    '证据只和它那条观点下的证据比，不拿证据去搜全库：先定好它连在哪条观点上（抽取时连上的，或者候选观点比对后去的那条），再在这条观点下没被替代的证据里搜前 N 条，交给模型比。候选观点搜的是整个观点库，证据只搜它那条观点下的。',
    '一条证据连几条观点，也只存一条：和这几条观点下的证据一起比一次；其中有连在候选观点上的，等候选观点有了去向再一起比。',
    '被替代的证据还连着别的观点，新的那条也连过去，其中开着的也重判；不然那条观点手里只剩一个过时的说法。',
    '证据是一句话或一个数，替掉的只是那一句：卖方新报告改了收入预测，替掉的是它上一份里的那个预测，别的论据照样算数。',
    '比对不读整份原文，读的是证据里“一句话说清”的那句，加上谁说的、原始来源和哪天说的；拿不准算新证据，最坏也就是两条都算数，由重判自己看。',
  ];


  const INTAKE_EXAMPLE_TREE = {
    label: '三条信息，库从空的开始', note: '示意',
    children: [
      {
        answer: '2025-04-15 NVDA 的 8-K', label: '库是空的，交来两个候选观点', question: '比对：清单是空的，都开新观点',
        children: [
          { answer: '#1 主题观点', label: '这一档芯片对华出口许可（事件）', note: '证据：H20 出口中国要许可证（发生的事）', act: true },
          { answer: '#2 对象观点（NVDA）', label: 'FY26 全年中国区收入（数字）', note: '证据：预计最多约 55 亿美元的费用（当事人说的）；依赖 #1，放松那头看多', act: true },
        ],
      },
      {
        answer: '2025-04-16 AMD 的 8-K', label: '讲的是 AMD，AMD 还没有观点，交来两个候选观点', question: '比对',
        children: [
          { answer: '候选观点“MI308 对华许可”', label: '归入 #1', note: '搜到 #1，模型判是同一件事（同一条规定管的同一档芯片）；它的证据再和 #1 下的证据比：AMD 说的是 MI308，是新证据；#1 重判，写“没变”：多了一个受管的型号，撑着结论的关键事实没变，状态也还在同一格，所以 #2 不判', act: true },
          { answer: '候选观点“AMD 2025 全年中国区收入”', label: '新观点 #3', note: 'AMD 还没有开着的观点；证据：预计最多约 8 亿美元的费用（当事人说的）', act: true },
        ],
      },
      {
        answer: '2025-04-16 路透的报道，转述 NVDA 的 8-K', label: '已有的观点：#2 和它依赖的 #1', question: '比对',
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
    { item: '3-10 摩根士丹利：预计涨 18%', matched: '新证据（另一个人说的）', store: '加 m1', rejudge: '判' },
    { item: '4-30 电话会：指引改成涨 25%', matched: '替代 g1', store: 'g2 算数，g1 被替代', rejudge: '判，读到“12% → 25%”' },
    { item: '5-02 摩根士丹利：改成涨 27%', matched: '替代 m1', store: 'm2 算数，m1 被替代', rejudge: '判' },
    { item: '5-20 才到：摩根士丹利 2 月报告里的预测', matched: '晚到的旧说法：摩根士丹利后来已经改过两次（3 月 m1、5 月 m2）', store: '这条预测不加进来，处理记录里写一笔“过时，没用”；m2 照旧算数', rejudge: '不判' },
    { item: '6-10 会上重申“还是 25% 左右”', matched: '重复 g2', store: 'g2 多一个出处（最近一次 6-10）', rejudge: '不判' },
  ];

  const EVIDENCE_EXAMPLE_NOTE = '半年后这条观点下可能有几十条证据，重判读的只是没被替代的那几条：公司指引涨 25%（2 月是 12%），摩根士丹利预计涨 27%（3 月是 18%），加上别的人、别的事。';

  // The judge of step 4, its records, and the labels that will train a faster model.
  const JUDGE_STEPS = [
    { code: '1', name: '大模型比对', who: '模型', does: '第一版用通用大模型做比对（Config 里的“比对”设置），先让系统跑起来' },
    { code: '2', name: '每次都记', who: '代码', does: '每次比对留一条比对记录：给模型看了什么、它答了什么、最后写进库的是什么' },
    { code: '3', name: '人来标', who: '人', does: '挑两种给人标：被代码退回的（第 5 步核对没过的），和隔一段时间随机抽的几条；人标出正确的结果' },
    { code: '4', name: '训练小模型', who: '代码', does: '用人标的结果，训练一个更快的小模型' },
    { code: '5', name: '小模型接手', who: '代码', does: '以后由小模型做比对；什么时候接手还没定' },
  ];

  const TRACE_FIELDS = [
    { part: '哪条信息', meaning: '上游编号、顺序号' },
    { part: '交来的', meaning: '抽取交来的候选观点、研究归属、新主线定义和证据，原样留存；给比对模型看的内容另记' },
    { part: '给模型看的', meaning: '候选观点比的是搜出来的前 N 条（带名次）；证据比的是它那条观点下搜出来的前 N 条；新观点挑依赖时，还有抽取第 5 块列的观点和同一条信息里新建的' },
    { part: '谁定的', meaning: '大模型、以后的小模型，或人' },
    { part: '请求和返回', meaning: '实际发出的请求、原始返回、Config 版本（模型、提示词版本、温度）' },
    { part: '决定', meaning: '每个候选观点的去向和理由；新观点依赖哪几条、各往哪个方向；每条证据是重复、替代还是新证据；代码核对的结果和拒绝的原因' },
    { part: '写进库的', meaning: '最后写进库的结果' },
  ];


  // How a view ends.
  const LIFECYCLE_TREE = {
    label: '一条观点', question: '开着还是关了？', note: '只有这一个开关',
    children: [
      { answer: '开着', label: '读的东西变了就重判，条件见“什么时候重判”那一条', note: '比对开观点时，同一样东西同时只开一条；数字的同一个数，今年、明年各一条' },
      { answer: '关了', label: '不再更新，不重判', note: '状态停在关掉时的样子（判过的停在那一格，还没判的就是还没判）；留在库里，搜得到', act: true },
    ],
  };

  const LIFECYCLE_NOTES = [
    '到期那天由 Pull 模式关掉：状态停在哪一格，就定格在那一格，连同理由，就是这条观点最后的结论；要接着看，就开一条新观点接续它。Pull 模式在每天结束时、或按定时任务的间隔主动跑；信息流这一边不管时间。Pull 模式以后设计。',
    '人也可以手动关掉或重新打开一条观点，比如资产退市；每次都新加一条记录，写明是谁、从哪个顺序号的信息之后算数。同一样东西同时只开一条，是比对时的规矩，人手动打开的不受它管。研究对象名单也由人手动改。',
  ];

  const VIEW_FIELDS = [
    { part: '对象', meaning: '名单里的哪个对象', example: 'NVDA' },
    { part: '种类', meaning: '对象观点或主题观点', example: '对象观点' },
    { part: '看的是什么', meaning: '数字：哪个数、哪一年；事件：哪件事', example: 'FY27 全年中国区收入' },
    { part: '问题', meaning: '一句话，写下不改', example: 'NVDA FY27 全年中国区收入，比 FY26 会怎样？' },
    { part: '梯子', meaning: '五格（只有是或否的问题两格），每格一个能核对的结果，写下不改', example: '涨 50% 及以上……降 80% 及以上' },
    { part: '到期日', meaning: '争论见分晓的那天；数字就是它公布的那天', example: 'FY27 年报的财报日' },
    { part: '状态', meaning: '这条观点处在梯子的哪一格；每次重判记一版，写明依据和结论变不变；你自己的备忘录开的观点，第一次连上证据以前，状态写“还没判”', example: '强烈看空' },
    { part: '依赖', meaning: '指向哪几条观点，各带一个方向；等着还没建的，写明等哪条链上的哪一年', example: '→ 这一档芯片对华出口许可：放松那头看多' },
    { part: '研究归属', meaning: '属于哪些研究主线；按本节归组规矩保存成员关系', example: '这一档芯片的对华许可与中国业务' },
    { part: '接续', meaning: '接着哪一条；可以没有', example: '接着 FY26 那条' },
    { part: '从哪来', meaning: '从哪条信息建的', example: '2026-02-25 NVDA FY26 年报的业绩发布（示意）' },
    { part: '开着还是关了', meaning: '开着或关了，只有这一个开关：到期那天由 Pull 模式定格、关掉；人也可以手动关掉或重新打开（比如资产退市）；关了的不再更新', example: '开着' },
  ];

  const EVIDENCE_FIELDS = [
    { part: '原文', meaning: '信息里的那一句，或表里的那个单元格' },
    { part: '一句话说清', meaning: '离开原文也看得懂的一句：谁、做了什么、多少、哪一期；比对和重判读这一句' },
    { part: '出处', meaning: '上游编号、类别、发布日、在信息里的位置；重复的（别人转述、同一条信息的正文和表格、同一个人再说一遍）记成这条证据的又一个出处' },
    { part: '谁说的', meaning: '说这句话的人或机构' },
    { part: '原始来源', meaning: '转述的，记下最初是谁、哪天说的；独立来源按它数，替代也按这一天排先后' },
    { part: '哪一层', meaning: '发生的事、当事人说的、第三方看法、传闻' },
    { part: '事情发生的时间', meaning: '事情什么时候发生或生效；数字写它属于哪一期' },
    { part: '被替代', meaning: '指向替代它的那一条：同一个人后来改了说法或数、官方证实或否认了这条传闻；或者原始来源自己出了修正版，把这句改了、删了（删了的，没有替它的新证据）；被替代的不再算数，留在历史里' },
  ];

  const ORDER_RULES = [
    '只有信息能产生证据；观点之间只传通知，不传证据，所以观点不会自己证明自己。',
    '每条观点只由一个队列来写：主题观点由主题的队列写，对象观点由它所属的公司、加密货币或商品的队列写；写进库时，同一条信息先写主题，再写对象；重判的先后另按依赖排（见“一条信息引起的变化算一轮”那条）。别的队列要它改的（它依赖的观点结论变了、要它重判，或者被替代的证据要连过来），作为通知交给它自己的队列，带着那条信息的顺序号。',
    '先后按顺序号排，不用电脑时钟。一条信息只读顺序号比它小的信息写下的内容，加上这一轮里它自己已经写下的；结果要和一条一条按顺序处理完全一样；几条信息同时处理时，一条信息读到的东西（搜出来的清单也算）在它写进库之前被别的信息改了，就重新做一次。',
    '一条信息引起的变化算一轮：先做完连证据、建观点、接续和连依赖，再按依赖先后重判：先判被依赖的观点，再判依赖它的，后者读的是前者这一轮刚判完的结论（状态和理由）；每条观点这一轮只判一次。美联储这样的观点被很多观点依赖：它判完写“变了”，依赖它的才各判一次；写“没变”，到此为止。',
    '记录只加不改：观点的问题、梯子和到期日写下就不动；比对、重判、接续、关掉、重新打开、标注，都是新加一条记录，带顺序号。',
    '时间线只往后加，不回头改：观点的每一次变化，按我们什么时候知道的往后记。晚到的信息，同一件事已经有更新的说法，它就不算数，不加进观点，只在处理记录里写一笔“过时，没用”；讲的是我们不知道的事，照常算，记上它真实的日期。分这两种由模型比证据时一起判，不另加规矩。',
    '一条信息出了修正版，只换它自己那一处出处：修正版只是转述别人的，不动原来那条证据；修正版本身就是原始来源的，改了的原句由新句替代，删了的标“被替代”。连着被改了、被删了的原句的开着的观点各重判一次；只换了转述出处的，不重判；过去的重判记录不改。',
    '失败：每条信息记下做到哪一步，从失败的那一步重试，重试只替换自己上次的结果；多次失败的放进人工复核池。',
    '两头都能查：从一条观点查到推过它的全部信息；从一条信息查到它建过的观点，和它作为出处的全部证据（重复的也查得到）。',
  ];

  const STORE_NOTE = '存在哪、用什么数据库，建的时候定。';

  const VIEWS_OPEN = [
    '搜索怎么搜：用语义搜索、关键词还是两样一起，怎么排先后；建的时候在存下的信息上试过再定。前几条先定 10，试的时候再调。',
    '观点的颗粒度，也就是一条观点管多大的范围，还没定，要专门定。现在只定了：是已有观点的一部分，就归入那条；太大太杂的不开。要紧的那一块要单独成一条（NVDA 中国区收入很关键，不能归入总收入）；太粗的话，观点会全变成财务指标，这不行；要让模型清楚知道这样抽是错的。先做一次完整的调研：从对冲基金的角度看，一条观点到底长什么样，什么该合、什么该拆，每个对象盯几个问题（现实里每家公司只盯 2–3 个）。',
    '标注的细节以后再补：谁来标、标多少、用什么界面；怎么考小模型准不准、训练怎么用标好的数据；小模型什么时候接手；抽取连错、漏掉的证据怎么查，也在这里一起补。',
    'Pull 模式以后设计：每天结束时、或按定时任务怎么跑，怎样把观点整体过一遍；最终判定还要不要单独一步，一起定。',
  ];

  // Claude's proposals that Alex has not decided (D45). None of them is built until he decides it.
  const VIEWS_PROPOSED = [
    'Pull 模式的事，设计 Pull 模式时再谈：除了到期定格，另外两种情况，答不出（不再披露这个数、事情本身没了；依赖它的观点标“缺这个输入”）和等公布（数字的观点期末已过、这个数还没公布）。',
    'Pull 模式的事，设计 Pull 模式时再谈：每天查重，Pull 模式每天发起，同一对象开着的观点两两比；后建的合并到先建的，连线和箭头搬过去，查环，重判；Config 里多一套“查重”的设置。',
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

  // Step cards; a card is { code?, title, who?, note?, strong? }. Joined by '→' (steps in order) or '+' (parts put
  // together) the cards stack top to bottom; joined by '·' they sit side by side. A short `who` is a tag, a sentence
  // is plain text.
  function flow(cards, separator, escapeHtml) {
    const code = (card) => (card.code !== undefined ? `<span class="flow__code">${escapeHtml(card.code)}</span>` : '');
    const who = (card) => (card.who
      ? `<span class="flow__who${card.who.length > 6 ? ' flow__who--text' : ''}">${escapeHtml(card.who)}</span>` : '');
    const cardClass = (card) => `flow__card${card.strong ? ' flow__card--strong' : ''}`;
    if (separator === '·') {
      return '<div class="flow flow--set">' + cards.map((card) => `<div class="${cardClass(card)}">`
        + `<div class="flow__top">${code(card)}<span class="flow__title">${escapeHtml(card.title)}</span></div>`
        + who(card)
        + (card.note ? `<p class="flow__note">${escapeHtml(card.note)}</p>` : '')
        + '</div>').join('') + '</div>';
    }
    return `<ol class="flow flow--steps${separator === '+' ? ' flow--parts' : ''}">` + cards.map((card) => `<li class="${cardClass(card)}">`
      + `${code(card) || '<span></span>'}`
      + `<div class="flow__head"><span class="flow__title">${escapeHtml(card.title)}</span>${who(card)}</div>`
      + `<p class="flow__note">${escapeHtml(card.note || '')}</p>`
      + '</li>').join('') + '</ol>';
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
          <p class="drill__intro">抽取只做一件事：每条信息整份交给模型，用资深对冲基金分析师的视角、按这一类的提示词，对着这些对象已有的观点读完，交出两样东西。一是证据：支持或削弱观点的话和数，连到已有观点上，或者这次的候选观点上。二是候选观点：已有观点管不到、又要紧的事，带着提出它的证据（你自己的备忘录照提示词说明处理）。每个候选观点同时带研究归属，按下节规矩交接；每条带出处，交给观点库；怎么和库里已有的比、写进去，是观点库的事。</p>
          <p class="drill__status"><span class="pill pill--strong">第一版已冻结 · 2026-10-18</span>定下：整份交给模型；每一类一份提示词，拼法相同；观点是模型的判断，证据是客观的；每条都带出处；抽取只读；证据连到已有观点上，和候选观点分开交；候选观点当场写全。没定：每一类提示词的具体写法，建的时候试过再定。</p>
          <h3 class="drill__heading drill__heading--spaced">抽取时同时确定研究归属</h3>
          <ul class="drill__rules">${listItems(EXTRACT_RELATIONS, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">一条信息，一步一步</h3>
          <p class="flow-legend">黑框是模型做的，灰框是代码做的。</p>
          ${flow(stepCards, '→', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">读出两样东西：证据和候选观点</h3>
          ${table(['', '证据', '候选观点'], EXTRACT_TWO.map((row) => [row.aspect, row.evidence, row.candidate]), escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">读到一句话或一个数，它算什么</h3>
          ${tree(EXTRACT_SORT_TREE, escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">第 1 步：每一类的提示词，都由同一个提示词模板的这五块拼起来</h3>
          ${flow(templateCards, '+', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">每一类有自己的提示词：以 T7 新闻为例，五块各写什么（只列要点）</h3>
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
          <h2 class="drill__title">观点库</h2>
          <p class="drill__intro">系统做的事，就是在这里建观点、更新观点、关掉观点。一条观点是一个问题、一把梯子和一个到期日：证据把它的状态往两头推，到期那天状态定格。抽取交来两样东西，都是先搜、再由模型比：候选观点和搜出来的几条已有观点比，判是归入已有的、接续、开新的，还是不开；证据和它那条观点下搜出来的证据比，判是重复、替代还是新证据。连着的证据只多了出处，本身不触发重判。每条证据都带出处；研究归属由抽取交来，按下节规矩保存；记录只加不改。</p>
          <p class="drill__status"><span class="pill pill--strong">第一版已冻结 · 2026-10-20</span>只写 Alex 说过或定过的；要改，先记一条新决定。还没定的、和 2 条 Pull 模式的事，单列在最后。</p>
          <h3 class="drill__heading drill__heading--spaced">研究主线：抽取时归组</h3>
          <ul class="drill__rules">${listItems(GROUP_RELATIONS, escapeHtml)}</ul>
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
          <h3 class="drill__heading drill__heading--spaced">进库：候选观点和证据都是先搜、再由模型比</h3>
          ${table(['', '候选观点', '证据'], INTAKE_SHAPE.map((row) => [row.aspect, row.views, row.evidence]), escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">一条信息进来，怎么写进库（一轮）</h3>
          <p class="flow-legend">黑框是模型做的，灰框是代码做的。</p>
          ${flow(stepCards(INTAKE_STEPS), '→', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">第 4 步比对：候选观点的去向</h3>
          ${table(['去向', '什么时候', '写什么'], MATCH_OUTCOMES.map((row) => [row.outcome, row.when, row.writes]), escapeHtml)}
          <ul class="drill__rules">${listItems(MATCH_NOTES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">第 4 步比对：证据的去向</h3>
          ${table(['去向', '什么时候', '写什么'], EVIDENCE_OUTCOMES.map((row) => [row.outcome, row.when, row.writes]), escapeHtml)}
          <ul class="drill__rules">${listItems(EVIDENCE_NOTES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">例子：三条信息怎么写进库</h3>
          ${tree(INTAKE_EXAMPLE_TREE, escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">例子：一条观点下的证据怎么跟着更新（AMZN 2026 全年资本开支，示意）</h3>
          ${table(['信息', '比对证据', '库里', '重判'], EVIDENCE_EXAMPLE.map((row) => [row.item, row.matched, row.store, row.rejudge]), escapeHtml)}
          <p class="drill__footnote">${escapeHtml(EVIDENCE_EXAMPLE_NOTE)}</p>
          <h3 class="drill__heading drill__heading--spaced">比对的裁判和标注：先用大模型跑起来，攒下标注，以后交给小模型</h3>
          <p class="flow-legend">黑框是模型做的，灰框是代码或人做的。</p>
          ${flow(stepCards(JUDGE_STEPS), '→', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">一条比对记录记什么</h3>
          ${table(['部分', '记什么'], TRACE_FIELDS.map((row) => [row.part, row.meaning]), escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">一条观点开着还是关了</h3>
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
              <h3 class="drill__heading drill__heading--spaced">先后顺序、同时处理和查来历</h3>
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
      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">最终判定（旧稿）：一条观点还成立吗</h2>
          <p class="drill__intro">现在：到期那天，观点的状态停在哪一格就定格、关掉，由 Pull 模式做；最终判定还要不要单独一步，以后和 Pull 模式一起定。下面是旧稿：一条观点要不要关，不由一条证据或一个条件直接决定，而是先送到这里，由模型把整条观点和它的全部证据完整看一遍再判。</p>
          ${status('旧稿 · 要重做', '观点库已按 D38–D40 重建，这里写的检验条件、证实和证伪、前提、前提被削弱时的 7 天兜底复核、同一层来源有分歧就送来都不再用（D38、D41）。已经定了：一条观点只有一个状态，到期那天状态定格就关掉，不另外定别的；Pull 模式每天结束时或按定时任务跑，不另外等（D54）。其余以后和 Pull 模式一起重做。', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">这些情况会把观点送来</h3>
          ${table(['触发', '谁发现'], VERDICT_TRIGGERS.map((trigger) => [trigger.trigger, trigger.who]), escapeHtml)}
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
