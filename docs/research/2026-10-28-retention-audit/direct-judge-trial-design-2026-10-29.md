# 小试验：让评委逐条判，而不是自己先挑

2026-10-29，发送前设计。原评委在你已判断的八项上三次各 3/8；新加坡案件的旧回答范围不完全相同，单独列出、不纳入旧分数。它自己读文章并挑事实，可能在“找事实”和“判断价值”之间丢失信息。假设：明确给出待判事实，可以单独测它是否理解你的核心／次要／不留标准。这个试验只测**已给事实的价值判断**，不测它能不能从全文找全事实，也不测页面或产品质量。

试验组给同一组六篇原文、当时问题及九段待判原句，要求每项给核心、次要或不留并解释。对照组保持原先的自由阅读任务和完整六篇输入，重新独立发送三次；试验组三次。两种任务不同，分数不能直接称作改进了识别完整率，只用对照衡量原任务的波动，用试验组检验新任务能否对齐你的九个明确判断。九项包含你对第 6 题的三个子项均为 B 的既有解释。九项均是开发案例，已经看过旧回答，不能称作未见测试。

发送前固定输入、九项用户答案、提示、文件摘要和评分规则。新加坡只问你实际排除的四家公司案件概况，不把其他个人资产细节算成已裁定。每项必须读该篇原文，保留计划、估计、说话人与时间的不确定性；一个返回必须有九个唯一 ID，任何缺项、重复 ID、无效标签、拒答或调用失败均记录并判本次未完成，不自动重试。预先以三次试验均 9/9 作为这九项对齐的最低条件；即使达到，也只能说这九项通过，不能用于大批量自动验收，仍须真正未见案例、语义和正确页面验证。这个全对门槛会放大偶然波动：若每项每次独立正确概率是 95%，27 项全对的概率仅约 25%；这个数字只是举例，不是该模型的实测正确率。对照组只按明确的八项计分，如三次自己不能稳定回答，就不作提升声称。失败后停止，不继续叠加提示词。

| 状态 × 事件 | 动作 |
|---|---|
| 未发送 × 输入、用户判断及摘要齐全 | 只创建新日期目录并固定文件；原金标、旧答案保持只读。 |
| 未发送 × 来源原句不在相应原文、九项不全或摘要不符 | 拒绝发送。 |
| 进行中 × 成功／拒答／故障 | 各次独立留输出和状态；缺少完整九项不计成功。 |
| 进行中 × 中断／同名结果已存在 | 保留已存在输出，不覆盖，不把部分结果当完整；不自动重发。 |
| 已完成 × 再运行 | 因结果目录已存在而拒绝；新一轮须新目录与事先登记。 |

| 写入值 × 读者／来源 | 合同 |
|---|---|
| 六篇原文、历史问题 | 来自已有六篇开发输入；两个任务都读取相同全文和问题。 |
| 九段候选原文 | 每项原句逐字来自对应文章；只用于定位，原文仍须整篇读；不含用户标签。 |
| 九项标准 | 单独文件来自 Alex 的九项具体裁定；评委不可读取，评分脚本和人可读。 |
| 模型输出 | 每次一个原始输出；试验输出的 ID 和标签必须完整，理由原样保存。对照沿用原输出形状并逐条人工映射。 |
| 得分 | 只统计是否符合该项“留／不留”和主次；对来源、内容、引用、对应问题另列，不把一个分数当整体质量。 |

实验形状的旧检查：文章身份、原句、日期、结果完整性、标签闭集、保留预测和来源、缺页不自动视为垃圾，均需满足。原自由阅读任务不接收候选答案。试验组得到候选是特意改变输入，不能拿它证明模型自主寻找更完整。对照和试验均使用此前评委同一模型，不修改产品模型、配置、预算或提示词。

已有决定边界：D214 要求正式比较之前先对齐标准；这里只使用 Alex 自己决定的九项，作开发校准，不能当产品验收。D215 保持旧金标不变、页面未决；D209 不改丢弃行为；不进行整条流程。

## 复核后补齐：输入、计分和费用

[第一轮独立复核](direct-judge-trial-independent-review-2026-10-29.txt)指出控制组可能把整篇漏答当正确排除、原句和输出形状未固定、自由阅读结果如何对照未定、费用缺少可执行上限、两个任务的分数不能视为同一件事。以下逐项补齐；这仍是发送前设计，不是运行结果。

九项只来自以下文章和原句，其他全文作为上下文照原样提供。`a` 到 `i` 只是试验编号；标签文件仅供评分，不发给评委。精确原句须在各自全文中逐字找到，否则不发送。

