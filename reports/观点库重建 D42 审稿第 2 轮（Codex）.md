这轮还不能说全部改好了。
- 最要紧的是：修正版先撤下旧证据，第 6 步却看不到它，可能接不上改写关系，也无法把新说法送到旧证据关联的其他观点。
- 多观点合流解决了“存两次”，但“在一处重复、在另一处替代旧说法”仍无法完整表达。
- “替代哪几条”还有 4 处旧写法；另有 1 处定义、2 处例子没跟上。
- “只收到重复证据就不重判”还有 4 处缺少条件。
- 新连上已有证据后，重判引用这条证据，现有核对规则说得通，不另报问题。
- 只读核对：52 段生成内容一致，66 个用词检查片段无禁用词命中。没有修改文件。

以下次数均指**设计文本的位置数**，页面数据与 PRD 副本分别计；不是实际运行中的发生次数。讨论记录只用于理解意图，不计措辞问题。

**一、8 项改动逐条核对**

| 改动 | 结论 | 已落实及残留 |
|---|---|---|
| 1．修正版按句处理，删除可以没有后继 | **规则大体改好，流程未接完整。** | [06-views.md：161、204、341、353](/Users/lchingen/hivemind/docs/prd/06-views.md:161)已经区分保留、改写、删除。但[验收第 382 行](/Users/lchingen/hivemind/docs/prd/06-views.md:382)仍笼统要求“修正版的证据替代旧版的”，**1 处旧验收未改**。改句如何接回旧证据，见下文新问题 1。 |
| 2．多观点只对上、存储一次，重复时补连线 | **主规则改好了，组合情况没闭合。** | [06-views.md：165、195、200](/Users/lchingen/hivemind/docs/prd/06-views.md:165)、[new-facts.js：282、316、323](/Users/lchingen/hivemind/docs/system-design/new-facts.js:282)均已写明。新增连线也明确算该观点拿到新证据。但重复与替代同时成立时，见新问题 2。 |
| 3．比较输入带来源、时间、层、期间 | **主要契约改好了，摘要留了旧口径。** | [06-views.md：205、338、340](/Users/lchingen/hivemind/docs/prd/06-views.md:205)、[new-facts.js：328、450、452](/Users/lchingen/hivemind/docs/system-design/new-facts.js:328)已明确。只有[06-views.md：16](/Users/lchingen/hivemind/docs/prd/06-views.md:16)还说“证据按事情的时间排”，应改成“替代的先后按原始来源的时间排”，**1 处**。 |
| 4．替代先认关系，再按时间定方向 | **主流程改好，记录、标注、例子没全跟上。** | [06-views.md：165、196、202、352](/Users/lchingen/hivemind/docs/prd/06-views.md:165)的方向一致。残留共 **7 处**，见新问题 3。另有同日先后问题，见新问题 4。 |
| 5．至少挂一处，允许同时挂卡片和候选观点 | **改好了。** | [05-extraction.md：29、44、50–53、152](/Users/lchingen/hivemind/docs/prd/05-extraction.md:29)、[new-facts.js：69、78、85–90](/Users/lchingen/hivemind/docs/system-design/new-facts.js:69)、[new-design.js：92、93](/Users/lchingen/hivemind/docs/system-design/new-design.js:92)一致。观点库第 1 步也已只核出处。**未发现残留的互斥要求。** |
| 6．重复观点交查重，证据标注先记录 | **改好了。** | [06-views.md：289](/Users/lchingen/hivemind/docs/prd/06-views.md:289)、[new-facts.js：404](/Users/lchingen/hivemind/docs/system-design/new-facts.js:404)、[new-design.js：133](/Users/lchingen/hivemind/docs/system-design/new-design.js:133)、[DECISIONS.md：942、943](/Users/lchingen/hivemind/docs/DECISIONS.md:942)已分清对象。 |
| 7．按有效证据变化或依赖变化重判 | **主流程改好，否定句未全收紧。** | [06-views.md：169、378](/Users/lchingen/hivemind/docs/prd/06-views.md:169)已经完整。残留在[06-views.md：86](/Users/lchingen/hivemind/docs/prd/06-views.md:86)、[new-facts.js：214](/Users/lchingen/hivemind/docs/system-design/new-facts.js:214)、[new-design.js：111](/Users/lchingen/hivemind/docs/system-design/new-design.js:111)、[DECISIONS.md：946](/Users/lchingen/hivemind/docs/DECISIONS.md:946)，共 **4 处**仍单说“只收到重复证据就不重判”。统一改成“本轮没被替代的证据集合未变，且依赖未变，才不重判”，也能避开新增连线的歧义。 |
| 8．拆开“候选”，改搜索范围 | **这次指定的文字替换已完成。** | 正文没有遗留裸用的“候选”；[用词表第 105 行](/Users/lchingen/hivemind/docs/prd/00-system.md:105)已增加“清单”；[06-views.md：150](/Users/lchingen/hivemind/docs/prd/06-views.md:150)、[new-facts.js：295](/Users/lchingen/hivemind/docs/system-design/new-facts.js:295)的搜索范围正确。但“清单”自身又被用于别的对象，见用词统计。 |

