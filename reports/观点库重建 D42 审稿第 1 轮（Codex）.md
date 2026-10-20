发现 7 类需要对齐的问题，另有一组用词混用：
- 修正版删掉句子后，“被替代”没有可指向的新证据，撤回这条路没写完整。
- 同一证据挂多条观点时，各条观点独立对上，可能与“证据只存一次”冲突。
- “只比一句话”不足以保证裁判能区分转载、独立观察和较晚的说法。
- “比现在算数的还旧就进历史”写得过宽，会误伤晚到的新证据。
- 抽取的单选式写法，与允许同一证据同时挂卡片、候选观点的写法冲突。
- 标注里的“重复”已包含证据，但后续仍一律送去合并观点。
- 三处摘要漏掉了“依赖变化也会重判”。

以下次数按有问题的句子或流程定义计，页面数据与 PRD 副本分别计；正确的对照条款不计。讨论记录不计。缺项按需要补齐的流程定义处计。

**1．修正版删除证据，不能完整表达为“旧证据指向新证据”**

**在哪，共 7 处：**

- 删除句子的规则：[06-views.md:161](/Users/lchingen/hivemind/docs/prd/06-views.md:161)、[06-views.md:203](/Users/lchingen/hivemind/docs/prd/06-views.md:203)；[new-facts.js:278](/Users/lchingen/hivemind/docs/system-design/new-facts.js:278)、[new-facts.js:326](/Users/lchingen/hivemind/docs/system-design/new-facts.js:326)；[DECISIONS.md:929](/Users/lchingen/hivemind/docs/DECISIONS.md:929)。
- “被替代”字段必须指向新证据：[06-views.md:340](/Users/lchingen/hivemind/docs/prd/06-views.md:340)、[new-facts.js:452](/Users/lchingen/hivemind/docs/system-design/new-facts.js:452)。

**哪里不通：**原稿只有一句“预计涨 25%”，修正版删掉它，没有新说法。旧证据应退出有效证据集，但没有新证据可供“被替代”字段指向。重判输入又要求每条有效证据带上它替掉的那条；这种只删除、不新增的变化，不能通过新证据带进去。

[06-views.md:352](/Users/lchingen/hivemind/docs/prd/06-views.md:352)已经要求旧版关联的观点重判，所以不能解释为“删除后什么也不做”；是字段和流程尚未把这个要求接起来。

**最简单的改法：**明确“被替代”可以因修正版撤回而没有后继证据，并把这次撤回写进本轮变化。旧证据连着的观点都重判。无须新增一套撤回系统。

**2．按观点分别对上，缺少回到“同一条证据”的合流规则**

**在哪：需要补齐的流程定义共 2 处：**[06-views.md:165](/Users/lchingen/hivemind/docs/prd/06-views.md:165)、[new-facts.js:282](/Users/lchingen/hivemind/docs/system-design/new-facts.js:282)。

**哪里不通：**设证据 e 已经连着观点 A，尚未连着 B。新信息又带来同一句话，这次挂到 A、B：

- 在 A 下比较，是“重复 e”，只多一个出处。
- B 下没有证据，按现文“不用问”，走新证据。

结果究竟是复用 e、补一条 e→B 连线，还是新建第二条证据？目前没写。后者违反[“证据只存一次”](/Users/lchingen/hivemind/docs/prd/06-views.md:102)；前者还必须说明 B 虽然拿到的是全库已有证据，但对 B 是第一次获得这份证据，应当重判。

**最简单的改法：**同一条输入证据的多个挂靠合并处理：一处已认出它是 e，其他挂靠复用 e；新增连线会改变相应观点的有效证据集，触发该观点重判。把“证据身份是否新增”和“某条观点是否得到新证据”分清。

**3．对上证据需要的来源和时间，没有完整进入裁判输入约定**

**在哪，共 7 处：**

- 将比较输入说成“一句话”的 5 处：[00-system.md:105](/Users/lchingen/hivemind/docs/prd/00-system.md:105)；[06-views.md:204](/Users/lchingen/hivemind/docs/prd/06-views.md:204)、[06-views.md:334](/Users/lchingen/hivemind/docs/prd/06-views.md:334)；[new-facts.js:327](/Users/lchingen/hivemind/docs/system-design/new-facts.js:327)、[new-facts.js:446](/Users/lchingen/hivemind/docs/system-design/new-facts.js:446)。
- 把数字的时间写成所属期间的 2 处：[06-views.md:339](/Users/lchingen/hivemind/docs/prd/06-views.md:339)、[new-facts.js:451](/Users/lchingen/hivemind/docs/system-design/new-facts.js:451)。

