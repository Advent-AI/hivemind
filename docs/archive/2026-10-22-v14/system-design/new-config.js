// The New design's Config module (the model settings a person chooses) and the dispatch step, the system's single entry.
// Edit the data at the top; the two drill-downs render it. Decisions D2-D4, D17, D18, D25, D27, D29, D31 and D41 in docs/DECISIONS.md. The texts
// are for a reader who did not follow the discussion: plain words, no field names.
(function () {
  'use strict';

  // What Config records: a version, its checksum and the model settings for reading text.
  const CONFIG_SCHEMA = [
    { item: '版本号', meaning: '每改一次设置，就是一个新版本。', source: '改设置时生成' },
    { item: '校验码', meaning: '由整份设置算出来的一串码。每次模型调用（读信息、比对、重判、最终判定……）的记录里都写下它，事后能查到当时用的是哪一版。', source: '系统自动算' },
    { item: '模型设置、搜索取前几条', meaning: '模型设置分三种。抽取按类别各一套，写明用哪个模型、哪一版提示词、让模型想得多深、温度（温度越低，回答越稳定）。观点库的比对、重判各一套。最终判定一套。另外记观点库搜索取前几条，先定 10。提示词里写什么，在抽取、观点库和最终判定模块里。一套定下来就不再改，要改就换一套新的。', source: '人来定' },
  ];

  // The dispatch tree. A branch asks one question; each child is one answer (`answer`). A child without children is
  // where the item ends up: `act` marks the one that processes it.
  const DISPATCH_TREE = {
    label: '一条信息进来', question: '信息完整吗？', note: '看有没有写明：谁发的、哪天发的、分类结果、上游编号',
    children: [
      { answer: '不完整', label: '退回', note: '这是上游的问题，同时放进人工复核池' },
      {
        answer: '完整', label: '查处理记录', question: '以前处理过吗？', note: '同一个上游编号；更新版是新的一条，有自己的编号',
        children: [
          { answer: '处理过', label: '跳过', note: '上游重发或测试重跑时，不重复花钱' },
          {
            answer: '没处理过', label: '看分类结果', question: '分类结果是什么？',
            children: [
              { answer: '不合格', label: '不处理', note: '写明原因；对照表里查不到的，放进人工复核池' },
              { answer: '不算材料', label: '不处理', note: '比如别人算好、我们自己就能算出来的指标，文件目录' },
              { answer: '重复的信息', label: '并到原来那条', note: '算原来那条的另一个出处，不再处理一遍' },
              { answer: '属于某一类', label: '交给抽取', note: '带上它的类别和顺序号；抽取按类别用不同的读法', act: true },
            ],
          },
        ],
      },
    ],
  };

  const TREE_NOTES = [
    '灰色框：到这里就停了，不处理。黑框：交给抽取。',
    '不看信息讲的是谁。推进来的信息都在研究对象名单的范围内，所以不再问“这一类要不要处理”。',
    '每一类都交给抽取，按类别用不同的读法，不需要人来选。每一类读出什么，见抽取。',
    '带了发布系列名、但发布系列表里没登记的，照常往下走，同时放进人工复核池。',
    '顺序号按到达的先后编，不用电脑时钟；后面每一步都按它排先后。',
    '“处理过”指已经处理完；上次没做完的，从记下的那一步接着做，不算处理过。',
  ];

  const RULES = [
    'Config 只管人要亲自选的设置：模型设置，加上观点库搜索取前几条。信息本身的情况（属于哪一类、哪天发的、讲的是谁）由上游分类给出；做事的顺序、失败了怎么办，由代码决定；研究什么、每样看哪几类信息，由研究对象名单决定。',
    '不设预算和并发上限。',
    '改任何一处都生成新版本，旧版本原样保留，不在旧版本上叠加修改。',
    '设置里引用了不存在的模型设置，或者缺了必填的内容，整个版本不能用，也不会拿它去处理任何信息。',
  ];

  const OPEN = [
    '暂无。',
  ];

  function renderBranch(branch, escapeHtml, isRoot) {
    const isOutcome = !branch.children;
    const classes = ['org-node', isRoot ? 'org-node--root' : '', isOutcome ? (branch.act ? 'org-node--act' : 'org-node--leaf') : '']
      .filter(Boolean).join(' ');
    const box = `<div class="${classes}">`
      + (branch.answer ? `<span class="org-node__family">${escapeHtml(branch.answer)}</span>` : '')
      + `<span class="org-node__label">${escapeHtml(branch.label)}</span>`
      + (branch.question ? `<span class="org-node__question">${escapeHtml(branch.question)}</span>` : '')
      + (branch.note ? `<span class="org-node__note">${escapeHtml(branch.note)}</span>` : '')
      + '</div>';
    const below = isOutcome ? ''
      : `<ul>${branch.children.map((child) => `<li>${renderBranch(child, escapeHtml, false)}</li>`).join('')}</ul>`;
    return box + below;
  }

  // Scale the tree down, never up, so the whole of it is in view.
  function fitTree(container) {
    const frame = container.querySelector('.org');
    const tree = container.querySelector('.org-tree');
    tree.style.zoom = '1';
    tree.style.zoom = String(Math.min(1, (frame.clientWidth - 8) / tree.scrollWidth));
  }

  const design = window.HIVEMIND_DESIGNS.new;
  design.drilldowns = design.drilldowns || {};

  design.drilldowns.dispatch = {
    button: '展开分发：怎么决定每条信息的去处',
    kicker: '分发 · 详细说明',
    size: 'full',
    render(container, context) {
      const escapeHtml = context.escapeHtml;

      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">分发：每条信息怎么决定去处</h2>
          <p class="drill__intro">每来一条信息，依次问三个问题：信息完整吗？以前处理过吗？分类结果是什么？最后只落到一个去处。哪些类别会推进来，由研究对象名单决定。</p>
          <div class="org"><div class="org-tree"><ul><li>${renderBranch(DISPATCH_TREE, escapeHtml, true)}</li></ul></div></div>
          <ul class="drill__rules">${TREE_NOTES.map((note) => `<li>${escapeHtml(note)}</li>`).join('')}</ul>
        </div>`;
      requestAnimationFrame(() => fitTree(container));
      window.addEventListener('resize', () => { if (container.isConnected) fitTree(container); });
    },
  };

  design.drilldowns.config = {
    button: '展开 Config',
    kicker: 'Config · 详细说明',
    size: 'full',
    render(container, context) {
      const escapeHtml = context.escapeHtml;
      const schemaRows = CONFIG_SCHEMA.map((row) => `<tr><td>${escapeHtml(row.item)}</td><td>${escapeHtml(row.meaning)}</td>`
        + `<td class="schema-table__quiet">${escapeHtml(row.source)}</td></tr>`).join('');

      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">Config：人要亲自选的设置</h2>
          <p class="drill__intro">Config 只管人要亲自选的设置。模型设置分三种：抽取按类别各一套，观点库的比对、重判各一套，最终判定一套；另外记观点库搜索取前几条。每一类读出什么、提示词模板怎么拼，在抽取模块里；研究什么、看哪几类信息，在研究对象名单里。</p>
          <div class="drill__columns drill__columns--schema">
            <section>
              <h3 class="drill__heading">记了什么</h3>
              <table class="schema-table schema-table--compact">
                <thead><tr><th>内容</th><th>说明</th><th>怎么来</th></tr></thead>
                <tbody>${schemaRows}</tbody>
              </table>
            </section>
            <section>
              <h3 class="drill__heading">规则</h3>
              <ol class="drill__rules">${RULES.map((rule) => `<li>${escapeHtml(rule)}</li>`).join('')}</ol>
              <h3 class="drill__heading drill__heading--spaced">还没定的</h3>
              <ul class="drill__rules">${OPEN.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>
            </section>
          </div>
        </div>`;
    },
  };
})();
