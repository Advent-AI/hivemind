**第四稿的大部分修正成立，但还有两处实现前需要补齐的缺口。** 例如：某个理由编号删除两轮后，模型已看不到它，却仍被要求知道这个编号不能再用。

1. **决策一致性：未发现新的直接冲突。**  
   §2、§4、§8 保留了事件触发、单一判断状态、原始证据和冻结版本；来源是否独立仍由模型判断。另开 v8、等你决定后再实施，符合 [D354](/Users/lchingen/hivemind/docs/DECISIONS.md:3694)。修订保留新旧两条也符合[实际读取逻辑](/Users/lchingen/hivemind/src/hivemind/views/store.py:412)。

2. **状态缺口：§3、§4 没有给模型足够的信息来遵守“编号永不复用”。**  
   假设删除 `k20`，下一版只保留 `k1`，再下一版连删除记录也不含 `k20`。模型只读上一版卡片，无法知道新编号必须大于 20。需要明确把“历史最大编号”带入请求，或由代码分配新编号。否则正常更新也可能反复被拒收。这是第三轮编号修正尚未闭合的部分，依据[设计输入及编号规则](/Users/lchingen/hivemind/docs/research/2026-11-04-argument-record/design.md:71)、[AGENTS 身份规则](/Users/lchingen/hivemind/AGENTS.md:134)。  
   成环、当天开题、种子无证据、主题优先和已提交判断不重跑的其他处理，与[当前调度](/Users/lchingen/hivemind/src/hivemind/views/judging.py:300)相符。

3. **检查缺口：§5、§6 没有解决“被拒收请求”的历史上下文从哪里取。**  
   §5 要求按“那次请求序号之前”检查，但[模型存档](/Users/lchingen/hivemind/src/hivemind/model.py:33)没有轮次序号；只有成功判断才把 `call_id` 和 `seq` [一起入库](/Users/lchingen/hivemind/src/hivemind/views/judging.py:234)。拒收两次或写入回滚后，这个关联不存在，[失败记录](/Users/lchingen/hivemind/src/hivemind/views/round.py:27)也没有调用编号。应明确保存每次尝试对应的轮次、上一判断及卡片，包括失败尝试；旧存档无法恢复的应明确报“无法核验”。  
   其余新增字段的主要读取方已覆盖；保留种子身份、日期、档位和边界后，[现有评分程序](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py:40)可以不改。

4. **大小：§7 承认“整个请求没有硬上限”，这个修正成立。**  
   四十条只是卡片直接引用的数量上限。新到证据、关闭期间积累、首次建卡及全部主题仍可能很大；[当前主题读取](/Users/lchingen/hivemind/src/hivemind/views/judging.py:83)确实没有数量上限。因此能承诺的是限制反复携带的旧根据，不能承诺任何一天都不会因请求过大而停机。

5. **不做周期更新：§2 的结论成立。**  
   未发现必须在无新判断时重写卡片正文的情况。关闭、重开、主题停用可以改变展示状态，历史卡片仍解释当时判断；这符合 [D356](/Users/lchingen/hivemind/docs/DECISIONS.md:3734)。依赖变化走正常判断即可。

本次只读，未修改文件，未调用付费模型。

