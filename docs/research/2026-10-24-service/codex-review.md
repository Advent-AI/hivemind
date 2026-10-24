这版还不能作为可靠的服务交给调用方：HTTP 请求会失败，历史查询会混入未来关系和出处，金额判断也有实质错误。最直接的例子是：请求 `/days`，数据库还没读出来，就会因跨线程使用 SQLite 连接而报错。

未修改文件，未调用模型 API。以下发现只涉及指定范围。

**按调用方受到的影响排序**

1. **[P1] HTTP 的所有数据库路由都会在请求线程报错。**

   [hivemind_api.py:102](/Users/lchingen/hivemind/scripts/hivemind_api.py:102)：
   ```python
   http.server.ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
   ```
   `LEDGER`、`INDEX` 在主线程创建，请求在另一线程执行。连接使用 SQLite 默认的线程限制。

   已用同一个只读连接在请求线程调用 `route(['days'], {})`，得到：
   ```text
   sqlite3.ProgrammingError: SQLite objects created in a thread
   can only be used in that same thread.
   ```
   `do_GET()` 不捕获这个异常，因此调用方收不到正常 JSON。影响全部九类有效 HTTP 路由。

   **应守住的规则：数据库连接由使用它的线程持有。**

2. **[P1] 查询旧日期的观点，会返回未来才建立的关系。**

   [service.py:113](/Users/lchingen/hivemind/src/hivemind/service.py:113)：
   ```python
   'dependencies': dependencies(conn, view_id),
   'dependants': store.dependants_of(conn, view_id),
   ```
   两条读取路径都没有传入 `as_of`。

   输入 `view('v1', '2026-02-25')`，返回的 `dependants` 包含 `v94`，但 `v94` 到 **2026-08-15** 才建立。封存账本共有 **28 条关系、涉及 12 个被依赖观点**存在这种未来关系泄漏。`views()`、`search()` 也继承它。

   向外指的依赖在当前账本恰好都与观点同时建立，所以尚未实际泄漏；但依赖转向读取的是最新结果，同样没有日期过滤。账本没有转向记录，不能据此声称通过。

   **应守住的规则：关系和关系的目标，都经过同一个截止日期过滤。**

3. **[P1] `changes()` 返回历史判断时，会带上后来追加的出处。**

   [service.py:206](/Users/lchingen/hivemind/src/hivemind/service.py:206)：
   ```python
   cited = [store.evidence(conn, e) for e in ...]
   ```
   `store.evidence()` 返回这条证据目前的全部出处。

   输入 `changes('2026-02-24', '2026-02-25')`，`v4` 引用的 `e3` 包含 **2026-05-20、2026-08-06** 的出处。对应日期的 `evidence()` 会正确排除它们，两种接口因此给出不同的历史。

   全账本有 **42 次 changed 判断、9 个观点**受到影响；未来出处被重复带出 **750 次**。

   **应守住的规则：嵌套返回的证据，也走带截止日期的证据读取。**

4. **[P1] 金额解析没有保留原条件的范围和边界。**

   [service.py:232](/Users/lchingen/hivemind/src/hivemind/service.py:232)：
   ```python
   if len(numbers) >= 2 and numbers[1] > numbers[0]:
       return [numbers[0], numbers[1]]
   ```
   后续所有范围统一按左闭右开处理。解析也遗漏了“不超过”“至少”“大于或等于”、负数及万美元等表达。

   两个实际例子：

   - `evaluate('v17', '>=', 50e9)` 返回 `holds`。当前条件却是“0 至不足 1000 亿美元”，其中包含低于 500 亿的结果，应该是 `borderline`。程序把这个范围读成了 `[1000,1000]`。
   - `evaluate('v27', '>=', 169e9)` 返回 `not_yet`，并把门槛放到第 4 格。原第 3 格明确包含“不高于 1690 亿”，所以门槛属于第 3 格，判断应是 `borderline`。

   我逐项按账本原文解释 **42 把美元金额梯子**，比较各边界及边界两侧；其中 **18 把**至少一处被读错：
   `v17,v19,v27,v28,v37,v47,v49,v50,v53,v77,v78,v79,v80,v82,v83,v84,v86,v94`。

   **应守住的规则：不能准确表达整把梯子的条件，就不能给出确定的金额判断。**

