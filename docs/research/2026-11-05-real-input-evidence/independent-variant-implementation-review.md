# Independent read-only review

**结论：现在不能进行正式的付费 A/B 实验，也不能用现有草稿评分。** 保存的免费检查表明，三篇文章构造出的两组模拟请求只差财报背景；但来源与时间的核验还有缺口，真实读写链路也没有按两组实验验证完。

例如，模型可能引用新闻中的一句原话，却在摘要里混入财报的旧数字。现有检查只证明一条完全来自财报的句子被拒绝，不能发现这种混合错误。

1. **存档身份和日期没有从原始网页独立核实。** [build_archived_variants.py:94](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/build_archived_variants.py:94) 用文章 ID 找存档文件，却没有核对索引里的抓取时间、网址与输入包是否一致；[第 98 行](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/build_archived_variants.py:98)直接相信输入包里的抓取和发布时间，再用这些值生成存档链接。哈希证明正文与保存的文件一致，**不证明这些日期和链接属于该文件**。我对照了现有三篇输入包和存档索引，时间字段彼此一致，财报时间也早于三篇文章；但这还不是对网页原始元数据和链接的独立验证，不能说已发现这三篇日期写错。

2. **读者可能看不到这是什么版本。** [build_archived_variants.py:103](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/build_archived_variants.py:103) 把来源设为存档网址，但标题、出版方等从旧记录继承，未独立确认。[check_variant_writer_reader.py:79](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/check_variant_writer_reader.py:79)只检查来源 ID 和网址；实际读取接口返回的来源资料也没有抓取时间或“元数据未经确认”的标记，见 [bundle.py:28](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/bundle.py:28)。因此这个检查不能证明最终读者知道自己看到的是哪次存档、哪些资料尚未核实。

3. **A/B 请求的模拟检查成立，但不等于实验发送和公平性已经验证。** [preflight_archived_variants.py:81](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/preflight_archived_variants.py:81)为两组使用同一篇文章和空研究库，只给 B 组插入财报，并比较去掉财报后的请求。保存的[结果](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/preflight-d369/variant-preflight.json:1)记录了三篇、六个模拟请求通过。但它没有证明正式发送时使用相同的冻结输入、独立状态和同日对照；方案也明确说正式发送流程尚未完成独立审查和实现，见 [design.md:88](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/design.md:88)。空研究库的结论也只能用于空库场景，不能代表有历史研究库时的效果。

4. **写入和读取检查没有覆盖实际两组的答案。** [preflight_archived_variants.py:91](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/preflight_archived_variants.py:91)给两组塞入同一个模拟答案；新闻原话因没有接收它的问题而被丢弃，没有进入实际写入和读取。[check_variant_writer_reader.py:17](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/check_variant_writer_reader.py:17)则另选一篇，用手写问题、手写答案和模拟判断验证一条记录能写入并读出。它没有测试三篇文章的两组真实回答，也没有核对读出的摘要、人物、日期和限定语是否被财报污染。代码中的引用修复还可能把混合引文修成新闻原文，而保留被污染的摘要，见 [extraction.py:671](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/extraction.py:671)。

5. **参考答案尚不能用于判定输赢。** [CURRENT_STATE.md:7](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/CURRENT_STATE.md:7)记录三篇来源和参考答案仍是草稿，部分保留边界有分歧，尚未完成独立审阅和你的签字。旧参考标准没有改动；现在把草稿当正式答案评分，会把尚未解决的分歧算成模型错误。

建议先完成三篇存档网页的来源、时间及展示核验，并把参考答案中仍有分歧的地方交给你确认；随后用同一套模拟输入检查两组从抽取到实际写入、读取的全过程，尤其检查混合引用和摘要。完成这些以后，再判断是否具备正式实验条件。

本次没有修改文件，也没有调用付费服务。我只审阅了保存的检查结果和相关代码；由于当前环境只读，**没有重新运行需要创建临时数据库的脚本**。


Note: after this review started, the builder was updated to check archive-index identity and publisher timestamp directly in saved HTML; it was then rebuilt and checked again. Other findings remain open.