| 编号／用户题 | 原文 input_id | 精确定位原句或片段 | 用户判断 |
|---|---|---|---|
| a / 1 | gnews:71df54965281684cc500960f | `That sounds like further revenue growth ahead`、`For the rest of this year, they expect 82% growth. For 2027, that figure rises to 41%.` | core |
| b / 2 | gnews:71df54965281684cc500960f | `For fiscal 2028, ending January 2028, the average analyst projects $12.76 in earnings per share.` | exclude |
| c / 3 | gnews:fbce0469dbb5b33e2c34a0f5 | `2027 is set to be the “worst year” for the memory shortage and said that the crunch will last until 2030.` | core |
| d / 4 | gnews:55b3b854d30ecb73679c2088 | `AMD estimates its EPYC 9965 (Turin) chip delivers approximately 2.4x`、`EPYC 6 (Venice) projected to extend that advantage to roughly 3.3x`；同段注明 100kW 和 AMD 的模型估算 | colour |
| e / 5 | gnews:1eeceeb212a2c82c2e75e806 | `The four companies will also face a total of eight charges of fraud by false representation`、`servers in question, which may have contained advanced Nvidia AI chips` | exclude |
| f / 6a | gnews:f9e7da6ddbf890fa64baf922 | `released a letter Friday urging policymakers to avoid "premature restrictions" on open-weight artificial intelligence models` | colour |
| g / 6b | gnews:f9e7da6ddbf890fa64baf922 | `the Trump administration would look into whether Chinese companies were stealing American intellectual property` | colour |
| h / 6c | gnews:f9e7da6ddbf890fa64baf922 | `China's Moonshot AI developed its Kimi K3 model by distilling Anthropic's technology` | colour |
| i / 7 | gnews:71df54965281684cc500960f | `it expects hyperscaler spending to top $1 trillion in 2027 after reaching a projected $650 billion in 2026` | core |

对照的提示沿用原提示正文，但原来由 Codex 读文件，现在由同一 OpenAI 模型 API 直接收到同样的六篇输入；必须明说这是执行方式改变，不能将它当成原来 Codex 会话的完全相同请求。试验组也采用同一 API 和模型、六篇全文、历史问题，再加九项各自的原句定位。试验组的完整任务要求：

> 你是投资 NVIDIA 的资深对冲基金分析师。逐篇读提供的正文和当时的问题。对每个指定事项独立判断：core 是当天应重点记录、可能改变投资看法；colour 是值得保留的辅助信息；exclude 是此项不需要留下。判断投资意义，不因数字或名字就自动保留，也不因是预测、第三方或缺页面就自动排除。按照原文保留谁说的、时间、预测与实际和不确定性。每项输出唯一 id、label、依据原文写的 meaning、原文 quote 和判断理由 why。只输出要求的九项，不输出额外项；不确定时 label 写 uncertain。页面是否正确不在此任务中。

试验回答是严格 JSON 对象，唯一字段 `items` 是 9 项数组；每项唯一字段 `id`（a–i）、`label`（core/colour/exclude/uncertain）、`meaning`、`quote`、`why`，后三项均为非空字符串。重复、缺失或额外 ID，或其他结构不符，整个样本不计分。每个引用必须是该条对应文章原文逐字子串；错误引用单列，不能因标签正确声称整条通过。人工逐条核 `meaning` 的主体、指标、两个期间、预测、数量及限制；漏“收入”等记内容错误，不改标签分。`uncertain` 保留并视为与用户标签不一致，不改成 exclude。每次理由保留原样。

对照回答仍是原 `articles` 形状，必须返回全部六个已知文章 ID，各一次，且每个 facts 为数组；整篇缺失或结构错误的样本无效，不能把任何缺项视为正确排除。有效样本由人对照上述八个已裁定的事项和原始事实内容：全部要点同一条或多条共同表达且权重一致才算找到；只给部分记 partial；多条权重冲突或身份不确定记 ambiguous；两者均不暗中算遗漏或正确。明确无匹配且对应文章有效才算 omitted；所给来源、页面和其他新事实分别保留、不自动算垃圾。新加坡控制组回答所指细节范围不一，不纳入八项得分。两组任务不同，数字只是各自任务上的观察，不是经济判断能力改善的受控估计。