5. **[P1] 等号判断把“落在范围内”当成“等于这个数”。**

   [service.py:265](/Users/lchingen/hivemind/src/hivemind/service.py:265)：
   ```python
   verdict = 'holds' if judged[0] <= yi < judged[1] else 'not_yet'
   ```

   `evaluate('v3', '=', 325e9)` 返回 `holds`。实际判断只是“3000 亿以上、低于 3500 亿”，不能说明恰好等于 3250 亿。按接口对 `borderline` 的解释，这里应返回 `borderline`。

   这个问题独立于上一条；即使范围解析完全正确，等号仍会答错。

   **应守住的规则：判断一个范围是否支持命题，不能只检查门槛是否在范围内。**

6. **[P2] 缺少观点向量时，搜索仍宣称是语义搜索。**

   [search.py:155](/Users/lchingen/hivemind/src/hivemind/search.py:155)：
   ```python
   semantic = cosine(...) if ... record['view_id'] in vectors else 0.0
   ```
   缺向量只变成零分，不改变 `mode`。两个前端只调用 `open_index()`，不会建立观点向量。

   用只读方式保留现有查询缓存、隐藏观点向量后，同一句：
   ```text
   Can NVIDIA's data center revenue top $300B this year?
   ```
   仍返回 `mode='semantic'`，第一名变成讨论供电设备的 `v76`，所有语义分数都是零。完整索引中第一名是 `v3`。

   新建空索引、换账本但未重建索引、新观点尚未嵌入，都能走到这条路径。搜索读取时也不核对存储的文本哈希。

   **应守住的规则：缺失或过期的向量必须明确进入降级状态，不能冒充已完成的语义排名。**

7. **[P2] 搜索验收把 `none` 当观点编号，而且失败仍正常退出。**

   [search_eval.py:42](/Users/lchingen/hivemind/scripts/search_eval.py:42)：
   ```python
   sentences.append((row['sentence'], row['mapped_view_id'] or None))
   ```
   CSV 中六条记录使用字符串 `"none"`，它是真值，因此被当作必须召回的观点。

   本次仅复用现有缓存，结果为：

   - 有真实目标编号：**14 条，5 条进入前三名**。
   - 脚本计算：**5/20**。
   - 四条示例中，“AI capex bubble”对应的 `v1` 排第 **10**。

   [脚本末尾](/Users/lchingen/hivemind/scripts/search_eval.py:55)只打印结果，不因未达到检查条件而失败。当前设计所写的前三名检查没有通过；这些编号仍只是线索，不能据此直接调排名或改预期。

   **应守住的规则：检查明确区分无目标记录，并如实报告未通过。**

8. **[P2] 嵌入错误正文可以把凭据内容带入日志。**

   [search.py:63](/Users/lchingen/hivemind/src/hivemind/search.py:63)：
   ```python
   last = f'HTTP {error.code}: {error.read().decode(...)[:300]}'
   ```
   远端错误正文原样进入异常；`search_eval.py` 不捕获建索引异常，最终会进入 traceback。

   我用假的 401 响应和假的 `review-dummy-key` 验证，异常完整包含该字符串。没有读取或发送真实凭据。这证明了泄漏通道，不表示本次发现了真实密钥泄漏。

   **应守住的规则：鉴权失败的日志只保留错误类别和安全字段，不转抄远端正文。**

**1．各读取函数的日期边界**

| 函数 | 实际可见范围 |
|---|---|
| `open_ledger` | 只读连接，不过滤日期。 |
| `default_as_of` | 最后一条完成日；没有完成日时取判断的最大发布日。封存账本为 `2026-08-15`。 |
| `seq_day_map`、`day_of_seq`、`visible` | 顺序号映射到处理记录的发布日；缺映射即不可见。 |
| `view_exists`、`is_open_as_of` | 按建立和开关记录的顺序日期过滤。 |
| `state_as_of` | 发布日不晚于截止日的判断，按判断编号选最后一条。 |
| `views`、`view` | 观点、开关、判断、证据有日期过滤；关系没有，见发现 2。 |
| `dependencies` | 无日期参数，返回当前依赖目标。 |
| `evidence` | 连线、替代、出处均按顺序日期过滤；正文随已可见连线读取。 |
| `history` | 判断按发布日过滤；到达、替代、开关按顺序日期过滤。 |
| `record` | 取截止日前最后判断；统计该判断日的处理数量和证据到达数量。 |
| `changes` | 判断按日期过滤；引用证据的出处未过滤，见发现 3。 |
| `evaluate` | 继承 `view` 的日期范围；金额语义另有发现 4、5。 |
| `_json`、`rung_numbers`、`band` | 不处理日期。 |

