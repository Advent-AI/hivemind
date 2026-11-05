**仍有严重问题，暂不适合开始实现。** 最明显的是：一条否认报道可以被标成“修订”，设计随后禁止引用原报道，但现有决策明确要求两条都留给判断。

1. **与决策冲突——设计 §4、§6。**

   - **混淆“修订”和“替代”。** “旧证据不能再引、只能改引新的或删掉”违反 [D202](/Users/lchingen/hivemind/docs/DECISIONS.md:2596)。现行修订保留新旧证据；真正使旧证据失效的 `replacements` 仅用于历史数据。两种情况必须分开。
   - **不能把匹配意见直接算成“独立来源”。** 同一说法不等于同一来源，没有重复关系也不等于来源独立。§4 根据说话人、日期和匹配关系直接给出确定数量，把尚待判断的关系当成事实，违反 [D201](/Users/lchingen/hivemind/docs/DECISIONS.md:2587)；当前请求明确把这些关系标为“未经验证的意见”。[代码](/Users/lchingen/hivemind/src/hivemind/views/judging.py:133)

2. **状态表缺项——设计 §5、§6。**

   - **写入失败可能留下半张记录。** 假如判断插入成功、卡片插入失败，现有错误处理会直接 `commit`；续跑又因判断已经存在而跳过。这不是“同一次提交”一句话能保证的，需要明确失败时整组回滚。[失败处理](/Users/lchingen/hivemind/src/hivemind/views/round.py:27)、[跳过条件](/Users/lchingen/hivemind/src/hivemind/views/judging.py:300)
   - **缺少“已有 v7 判断、但没有卡片”的首次升级。** §6 只覆盖新题首次判断，以及已有旧卡片的版本升级。现有数据库属于第三种状态：只读“上次判断以后新增的”会漏掉建立第一张卡所需的旧材料。[当前状态](/Users/lchingen/hivemind/src/hivemind/views/store.py:223)
   - **循环依赖没有确定读取规则。** A 依赖 B、B 又依赖 A 时，现有代码会强行先处理一个，并非都能读到对方当天的新结论。设计需要写清各自引用哪个判断版本，以及中断后如何保持一致。[调度](/Users/lchingen/hivemind/src/hivemind/views/judging.py:306)
   - **缺少手动关闭／重开、处理中换配置，以及第二个运行者写入的情况。** 手动开关是已有功能；运行到一半换配置目前会被拒绝；数据库只保证同题同序号不重复，不能据此宣称“两处同时写不会发生”。[生命周期约定](/Users/lchingen/hivemind/docs/prd/06-views.md:273)、[配置检查](/Users/lchingen/hivemind/src/hivemind/parallel_day.py:85)、[唯一约束](/Users/lchingen/hivemind/src/hivemind/views/store.py:45)

   种子无证据不判断、当天开题当天首次判断、模型拒收后重试，这些基本方向正确；缺的是上述交叉情况。

3. **读取方与检查没有闭合——设计 §3–§7。**

   - **卡片无法明确记录依赖题和主题提供的理由。** 输入允许读取它们，但理由只能引用证据编号，没有对应判断版本的引用。还没规定旧的 `reasons / cites / cites_views / pushes / theme_pushes / changed` 如何与卡片保持一致；其中 `changed` 直接决定是否继续判断其他题。[现有输出约定](/Users/lchingen/hivemind/src/hivemind/views/judging.py:54)、[传播条件](/Users/lchingen/hivemind/src/hivemind/views/judging.py:332)
   - **页面不只是多读一个表。** 历史日期查询必须取当时的卡片，不能拿最新卡片解释过去的判断；还要覆盖历史、变化列表、导出和前端转换。现有前端转换会丢掉新增字段，页面格式也拒绝未声明字段。[历史读取](/Users/lchingen/hivemind/src/hivemind/service.py:197)、[变化列表](/Users/lchingen/hivemind/src/hivemind/service.py:267)、[前端转换](/Users/lchingen/hivemind/poc/ui/src/adapters/bundle.js:112)、[格式检查](/Users/lchingen/hivemind/poc/ui/src/model/thesis.schema.json:103)
   - **“现有检查照旧”不成立。** 引用检查只识别一个固定证据区块；拆成“根据＋新到的”后必须重新定义识别方式。当前预检也没有重放判断的业务检查；通用格式检查不执行 `maxItems/maxLength`。[引用解析](/Users/lchingen/hivemind/src/hivemind/views/judging.py:188)、[预检入口](/Users/lchingen/hivemind/scripts/preflight.py:303)、[格式检查实现](/Users/lchingen/hivemind/src/hivemind/model.py:181)

   **评分程序本身可以保持不动**，前提是保留原有判断表、日期、档位和种子身份。[评分读取](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py:63) 冻结范围还包括 v7 的输出格式，不只是提示词文件。[冻结检查](/Users/lchingen/hivemind/tests/test_frozen_questions_and_judgement.py:33)

4. **请求大小有固定上限的结论不成立——设计 §4、§6、§8。**

   四十条只是卡片引用数量的上限。“一天最多二十几条”是样本最大值，不是系统限制；首次建卡可能要读历史积累；依赖题和主题数量没有上限。卡片自身还有“新到几条就写几条”的处理清单，下一次若整张读回，也会继续携带这部分内容。因此目前只能说**可能减少输入**，不能保证大小固定。[设计的上限论证](/Users/lchingen/hivemind/docs/research/2026-11-04-argument-record/design.md:62)、[全部主题读取](/Users/lchingen/hivemind/src/hivemind/views/judging.py:83)

5. **不做定期模型更新是对的，但要区分论证和页面状态——设计 §2、§6。**

   目前没有发现必须在无新判断时重新生成论证正文的情况。关闭、重开、主题退出使用范围时，页面状态及引用标记仍可能变化；它们应保留旧卡片“当时为何这样判断”的含义，而非触发周期重写。到期但从未判断的题也没有卡片编号，关闭记录必须允许这种情况。[D356](/Users/lchingen/hivemind/docs/DECISIONS.md:3734)、[现有关闭处理](/Users/lchingen/hivemind/src/hivemind/pull.py:11)

本次仅作只读审查，未修改文件，未调用付费模型。