**二、第一轮没报过的新问题**

**1．每一步手里有什么：修正版撤下的旧证据，第 6 步再也看不到**

修正版处理约定共 **7 处**：

- [06-views.md：161、204、353](/Users/lchingen/hivemind/docs/prd/06-views.md:161)
- [new-facts.js：278、327、463](/Users/lchingen/hivemind/docs/system-design/new-facts.js:278)
- [DECISIONS.md：929–932](/Users/lchingen/hivemind/docs/DECISIONS.md:929)

冲突发生在[第 6 步及其输入说明](/Users/lchingen/hivemind/docs/prd/06-views.md:165)：它只比较**没被替代的证据**。

具体走一遍：

1. 旧证据 e1“预计涨 12%”连着 A、B。
2. 修正版把它改成“预计涨 25%”，抽取的新证据 e2 只挂 A。
3. 第 2 步先把 e1 标成“被替代”。
4. 第 6 步看不到 e1，不能认出 e2 是它的后继。
5. 第 8 步“把新证据连到旧证据关联的其他观点”就缺少对应关系。B 会因撤下 e1 重判，却拿不到 e2。

这不是第一轮的“删句没有后继”：**删句确实不需要后继；改句需要辨认后继，目前把辨认所需的旧句提前移出了比较范围。**

最简单的改法：本轮被修正版撤下的旧证据，另作为历史输入交给第 6 步，只用于辨认改写关系，不恢复为有效证据；找到后继才传播到原关联观点，纯删除没有后继。第 7 步的编号核对也必须允许引用这份明确列出的历史输入。

**2．说的是不是同一件事：一次“重复”会吞掉另一处应做的“替代”**

排他选择或整条并入的直接约定共 **5 处**：

- [06-views.md：165、200](/Users/lchingen/hivemind/docs/prd/06-views.md:165)
- [new-facts.js：282、323](/Users/lchingen/hivemind/docs/system-design/new-facts.js:282)
- [DECISIONS.md：933–941](/Users/lchingen/hivemind/docs/DECISIONS.md:933)

现文要求每条证据只答一次：“重复哪条、替代哪些，**还是**新证据”；又规定任一观点下认出重复，整条就并过去。

但局部比较允许形成这个状态：

- A 下已有同一来源较新的 e2“涨 25%”。
- B 下仍有较旧的 e1“涨 12%”。此前 e2 没去 B，也没比较到 e1。
- 现在一条复述 e2 的证据同时去 A、B。

正确动作必须同时包含：**复用 e2、让 e1 被 e2 替代、把 e2 连到 B。**  
只答“重复 e2”，B 就会同时保留 12% 和 25%；只答“替代 e1”，又可能重复存 e2。

最简单的改法：仍只调用一次、只存一条，但把“复用哪条证据”和“它与哪些旧证据构成替代关系”分开表达，允许同一次结果同时成立。这不需要搜全库。

**3．用词和记录：模型判的是前后关系，记录却仍要求它指定替代方向**

共 **7 处**，分成三组：

- **4 处“替代哪几条”**：[06-views.md：277、286](/Users/lchingen/hivemind/docs/prd/06-views.md:277)、[new-facts.js：394、401](/Users/lchingen/hivemind/docs/system-design/new-facts.js:394)。
- **1 处旧定义**：[00-system.md：107](/Users/lchingen/hivemind/docs/prd/00-system.md:107)，仍定义为“替代让已有的那条过时”。
- **2 处例子**：[06-views.md：244](/Users/lchingen/hivemind/docs/prd/06-views.md:244)、[new-facts.js：371](/Users/lchingen/hivemind/docs/system-design/new-facts.js:371)，让晚到旧报告与 m1、m2 比，但 m1 已被替代，不在第 6 步规定的输入里。

例如晚到的 2 月报告，模型应答“与 m2 是前后两个说法”；它并不替代 m2。若标注仍问“替代哪几条”，正确标签要么无法填写，要么方向写反。

最简单的改法：

- 模型结果、人工标签统一写“与哪几条构成前后两个说法”。
- 最终写入记录另写清“哪条被哪条替代”，由时间排序决定。
- 用词表不要再把“已有的”固定为被替代方。
- 例子只与当前的 m2 比；m1 若出现，注明它只是历史背景。

**4．每一步手里有什么：同一天两个说法，时间还不能唯一决定方向**

直接冲突涉及 **4 处契约**：

