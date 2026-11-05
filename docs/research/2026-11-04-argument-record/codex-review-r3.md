**第三稿仍有实质缺口；前两轮的大部分修正成立。** 最直接的例子：旧理由 `k1` 可以被换成完全不同的内容，只要编号还叫 `k1`，目前设计的检查就不会要求解释旧理由为什么消失。

1. **规则一致性——§4 的理由身份和处理记录还没闭合。**  
   “旧编号仍在”不能保证旧理由仍在。需要明确编号何时保留、何时换新，以及禁止重复编号和复用已删除编号，才能兑现“不悄悄丢理由”。依据：[设计 §4](/Users/lchingen/hivemind/docs/research/2026-11-04-argument-record/design.md:71)、[AGENTS 身份规则](/Users/lchingen/hivemind/AGENTS.md:134)。  
   同处还有一个漏洞：新证据把**自己**列为重复对象，或两条新证据互相指作重复，都满足“指向给看过的证据”。需要补上这些引用关系的检查；这属于检查身份关系，不是替模型判断重要性。[设计检查](/Users/lchingen/hivemind/docs/research/2026-11-04-argument-record/design.md:72)、[AGENTS 闭合集合要求](/Users/lchingen/hivemind/AGENTS.md:109)。

2. **状态与恢复——§6 漏了“关闭期间仍收到修订，后来重开”。**  
   当前写入代码会把修订链接到旧证据所在的题，**包括已关闭的题**，只是不给关闭的题安排判断。因此重开后下一次判断的“新到证据”可能积累了很多天；从未判断过就关闭的题，还可能首次建卡就读到这批积累。应补这一行，明确首次建卡和已有卡片分别怎么读。[设计 §6](/Users/lchingen/hivemind/docs/research/2026-11-04-argument-record/design.md:116)、[实际写入顺序](/Users/lchingen/hivemind/src/hivemind/views/writing.py:255)。  
   成环时记录实际读到的判断版本、已提交的不重判、失败先回滚，这些修正与现有调度相符，未发现新的必然重复写入问题。[调度与恢复](/Users/lchingen/hivemind/src/hivemind/views/judging.py:275)。

3. **读取方与检查——§5、§10 的预检修改仍不完整。**  
   预检 A 固定使用一个判断格式。仅新增业务检查，仍会把 v8 的卡片字段报为非法，并把不再由模型输出的 `cites / cites_views` 报为缺失；内存验证已确认。需要按原请求的版本选择格式，不能改冻结的 v7 格式。[预检选择](/Users/lchingen/hivemind/scripts/preflight.py:35)、[实际检查](/Users/lchingen/hivemind/scripts/preflight.py:67)。  
   读取清单还漏了历史研究工具的 `research_context.Reader.expand`：它直接返回整行判断，新增长处理记录会进入其有大小限制的返回内容，需要明确兼容方式。[读取及大小检查](/Users/lchingen/hivemind/src/hivemind/research_context.py:111)。**判断评分程序可以保持不动**，前提是保留种子身份、日期、档位和档位边界。[评分读取](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py:40)。

4. **大小——§7 承认整个请求没有硬上限，这次是对的；末句仍说得过满。**  
   上述关闭期间的积累说明，“新到的”不总是当天的量。首次建卡、依赖和主题数量的例外已正确列出。另外，§4 的“删除原因”没有字数上限，因此连“卡片自身大小钉死”也尚未完全成立。能承诺的是**限制常规卡片的理由数和直接引用数**。[设计 §4](/Users/lchingen/hivemind/docs/research/2026-11-04-argument-record/design.md:52)、[§7](/Users/lchingen/hivemind/docs/research/2026-11-04-argument-record/design.md:133)。

5. **不做周期更新——结论成立。**  
   未发现必须在没有新判断时重新生成论证正文的情况。关闭、重开和主题停用改变展示状态，旧卡片仍解释当时的判断；不应因此增加周期模型调用。[D356](/Users/lchingen/hivemind/docs/DECISIONS.md:3730)。修订保留两条、来源独立性交给模型、只追加历史、另开 v8 而不修改冻结文件，这些回答也成立。

本次未编辑文件，未调用付费模型；验证仅含只读检查和内存计算。