费用和执行：沿用 `gpt-6.1-terra`，OpenAI API 标准服务；三次对照、三次试验，最多六次请求，无自动重试。按[官方 API 价格](https://developers.openai.com/api/docs/pricing)，该模型每百万输入 $1、每百万输出 $5；[模型说明](https://developers.openai.com/api/docs/models/gpt-6.1-terra)给出的 30 分钟缓存写入为每百万 $1.25，按更高的 $1.25 计入全部输入作保守估计。实际费用按返回的 usage 记录，缺 usage 标未知而不是 $0。不得开快速服务、额外重试或提高上限。请求失败可能仍收费，预算仍按整次保留；所有六个位置的预算发送前一起预留，不以并发期间的已完成费用冒充总风险。单次超时 180 秒，未完成保留失败，不补发。发送前用修复后的 preflight 重放 98 个存档并核对已知拒绝；API 凭证不存在、模型不可用、服务或实际计费规则不符时直接停止。

第二轮只读复核对第一轮的处理提出四处剩余问题：[记录](direct-judge-trial-independent-review-v2-2026-10-29.txt)。以下进一步固定合同，不以复核本身作为发起试验的许可。

1. 对照实际系统消息逐字为：`你是投资 NVIDIA 的资深对冲基金分析师。输入包含六篇文章的原文和当时已知的问题；不要使用其他资料。逐篇读完正文及当时的问题，找出会实质影响对 NVIDIA 业务、风险、增长、竞争、定价或产品判断的信息；一篇可以没有或有多条。既考虑定量，也考虑有明确经济意义的定性事实。可决定哪些值得当天重点记录 core、哪些只作次要但有意义的 colour；单纯有数字、名字、话题相关不足以证明有价值。区分发布者、原始说话人、时间、事实与估计或计划；有重要信息但没有现成问题时也报告，并将 pages 留空。记者观点、推广、重复旧事实、无规模的规格跑分、股价和仓位通常不是新业务事实，但必须看具体上下文，别机械判断。每篇按输出结构返回 input_id、facts 和 excluded；facts 含 quote、meaning、weight、pages 和 why。六篇各一条，一项事实只记一次；对信息或归属不确定就说清，不许根据后来的事件补事实。` 用户消息为六篇历史输入的紧凑 JSON；结构化输出闭集：`articles` 数组，每项只有 `input_id`、`facts`、`excluded`；每条 fact 只有 `quote`、`meaning`、`weight`（core/colour）、`pages`（字符串数组）、`why`。此为 API 新鲜对照，不是旧 Codex 会话的完全相同请求；两个任务差异无法归因于单一原因。
2. 对试验组逐项保存三套判断：标签与用户是否一致、整篇原文是否支持 meaning、引用是否本身覆盖 meaning 全部实质内容。引用必须既是正确文章逐字原句，又由人工判断是否支持完整意思；例如 a 要同时支持收入、82%、41% 和对应期间。缺一部分记不支持；不能仅因引文是原文子串通过。模型写的解释错或引文不足，即使标签对也不能说该项整体通过；三次 9/9 仅指标签对齐。
3. 对照每项保留该篇完整回答、对应 fact 的数组索引、原始事实及人工理由；拆分可共同覆盖但权重必须一致，部分覆盖或身份不明均标未定，冲突也标未定，不判正确或自动当遗漏。每次的八项计 correct、incorrect、unresolved，三者相加恒为 8；无效样本不产生得分。没有输出对应事实且该篇完整时，用户要求保留者为 incorrect，用户排除者为 correct。引用、完整原意和页面另判，不混入标签结果。评委在任何文章的 facts、excluded 或其他字段中明说拒答、无权阅读或未完整阅读，即使结构齐全也将该样本标无效，不能把缺项算为排除；语义无法确定是否拒答时标待审，不算通过。此规则同样适用于试验组理由里的拒答。[第三轮复核](direct-judge-trial-independent-review-v3-2026-10-29.txt)指出仅检查字段无法识别文章内拒答。
4. 不再靠 UTF-8 字节推算最终 token。改用 [Responses 输入 token 计数接口](https://developers.openai.com/api/docs/guides/token-counting)，对已经固定的实际两种请求各计一次，包含模型、完整消息和输出 schema；只在接口返回准确计数、输入不超过模型限额、六次最坏费用加上两个计数请求的保守预留低于 $0.60 时发送。最坏费用按每次精确输入 token 的 $1.25/百万、每次最多 8,000 输出 token 的 $5/百万，以及两个计数请求各预留一次相同输入费用计算；若计数失败、费用无法确认或任何参数变化则停止。`max_output_tokens=8000`、`service_tier=default`、相同模型、独立请求、不重试，三个对照和三个试验并发发送。8,000 替代此前的 3,000，以免思考和六篇结果被截断；总上限仍为 $0.60，先计数再决定能否发。计数及六个生成调用无凭证写入日志或参数。

[第四轮复核](direct-judge-trial-independent-review-v4-2026-10-29.txt)发现拒答可能出现在试验组任何字段，且对照 `excluded` 类型未固定。统一规则：人工检查**任一输出字段**及 API 状态；明确拒答或未读完使样本无效，无法判断则样本待审，二者都不算通过。每条 meaning 与引文覆盖另判 `yes/no/uncertain`，`uncertain` 不算整体通过。对照每篇的 `excluded` 是字符串；文章、fact 和整个输出均为仅含规定字段的对象，`facts` 和 `pages` 均是数组，`quote`、`meaning`、`why` 均为字符串，`weight` 仅 core/colour；六篇 ID 必须完整且不重复。