封存账本统计如下。所有列出的业务记录都有映射：

| 表 | 行数 | 无顺序日期 |
|---|---:|---:|
| views | 94 | 0 |
| evidence | 827 | 0 |
| judgements | 465 | 0 |
| evidence_links | 1212 | 0 |
| evidence_sources | 1021 | 0 |
| replacements | 2 | 0 |
| view_switches | 96 | 0 |
| dependencies | 62 | 0 |
| dependency_resolutions / successions | 0 / 0 | 未覆盖 |
| days_completed | 172 | 0 |

判断、出处、替代、两个关闭记录的日期都与顺序日期一致。没有发现它们挂在更晚日期的顺序号下。

**141 条完成日记录**复用了较早日期的顺序号。它们是完成日标记；服务读取其自身的 `day`，没有把它们的日期用于观点可见性，所以当前不构成泄漏。顺序号没有对应多个发布日，也没有日期倒退。

以下是计数查询；均在只读连接运行：

```sql
WITH m AS (
  SELECT sequence_no, MIN(publication_day) AS day
  FROM processing_steps WHERE sequence_no > 0
  GROUP BY sequence_no
), r(kind, seq) AS (
  SELECT 'views', created_seq FROM views
  UNION ALL SELECT 'evidence', created_seq FROM evidence
  UNION ALL SELECT 'judgements', seq FROM judgements
  UNION ALL SELECT 'links', seq FROM evidence_links
  UNION ALL SELECT 'sources', seq FROM evidence_sources
  UNION ALL SELECT 'replacements', seq FROM replacements
  UNION ALL SELECT 'switches', after_seq FROM view_switches
  UNION ALL SELECT 'dependencies', seq FROM dependencies
  UNION ALL SELECT 'resolutions', seq FROM dependency_resolutions
  UNION ALL SELECT 'successions', seq FROM successions
  UNION ALL SELECT 'days_completed', seq FROM days_completed
)
SELECT kind, COUNT(*) AS n, SUM(m.day IS NULL) AS unmapped
FROM r LEFT JOIN m ON m.sequence_no = r.seq
GROUP BY kind;
```

```sql
WITH m AS (
  SELECT sequence_no, MIN(publication_day) AS day
  FROM processing_steps WHERE sequence_no > 0
  GROUP BY sequence_no
), r(kind, seq, day) AS (
  SELECT 'judgements', seq, publication_day FROM judgements
  UNION ALL SELECT 'sources', seq, publication_day FROM evidence_sources
  UNION ALL SELECT 'replacements', seq, said_day FROM replacements
  UNION ALL SELECT 'days_completed', seq, day FROM days_completed
  UNION ALL
  SELECT 'closures', s.after_seq, v.due_day
  FROM view_switches s JOIN views v USING(view_id)
  WHERE s.open = 0
)
SELECT kind, COUNT(*) AS n,
       SUM(m.day > r.day) AS mapped_later,
       SUM(m.day < r.day) AS mapped_earlier
FROM r JOIN m ON m.sequence_no = r.seq
GROUP BY kind;
```

未来关系和出处的计数：

```sql
WITH m AS (
  SELECT sequence_no, MIN(publication_day) AS day
  FROM processing_steps WHERE sequence_no > 0
  GROUP BY sequence_no
)
SELECT COUNT(*) AS relationships,
       COUNT(DISTINCT d.depends_on) AS affected_views
FROM dependencies d
JOIN views v ON v.view_id = d.depends_on
JOIN m md ON md.sequence_no = d.seq
JOIN m mv ON mv.sequence_no = v.created_seq
WHERE md.day > mv.day;
-- 28 / 12
```

```sql
WITH m AS (
  SELECT sequence_no, MIN(publication_day) AS day
  FROM processing_steps WHERE sequence_no > 0
  GROUP BY sequence_no
)
SELECT COUNT(*) AS source_exposures,
       COUNT(DISTINCT j.judgement_id) AS judgements,
       COUNT(DISTINCT j.view_id) AS views
FROM judgements j, json_each(j.cited_evidence_json) e
JOIN evidence_sources s ON s.evidence_id = e.value
JOIN m ON m.sequence_no = s.seq
WHERE j.changed = 1 AND m.day > j.publication_day;
-- 750 / 42 / 9
```

**2．搜索引擎其余核对结果**