**哪里不通：**“工厂已开工”这句可以来自同一报道的转载，也可以来自另一名记者的独立观察。只看一句话，分不出来。

时间同样如此：2 月提出的 FY2026 指引与 4 月修改的 FY2026 指引，所属期间都是 FY2026；转载的发布日期又不等于原说法提出的日期。现文要求按时间判谁替代谁，却没有明确区分这两个时间。

证据已经保存来源等字段，这是好事；问题是“保存了”不等于“裁判收到这些字段”。

**最简单的改法：**明确对上输入是一句话，加说话人、原始来源、层、原说法提出或原数公布的时间、所属期间。“不读整份原文”可以保留，“只比一句话”应改掉。数字所属期间不能代替说法的先后时间。

**4．“旧”被写成了整条观点下的时间比较，缺少“同一条替代链”的限制**

**在哪，共 2 处：**[06-views.md:351](/Users/lchingen/hivemind/docs/prd/06-views.md:351)、[new-facts.js:461](/Users/lchingen/hivemind/docs/system-design/new-facts.js:461)。

**哪里不通：**两处都说，比现在算数的还旧，就直接进历史。

例如观点下已有 4 月公司指引，5 月才收到一份 3 月的独立渠道调查。这份调查发生得更早，但没有被公司指引替代；按[新证据规则](/Users/lchingen/hivemind/docs/prd/06-views.md:197)，它仍可以是有效的新证据。不能仅因时间早而失效。

**最简单的改法：**限定为：“已经认出属于同一条替代链、且比链上当前说法更早的，进历史。”其他晚到证据照常判断重复、替代或新证据。AMZN 晚到旧预测的例子可以保留。

**5．抽取一处允许多挂，另一处却要求单选；卡片与候选观点能否同时挂也没有统一**

**在哪，共 8 处：**

- 单挂或二选一的表述共 6 处：[05-extraction.md:29](/Users/lchingen/hivemind/docs/prd/05-extraction.md:29)、[05-extraction.md:44](/Users/lchingen/hivemind/docs/prd/05-extraction.md:44)、[05-extraction.md:152](/Users/lchingen/hivemind/docs/prd/05-extraction.md:152)；[new-facts.js:69](/Users/lchingen/hivemind/docs/system-design/new-facts.js:69)、[new-facts.js:78](/Users/lchingen/hivemind/docs/system-design/new-facts.js:78)；[new-design.js:92](/Users/lchingen/hivemind/docs/system-design/new-design.js:92)。
- 分流树共 2 处：[05-extraction.md:50](/Users/lchingen/hivemind/docs/prd/05-extraction.md:50)、[new-facts.js:85](/Users/lchingen/hivemind/docs/system-design/new-facts.js:85)。

**哪里不一致：**验收要求“一张卡片或一个候选观点”；树却说一句话可以挂几张卡片。观点库又明确保留[候选不开、但还挂在卡片上的证据](/Users/lchingen/hivemind/docs/prd/06-views.md:181)，说明同一证据可能两边都挂。

例如一句新监管措施，既影响已有收入观点，也提出尚未覆盖的监管问题。分流树如果按互斥分支执行，命中已有卡片后，就不会提出候选问题。

**最简单的改法：**统一为“每条证据至少挂一个本次有效目标，可同时挂多个卡片和候选观点”；分开问它支持哪些已有问题、是否还提出未覆盖的问题。候选不开，只移除它对应的挂靠，不影响其他挂靠。

**6．标注结果中的“重复”混用了证据重复与观点重复**

**在哪，共 3 处：**[06-views.md:288](/Users/lchingen/hivemind/docs/prd/06-views.md:288)、[new-facts.js:403](/Users/lchingen/hivemind/docs/system-design/new-facts.js:403)、[new-design.js:133](/Users/lchingen/hivemind/docs/system-design/new-design.js:133)。

**哪里不通：**D42 已把证据对上纳入标注。这三处仍说“人标出来的重复，交给查重并入”。但这里的[查重](/Users/lchingen/hivemind/docs/prd/06-views.md:214)处理的是重复观点：关闭后一条观点、转移连线和箭头。

人发现两条证据重复，不代表它们所属的两条观点重复，不能送去合并观点。

**最简单的改法：**写全对象：人发现的“重复观点”交给观点查重；证据的标注结果按“其余先记着”处理。若要让证据标注修库，需要另行决定，不能借现有查重规则隐含完成。

