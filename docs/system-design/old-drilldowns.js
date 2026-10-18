// The Old design's Configuration drill-down, ported from the old page's dialog (renderConfigPanel) with its wording
// unchanged. It reads the configuration data copy_old_design.py copied into old-design.js.
(function () {
  'use strict';

  const design = window.HIVEMIND_DESIGNS.old;
  const configuration = design.configuration;

  const PROFILE_OPTIONS = [
    ['current', 'current.json · 公司研究'],
    ['v2', 'factor-v2 · 显式启用因子研究'],
    ['v13', 'factor-v13 · 本地未采用候选'],
  ];

  function referencesFor(...symbols) {
    return configuration.references.filter((reference) => symbols.includes(reference.symbol));
  }

  function stepItem(title, input, decision, output, references, context, open) {
    return `<li><details${open ? ' open' : ''}><summary>${context.escapeHtml(title)}</summary>`
      + '<div class="drill__step">'
      + `<p><strong>输入：</strong>${input}</p>`
      + `<p><strong>判断 / 处理：</strong>${decision}</p>`
      + `<p><strong>输出：</strong>${output}</p>`
      + `<div class="drill__refs">${context.referenceLinks(references)}</div>`
      + '</div></details></li>';
  }

  function chainSteps(entry, profileId, context) {
    const daily = entry === 'daily';
    const profile = configuration.profiles[profileId];
    const key = profileId === 'current' ? 'current' : `factor-${profileId}`;
    let steps = '';
    if (daily) {
      steps += stepItem('读取每日任务设置', '<code>config/ops/daily-factor-v3.json</code>。',
        '检查必要字段和 formation.active 是否有对应配置；formation 设置覆盖 daily.flags 的同名项。',
        '准备命令参数，其中包含 <code>--preset factor-v2</code>。',
        referencesFor('load_config', 'production_flags'), context, true);
    }
    steps += stepItem('读取默认设置', '<code>config/runs/current.json</code>。',
      'CLI 的模型策略、规则和版本默认值从 current 读取；数据文件路径没有这些隐式默认值。',
      '默认参数；没有显式 preset 时，因子开关也查 current。',
      referencesFor('run_config', 'factor_config'), context, !daily);
    steps += stepItem('判断：有没有指定 preset？',
      daily ? 'daily 给出的 <code>--preset factor-v2</code>。' : `命令中的 <code>--preset ${context.escapeHtml(key)}</code>（本例显式指定）。`,
      '有：把所选文件的 replay_flags 放到命令参数前面，包括数据路径；没有：保留原命令。相对数据路径转成仓库下的绝对路径。',
      '加入 preset 设置后的命令参数。',
      referencesFor('preset_argv'), context, false);
    steps += stepItem('判断：同一个参数是否被覆盖？', '默认设置、preset 参数，以及命令自己写出的参数。',
      '普通参数由后出现的值生效。显式指定 catalog-dir 或 consensus 时，替换 preset 中该项的列表。daily 参数位于 preset 参数之后。',
      'CLI 最终解析出的参数。这里展示覆盖机制，不表示任意组合都已通过语义验证。',
      referencesFor('preset_argv', 'main'), context, false);
    steps += stepItem('判断：是否开启因子研究？', '所选 preset 的顶层 factor_ladders 和 factor 配置；未指定 preset 时读取 current。',
      '只有 factor_ladders 为 true，才加入因子客户端。仅存在 factor 配置段不会启用它。此开关读取 JSON，不是普通 CLI 覆盖参数。',
      profile.factor_enabled
        ? '本例开启：装配 ladder、registry、band-check 以及配置的 identity 客户端。'
        : '本例关闭：不加入因子客户端及其阶段回调。',
      referencesFor('factor_config', 'factor_clients'), context, false);
    steps += stepItem('装配客户端、日期和数据输入', '最终策略 ID、所选因子配置、数据路径与运行日期参数。',
      '客户端按策略 ID 读取模型配置；市场快照在命令内读取后复用。日期由命令 / replay 上下文决定，JSON 顶层 as_of 不会自动成为运行日期。',
      '模型客户端、规则版本、已读取的市场快照，以及交给后续流程使用的运行日期。',
      referencesFor('debates_client', 'load_policy', 'loop_snapshots', 'loop_today'), context, false);
    steps += stepItem('交给流程编排，开始下游工作', '上面构造的设置与客户端。',
      '后续代码决定何时运行哪个研究步骤。例如因子阶段是否先于新闻判断，还会读取 decide 策略的 factor_direction；不能只看因子开关。',
      '进入材料处理和研究流程。配置模块本身没有生成观点、因子或评估结果。',
      referencesFor('factor_first', 'reconcile'), context, false);
    return steps;
  }

  function outputRows(entry, profileId) {
    const daily = entry === 'daily';
    const key = profileId === 'current' ? 'current' : `factor-${profileId}`;
    const profile = configuration.profiles[profileId];
    const factorPreset = configuration.presets[profileId];
    const rows = [
      ['所选配置', key + (key === 'factor-v13' ? ' · 本地未采用' : '')],
      ['公司研究判断使用的策略', profile.decide_policy],
      ['是否装配因子研究', profile.factor_enabled ? '是' : '否'],
      ['新闻判断前的因子阶段条件', configuration.factorDirection[profileId]
        ? '所选 decide 策略包含 factor_direction'
        : '所选 decide 策略不含 factor_direction'],
    ];
    if (factorPreset) {
      rows.push(['公司因子构建策略', factorPreset.ladder_policy], ['全球因子登记策略', factorPreset.registry_policy]);
    }
    rows.push(
      [daily ? '数据输入（daily 覆盖 preset）' : '数据输入示例（显式 preset）',
        daily ? 'daily 为运行日期准备的快照路径；实际文件由当天任务确定。' : configuration.flags[profileId].calendar],
      ['日期来源', '命令参数 / replay 上下文；不是配置文件顶层 as_of'],
      ['模型、提示词、预算与超时', '各策略文件及运行时参数继续解析；不由 preset 名称单独决定'],
    );
    return rows;
  }

  design.drilldowns.config = {
    button: '展开 Configuration：输入 → 判断 → 输出',
    kicker: 'Configuration · 模块展开 / 当前代码',
    render(container, context) {
      let entry = 'direct';
      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">开工前，系统怎样确定这次的运行设置？</h2>
          <p class="drill__intro">这个环节读取设置、合并覆盖项、装配下游需要的客户端。财报和新闻的正文不会在这里被分析；研究步骤的执行顺序由后面的流程编排负责。</p>
          <div class="drill__controls">
            <label class="field">查看进入方式
              <span class="field__control"><select class="field__select" data-role="entry">
                <option value="direct">直接运行 CLI 命令</option>
                <option value="daily">每日任务 daily</option>
              </select></span>
            </label>
            <label class="field">查看配置文件
              <span class="field__control"><select class="field__select" data-role="profile">
                ${PROFILE_OPTIONS.map(([value, label]) => `<option value="${value}">${label}</option>`).join('')}
              </select></span>
            </label>
          </div>
          <p class="drill__banner" data-role="scenario"></p>
          <details class="drill__question" data-role="daily-check" hidden>
            <summary>daily 外层：付费运行前的检查</summary>
            <p>daily 的 preflight 检查日期、账本、预算、进程及配置指纹。指纹包含 preset 文件；同一天已有付费步骤后改变配置，会被拒绝。下面展示传入 CLI 的配置依赖链，不代表先完成研究再检查。</p>
            <div class="drill__refs">${context.referenceLinks(referencesFor('config_sha', 'preflight'))}</div>
          </details>
          <div class="drill__columns">
            <section>
              <h3 class="drill__heading">决策链路 · 点击每一步展开</h3>
              <ol class="drill__chain" data-role="chain"></ol>
            </section>
            <section>
              <h3 class="drill__heading">最终交给下游什么？</h3>
              <dl class="drill__outputs" data-role="output"></dl>
              <div class="drill__boundary">
                <strong>这个环节到此结束</strong>
                <p>下游拿到设置后，才读取材料、提取事实、建立或更新研究、保存结果。配置成功不代表研究结果正确。</p>
              </div>
              <details class="drill__question">
                <summary>待验证的设计问题 · 不是已确认故障</summary>
                <p>分别覆盖的设置，组合起来是否仍符合所选研究流程？此前只读实验中，factor-v2 保持开启，但把 decide 改为默认版本后，“因子先于新闻判断”的分支关闭。尚未证明这个组合违反哪条兼容要求，也未证明实际运行使用过它或产生错误结果。</p>
                <p>这里展示现有行为；没有新增统一校验器、没有修改研究引擎。</p>
              </details>
            </section>
          </div>
          <details class="drill__question">
            <summary>具体 I/O：一份财报进来，这个环节会输出什么？</summary>
            <dl class="drill__example">
              <dt>输入</dt><dd>某公司的研究任务、研究日期、财报等材料的位置，以及所选配置。正文“本季度收入增长 18%”是示意，不是实际运行结果。</dd>
              <dt>本模块的输出</dt><dd>使用哪套研究流程；各步骤使用哪个模型策略、提示词与规则；数据快照位置；运行参数。</dd>
              <dt>后续模块的输出</dt><dd>从正文提取事实，再用于建立或更新研究判断。这些不由 Configuration 生成。</dd>
            </dl>
          </details>
          <p class="drill__footnote">这是代码阅读图，不是实时运行日志。选择器只切换说明，不会执行命令、调用模型或改变配置。daily 示例固定使用现有 daily-factor-v3 → factor-v2。</p>
        </div>`;

      const entrySelect = container.querySelector('[data-role="entry"]');
      const profileSelect = container.querySelector('[data-role="profile"]');

      function refresh() {
        const daily = entry === 'daily';
        const profileId = daily ? 'v2' : context.getProfile();
        const key = profileId === 'current' ? 'current' : `factor-${profileId}`;
        entrySelect.value = entry;
        profileSelect.value = profileId;
        profileSelect.disabled = daily;
        container.querySelector('[data-role="scenario"]').innerHTML = daily
          ? '<strong>每日任务示例：</strong>daily-factor-v3 指向 factor-v2。先形成 daily 的命令参数，再交给同一个 CLI 配置入口。'
          : `<strong>直接运行示例：</strong>显式选择 ${context.escapeHtml(key)}；如果没有 --preset，则从 current 读取默认设置，但不自动带入其数据文件路径。`;
        container.querySelector('[data-role="daily-check"]').hidden = !daily;
        container.querySelector('[data-role="chain"]').innerHTML = chainSteps(entry, profileId, context);
        container.querySelector('[data-role="output"]').innerHTML = outputRows(entry, profileId)
          .map(([label, value]) => `<dt>${context.escapeHtml(label)}</dt><dd><code>${context.escapeHtml(value)}</code></dd>`)
          .join('');
      }

      entrySelect.addEventListener('change', () => { entry = entrySelect.value; refresh(); });
      profileSelect.addEventListener('change', () => { context.setProfile(profileSelect.value); refresh(); });
      refresh();
    },
  };
})();
