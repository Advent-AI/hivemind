// One renderer for both designs: the New tab (new-design.js) and the Old tab (old-design.js). The address keeps the
// place: #<design>/<view>/<node>[/<profile>]; the old page's own form (#system/config/v2) opens the Old tab there.
(function () {
  'use strict';

  const designs = window.HIVEMIND_DESIGNS;
  const DESIGN_ORDER = ['new', 'old'];
  const NODE_WIDTH = 206;
  const NODE_HEIGHT = 142;
  // A node placed by [column, row] lands on the same lanes Old's views use.
  const GRID_LEFT = 20;
  const GRID_TOP = 45;
  const GRID_COLUMN_STEP = 240;
  const GRID_ROW_STEP = 200;
  const ZOOM_MIN = 0.6;
  const ZOOM_MAX = 1.5;

  const KINDS = {
    control: '控制',
    external: '外部输入',
    model: '模型判断',
    code: '代码 / 规则',
    mixed: '代码 + 条件模型',
    store: '存储',
  };
  const LINE_STYLES = [
    ['', '数据 / 执行'],
    ['control', '控制 / 反馈'],
    ['candidate', '仅本地路径'],
  ];
  const MIGRATION_LABELS = { carried: '已迁入 New', dropped: '不迁', open: '未决定' };
  const MIGRATION_PILLS = { carried: 'pill pill--strong', dropped: 'pill pill--mixed', open: 'pill pill--quiet' };

  const elements = {
    designTabs: document.getElementById('designTabs'),
    profileField: document.getElementById('profileField'),
    profileSelect: document.getElementById('profileSelect'),
    heading: document.getElementById('designHeading'),
    summary: document.getElementById('designSummary'),
    meta: document.getElementById('designMeta'),
    panel: document.getElementById('designPanel'),
    viewTabs: document.getElementById('viewTabs'),
    viewTitle: document.getElementById('viewTitle'),
    viewCaption: document.getElementById('viewCaption'),
    banner: document.getElementById('banner'),
    legend: document.getElementById('legend'),
    steps: document.getElementById('steps'),
    viewport: document.getElementById('viewport'),
    canvas: document.getElementById('canvas'),
    edges: document.getElementById('edges'),
    nodes: document.getElementById('nodes'),
    zoomOut: document.getElementById('zoomOut'),
    zoomIn: document.getElementById('zoomIn'),
    zoomFit: document.getElementById('zoomFit'),
    zoomLabel: document.getElementById('zoomLabel'),
    detail: document.getElementById('detail'),
    migration: document.getElementById('migration'),
    documents: document.getElementById('documents'),
    sheet: document.getElementById('sheet'),
    sheetScrim: document.getElementById('sheetScrim'),
    sheetPanel: document.getElementById('sheetPanel'),
    sheetKicker: document.getElementById('sheetKicker'),
    sheetActions: document.getElementById('sheetActions'),
    sheetClose: document.getElementById('sheetClose'),
    sheetBody: document.getElementById('sheetBody'),
  };

  const state = {
    designId: 'new',
    zoom: 1,
    positions: { new: { viewId: null, nodeId: null }, old: { viewId: null, nodeId: null } },
    profiles: { new: designs.new.defaultProfile || null, old: designs.old.defaultProfile || null },
    focusBeforeSheet: null,
  };

  // ------------------------------------------------------------------ reading the designs

  // A view may be written short: nodes as [id, column, row], edges as [source, target, label, style], no order (the
  // node list's order), no size (the placed nodes' extent). Old's views are already written long and pass unchanged.
  // A design may set its own node height, grid row step and subtitle lines (nodeHeight, gridRowStep, subtitleLines);
  // the Old tab keeps the defaults its absolute positions were drawn for.
  function expandView(view, design) {
    const nodeHeight = design.nodeHeight || NODE_HEIGHT;
    const rowStep = design.gridRowStep || GRID_ROW_STEP;
    const placedNodes = view.nodes.map((placed) => (Array.isArray(placed)
      ? { id: placed[0], x: GRID_LEFT + placed[1] * GRID_COLUMN_STEP, y: GRID_TOP + placed[2] * rowStep }
      : placed));
    const edges = (view.edges || []).map((edge) => (Array.isArray(edge)
      ? { source: edge[0], target: edge[1], label: edge[2] || '', style: edge[3] || '' }
      : edge));
    return {
      ...view,
      kind: view.kind || '',
      caption: view.caption || '',
      nodes: placedNodes,
      edges,
      order: view.order || placedNodes.map((placed) => placed.id),
      width: view.width || Math.max(...placedNodes.map((placed) => placed.x)) + NODE_WIDTH + 60,
      height: view.height || Math.max(...placedNodes.map((placed) => placed.y)) + nodeHeight + 60,
      nodeHeight,
      subtitleLines: design.subtitleLines || 2,
    };
  }

  // A design may leave out what it does not use yet.
  const LIST_FIELDS = ['views', 'profiles', 'documents'];
  const MAP_FIELDS = ['nodes', 'issues', 'dropped', 'drilldowns'];
  DESIGN_ORDER.forEach((designId) => {
    const design = designs[designId];
    LIST_FIELDS.forEach((field) => { design[field] = design[field] || []; });
    MAP_FIELDS.forEach((field) => { design[field] = design[field] || {}; });
    design.views = design.views.map((view) => expandView(view, design));
  });

  function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, (character) => (
      { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[character]
    ));
  }

  function currentDesign() { return designs[state.designId]; }
  function currentPosition() { return state.positions[state.designId]; }

  function currentView() {
    const design = currentDesign();
    return design.views.find((view) => view.id === currentPosition().viewId) || design.views[0] || null;
  }

  function activeProfile(design = currentDesign()) {
    if (!design.profiles.length) return null;
    return design.profiles.find((profile) => profile.id === state.profiles[design.id]) || design.profiles[0];
  }

  function visibleEdges(view, design = currentDesign()) {
    const profile = activeProfile(design);
    return view.edges.filter((edge) => !edge.profiles || (profile && edge.profiles.includes(profile.id)));
  }

  function openIssueCount(design, node) {
    const profile = activeProfile(design);
    if (profile && !profile.showIssueCount) return 0;
    return (node.issues || []).filter((issueKey) => design.issues[issueKey]?.open).length;
  }

  function carriedInto(oldNodeId) {
    return Object.entries(designs.new.nodes)
      .filter(([, node]) => (node.from || []).includes(oldNodeId))
      .map(([newNodeId]) => newNodeId);
  }

  function migrationStatus(oldNodeId) {
    if (carriedInto(oldNodeId).length) return 'carried';
    if (designs.new.dropped[oldNodeId]) return 'dropped';
    return 'open';
  }

  function migrationCounts() {
    const counts = { carried: 0, dropped: 0, open: 0 };
    Object.keys(designs.old.nodes).forEach((oldNodeId) => { counts[migrationStatus(oldNodeId)] += 1; });
    return counts;
  }

  function firstViewWith(design, nodeId) {
    return design.views.find((view) => view.order.includes(nodeId)) || null;
  }

  function referenceLinks(design, references) {
    return (references || []).map((reference) => {
      const location = reference.path + (reference.line ? `:${reference.line}` : '');
      const href = design.repositoryRoot + reference.path + (reference.line ? `#L${reference.line}` : '');
      return `<div class="ref"><a class="ref__path" href="${escapeHtml(href)}" target="_blank" rel="noopener">${escapeHtml(location)}</a>`
        + (reference.symbol ? `<span class="ref__symbol">${escapeHtml(reference.symbol)}</span>` : '')
        + '</div>';
    }).join('');
  }

  // ------------------------------------------------------------------ the address

  function readAddress() {
    const segments = decodeURIComponent(window.location.hash.slice(1)).split('/').filter(Boolean);
    if (!segments.length) return;
    let designId = 'old';
    let remaining = segments;
    if (designs[segments[0]]) {
      designId = segments[0];
      remaining = segments.slice(1);
    }
    const design = designs[designId];
    const [viewId, nodeId, profileId] = remaining;
    state.designId = designId;
    if (viewId && design.views.some((view) => view.id === viewId)) state.positions[designId].viewId = viewId;
    if (nodeId) state.positions[designId].nodeId = nodeId;
    if (profileId && design.profiles.some((profile) => profile.id === profileId)) state.profiles[designId] = profileId;
  }

  function writeAddress() {
    const parts = [state.designId];
    const view = currentView();
    if (view) parts.push(view.id, currentPosition().nodeId);
    const profile = activeProfile();
    if (profile) parts.push(profile.id);
    try { window.history.replaceState(null, '', `#${parts.join('/')}`); } catch (error) { /* file:// may refuse */ }
  }

  function settlePosition() {
    const view = currentView();
    const position = currentPosition();
    if (!view) { position.viewId = null; position.nodeId = null; return; }
    position.viewId = view.id;
    if (!view.order.includes(position.nodeId)) position.nodeId = view.order[0];
  }

  // ------------------------------------------------------------------ the top bar and the heading

  function renderBar() {
    elements.designTabs.innerHTML = DESIGN_ORDER.map((designId) => {
      const design = designs[designId];
      const count = Object.keys(design.nodes).length;
      return `<a class="ticker${count ? '' : ' ticker--empty'}" href="#${designId}" data-design="${designId}"`
        + `${designId === state.designId ? ' aria-current="page"' : ''}>${escapeHtml(design.title)}`
        + `<span class="ticker__count">${count}</span></a>`;
    }).join('');

    const design = currentDesign();
    const profile = activeProfile(design);
    elements.profileField.hidden = !profile;
    if (profile) {
      elements.profileSelect.innerHTML = design.profiles
        .map((option) => `<option value="${escapeHtml(option.id)}">${escapeHtml(option.label)}</option>`).join('');
      elements.profileSelect.value = profile.id;
    }
  }

  function renderHeading() {
    const design = currentDesign();
    const counts = migrationCounts();
    elements.heading.textContent = design.heading;
    elements.summary.textContent = design.summary;
    const facts = [`${Object.keys(design.nodes).length} 个组件`, `${design.views.length} 张视图`];
    if (design.source) {
      facts.unshift(`源码快照 ${design.source.snapshot} · ${design.source.revision} · main ${design.source.head.slice(0, 9)}`);
    }
    facts.push(`迁移：已迁入 ${counts.carried} · 不迁 ${counts.dropped} · 未决定 ${counts.open}`);
    elements.meta.innerHTML = facts.map((fact) => `<span>${escapeHtml(fact)}</span>`).join('')
      + (design.source ? `<a href="${escapeHtml(design.source.page)}" target="_blank" rel="noopener">原页面</a>` : '')
      + (design.prd ? `<button class="text-button" type="button" data-prd-path="${escapeHtml(design.prd)}" data-prd-title="${escapeHtml(design.prdTitle || design.heading)}">查看系统 PRD ↗</button>` : '');
  }

  // ------------------------------------------------------------------ a view

  // A design with one view has nothing to switch between, so its tabs stay hidden.
  function renderViewTabs() {
    const design = currentDesign();
    const view = currentView();
    elements.viewTabs.hidden = design.views.length < 2;
    elements.viewTabs.innerHTML = design.views.map((candidate) => (
      `<button class="filter" type="button" data-view="${escapeHtml(candidate.id)}" aria-pressed="${candidate.id === view.id}">`
      + `${escapeHtml(candidate.title)}<span class="filter__count">${candidate.order.length}</span></button>`
    )).join('');
  }

  function renderViewHead() {
    const view = currentView();
    const profile = activeProfile();
    elements.viewTitle.innerHTML = `${escapeHtml(view.title)}<span class="view-head__kind">${escapeHtml(view.kind)}</span>`;
    elements.viewCaption.textContent = view.caption;
    const notice = profile && view.notices ? view.notices[profile.id] : null;
    elements.banner.hidden = !profile;
    if (profile) {
      elements.banner.innerHTML = `<span class="pill pill--strong">${escapeHtml(profile.tag)}</span>`
        + `<div class="banner__lines">${profile.lines.map((line) => `<span>${escapeHtml(line)}</span>`).join('')}`
        + (notice ? `<span class="banner__notice">${escapeHtml(notice)}</span>` : '')
        + '</div>';
    }
  }

  function renderLegend() {
    const design = currentDesign();
    const kindsInDesign = Object.keys(KINDS).filter((kind) => Object.values(design.nodes).some((node) => node.kind === kind));
    elements.legend.innerHTML = kindsInDesign
      .map((kind) => `<span class="legend__item"><i class="glyph glyph--${kind}"></i>${KINDS[kind]}</span>`).join('')
      + LINE_STYLES.map(([style, label]) => `<span class="legend__item"><i class="line-sample${style ? ` line-sample--${style}` : ''}"></i>${label}</span>`).join('');
  }

  function renderSteps() {
    const view = currentView();
    const design = currentDesign();
    const selectedNodeId = currentPosition().nodeId;
    elements.steps.innerHTML = view.order.map((nodeId, index) => (
      `<button class="step" type="button" data-node="${escapeHtml(nodeId)}" aria-pressed="${nodeId === selectedNodeId}"`
      + ` title="${index + 1}. ${escapeHtml(design.nodes[nodeId].title)}">${index + 1}</button>`
    )).join('');
  }

  // Where an edge runs between two placed nodes: the old page's routing, unchanged.
  function edgePath(edge, placedNodes, view) {
    const from = placedNodes[edge.source];
    const to = placedNodes[edge.target];
    let startX = from.x + NODE_WIDTH / 2;
    let startY = from.y + view.nodeHeight / 2;
    let endX = to.x + NODE_WIDTH / 2;
    let endY = to.y + view.nodeHeight / 2;
    const deltaX = endX - startX;
    const deltaY = endY - startY;
    if (edge.route === 'bottom') {
      startY = from.y + view.nodeHeight;
      endY = to.y + view.nodeHeight;
      const laneY = Math.min(view.height - 13, Math.max(startY, endY) + 26);
      return { d: `M${startX},${startY} V${laneY} H${endX} V${endY}` };
    }
    if (edge.route === 'left') {
      startX = from.x; endX = to.x;
      const laneX = 8;
      return { d: `M${startX},${startY} H${laneX} V${endY} H${endX}` };
    }
    if (edge.route === 'right') {
      startX = from.x + NODE_WIDTH; endX = to.x + NODE_WIDTH;
      const laneX = view.width - 9;
      return { d: `M${startX},${startY} H${laneX} V${endY} H${endX}` };
    }
    if (Math.abs(deltaY) < 5) {
      startX = deltaX > 0 ? from.x + NODE_WIDTH : from.x;
      endX = deltaX > 0 ? to.x : to.x + NODE_WIDTH;
      return { d: `M${startX},${startY} L${endX},${endY}` };
    }
    if (Math.abs(deltaX) < 5) {
      startY = deltaY > 0 ? from.y + view.nodeHeight : from.y;
      endY = deltaY > 0 ? to.y : to.y + view.nodeHeight;
      return { d: `M${startX},${startY} L${endX},${endY}` };
    }
    if (edge.route === 'down' || Math.abs(deltaY) > Math.abs(deltaX)) {
      startY = deltaY > 0 ? from.y + view.nodeHeight : from.y;
      endY = deltaY > 0 ? to.y : to.y + view.nodeHeight;
      const middleY = (startY + endY) / 2;
      return { d: `M${startX},${startY} V${middleY} H${endX} V${endY}` };
    }
    startX = deltaX > 0 ? from.x + NODE_WIDTH : from.x;
    endX = deltaX > 0 ? to.x : to.x + NODE_WIDTH;
    const middleX = (startX + endX) / 2;
    return { d: `M${startX},${startY} H${middleX} V${endY} H${endX}` };
  }

  function nodeMarkers(design, nodeId, node) {
    const markers = [];
    if (node.status) markers.push('<span class="pill pill--tiny pill--strong">已冻结</span>');
    if (node.draft) markers.push('<span class="pill pill--tiny pill--mixed">旧稿</span>');
    const issueCount = openIssueCount(design, node);
    if (issueCount) {
      markers.push(`<span class="pill pill--tiny pill--neutral" title="${issueCount} 个未解决问题">问题 ${issueCount}</span>`);
    }
    if (design.id === 'old') {
      const status = migrationStatus(nodeId);
      if (status !== 'open') markers.push(`<span class="${MIGRATION_PILLS[status]} pill--tiny">${MIGRATION_LABELS[status]}</span>`);
    }
    if (design.drilldowns[nodeId]) markers.push('<span class="pill pill--tiny pill--quiet" title="点开有模块展开">展开 ↗</span>');
    return markers.length ? `<span class="node__markers">${markers.join('')}</span>` : '';
  }

  function renderDiagram() {
    const design = currentDesign();
    const view = currentView();
    const selectedNodeId = currentPosition().nodeId;
    const placedNodes = Object.fromEntries(view.nodes.map((placed) => [placed.id, placed]));
    const edges = visibleEdges(view);

    elements.canvas.style.width = `${view.width}px`;
    elements.canvas.style.height = `${view.height}px`;
    elements.nodes.innerHTML = view.nodes.map((placed) => {
      const node = design.nodes[placed.id];
      return `<button type="button" class="node node--${node.kind}" style="left:${placed.x}px;top:${placed.y}px;height:${view.nodeHeight}px;--sub-lines:${view.subtitleLines}"`
        + ` data-node="${escapeHtml(placed.id)}" aria-pressed="${placed.id === selectedNodeId}">`
        + `<span class="node__kind">${node.kind ? `<i class="glyph glyph--${node.kind}"></i>${escapeHtml(KINDS[node.kind] || node.kind)}` : ''}`
        + `${nodeMarkers(design, placed.id, node)}</span>`
        + `<span class="node__title">${escapeHtml(node.title)}</span>`
        + `<span class="node__sub">${escapeHtml(node.subtitle)}</span>`
        + '</button>';
    }).join('');

    elements.edges.setAttribute('width', view.width);
    elements.edges.setAttribute('height', view.height);
    const markers = '<defs>'
      + '<marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" style="fill: var(--ink-4)"/></marker>'
      + '<marker id="arrow-active" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" style="fill: var(--ink)"/></marker>'
      + '</defs>';
    // An edge's label is shown in the detail's connection list, not on the canvas, where nodes would cover it.
    const paths = edges.map((edge) => {
      const route = edgePath(edge, placedNodes, view);
      const active = edge.source === selectedNodeId || edge.target === selectedNodeId;
      return `<path class="edge${edge.style ? ` edge--${edge.style}` : ''}${active ? ' edge--active' : ''}" d="${route.d}"`
        + ` marker-end="url(#${active ? 'arrow-active' : 'arrow'})"/>`;
    }).join('');
    elements.edges.innerHTML = markers + paths;
    applyZoom();
  }

  // ------------------------------------------------------------------ the selected node

  function migrationBlock(design, nodeId, node) {
    if (design.id === 'old') {
      const status = migrationStatus(nodeId);
      let body = '<p class="detail__text">还未决定：迁入 New，或者写进 new-design.js 的 dropped 并写明理由。</p>';
      if (status === 'carried') {
        body = `<div class="jumps">${carriedInto(nodeId).map((newNodeId) => (
          `<button class="jump" type="button" data-go-design="new" data-go-node="${escapeHtml(newNodeId)}">→ ${escapeHtml(designs.new.nodes[newNodeId].title)}</button>`
        )).join('')}</div>`;
      } else if (status === 'dropped') {
        body = `<p class="detail__text">${escapeHtml(designs.new.dropped[nodeId])}</p>`;
      }
      return `<h3 class="detail__heading">在 New 中 <span class="${MIGRATION_PILLS[status]} pill--small">${MIGRATION_LABELS[status]}</span></h3>${body}`;
    }
    const sources = node.from || [];
    if (!sources.length) return '<h3 class="detail__heading">来自 Old</h3><p class="detail__text">新组件，不取代 Old 中的节点。</p>';
    return `<h3 class="detail__heading">来自 Old</h3><div class="jumps">${sources.map((oldNodeId) => (
      `<button class="jump" type="button" data-go-design="old" data-go-node="${escapeHtml(oldNodeId)}">← ${escapeHtml(designs.old.nodes[oldNodeId]?.title || oldNodeId)}</button>`
    )).join('')}</div>`;
  }

  function renderDetail() {
    const design = currentDesign();
    const view = currentView();
    const profile = activeProfile();
    const nodeId = currentPosition().nodeId;
    const node = design.nodes[nodeId];
    const index = view.order.indexOf(nodeId);

    const connections = visibleEdges(view)
      .filter((edge) => edge.source === nodeId || edge.target === nodeId)
      .map((edge) => {
        const outgoing = edge.source === nodeId;
        const otherNodeId = outgoing ? edge.target : edge.source;
        return `<li><button class="jump" type="button" data-select="${escapeHtml(otherNodeId)}">${outgoing ? '→' : '←'} ${escapeHtml(design.nodes[otherNodeId].title)}</button>`
          + (edge.label ? `<span class="connection__label">${escapeHtml(edge.label)}</span>` : '') + '</li>';
      }).join('');

    const variant = node.variant
      ? `<p class="detail__note">${escapeHtml((profile && node.variant[profile.id]) || node.variantFallback || '')}</p>` : '';
    const drilldownButton = design.drilldowns[nodeId]
      ? `<button class="action" type="button" data-drilldown="${escapeHtml(nodeId)}">${escapeHtml(design.drilldowns[nodeId].button)} ↗</button>` : '';
    const prdButton = node.prd
      ? `<button class="action action--quiet" type="button" data-prd-path="${escapeHtml(node.prd)}" data-prd-title="${escapeHtml(node.title)}">查看 PRD ↗</button>` : '';
    const drilldown = drilldownButton || prdButton ? `<div class="detail__actions">${drilldownButton}${prdButton}</div>` : '';
    // A node shows only the fields it has, so a New node can start as a title and grow.
    const facts = [['输入', node.inputs], ['输出', node.outputs], ['约束与边界', node.checks]]
      .filter(([, value]) => value)
      .map(([label, value]) => `<dt>${label}</dt><dd>${escapeHtml(value)}</dd>`).join('');
    const issues = (node.issues || []).map((issueKey) => {
      const issue = design.issues[issueKey];
      return `<li class="issue"><div class="issue__head"><strong>${escapeHtml(issue.label)}</strong>`
        + `<span class="pill pill--small ${issue.open ? 'pill--strong' : 'pill--quiet'}">${escapeHtml(issue.status)}</span></div>`
        + `<p class="detail__text">${escapeHtml(issue.detail)}</p>`
        + `<a class="ref__path" href="${escapeHtml(design.repositoryRoot + issue.evidence)}" target="_blank" rel="noopener">${escapeHtml(issue.evidence)}</a>`
        + `${referenceLinks(design, issue.refs)}</li>`;
    }).join('');

    elements.detail.innerHTML = `
      <div class="detail__nav">
        <button class="text-button" type="button" data-step="-1"${index === 0 ? ' disabled' : ''}>← 上一个</button>
        <span class="num detail__count">${index + 1} / ${view.order.length}</span>
        <button class="text-button" type="button" data-step="1"${index === view.order.length - 1 ? ' disabled' : ''}>下一个 →</button>
      </div>
      ${node.kind ? `<div class="detail__pills"><span class="pill pill--quiet"><i class="glyph glyph--${node.kind}"></i>${escapeHtml(KINDS[node.kind] || node.kind)}</span>${node.status ? `<span class="pill pill--strong">${escapeHtml(node.status)}</span>` : ''}${node.draft ? `<span class="pill pill--mixed">${escapeHtml(node.draft)}</span>` : ''}</div>` : ''}
      <h2 class="detail__title">${escapeHtml(node.title)}</h2>
      ${node.subtitle ? `<p class="detail__subtitle">${escapeHtml(node.subtitle)}</p>` : ''}
      ${node.purpose ? `<p class="detail__purpose">${escapeHtml(node.purpose)}</p>` : ''}
      ${drilldown}
      ${variant}
      ${facts ? `<dl class="facts detail__facts">${facts}</dl>` : ''}
      ${(node.inspect || []).length ? `<h3 class="detail__heading">检查顺序</h3><ol class="detail__steps">${node.inspect.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ol>` : ''}
      ${(node.verified || []).length ? `<h3 class="detail__heading">验证</h3><ul class="detail__steps">${node.verified.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>` : ''}
      ${(node.open || []).length ? `<h3 class="detail__heading">还没定的</h3><ul class="detail__steps">${node.open.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>` : ''}
      ${connections ? `<h3 class="detail__heading">本视图中的连接</h3><ul class="connections">${connections}</ul>` : ''}
      ${(node.refs || []).length ? `<h3 class="detail__heading">代码位置</h3><div class="refs">${referenceLinks(design, node.refs)}</div>` : ''}
      ${issues ? `<h3 class="detail__heading">已记录的问题</h3><ul class="issues">${issues}</ul>` : ''}
      ${migrationBlock(design, nodeId, node)}`;
  }

  // ------------------------------------------------------------------ the New tab's migration list

  function renderMigration() {
    const showMigration = state.designId === 'new';
    elements.migration.hidden = !showMigration;
    if (!showMigration) return;
    const counts = migrationCounts();
    const listed = new Set();
    const groups = designs.old.views.map((view) => {
      const nodeIds = view.order.filter((nodeId) => !listed.has(nodeId));
      nodeIds.forEach((nodeId) => listed.add(nodeId));
      if (!nodeIds.length) return '';
      const items = nodeIds.map((nodeId) => {
        const node = designs.old.nodes[nodeId];
        const status = migrationStatus(nodeId);
        return `<li><button class="migration__item" type="button" data-go-design="old" data-go-view="${escapeHtml(view.id)}" data-go-node="${escapeHtml(nodeId)}">`
          + `<i class="glyph glyph--${node.kind}"></i>`
          + `<span class="migration__name">${escapeHtml(node.title)}<span class="migration__sub">${escapeHtml(node.subtitle)}</span></span>`
          + `<span class="${MIGRATION_PILLS[status]} pill--small">${MIGRATION_LABELS[status]}</span>`
          + '</button></li>';
      }).join('');
      return `<section class="migration__group"><h3 class="migration__view">${escapeHtml(view.title)}</h3><ul class="migration__list">${items}</ul></section>`;
    }).join('');
    // Folded by default: the list serves the move from Old, not the reading of New.
    elements.migration.innerHTML = `
      <details class="migration__fold">
        <summary>
          <h2 class="block__title">迁移清单</h2>
          <p class="block__note">Old 共 ${Object.keys(designs.old.nodes).length} 个组件 · 已迁入 ${counts.carried} · 不迁 ${counts.dropped} · 未决定 ${counts.open}</p>
        </summary>
        <p class="migration__lead">每个 Old 组件只列在它第一次出现的视图下。点一下切到 Old 并选中它。</p>
        <div class="migration__groups">${groups}</div>
      </details>`;
  }

  function renderDocuments() {
    const design = currentDesign();
    elements.documents.innerHTML = (design.documents || []).map((document) => (
      `<a href="${escapeHtml(design.repositoryRoot + document.path)}" target="_blank" rel="noopener">${escapeHtml(document.label)}</a>`
    )).join('') + (design.source ? `<span class="documents__note">${escapeHtml(design.source.note)}</span>` : '');
  }

  // ------------------------------------------------------------------ zoom and movement

  function applyZoom() {
    const view = currentView();
    if (!view) return;
    elements.canvas.style.transform = `scale(${state.zoom})`;
    elements.canvas.style.marginRight = `${view.width * (state.zoom - 1)}px`;
    elements.canvas.style.marginBottom = `${view.height * (state.zoom - 1)}px`;
    elements.zoomLabel.textContent = `${Math.round(state.zoom * 100)}%`;
  }

  function fitZoom() {
    const view = currentView();
    if (!view) return;
    state.zoom = Math.max(ZOOM_MIN, Math.min(1, (elements.viewport.clientWidth - 16) / view.width));
    elements.viewport.scrollTo(0, 0);
  }

  function panToSelected() {
    const view = currentView();
    const placed = view.nodes.find((candidate) => candidate.id === currentPosition().nodeId);
    if (!placed) return;
    elements.viewport.scrollTo({
      left: Math.max(0, placed.x * state.zoom - 60),
      top: Math.max(0, placed.y * state.zoom - 60),
      behavior: 'smooth',
    });
  }

  function renderAll({ fit = false, pan = false } = {}) {
    settlePosition();
    renderBar();
    renderHeading();
    const view = currentView();
    elements.panel.hidden = !view;
    if (view) {
      renderViewTabs();
      renderViewHead();
      renderLegend();
      if (fit) fitZoom();
      renderSteps();
      renderDiagram();
      renderDetail();
      if (pan) panToSelected();
    }
    renderMigration();
    renderDocuments();
    writeAddress();
  }

  function selectNode(nodeId, pan) {
    if (!currentView().order.includes(nodeId)) return;
    currentPosition().nodeId = nodeId;
    renderSteps();
    renderDiagram();
    renderDetail();
    writeAddress();
    if (pan) panToSelected();
  }

  function goTo(designId, nodeId, viewId) {
    const design = designs[designId];
    const view = (viewId && design.views.find((candidate) => candidate.id === viewId)) || firstViewWith(design, nodeId);
    if (!view) return;
    state.designId = designId;
    state.positions[designId] = { viewId: view.id, nodeId };
    renderAll({ fit: true, pan: true });
    window.scrollTo({ top: 0 });
  }

  // ------------------------------------------------------------------ the drill-down sheet

  function openDrilldown(nodeId) {
    const design = currentDesign();
    const drilldown = design.drilldowns[nodeId];
    if (!drilldown) return;
    state.focusBeforeSheet = document.activeElement;
    elements.sheetPanel.classList.toggle('sheet__panel--full', drilldown.size === 'full');
    elements.sheetKicker.textContent = drilldown.kicker;
    elements.sheetBody.replaceChildren();
    drilldown.render(elements.sheetBody, {
      getProfile: () => activeProfile(design)?.id,
      setProfile: (profileId) => { state.profiles[design.id] = profileId; renderAll(); },
      referenceLinks: (references) => referenceLinks(design, references),
      escapeHtml,
    });
    elements.sheetBody.scrollTop = 0;
    const node = design.nodes[nodeId];
    elements.sheetActions.innerHTML = node && node.prd
      ? `<button class="action action--quiet" type="button" data-prd-path="${escapeHtml(node.prd)}" data-prd-title="${escapeHtml(node.title)}">查看这个模块的 PRD ↗</button>`
      : '';
    elements.sheet.hidden = false;
    elements.sheetPanel.focus();
  }

  // A PRD opens in the sheet. Served over HTTP the page reads the .md file itself; opened from disk the browser refuses
  // that read, and the copy bundled by docs/prd/build_bundle.py (prd-bundle.js) is shown instead.
  function openPrd(path, title) {
    const design = currentDesign();
    state.focusBeforeSheet = document.activeElement;
    elements.sheetPanel.classList.add('sheet__panel--full');
    elements.sheetKicker.textContent = `PRD · ${title}`;
    elements.sheetBody.innerHTML = '<p class="prd__source">正在打开…</p>';
    elements.sheet.hidden = false;
    elements.sheetPanel.focus();
    const backTo = Object.keys(design.nodes || {}).find((id) => design.nodes[id].prd === path && (design.drilldowns || {})[id]);
    elements.sheetActions.innerHTML = backTo
      ? `<button class="action action--quiet" type="button" data-drilldown="${escapeHtml(backTo)}">← 回到展开页</button>` : '';
    const show = (markdown, fromBundle) => {
      elements.sheetBody.innerHTML = `<p class="prd__source">来源：<code>${escapeHtml(path)}</code>${fromBundle ? '（打包副本）' : ''}</p>`
        + `<article class="prd">${window.HIVEMIND_MARKDOWN.render(markdown)}</article>`;
      elements.sheetBody.scrollTop = 0;
    };
    const bundled = (window.HIVEMIND_PRD || {})[path];
    fetch(`${design.repositoryRoot || ''}${path}`)
      .then((response) => (response.ok ? response.text() : Promise.reject(new Error(String(response.status)))))
      .then((markdown) => show(markdown, false))
      .catch(() => {
        if (bundled !== undefined) { show(bundled, true); return; }
        elements.sheetBody.innerHTML = `<p class="prd__source">找不到 <code>${escapeHtml(path)}</code>：重跑 <code>python3 docs/prd/build_bundle.py</code> 后刷新。</p>`;
      });
  }

  function closeSheet() {
    if (elements.sheet.hidden) return;
    elements.sheet.hidden = true;
    state.focusBeforeSheet?.focus?.();
  }

  // ------------------------------------------------------------------ events

  elements.designTabs.addEventListener('click', (event) => {
    const tab = event.target.closest('[data-design]');
    if (!tab) return;
    event.preventDefault();
    state.designId = tab.dataset.design;
    renderAll({ fit: true });
  });

  elements.profileSelect.addEventListener('change', () => {
    state.profiles[state.designId] = elements.profileSelect.value;
    renderAll();
  });

  elements.viewTabs.addEventListener('click', (event) => {
    const tab = event.target.closest('[data-view]');
    if (!tab) return;
    currentPosition().viewId = tab.dataset.view;
    currentPosition().nodeId = null;
    renderAll({ fit: true });
  });

  elements.steps.addEventListener('click', (event) => {
    const step = event.target.closest('[data-node]');
    if (step) selectNode(step.dataset.node, true);
  });

  elements.nodes.addEventListener('click', (event) => {
    const nodeButton = event.target.closest('[data-node]');
    if (!nodeButton) return;
    selectNode(nodeButton.dataset.node, false);
    if (currentDesign().drilldowns[nodeButton.dataset.node]) openDrilldown(nodeButton.dataset.node);
  });

  function followJump(event) {
    const stepButton = event.target.closest('[data-step]');
    if (stepButton) {
      const view = currentView();
      const index = view.order.indexOf(currentPosition().nodeId) + Number(stepButton.dataset.step);
      if (index >= 0 && index < view.order.length) selectNode(view.order[index], true);
      return;
    }
    const selectButton = event.target.closest('[data-select]');
    if (selectButton) { selectNode(selectButton.dataset.select, true); return; }
    const drilldownButton = event.target.closest('[data-drilldown]');
    if (drilldownButton) { openDrilldown(drilldownButton.dataset.drilldown); return; }
    const prdButton = event.target.closest('[data-prd-path]');
    if (prdButton) { openPrd(prdButton.dataset.prdPath, prdButton.dataset.prdTitle); return; }
    const jumpButton = event.target.closest('[data-go-design]');
    if (jumpButton) goTo(jumpButton.dataset.goDesign, jumpButton.dataset.goNode, jumpButton.dataset.goView);
  }
  elements.detail.addEventListener('click', followJump);
  elements.migration.addEventListener('click', followJump);
  elements.meta.addEventListener('click', (event) => {
    const prdButton = event.target.closest('[data-prd-path]');
    if (prdButton) openPrd(prdButton.dataset.prdPath, prdButton.dataset.prdTitle);
  });

  elements.zoomIn.addEventListener('click', () => { state.zoom = Math.min(ZOOM_MAX, state.zoom + 0.1); applyZoom(); });
  elements.zoomOut.addEventListener('click', () => { state.zoom = Math.max(ZOOM_MIN, state.zoom - 0.1); applyZoom(); });
  elements.zoomFit.addEventListener('click', () => { fitZoom(); applyZoom(); });

  // Links in the sheet's top bar and body: a detail page opens its module's PRD, and a PRD goes back to its detail page.
  function followSheetLink(event) {
    const prdButton = event.target.closest('[data-prd-path]');
    if (prdButton) { openPrd(prdButton.dataset.prdPath, prdButton.dataset.prdTitle); return; }
    const drilldownButton = event.target.closest('[data-drilldown]');
    if (drilldownButton) openDrilldown(drilldownButton.dataset.drilldown);
  }
  elements.sheetBody.addEventListener('click', followSheetLink);
  elements.sheetActions.addEventListener('click', followSheetLink);
  elements.sheetClose.addEventListener('click', closeSheet);
  elements.sheetScrim.addEventListener('click', closeSheet);
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') closeSheet(); });

  window.addEventListener('hashchange', () => { readAddress(); renderAll({ fit: true, pan: true }); });

  readAddress();
  renderAll({ fit: true, pan: true });
})();