- [02-classification.md：108](/Users/lchingen/hivemind/docs/prd/02-classification.md:108)：几点几分不参与判断，同一天按到达顺序排。
- [06-views.md：196](/Users/lchingen/hivemind/docs/prd/06-views.md:196)、[new-facts.js：317](/Users/lchingen/hivemind/docs/system-design/new-facts.js:317)：后说的算数。
- [DECISIONS.md：934–939](/Users/lchingen/hivemind/docs/DECISIONS.md:934)：输入是带日期的原始来源，方向不能按到达顺序定。

同一天上午说 12%、下午改成 25%，下午那份先到。现有约定既不能用到达顺序，也没有规定怎样从原始来源取得同日先后。仅有“哪一次、哪天”，不必然带有可排序的关系。

最简单的改法：补清同日原始披露的先后依据；无法确认先后的，不判定替代方向。不能让实现者自行拿到达顺序冒充发布时间，也不能未经决定就改变已冻结的分类时间规则。

**“证据和候选观点有没有分开讲清楚”这一类，没有发现第一轮之外的新问题。**  
这轮的双问分流、多挂、候选观点不开时只丢弃其独占证据，已经能互相接上。

**三、用词重新计数**

未把一般近义表达都算成术语问题。能够落到同一字段或不同决策对象上的，剩下这几组：

| 类别 | 全部位置、次数 | 最简单的改法 |
|---|---|---|
| **“清单”被用于候选观点比较、依赖挑选、证据比较三种对象** | 超出用词表定义的 **4 处、4 次**：[06-views.md：127、274](/Users/lchingen/hivemind/docs/prd/06-views.md:127)；[new-facts.js：262、391](/Users/lchingen/hivemind/docs/system-design/new-facts.js:262)。前两组分别是依赖挑选、对上证据。定义在[00-system.md：105](/Users/lchingen/hivemind/docs/prd/00-system.md:105)。 | 保留“清单”指对上候选观点的已有观点；依赖处写“供挑选的依赖观点”；记录表把公共栏目改为“比较对象”，分别写观点或证据。 |
| **“替代”同时表示无方向的前后关系、输入替掉已有证据** | 旧方向表达 **5 处、5 次**：上述“替代哪几条”4 处，加[00-system.md：107](/Users/lchingen/hivemind/docs/prd/00-system.md:107)。 | 按新问题 3 修改。不另算一类新缺陷。 |
| **“梯子”又叫“刻度”** | **2 处、2 次**：[06-views.md：75](/Users/lchingen/hivemind/docs/prd/06-views.md:75)、[new-facts.js：206](/Users/lchingen/hivemind/docs/system-design/new-facts.js:206)。两处都是指候选观点带来的整把梯子。 | “候选观点带的梯子一律不要”。 |
| **“事情发生的时间”还兼指数字所属期间** | 字段名出现 **5 处、5 次**：[05-extraction.md：45、153](/Users/lchingen/hivemind/docs/prd/05-extraction.md:45)、[06-views.md：340](/Users/lchingen/hivemind/docs/prd/06-views.md:340)、[new-facts.js：79、452](/Users/lchingen/hivemind/docs/system-design/new-facts.js:79)。其中后两份字段定义明确让它兼指“哪一期”。这是第一轮时间问题的用词残留，不算新发现。 | 写成“事情发生或生效的时间；数字所属期间”，不要让一个字段名暗示二者相同。 |
| **排序仍叫“按事情的时间排”** | **1 处、1 次**：[06-views.md：16](/Users/lchingen/hivemind/docs/prd/06-views.md:16)。 | 改成“替代的先后按原始来源的时间排”。同上，不另算新发现。 |

裸用“候选”、“只多了重复的观点”、旧搜索范围，本轮未发现残留。用词表列出的禁用写法，排除表内用于说明禁词的文字后，检查为零命中。

**站得住的部分**

- 新连上一条已有证据，确实改变该观点的证据集合。先写连线再重判，引用这条未被替代的证据，可以通过现有核对。对上结果仍记“重复”、写入结果记“新增连线”，也不矛盾。
- 重判读取当前证据，同时读取历史替代背景，是合理的。历史背景不能冒充当前有效依据；我没有把“看到了历史证据”本身算成缺陷。
- 原始来源时间与数字所属期间，主流程已经明确分开；不在同一替代链上的晚到证据也保住了。
- 证据标注没有再隐含触发观点合并；抽取与观点库的编号核对责任已经分开。

**我最不确定的三点**

1. “原始来源的哪一次”是否本来就准备保存同日先后。如果有，新问题 4 主要是输入契约漏写；目前文本看不出来。
2. “只答一次”是否原意允许同时返回重复关系和替代关系。如果允许，新问题 2 可以通过写清输出解决，但现在的“还是”表达的是互斥。
3. 修正版里的“原句还在”是否包含表头、单位、期间等上下文也没变。如果仅检查句子或格子文字，单位从百万改成十亿、格子仍写“100”，会被误当成不变；本轮我没有把这个解释尚不确定的问题列为正式发现。