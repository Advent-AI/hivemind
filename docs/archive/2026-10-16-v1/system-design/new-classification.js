// The New design's input classification module: a top-down issue tree that gives every input exactly one outcome (a
// tag, "not an input", or a refusal), the tag schema, and the input schema the tree reads. Edit the data at the top;
// the drill-down renders it. docs/system-design/simulate_classification.py runs the same rules over test inputs.
(function () {
  'use strict';

  // ------------------------------------------------------------------ the tags: rule = what puts an input here

  const TAGS = {
    T1: { name: 'results_release', label: '业绩发布', forms: '两者', decide: '文字：8-K 里 Item 2.02 点名的附件、6-K 里的财期业绩附件、交易所的业绩公告、来源标为“业绩”的文件。表格：数据集表里登记为业绩数字的。', rule: '一个财期的业绩稿、股东信、当天的数字', definition: '一个财期（季度、半年、全年）的业绩发布。文字：8-K 里 Item 2.02 那一段点名的附件（业绩稿、股东信、CFO 解读、Update deck），6-K 里写明是财期业绩的附件，交易所的业绩公告，来源标为“业绩”的文件。表格：业绩当天公布的数字和指引（业绩表、指引历史）。月度经营数据不在这里，归 T6。同一份业绩稿的转载，并到原件。', examples: 'Apple 季度业绩稿、Tesla Update deck、指引历史' },
    T2: { name: 'periodic_report', label: '定期报告', forms: '两者', decide: '文字：10-K、10-Q、20-F、40-F、ARS（含修正版 /A），交易所的年报、中报，来源标为“定期报告”的文件。表格：XBRL 数字、标准化报表。', rule: '10-K、10-Q、20-F、40-F、ARS 和里面的数字', definition: '文字：10-K、10-Q、20-F、40-F、ARS 及修正版（/A，注明它替换了哪一版），交易所的年报、中报、季报，来源标为“定期报告”的文件。表格：这些报告里的 XBRL 数字，数据商整理的标准化报表和分部数据（注明出自哪份报告）。是年报还是季报，只是一个属性。', examples: 'Meta 10-K、10-K/A、SEC companyfacts、标准化利润表' },
    T3: { name: 'legal_and_capital_markets', label: '法律与资本市场文件', forms: '文本', decide: '文字：委托书、融资、并购、要约收购类申报（不管谁提交的），申报里编号 2、3、4、10 的附件，交易所通函，来源标为“法律”的文件。', rule: '委托书、融资、并购、要约；附件 2、3、4、10', definition: '不管谁提交的：委托书（包括代理权争夺双方的材料）、融资、并购、要约收购（包括收购方、私募发起的）申报及修正版；SEC 规定编号 2、3、4、10 的附件（并购协议、公司章程、证券和债务工具、重大合同）；交易所通函；来源标为“法律”的文件。读法：读出条款和各方的主张，主张算提交方说的。', examples: 'DEF 14A、激进投资者的 DEFC14A、424B5、合并协议、信贷协议' },
    T4: { name: 'call_transcript', label: '电话会文字稿', forms: '文本', decide: '文字：文字稿，而且是公司在讲（公司自己办的会，或在投资者会议上发言）；425 申报里的并购电话会。', rule: '公司自己在讲的会议文字稿', definition: '公司在讲的会议文字稿：公司自己办的（业绩会、投资者日、公司播客），在投资者会议上的发言（券商会议），以及 425 申报里的并购电话会。媒体办的活动归 T7。在哪开的、谁办的、谁整理的文字稿，都只是属性。', examples: 'MSFT 业绩会、NVDA 在券商会议上的炉边对谈' },
    T5: { name: 'presentation', label: '演示材料', forms: '文本', decide: '文字：公司的幻灯片：8-K 里 7.01 项和 425 申报里的演示稿、IR 网站上的 PPT。', rule: '幻灯片、PDF 演示稿', definition: '公司发布的幻灯片或 PDF 演示稿：8-K 里 7.01 项和 425 申报里的演示稿、IR 网站上不属于业绩 8-K 的 PPT。', examples: '投资者日 PPT、IR 网站上的业绩 PPT' },
    T6: { name: 'company_communication', label: '公司其他发布', forms: '两者', decide: '文字：公司的其余文件（8-K 正文和其他附件、其余 6-K、给 SEC 的回函、延期申报通知、新闻稿、官方账号的帖子）。表格：IR 网站的补充表格、月度经营数据。', rule: '公司的其余文件和数据（公司发的其余内容都归这里）', definition: '文字：申报里不属于前几类的（8-K 正文、业绩那一段没点名的附件和其他项、其余 6-K、给 SEC 的回函、延期申报通知），以及新闻稿、经营更新、ESG 报告、新闻室、博客、IR 和产品页面、公司官方社交账号的帖子。表格：公司自己发布的补充资料和月度经营数据（IR 网站上的 Excel、CSV）。', examples: '高管任免 8-K、季度交付量公告、IR 网站上的 KPI 表' },
    T7: { name: 'news', label: '新闻', forms: '文本', decide: '文字：作者是媒体，没有登记过发布系列，栏目不是评论或分析（没写栏目也算新闻）。', rule: '媒体的报道（媒体发的其余内容都归这里）', definition: '媒体发的内容，除了评论和分析：新闻报道、访谈、播客文字稿、媒体自己办的活动（比如 WSJ Tech Live）、媒体账号的帖子；综合、财经、行业媒体都算。没写栏目的按新闻算。评论和分析栏目归 T8；媒体登记过的发布系列按系列归类（比如 Reuters 的经济学家调查归 T8）。', examples: 'Reuters 报道、CNBC 对 CEO 的访谈、DigiTimes 的供应链消息' },
    T8: { name: 'opinion_analysis', label: '观点与分析', forms: '两者', decide: '文字：登记为预测、展望或研究的发布系列（不管谁发的）；媒体的评论和分析栏目；分析方写的、不是对话记录的文字；个人写的所有文字；申报里投资者写给董事会的信。表格：预测、评级、目标价、一致预期、投资者情绪调查。', rule: '有作者的观点、分析、预测和评级', definition: '有作者的观点和分析，不管作者是谁、多长、发在哪。文字：卖方和独立研究、评级机构、行业研究、智库和学术、官方和国际组织的预测、展望和研究（IMF 世界经济展望、CBO 预算展望、央行工作论文）、投资者（基金信、做空报告、申报里写给董事会的信）、媒体的评论栏目、个人的帖子和长文，以及你自己的投资备忘录。表格：分析师预测和修正历史、投资评级、目标价、一致预期、信用和 ESG 评级、经济学家和官方机构的预测（包括 GDPNow 这种实时预测）、投资者情绪调查（一群人看法的汇总，和一致预期一样）、行业估计、上传的“预测表”模板。观点和估计算作者说的，不当成已经发生的事；作者是你自己的，只当作要跟踪的观点，不当作证据。', examples: '卖方首次覆盖、做空报告、IMF 世界经济展望、Reddit 帖子、FY27 EPS 一致预期、你的盈利模型' },
    T9: { name: 'interview_notes', label: '访谈记录', forms: '文本', decide: '文字：作者是分析方，形式是逐字稿或纪要。', rule: '对话的逐字稿或纪要', definition: '分析方记录的对话：专家网络的访谈、你约的管理层会面和渠道调研。形式是逐字稿或纪要。话算原来说话的人说的，记录的人只是属性。公司自己在讲的活动归 T4。', examples: '专家网络访谈、与 CFO 会面的纪要' },
    T10: { name: 'official_record', label: '官方行为与记录', forms: '两者', decide: '文字：登记为行动或记录的官方发布系列；作者是官方、但没登记发布系列的（官方的其余内容都归这里）；SEC 意见函、法院案卷。表格：政府公布的记录。', rule: '官方的文件、程序和记录', definition: '官方发的、不属于别处的都归这里。文字：监管、法院、立法、行政、交易所的正式文件和程序记录（裁决、审批、召回、法规、制裁、出口管制、关税、合同授予、听证会和庭审文字稿、SEC 意见函、法院案卷）。表格：政府公布的记录（合同、游说、政治献金、专利、诉讼案卷信息、召回、海关提单）。官方的预测、展望和研究归 T8，统计数据归 T11。官员在任期内的个人账号也算官方（比如总统在社交平台上宣布关税）。里面的说法算原来说话的人或提交方说的。', examples: '欧盟委员会决定、FTC 诉状、SEC 意见函、国防合同授予、专利授权' },
    T11: { name: 'macro_policy_statistics', label: '宏观政策与统计', forms: '两者', decide: '文字：登记为货币政策或统计的发布系列，不管发布方是官方还是民间。表格：宏观统计和政策利率。', rule: '货币政策、宏观统计（官方民间都算）', definition: '文字：登记为货币政策或统计的发布内容，不管谁发的：央行关于货币政策和经济形势的材料（声明、纪要、讲话、点阵图、褐皮书），统计发布稿（官方的 CPI、非农；民间的 ISM PMI、ADP 就业、密歇根消费者信心）。表格：衡量整体经济或整个行业的统计和政策利率，官方民间都算，每条都带它是哪天发布的（数据会修正，旧版留着）；权重不公开、我们自己算不出来的合成指标（领先指标 LEI、金融条件指数）也在这里。市场上的利率和汇率归 T12；针对具体公司、产品、地点、链和协议的测量归 T15。', examples: 'FOMC 声明、褐皮书、CPI 与非农、ISM PMI、联邦基金利率' },
    T12: { name: 'market_data', label: '市场价格与成交', forms: '结构化', decide: '表格：数据集表里登记为价格和成交的。', rule: '股票、期权、利率、汇率、商品、加密、CDS', definition: '能交易的东西的价格和成交：股票、ETF、期权链、期货、利率、汇率、商品、加密货币、信用利差和 CDS、预测市场；分红、拆股这类公司行动，股本。', examples: '日线、期权隐含波动率、10 年期国债收益率' },
    T13: { name: 'positioning', label: '持仓与资金流', forms: '结构化', decide: '表格：数据集表里登记为持仓和资金流的；持股类申报的表格版本。', rule: '13F、Form 4、13D/G、空头、资金流', definition: '市场参与者的持仓和资金流：Form 4、13D/G、13F、144 的表格版本，空头持仓、融券费率和使用率、ETF 和基金的资金流、CFTC 持仓报告、加密货币的大户和“聪明钱”持仓。', examples: '机构持仓变化、内部人卖出' },
    T14: { name: 'calendar', label: '日历', forms: '结构化', decide: '表格：数据集表里登记为排好的日期的。', rule: '财报日、会议、截止日', definition: '已经排好的日期：财报、投资者日、发布会、宏观数据发布、央行会议、法院和监管的截止日、指数调整、解禁和代币解锁、期权到期。', examples: '下次财报日、FOMC 会议日' },
    T15: { name: 'third_party_measurement', label: '第三方测量', forms: '结构化', decide: '表格：数据集表里登记为实际活动测量的。', rule: '刷卡、App、流量、卫星、链上', definition: '数据商测到的、针对具体公司、产品、地点、链和协议的实际活动：刷卡、App 使用、网站流量、搜索、客流、卫星和航运、招聘、价格抓取、评论、链上活动（链和协议的使用量、收入）。是测出来的，不是估的：机构的行业估计和预测归 T8；衡量整体经济或整个行业的统计归 T11。', examples: 'App 下载量、刷卡消费数据' },
    T16: { name: 'reference', label: '参照数据', forms: '结构化', decide: '表格：数据集表里登记为身份和分类的。', rule: '身份、分类、指数成分', definition: '公司和资产的身份、行业分类、公司结构、供应链关系、指数成分和权重。研究对象默认都不看这一类；身份对照由上游用来认出信息讲的是谁。', examples: 'ticker 对应 CIK、GICS 行业分类、标普 500 权重' },
  };

  // ------------------------------------------------------------------ the issue tree: the taxonomy, each tag once
  // A branch has a label and either children or tags (its leaves). The tree shows what kinds of information there are;
  // ROUTING says how one input finds its leaf.

  const TREE = {
    label: '所有信息', question: '这是哪一类信息？', field: '先查合不合格、是不是重复（见下方“判断顺序”第 1 步）；每条信息只落到一个类别',
    children: [
      { label: '公司与申报披露', question: '哪种披露？', field: '看表格代码、来源栏目、形式', tags: ['T1', 'T2', 'T3', 'T4', 'T5', 'T6'] },
      { label: '媒体报道', question: '媒体的报道', field: '作者是媒体', tags: ['T7'] },
      { label: '观点与对话', question: '是观点，还是对话记录？', field: '作者是分析方或个人，或登记为预测、研究', tags: ['T8', 'T9'] },
      { label: '官方行动与宏观统计', question: '是行动记录，还是政策和统计？', field: '看发布系列；作者是官方', tags: ['T10', 'T11'] },
      { label: '市场与测量数据', question: '测的是什么？', field: '看数据集表', tags: ['T12', 'T13', 'T14', 'T15', 'T16'] },
    ],
  };

  // How one input finds its leaf, in order. Text or structured only decides which table answers.
  const ROUTING = [
    '先检查：缺必填信息、对象代码写得不对、没有文字可读、系统自己的产出 → 不合格；以前收过的同一内容 → 并到原来那条。',
    '表格数据：不逐条判断。每个数据集接入时，在数据集表里登记一次属于哪一类（一个接口返回好几类内容的，按字段分开登记），之后每条都直接用这个类别；没登记的数据集 → 不合格，放进人工复核池。',
    '文字，而且是申报文件（SEC、交易所、法院）：查这个系统的表格代码表，不管谁提交的；表里没有的代码 → 不合格，放进人工复核池。',
    '其余文字，发布方登记过这个发布系列：查发布系列表定类别（只可能是 T8、T10、T11），不管作者是谁。带了系列名、但表里没有的（新指标）→ 放进人工复核池，这条照常往下判。',
    '其余文字：先看作者是哪种（查作者表，看发布那天是否在有效期内；查不到就用渠道的默认类型），再看栏目或形式定类别；官方作者没登记发布系列 → T10；判断不了作者是哪种 → 不合格，放进人工复核池。',
  ];

  // ------------------------------------------------------------------ the input schema

  // Every input carries this envelope. `classify` marks the fields the tree reads; the rest place the input in time and
  // provenance. A required field that is missing refuses the input before the tree runs.
  const INPUT_SCHEMA = [
    { group: '身份', field: 'input_id', meaning: '这条信息的固定编号', required: '必填' },
    { group: '身份', field: 'content_sha256', meaning: '由内容算出的指纹；同样的内容只收一次', required: '必填' },
    { group: '身份', field: 'copy_of', meaning: '以前收过同样的内容时，写原来那条的编号；有就并过去', required: '有原件时', classify: true },
    { group: '身份', field: 'supersedes', meaning: '更新版写明它替换的是哪一版（新闻更新、10-K/A、改过的帖子、数据修正、类别改了）；新版不覆盖旧版', required: '有前版时' },
    { group: '来源', field: 'channel', meaning: '从哪个渠道来：接口、通稿平台、转载站、EDGAR、社交或投稿平台、你的上传', required: '必填' },
    { group: '来源', field: 'source_uri', meaning: '原始地址；SEC 文件写文件编号，帖子写帖子编号', required: '必填' },
    { group: '来源', field: 'publisher', meaning: '作者，也就是对内容负责的一方，不是转发它的渠道；社交帖子写账号', required: '必填', classify: true },
    { group: '来源', field: 'publisher_type', meaning: '作者是哪种：公司、媒体、分析方、官方、个人；先查作者表（看发布那天是否在有效期内），查不到用渠道的默认类型', required: '查表或渠道给', classify: true },
    { group: '来源', field: 'event_organizer', meaning: '会议、访谈这类口头活动是谁办的：公司、投资者会议、媒体、官方、专家网络、你；决定文字稿算谁的', required: '文字稿', classify: true },
    { group: '来源', field: 'authors', meaning: '署名的人，或账号背后的真实身份；用来把观点算到人头上', required: '可选' },
    { group: '来源', field: 'derived_from', meaning: '出自哪条信息（比如 XBRL 数字出自哪份 10-K）', required: '有出处时' },
    { group: '来源', field: 'context', meaning: '帖子的上下文：回复的谁、引用了谁、在哪个帖子串或版块', required: '可选' },
    { group: '时间', field: 'period', meaning: '内容讲的是哪段时间：哪个财期、观察期、事件发生日', required: '定期报告和数据' },
    { group: '时间', field: 'published_at', meaning: '发布方公开它的时间；只看是纽约时间的哪一天（发布日）；重复的取最早那天', required: '必填' },
    { group: '时间', field: 'filing_date', meaning: 'SEC 的法定申报日（下午 5:30 以后受理的算下一个工作日）；判断时不用它', required: 'SEC 文件' },
    { group: '时间', field: 'retrieved_at', meaning: '我们拿到它的时间；只用来留底，不参与任何判断', required: '必填' },
    { group: '分类', field: 'is_structured', meaning: '是表格还是文字（这是形式，不是类别）：表格是有固定字段的记录（JSON、XBRL、XML、CSV、上传模板），查数据集表、由程序读；文字按分类规则判、由模型读', required: '必填', classify: true },
    { group: '分类', field: 'has_readable_text', meaning: '有没有能读的文字：音频、视频、图片、没有文字层的扫描件都算没有', required: '文字必填', classify: true },
    { group: '分类', field: 'dataset', meaning: '来自哪个数据集、接口或上传模板；接入时登记一次属于哪一类，每条记录都直接用它', required: '表格', classify: true },
    { group: '分类', field: 'filing_system', meaning: '来自哪个申报系统：EDGAR、港交所、法院案卷……；每个系统一张表格代码表', required: '申报文件', classify: true },
    { group: '分类', field: 'filing_form', meaning: '表格代码：10-K、10-K/A、8-K、DEF 14A、425……', required: '申报文件', classify: true },
    { group: '分类', field: 'filing_items', meaning: '8-K 里有哪几项，以及业绩那一项（2.02）点名了哪些附件', required: '8-K', classify: true },
    { group: '分类', field: 'exhibit', meaning: '附件编号和说明：99.1 业绩稿、4.1 债券契约、10.1 重大合同……', required: '附件', classify: true },
    { group: '分类', field: 'document_format', meaning: '形式：逐字稿、纪要、备忘录、报告、幻灯片、文章、信、帖子；渠道写明，上传必须写明；长短和平台只是属性', required: '文字', classify: true },
    { group: '分类', field: 'channel_category', meaning: '来源标的栏目：媒体的新闻、评论、分析、转载的新闻稿；IR 网站、通稿、数据室的业绩、定期报告、法律文件', required: '可选（没有就按默认）', classify: true },
    { group: '分类', field: 'series', meaning: '发布系列，任何发布方都可能有（官方或民间）：FOMC 声明、褐皮书、ISM PMI、世界经济展望……；在发布系列表里登记过才起作用，没登记的放进人工复核池', required: '可选（没有就看作者）', classify: true },
    { group: '内容', field: 'media_type', meaning: '文件格式：网页、PDF、JSON、XML、CSV、Excel、音频、视频、图片', required: '必填' },
    { group: '内容', field: 'language', meaning: '语言', required: '必填' },
    { group: '对象', field: 'object_identifiers', meaning: '渠道给的对象代码，每个写三样：哪种代码（CIK、股票代码、名称、加密货币代码、商品代码、主题编号）、代码本身、为什么挂在这条上（申报对象、申报人、数据字段、渠道标签、上游为它推的、上传时写明的）；可以没有', required: '可选' },
  ];

  const OUTPUT_FIELDS = '一个类别，加上它讲的是哪些对象（对象编号、种类、为什么挂在这条上）和查不到的代码（原样留着）；或者并到原来那条；或者“不算材料”；或者不合格并写明原因';

  // Which objects an input concerns (D1, D11). Read off the identifiers the channel gives, never off the text; no model.
  const OBJECT_RULES = [
    '对象有四种：公司、加密货币、商品、主题（和研究对象名单一样）。一条信息可以讲好几个对象，也可以一个都没有。',
    '讲的是谁，只看渠道给的对象代码（申报对象、申报人、数据字段、渠道标签、上游为它推的、上传时写明的），再加上作者本人——只限作者是公司的时候（通稿算发稿的公司，公司自己讲的会议算这家公司）。每个对象都写明为什么挂在这条上。代码的种类或理由不在规定范围内、或者是空的，整条不合格。',
    '代码按种类分开写，因为同一个代码在不同种类里可能指不同的东西：公司用 CIK、股票代码、名称；加密货币用加密代码；商品用商品代码；主题用主题库的编号。',
    '主题只有两个来处：上游为这个主题推来的，或者上传时写明的；不从正文里猜。',
    '只看代码，不读正文，也不看网址：代理申报机构的编号会出现在网址里（旧数据里 Amazon 有一份 8-K，网址里是代理机构的编号 1104659）。',
    '公司、加密货币、商品的代码去参照数据里查：CIK 补足 10 位；股票代码按发布那天的对应关系查（FB 在 2022-06-09 以前是 Meta，之后不是）；名称只认登记过的别名。主题编号去主题库里查。查不到的原样留着，记为“查不到”，这条信息照常处理，等登记后再补。',
    '作者不是公司的时候（媒体、分析方、官方、个人），作者不算这条讲的对象；申报人和申报对象都留着，写明谁是谁（比如 13D 里，激进投资者是申报人，被持股的公司是申报对象）。',
    '正文里顺带提到的公司或主题，不在这里标；模型读的时候在具体事实上标。',
    '重复的并到原来那条时，讲的对象取两边的合集。讲的是谁不影响类别。不合格的和“不算材料”的，不标对象。',
  ];

  const TIME_RULES = [
    '时间只看“哪一天”：每条信息按纽约时间算是哪天发布的；几点几分不参与任何判断，同一天的信息不分先后。',
    '每条信息只有一个时间：它的发布日。内容讲的是哪段时间（比如哪个财季）只是属性。系统里没有“今天是哪天”这个概念。',
    '渠道晚了几天才拿到，不另外记。任何规则都不看电脑时间；我们拿到它的时间只用来留底。',
    'SEC 文件按 EDGAR 受理那天算发布日（纽约时间），不按法定申报日。',
    '重复的并到原来那条后，发布日取最早的那天：市场最早在哪里看到，就从那天算知道。',
    '修正、更新、重述、编辑、类别改了，都是新版本，旧版本留着，不覆盖。',
    '没有发布时间的信息放不到时间线上，不合格。',
  ];

  const RULES = [
    '类别按“信息是什么”分；是文字还是表格、多长、发在哪、从哪个渠道来，都只是属性。同一类信息可以是文字也可以是表格，形式只决定由模型读还是程序读。',
    '每条信息只有一个结果：一个类别、并到原来那条、“不算材料”，或者不合格并写明原因。判断只用固定规则和对照表，不用模型。',
    '作者是对内容负责的一方，不是转发它的渠道：通稿平台、转载站、文字稿供应商、数据商、社交和投稿平台、EDGAR 上的代理申报机构、你的上传，都只是渠道。',
    '作者是哪种，先查作者表；查不到就用渠道的默认类型（新闻索引默认是媒体，通稿默认是公司，社交、投稿和 newsletter 平台上的账号默认是个人）；两样都定不了才算不合格。有没有登记过，记为属性。国际组织（IMF、世界银行、OECD、OPEC、WTO）算官方。',
    '作者表里每一条都有有效期，按发布那天查，按任期算、不按影响力算：同一个账号在任期内算官方，任期外（竞选期间、当选还没就职、卸任以后）算个人。',
    '发布系列先于作者：登记过的发布系列按表归类，不管发布方是官方、民间、媒体还是公司（ISM 的 PMI 报告 → T11，Reuters 的经济学家调查 → T8，CBO 预算展望 → T8，CBO 月度赤字数据 → T11）。',
    '会议、访谈这类口头活动的文字稿，按谁办的定作者：公司办的、在投资者会议上发言的算公司；媒体办的算媒体；听证会、庭审算官方；专家网络办的算专家网络；你约的会面算你。',
    '申报文件先查表格代码表，不管谁提交的：每个申报系统（EDGAR、交易所、法院案卷）一张列全的表；修正版（/A）和原表格同一类；表里没有的代码不合格，放进人工复核池，登记后再收。',
    '8-K 里只有 Item 2.02 那一段点名的附件才算业绩发布；同一份 8-K 的其他附件各按自己的类型判断。',
    '一份申报的正文和每个附件各算一条信息；带 XBRL 数字的申报另外产生一批表格记录（T2），注明出自哪份申报；持股类申报（Form 4、13D/G、13F、144）用表格版本，归 T13。',
    '以前收过的同一内容（指纹相同，或和原件对得上），并到原来那条，算原来那条的另一个出处，类别跟原来那条一样。',
    '同一种内容不因作者、长短而换类别：作者是谁（券商、评级机构、媒体评论员、投资者、个人、你自己……）、多长、发在哪，都只是属性；长短只决定怎么切开来读。观点和估计算作者说的。',
    '手动上传必须写明是哪种文字或用的哪个表格模板，没写的不合格；系统自己的产出不算信息。',
    '一个表格接口返回好几种东西的，按东西拆成多条；别人算好的指标、文件目录不算信息。',
    '文档里引用别人的话，在具体事实上算原来说话的人说的；文档本身的类别不变。',
    '只是附带情况不同的，记为属性：渠道、平台、长短、摘要还是全文、在哪开的、谁办的、年报还是季报、是不是持仓、是不是高管、有没有登记。',
  ];

  // The lookup tables the tree reads (D8). Each is looked up by its key; what comes out is a tag, or an author type.
  const LOOKUP_TABLES = [
    { table: '数据集表', lookup: '数据集 → 类别，或“不算材料”', example: '日线行情 → T12；财务报表 → T2；ISM PMI、领先指标 LEI → T11；GDPNow → T8；技术指标、恐惧贪婪指数 → 不算材料' },
    { table: '表格代码表（每个申报系统一张）', lookup: '表格代码 → 类别；8-K 和 6-K、425、持股类表格光看代码定不了，按规则再分', example: '10-K → T2；DEF 14A → T3；8-K → 看里面有哪几项、哪些附件' },
    { table: '发布系列表', lookup: '（发布方，系列）→ T8、T10 或 T11；任何发布方都能登记，T10 只给官方', example: 'FOMC 声明、褐皮书、ISM PMI → T11；IMF 世界经济展望、CBO 预算展望 → T8；OFAC 制裁公告 → T10' },
    { table: '作者表', lookup: '作者 → 作者是哪种（公司、媒体、分析方、官方、个人），每条有有效期；查不到用渠道的默认类型', example: 'Reuters → 媒体；Morgan Stanley → 分析方；IMF → 官方；总统个人账号在任期内 → 官方' },
  ];

  const LOOKUP_RULES = [
    '四张表放在同一份 JSON 数据文件里，正式运行和测试读同一份。改了表，就是分类的新版本。',
    '前三张查出来直接是类别，不经过中间名称。作者表查出来是作者的种类，不是类别：同一个作者会落到不同类别（Reuters 的新闻归 T7，评论栏目归 T8），还要看栏目、形式或发布系列。',
    '登记的原则（数据集表和发布系列表一样）：统计数据，官方民间都算 → T11；央行关于货币政策和经济形势的材料（声明、纪要、讲话、点阵图、褐皮书）→ T11，央行的研究和工作论文 → T8；预测、展望、研究 → T8；行动和记录 → T10，只限官方。衡量整体经济或整个行业的 → T11；针对具体公司、产品、地点、链和协议的 → T15。',
    '读文件时只检查一件事：查出来的值必须有效（数据集表：16 个类别之一或“不算材料”；表格代码表：类别或规则；发布系列表：T8、T10、T11 之一，T10 只给官方；作者表：5 种作者之一），不对就不启动。',
    '表里没有的（新数据集、新表格代码、新发布系列、新作者）不猜，放进人工复核池，由人登记。',
    '代码和对象的对照（比如 AAPL 对应 Apple）不是分类的表：它不决定类别，只用来认出信息讲的是谁、检查研究对象名单。分类在上游做，这张表也归上游管，以后再谈。',
  ];

  const NOT_SOURCES = [
    '别人算好的指标：用我们已有的信息就能自己算出来的（估值倍数、因子暴露、技术指标、用价格或成交算出来的情绪指标，比如恐惧贪婪指数），数据商给的一律“不算材料”。我们自己算不出来的（权重不公开，或底层数据拿不到）按它是什么归类：领先指标 LEI、金融条件指数 → T11；GDPNow 这种实时预测 → T8。',
    '文件目录（EDGAR 文件列表、新闻搜索结果）：只用来找到信息，本身不算信息。',
    '没有文字的音频、视频、图片、扫描件：不合格；只能通过文字稿进来（T4、T7、T9、T10）。',
    '系统自己的产出（报告、导出、被转载的内容）：不合格，免得自己引用自己。',
    '股票池、观察列表属于研究对象名单；你自己的持仓、交易、盈亏和投资授权不算信息，放在哪以后再定。',
  ];

  // ------------------------------------------------------------------ the drill-down

  const FORM_LABELS = { '两者': '文字和表格', '文本': '文字', '结构化': '表格' };

  const CIRCLED = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨'];

  // Every path to each tag, read off the tree, for the schema table.
  function tagPaths(branch, trail, paths) {
    const here = trail.concat(branch.label);
    (branch.tags || []).forEach((code, index) => {
      const path = here.slice(1).join(' › ') + (branch.ordered ? ` › ${CIRCLED[index]}` : '');
      (paths[code] = paths[code] || []).push(path);
    });
    (branch.children || []).forEach((child) => tagPaths(child, here, paths));
    return paths;
  }

  function branchBox(branch, escapeHtml, isRoot) {
    return `<div class="org-node${isRoot ? ' org-node--root' : ''}">`
      + (branch.family ? `<span class="org-node__family">${escapeHtml(branch.family)}</span>` : '')
      + `<span class="org-node__label">${escapeHtml(branch.label)}</span>`
      + (branch.question ? `<span class="org-node__question">${escapeHtml(branch.question)}</span>` : '')
      + (branch.field ? `<span class="org-node__note">${escapeHtml(branch.field)}</span>` : '')
      + (branch.merge ? `<span class="org-node__refuse">${escapeHtml(branch.merge)}</span>` : '')
      + (branch.refuse && branch.children ? `<span class="org-node__refuse">${escapeHtml(branch.refuse)}</span>` : '')
      + '</div>';
  }

  function tagCard(code, order, branchLabel, escapeHtml) {
    const tag = TAGS[code];
    const rule = tag.rule;
    return `<button class="org-tag" type="button" data-tag="${code}">`
      + (order ? `<span class="org-tag__order">${order}</span>` : '')
      + `<span class="org-tag__top"><span class="org-tag__code">${code}</span><span class="org-tag__label">${escapeHtml(tag.label)}</span></span>`
      + `<span class="org-tag__rule">${escapeHtml(rule)}</span>`
      + '</button>';
  }

  function renderBranch(branch, escapeHtml, isRoot) {
    let below = '';
    if (branch.children) {
      below = `<ul>${branch.children.map((child) => `<li>${renderBranch(child, escapeHtml, false)}</li>`).join('')}</ul>`;
    } else if (branch.tags) {
      below = '<div class="org-stack">'
        + branch.tags.map((code, index) => tagCard(code, branch.ordered ? CIRCLED[index] : '', branch.label, escapeHtml)).join('')
        + (branch.notInput ? `<div class="org-tag org-tag--outcome">${escapeHtml(branch.notInput)}</div>` : '')
        + (branch.refuse ? `<div class="org-tag org-tag--refuse">${escapeHtml(branch.refuse)}</div>` : '')
        + '</div>';
    }
    return branchBox(branch, escapeHtml, isRoot) + below;
  }

  // Scale the tree down, never up, so the whole of it is in view.
  function fitTree(container) {
    const frame = container.querySelector('.org');
    const tree = container.querySelector('.org-tree');
    tree.style.zoom = '1';
    const scale = Math.min(1, (frame.clientWidth - 8) / tree.scrollWidth);
    tree.style.zoom = String(scale);
  }

  const design = window.HIVEMIND_DESIGNS.new;
  design.drilldowns = design.drilldowns || {};
  design.classification = { TAGS, TREE, INPUT_SCHEMA };
  design.drilldowns.classify = {
    button: '展开分类规则：16 个类别怎么判',
    kicker: '分类 · 详细说明',
    size: 'full',
    render(container, context) {
      const escapeHtml = context.escapeHtml;
      const paths = tagPaths(TREE, [], {});
      const total = Object.keys(TAGS).length;
      const schemaRows = Object.keys(TAGS)
        .sort((first, second) => Number(first.slice(1)) - Number(second.slice(1)))
        .map((code) => {
          const tag = TAGS[code];
          return `<tr id="tag-row-${code}"><td><span class="org-tag__code">${code}</span></td>`
            + `<td><code>${escapeHtml(tag.name)}</code><div class="schema-table__label">${escapeHtml(tag.label)}</div></td>`
            + `<td>${escapeHtml(FORM_LABELS[tag.forms])}</td><td>${(paths[code] || []).map(escapeHtml).join('<br>')}</td><td>${escapeHtml(tag.decide)}</td>`
            + `<td>${escapeHtml(tag.definition)}</td><td class="schema-table__quiet">${escapeHtml(tag.examples)}</td></tr>`;
        }).join('');
      const schemaFieldRows = INPUT_SCHEMA.map((row, index) => {
        const firstOfGroup = index === 0 || INPUT_SCHEMA[index - 1].group !== row.group;
        return `<tr class="${firstOfGroup ? 'schema-table__group-start' : ''}"><td class="schema-table__group">${firstOfGroup ? escapeHtml(row.group) : ''}</td>`
          + `<td><code>${escapeHtml(row.field)}</code></td><td>${escapeHtml(row.meaning)}</td>`
          + `<td class="schema-table__quiet">${escapeHtml(row.required)}</td><td>${row.classify ? '✓' : ''}</td></tr>`;
      }).join('');

      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">分类规则：每条信息归到哪一类</h2>
          <p class="drill__intro">分类由上游完成：推给我们的每条信息，都已经按这里的规则贴好类别、标明讲的是谁；我们照着这里检查。上游只推研究对象名单范围内的信息。一共 ${total} 个类别，按“信息是什么”分成 5 个大类，每个类别只出现一次。是文字还是表格只是形式，决定由模型读还是程序读。点任意一个类别，跳到它的定义。</p>
          <p class="drill__status"><span class="pill pill--strong">第一版已冻结 · 2026-10-16</span>用旧系统 412 条真实材料和 161 个手写例子测过，全部分对；“讲的是哪家公司”测了 24 个例子，也全对。只测了公司；宏观类的规则和加密、商品、主题是推演出来的，还没跑测试。改了规则要重跑 <code>python3 docs/system-design/simulate_classification.py</code>，必须全部通过。</p>
          <div class="org"><div class="org-tree"><ul><li>${renderBranch(TREE, escapeHtml, true)}</li></ul></div></div>
          <section>
            <h3 class="drill__heading">判断顺序：一条信息怎样找到它的类别</h3>
            <ol class="drill__rules">${ROUTING.map((step) => `<li>${escapeHtml(step)}</li>`).join('')}</ol>
          </section>
          <section>
            <h3 class="drill__heading">对照表：分类时要查的四张表</h3>
            <table class="schema-table schema-table--compact">
              <thead><tr><th>表</th><th>拿什么查，查出什么</th><th>例子</th></tr></thead>
              <tbody>${LOOKUP_TABLES.map((row) => `<tr><td>${escapeHtml(row.table)}</td><td>${escapeHtml(row.lookup)}</td><td class="schema-table__quiet">${escapeHtml(row.example)}</td></tr>`).join('')}</tbody>
            </table>
            <ul class="drill__rules">${LOOKUP_RULES.map((rule) => `<li>${escapeHtml(rule)}</li>`).join('')}</ul>
          </section>

          <div class="drill__columns drill__columns--schema">
            <section>
              <h3 class="drill__heading">每条信息要带的字段</h3>
              <table class="schema-table schema-table--compact">
                <thead><tr><th>分组</th><th>字段</th><th>意思</th><th>必填</th><th>分类时用</th></tr></thead>
                <tbody>${schemaFieldRows}</tbody>
              </table>
              <p class="drill__output"><strong>分类结果：</strong>${escapeHtml(OUTPUT_FIELDS)}</p>
            </section>
            <section>
              <h3 class="drill__heading">时间规则</h3>
              <ol class="drill__rules">${TIME_RULES.map((rule) => `<li>${escapeHtml(rule)}</li>`).join('')}</ol>
              <h3 class="drill__heading drill__heading--spaced">分类规则</h3>
              <ol class="drill__rules">${RULES.map((rule) => `<li>${escapeHtml(rule)}</li>`).join('')}</ol>
              <h3 class="drill__heading drill__heading--spaced">讲的是谁（相关对象）</h3>
              <ol class="drill__rules">${OBJECT_RULES.map((rule) => `<li>${escapeHtml(rule)}</li>`).join('')}</ol>
              <h3 class="drill__heading drill__heading--spaced">不算信息的东西</h3>
              <ul class="drill__rules">${NOT_SOURCES.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>
            </section>
          </div>

          <section>
            <h3 class="drill__heading">${total} 个类别</h3>
            <table class="schema-table">
              <thead><tr><th>编号</th><th>类别</th><th>形式</th><th>所在大类</th><th>怎么判</th><th>定义</th><th>例子</th></tr></thead>
              <tbody>${schemaRows}</tbody>
            </table>
          </section>
        </div>`;

      container.querySelectorAll('[data-tag]').forEach((card) => card.addEventListener('click', () => {
        const row = container.querySelector(`#tag-row-${card.dataset.tag}`);
        row.scrollIntoView({ behavior: 'smooth', block: 'center' });
        row.classList.remove('schema-table__row--flash');
        void row.offsetWidth;
        row.classList.add('schema-table__row--flash');
      }));
      requestAnimationFrame(() => fitTree(container));
      window.addEventListener('resize', () => { if (container.isConnected) fitTree(container); });
    },
  };
})();
