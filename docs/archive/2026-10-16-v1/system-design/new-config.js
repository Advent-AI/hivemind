// The New design's Config module (the model settings a person chooses) and the dispatch step, the system's single entry.
// Edit the data at the top; the two drill-downs render it. Decisions D2-D4, D17 and D18 in docs/DECISIONS.md. The texts
// are for a reader who did not follow the discussion: plain words, no field names.
(function () {
  'use strict';

  // What Config records: a version, its checksum and the model settings for reading text.
  const CONFIG_SCHEMA = [
    { item: '版本号', meaning: '每改一次设置，就是一个新版本。', source: '改设置时生成' },
    { item: '校验码', meaning: '由整份设置算出来的一串码。每条处理记录都写下它，事后能查到当时用的是哪一版。', source: '系统自动算' },
    { item: '模型设置', meaning: '模型读文字时用哪个模型、哪一版提示词、按什么格式输出、想得多深。一套定下来就不再改，要改就换一套新的。', source: '人来定' },
  ];

  // The dispatch tree. A branch asks one question; each child is one answer (`answer`). A child without children is
  // where the item ends up: `act` marks the two that process it.
  const DISPATCH_TREE = {
    label: '一条信息进来', question: '信息完整吗？', note: '看有没有写明：谁发的、哪天发的、属于哪一类、上游给的编号',
    children: [
      { answer: '不完整', label: '退回', note: '这是上游的问题，同时放进人工复核池' },
      {
        answer: '完整', label: '查处理记录', question: '以前处理过吗？', note: '同一个编号、同一个版本',
        children: [
          { answer: '处理过', label: '跳过', note: '上游重发或测试重跑时，不重复花钱' },
          {
            answer: '没处理过', label: '看分类结果', question: '分类结果是什么？',
            children: [
              { answer: '不合格', label: '不处理', note: '写明原因；对照表里查不到的，放进人工复核池' },
              { answer: '不算材料', label: '不处理', note: '比如别人已经算好的指标、文件目录' },
              { answer: '重复', label: '并到原来那条', note: '算原来那条的另一个出处，不再处理一遍' },
              {
                answer: '属于某一类', label: '看形式', question: '文字还是表格？',
                children: [
                  { answer: '表格', label: '程序读', note: '直接读出数字', act: true },
                  { answer: '文字', label: '模型读', note: '整理成一条条事实', act: true },
                ],
              },
            ],
          },
        ],
      },
    ],
  };

  const TREE_NOTES = [
    '灰色框：到这里就停了，不处理。最下面两个框：交给程序或模型。',
    '不看信息讲的是哪家公司或哪个主题。推进来的信息都在研究对象名单的范围内，所以不再问“这一类要不要处理”。',
    '程序读还是模型读，由信息是表格还是文字决定，不需要人来选。',
    '对照表里查不到的新指标，照常往下走，同时放进人工复核池。',
  ];

  // Where each form of a category goes; a category's forms come from the classification page's TAGS.
  const FORM_OUTCOMES = { text: '模型读', structured: '程序读' };
  const FORMS_OF = { '两者': ['text', 'structured'], '文本': ['text'], '结构化': ['structured'] };

  const RULES = [
    'Config 只管这一样设置。信息本身的情况（属于哪一类、哪天发的、讲的是谁）由上游分类给出；做事的顺序、失败了怎么办，由程序决定；研究什么、每样看哪几类信息，由研究对象名单决定。',
    '不设预算和并发上限。',
    '改任何一处都生成新版本，旧版本原样保留，不在旧版本上叠加修改。',
    '设定里引用了不存在的模型设置，或者缺了必填的内容，整个版本不能用，也不会拿它去处理任何信息。',
  ];

  const OPEN = [
    '所有类别的文字共用一套模型设置，还是每个类别各一套（以后再谈）。',
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
      const tags = design.classification.TAGS;
      const tagRows = Object.keys(tags)
        .sort((first, second) => Number(first.slice(1)) - Number(second.slice(1)))
        .map((code) => {
          const forms = FORMS_OF[tags[code].forms];
          const cell = (form) => (forms.includes(form) ? escapeHtml(FORM_OUTCOMES[form]) : '<span class="schema-table__quiet">—</span>');
          return `<tr><td><span class="org-tag__code">${code}</span> ${escapeHtml(tags[code].label)}</td><td>${cell('text')}</td><td>${cell('structured')}</td></tr>`;
        }).join('');

      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">分发：每条信息怎么决定去处</h2>
          <p class="drill__intro">每来一条信息，依次问四个问题：信息完整吗？以前处理过吗？分类结果是什么？是文字还是表格？最后只落到一个去处。</p>
          <div class="org"><div class="org-tree"><ul><li>${renderBranch(DISPATCH_TREE, escapeHtml, true)}</li></ul></div></div>
          <ul class="drill__rules">${TREE_NOTES.map((note) => `<li>${escapeHtml(note)}</li>`).join('')}</ul>
          <section>
            <h3 class="drill__heading">16 个类别：文字和表格各交给谁</h3>
            <table class="schema-table schema-table--compact">
              <thead><tr><th>类别</th><th>文字</th><th>表格</th></tr></thead>
              <tbody>${tagRows}</tbody>
            </table>
            <p class="drill__output">“—”表示这个类别不会出现这种形式。哪些类别会推进来，由研究对象名单决定。</p>
          </section>
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
          <h2 class="drill__title">Config：模型读文字时用的设置</h2>
          <p class="drill__intro">Config 只管一件事：模型读文字材料时，用哪个模型、哪一版提示词。研究什么、看哪几类信息不在这里，在研究对象名单里。</p>
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