- 嵌入文本符合设计：对象、种类、看的内容、问题、梯子条件；没有证据。
- 正常排名是余弦分数，加对象命中 `0.08`、全文命中 `0.04`。
- 词面降级确实按全文排名分配不同分数；不是把命中都排成一样。`Vera Rubin 量产 出货` 降级后的前四项为 `v7,v60,v15,v48`。
- 现有索引有 **94 个观点向量**，全部文本哈希与当前账本一致，模型均有记录。
- 查询缓存同时检查文本哈希和模型，不会把另一模型的向量误用过来。主键只有哈希，切换模型会覆盖旧缓存，影响复用而非正确性。
- 没有重建或删除索引，因此本次没有验证“删除后重新嵌入得到相同向量”。
- 凭据正常路径只进入请求头，不进入索引或命令参数；错误路径见发现 8。

**3．前端参数和错误**

除发现 1 外，参数转交基本一致：

- HTTP 的 `q/object/from/to/since` 分别对应服务参数。
- HTTP `/changes` 省略 `since` 时自行使用 `0000-00-00`；MCP 和函数都要求提供它。
- HTTP `/evaluate` 查不到观点时返回 `200 null`；`/views/<id>` 则返回 404。
- MCP 的 `view/evaluate` 查不到观点时返回普通 `{'error': ...}` 字典，作为成功工具结果，而非工具错误。
- HTTP 仅绑定 `127.0.0.1`；MCP 使用 stdio。
- HTTP 日志去掉查询串；没有发现正常搜索请求把查询文字写入日志。评估脚本会主动打印评估句子。
- 现有 MCP 同步工具在安装版本中直接执行，没有复现 HTTP 的跨线程问题。

**4．测试覆盖**

八个 service 测试通过：

```text
8 passed in 6.79s
```

这些测试都能追溯到设计：默认日期；状态、建立、关闭日期；历史和替代；金额判断；处理记录及变化。三个 search 测试也分别对应派生索引、排名/缓存/日期、词面降级，没有发现无需求来源的测试。

但覆盖不足：

- 没有前端入口测试，因此发现 1 完全漏过。
- 日期测试没有检查关系、判断引用中的出处、依赖转向。
- 金额测试只验证 `v3` 的常规区间，没有等号和其他表达。
- “修改问题后重新嵌入”的测试实际上修改的是索引哈希，未修改问题，不能证明这一条需求。
- 没有删除重建、换模型、缺向量、过期向量、凭据错误输出、证据不进入索引的直接断言。
- 设计中的二十句搜索检查没有成为会失败的自动检查。

没有运行会创建索引文件的三个 search 测试；上述搜索复核使用只读现有缓存。首次 pytest 的默认输出捕获尝试创建临时文件，被沙箱拒绝；关闭捕获与缓存后完成测试。

**5．设计表**

[service.md:15](/Users/lchingen/hivemind/docs/poc/service.md:15) 有“调用—返回—读者—计算方式”表，但不是完整的“值 × 读者”表：

- 没列索引写出的 `text_sha256/model/vector_json/tokens/built_at`，以及它们的写入者、读取者和输入来源。
- 返回值没有列全。遗漏包括搜索外层的 `query/as_of/mode`、结果的 `open`；观点的 `object_kind/year/created_day/created_from`；状态的判断日和理由；历史的顺序号和轮次；证据的原始来源、原始日期、事件时间、替代关系；变化的 `position_moved/why_changed`。
- `evaluate` 还会返回表里没有的 `evaluable/reason/not_judged`。
- 表中八种调用所承诺的主要返回内容都有实现，没有发现整项完全缺失。
- 开头说“每个调用接受 `as_of`”，但 `history/changes` 实际接受日期区间。

“新路径必须通过的检查”只有四条概要，缺少前端、嵌套日期、依赖转向、金额表达、空索引和模型切换等对应检查。也没有索引建立、失败、部分完成、过期状态的状态转换表。

**6．写入、时钟和隐藏失败**

没有发现服务写账本；索引写入集中在 `search.py`。读时钟仅用于索引行的 `built_at`；重试等待不参与排序。

另有一个明确隐藏失败的点：[service.py:176](/Users/lchingen/hivemind/src/hivemind/service.py:176) 将非法 JSON 静默变成 `[]`。例如 `_json('[broken')` 返回空列表，调用方会把坏记录理解为“没有引用”。封存账本的 465 条判断中，这两列非法 JSON 的数量都是零，所以这是已复现的错误处理缺口，不是本账本已发生的数据问题。