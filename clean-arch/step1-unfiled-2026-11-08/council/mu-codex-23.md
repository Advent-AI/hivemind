**这页现在不宜发给 Alex。** 建议做结构性测试可以作为待评估的选项，但现有证据和 D477 都不足以支持把它写成已经推荐、约 $3 的下一步。

需要改的陈述：

- **“40 个问题中写出了 22 个答案选项；其余 18 个被拒绝或答错。”** 22 是“写出的选项被判为正确”的数量，不是写出选项的总数；18 中有 10 个因正确拒绝而被判为正确。[统计输出](</Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/refused-shapes/right-by-refusal.output.txt>) 和 [D477](</Users/lchingen/hivemind/docs/DECISIONS-log.md:5384>)。
- **“两个内存价格案例都是因为写了截至 2027 年中期的 12 个月。”** 只有一个是滚动 12 个月；另一个同时追踪内存合约价格和机架内存成本。[来源核对](</Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/reachability/RESULT.md>)。
- **“四个都修好就正好达到 26。”** 这是纸面算术，不能当作预计结果：读者只确认相关文章支持同一事项上值得问的问题，并未证明答案选项质量，也不保证与原问题完全等价。[来源核对](</Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/reachability/RESULT.md>) 和 [D477](</Users/lchingen/hivemind/docs/DECISIONS-log.md:5384>)。
- **“四次措辞修改都在已有和未见过的文章上测试。”** 这个说法过宽；例如 c17 的目标和保护案例来自已有状态。[c17 结果](</Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/period-probe/RESULT.md>)。
- **“命名各主题包含什么，会解决 H100 的摇摆。”** 这是未经测试的预期，不是已证明的效果。而且九次中有三次归入半导体周期、一次归入错误主题、五次拒绝，不能概括为半数归入半导体周期。[主题统计](</Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/reachability/RESULT.md>)。
- **“在这个窗口中，它不改变任何最终答案。”** 没有同输入对照，不能作这个因果判断。31 次后续判断看到了 H100 主题，20 次以 ID 引用，其中一次的文字理由明确说租赁价格形成向下的抵消力量，但不足以跨档。[下游追踪](</Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/reachability/RESULT.md>)；[D477](</Users/lchingen/hivemind/docs/DECISIONS-log.md:5384>) 已明确区分“未显示改善”和“没有影响”。
- **“让第一步写答案选项，无法写出选项的问题就不会以该形状打开。”** 这是拟议结构想达到的效果，尚未验证；把任务放到第一步本身不能保证它做到。来源检查还表明，它最多直接触及两个内存案例和过度开题，除非同时改变主题限制，否则不解决 H100 拒绝。[来源核对](</Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/reachability/RESULT.md>)。
- **“这是唯一不同类型的杠杆；小测试约 $3，失败就选 3。”** “唯一”、成本及失败后的决策均缺少所列记录的支持。D476 要求先设计、估价和审查结构性测试，并综合其潜在效果与抑制风险；D477 只决定把选择写给 Alex，并暂停付费测试。[D476–D477](</Users/lchingen/hivemind/docs/DECISIONS-log.md:5372>)。

**建议判断：** 保留结构性测试作为一个可能的选择是有依据的；将它作为当前唯一推荐测试、承诺约 $3，以及预先决定失败后转回生产，都超出了现有证据和已记录的共识。页面应先呈现实测状态与选择，再把结构测试的收益、风险和成本标为尚待设计评估。

Council position: 修改上述表述后再交给 Alex；现有记录不支持按页面所写直接推荐并估价结构性测试。