**7．“只有新证据和替代才重判”与已定的依赖通知相矛盾**

**在哪，共 3 处：**[06-views.md:9](/Users/lchingen/hivemind/docs/prd/06-views.md:9)、[new-design.js:22](/Users/lchingen/hivemind/docs/system-design/new-design.js:22)、[new-facts.js:655](/Users/lchingen/hivemind/docs/system-design/new-facts.js:655)。

**哪里不一致：**这三处用了没有限定范围的“只有”。但 D42 [明确保留依赖变化触发重判](/Users/lchingen/hivemind/docs/DECISIONS.md:938)，进库第 10 步也这样写。

B 没收到直接证据，A 换格通知 B，B 仍须重判。这不是尚未决定的“格内变化通知门槛”，而是已经决定的路径。

**最简单的改法：**改为“直接证据带来的重判，只由新证据或替代触发；依赖变化另按通知规则触发”，或者直接列全三种触发。

**8．还有三组用词需要统一**

| 问题 | 全部位置与次数 | 最简单的改法 |
|---|---|---|
| “只多了重复的观点不重判”把证据写成观点 | **2 处**：[00-system.md:112](/Users/lchingen/hivemind/docs/prd/00-system.md:112)、[06-views.md:21](/Users/lchingen/hivemind/docs/prd/06-views.md:21) | 改为“本轮只收到重复证据，且没有依赖变化，不重判”。 |
| “候选”同时指抽取交来的候选观点、检索出来供比较的已有观点 | **20 个句子，22 次用词**。前者 14 处：00-system:110；05-extraction:122、123；06-views:163、226、227、368；09-review-pool:22；new-design:183；new-facts:119、120、280、350、351。后者 6 处：00-system:57；06-views:19、127、185；new-facts:262、309。 | 前者写全“候选观点”；后者写“供比较的已有观点”或“依赖备选观点”。尤其用词表自身的“数字的候选”也要改。 |
| 两条线对照表把候选观点一栏写成“搜全库吗：不搜” | **2 处**：[06-views.md:150](/Users/lchingen/hivemind/docs/prd/06-views.md:150)、[new-facts.js:295](/Users/lchingen/hivemind/docs/system-design/new-facts.js:295) | 写成“公司取该公司已有观点；主题检索全部开着的主题观点”。现文与第 4 步的跨主题检索相反。 |

上述简称位置涉及的文件：[00-system.md](/Users/lchingen/hivemind/docs/prd/00-system.md:110)、[05-extraction.md](/Users/lchingen/hivemind/docs/prd/05-extraction.md:122)、[06-views.md](/Users/lchingen/hivemind/docs/prd/06-views.md:163)、[09-review-pool.md](/Users/lchingen/hivemind/docs/prd/09-review-pool.md:22)、[new-design.js](/Users/lchingen/hivemind/docs/system-design/new-design.js:183)、[new-facts.js](/Users/lchingen/hivemind/docs/system-design/new-facts.js:119)。

**检查过、认为站得住的部分：**

- 证据是原信息中的话或数，候选观点是我们提出的问题；两者基本定义已经分开。候选保留梯子和到期日，符合讨论最后采用的版本。
- 抽取前按相关对象及一层依赖拿卡片；读完以后才按候选观点检索。这两个时点没有再混成同一张清单。
- 进库第 5 步对上候选观点、第 6 步对上证据，相关标题、流程和标注说明的编号一致。NVDA／AMD 例子的 #1、#2、#3 没发现前后换号。
- 没有旧证据时不调用证据裁判；被替代证据关联的其他观点也收到新证据；重复出处可追溯。这些主干要求均已写入。
- Config 两套对上设置、研究对象名单第 8 条、两格问题的例外，已对齐。
- 只读核对了范围内 **49 个 generated 段落，零差异**；现有禁用词检查 **66 个检查片段，零命中**。没有运行会重建打包文件的完整检查，没有修改文件。

**最不确定的三点：**

1. “只比一句话”是否只是表达简略，实际意图仍是把全部来源字段交给裁判。若是，第 3 条主要是输入约定漏写。
2. 多观点对上的结果是否原本打算由写入步骤统一合并。若是，第 2 条已有解决意图，但当前流程不足以让执行者唯一地还原它。
3. “一张卡片或一个候选观点”是否只是泛指。如果允许组合挂靠，第 5 条可通过统一文字和验收条件解决；若确实要求单选，就与现有多挂及“不开仍保留卡片证据”的规则冲突。