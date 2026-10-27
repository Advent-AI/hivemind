import { element } from './dom.js';
import { createThesisCard } from './thesis-card.js';
import { badgeHtml } from './primitives.js';
import { CH, chartStateY } from './thesis-chart.js';
import { assessmentAt } from '../model/thesis.js';
import { addDays, dayDiff, calendarX } from '../model/dates.js';
import { routeFanOut } from './connectors.js';
import { resolveGraph, layoutGraph } from '../model/graph.js';
import { createTreeReveal, revealSequence } from './tree-reveal.js';
import { createTriggerCard } from './trigger-card.js';
import { createActionCard } from './action-card.js';

let instanceCount = 0;
const ZOOM_ICONS = [
  '<path d="M12 5v14M5 12h14"/>',
  '<path d="M5 12h14"/>',
  '<path d="M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5"/>',
];
export function createCanvas({ root, onOpen = () => {}, onDayChange = () => {} }) {
  const scope = `canvas-${++instanceCount}`;
  const events = new AbortController();
  const stage = element('div', 'stage');
  stage.innerHTML = `<div class="world"><svg class="edges"></svg><div class="cards"></div></div><div class="replay" hidden><button type="button" data-play>▶ Replay</button><input type="range" min="0" step="1" aria-label="Replay date"><span class="num" data-day></span><div class="ranges"><button type="button" data-range="all">Full</button><button type="button" data-range="30d">Last 30 days</button></div></div><div class="zoom">${['Zoom in', 'Zoom out', 'Fit to view'].map((label, i) => `<button type="button" data-zoom="${i}" aria-label="${label}"><svg viewBox="0 0 24 24" aria-hidden="true">${ZOOM_ICONS[i]}</svg></button>`).join('')}</div>`;
  root.append(stage);
  const world = stage.querySelector('.world'),
    cards = stage.querySelector('.cards'),
    edges = stage.querySelector('.edges');
  const replay = stage.querySelector('.replay'),
    scrub = replay.querySelector('input'),
    play = replay.querySelector('[data-play]');
  let data = null,
    graph = null,
    day = null,
    range = 'all',
    frame = 0,
    running = false,
    destroyed = false;
  let zoom = 1,
    pan = { x: 0, y: 0 },
    dragging = null,
    moved = false,
    leading = null,
    trigger = null,
    action = null;
  let displayed = [];
  const start = () =>
    range === 'all'
      ? data.days[0] || data.as_of
      : [data.days[0] || data.as_of, addDays(data.as_of, -30)].sort().at(-1);
  const apply = () => {
    world.style.transform = `translate(${pan.x}px,${pan.y}px) scale(${zoom})`;
  };
  const treeReveal = createTreeReveal({
    stage,
    readCamera: () => ({ ...pan, zoom }),
    writeCamera(camera) {
      pan = { x: camera.x, y: camera.y };
      zoom = camera.zoom;
      apply();
    },
  });
  const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
  motionPreference.addEventListener(
    'change',
    (event) => {
      if (event.matches) treeReveal.cancel();
    },
    { signal: events.signal },
  );
  function stop() {
    treeReveal.cancel();
    trigger?.close();
    action?.close();
    running = false;
    cancelAnimationFrame(frame);
    play.textContent = '▶ Replay';
  }
  function cardBounds() {
    const nodes = [...cards.children];
    if (!nodes.length) return null;
    return {
      left: Math.min(...nodes.map((c) => c.offsetLeft)),
      top: Math.min(...nodes.map((c) => c.offsetTop)),
      right: Math.max(...nodes.map((c) => c.offsetLeft + c.offsetWidth)),
      bottom: Math.max(...nodes.map((c) => c.offsetTop + c.offsetHeight)),
    };
  }
  function fit() {
    treeReveal.cancel();
    const bounds = cardBounds();
    if (!bounds) return;
    const { left, top, right, bottom } = bounds;
    const safeTop = replay.hidden ? 24 : replay.offsetTop + replay.offsetHeight + 24;
    const width = stage.clientWidth - 48,
      height = stage.clientHeight - safeTop - 24;
    zoom = Math.max(0.35, Math.min(1, width / (right - left), height / (bottom - top)));
    pan = {
      x: 24 + (width - (right - left) * zoom) / 2 - left * zoom,
      y: safeTop + (height - (bottom - top) * zoom) / 2 - top * zoom,
    };
    apply();
  }
  function treeCamera() {
    const bounds = cardBounds();
    const scale = bounds ? Math.min(1, (stage.clientWidth - 48) / (bounds.right - bounds.left)) : 1;
    return bounds
      ? {
          x: stage.clientWidth / 2 - ((bounds.left + bounds.right) / 2) * scale,
          y: stage.clientHeight / 2 - ((bounds.top + bounds.bottom) / 2) * scale,
          zoom: scale,
        }
      : null;
  }
  function centerTree() {
    const camera = treeCamera();
    if (!camera) return;
    zoom = camera.zoom;
    pan = { x: camera.x, y: camera.y };
    apply();
  }
  function place(node, rect) {
    Object.assign(node.style, {
      left: `${rect.left}px`,
      top: `${rect.top}px`,
      width: `${rect.width}px`,
      height: `${rect.height}px`,
    });
  }
  function highlight(id) {
    if (treeReveal.running) return;
    const selected = new Set(),
      pending = id ? [id] : [],
      visited = new Set();
    while (pending.length) {
      const target = pending.pop();
      if (visited.has(target)) continue;
      visited.add(target);
      for (const edge of edges.querySelectorAll('.edge'))
        if (edge.dataset.target === target) {
          selected.add(edge);
          pending.push(edge.dataset.source);
        }
    }
    edges.querySelectorAll('.edge').forEach((edge) => {
      edge.classList.toggle('edge--on', selected.has(edge));
      edge.setAttribute(
        'marker-end',
        `url(#${scope}-${selected.has(edge) ? 'active-arrow' : 'arrow'})`,
      );
    });
    cards
      .querySelectorAll('.card')
      .forEach((card) => card.classList.toggle('is-hot', card.dataset.id === id));
  }
  function addCard(node, id, rect, show = true) {
    node.dataset.id = id;
    place(node, rect);
    cards.append(node);
    node.addEventListener('mouseenter', () => highlight(id));
    node.addEventListener('mouseleave', () => highlight(null));
    if (show)
      requestAnimationFrame(() => {
        if (!destroyed && node.isConnected) node.classList.add('is-on');
      });
    return node;
  }
  function fitLeading(node, centerY) {
    if (!node.classList.contains('has-composite')) return;
    node.style.height = 'auto';
    node.style.top = `${centerY - node.offsetHeight / 2}px`;
  }
  function connect(source, targets) {
    const bounds = (node) => ({
      left: node.offsetLeft,
      top: node.offsetTop,
      width: node.offsetWidth,
      height: node.offsetHeight,
    });
    for (const route of routeFanOut(bounds(source), targets.map(bounds))) {
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute(
        'class',
        `edge${source.classList.contains('card--trigger') || targets[route.index].classList.contains('card--trigger') ? ' edge--trigger' : ''}`,
      );
      path.dataset.source = source.dataset.id;
      path.dataset.target = targets[route.index].dataset.id;
      path.setAttribute('d', route.path);
      path.setAttribute('marker-end', `url(#${scope}-arrow)`);
      edges.append(path);
    }
  }
  function render(spec, { center = true, reveal = false } = {}) {
    const resolved = resolveGraph(spec, spec.dataset);
    const plan = layoutGraph(
      resolved,
      Boolean(spec.leadingCard),
      Boolean(spec.trigger),
      Boolean(spec.action),
    );
    const animate = reveal && plan.leading && !motionPreference.matches;
    stop();
    data = spec.dataset;
    graph = spec;
    day = spec.day || data.as_of;
    trigger?.destroy();
    trigger = null;
    action?.destroy();
    action = null;
    cards.replaceChildren();
    displayed = [];
    leading = null;
    const byId = new Map(data.theses.map((t) => [t.id, t]));
    const nodesById = new Map();
    if (plan.leading) {
      leading = addCard(
        spec.leadingCard({ width: plan.leading.width }),
        'idea',
        plan.leading,
        !animate,
      );
      fitLeading(leading, plan.leading.top + plan.leading.height / 2);
      nodesById.set('idea', leading);
    }
    if (plan.trigger) {
      trigger = createTriggerCard({
        condition: spec.trigger.condition,
        confidence: spec.trigger.getConfidence(),
        onChange: spec.trigger.onChange,
      });
      nodesById.set('trigger', addCard(trigger.element, 'trigger', plan.trigger, !animate));
    }
    if (plan.action) {
      action = createActionCard(spec.action);
      nodesById.set('action', addCard(action.element, 'action', plan.action, !animate));
    }
    function thesisNode(thesis, rect) {
      const node = createThesisCard(thesis, {
        day,
        start: start(),
        end: data.as_of,
        scope,
        weightPercent: spec.weightPercents ? (spec.weightPercents[thesis.id] ?? 0) : undefined,
        onOpen: (id) => {
          if (!moved) {
            stop();
            onOpen(id, day);
          }
        },
      });
      node.addEventListener('click', (event) => {
        if (!moved && !event.target.closest('button')) {
          stop();
          onOpen(thesis.id, day);
        }
      });
      addCard(node, thesis.id, rect, !animate);
      displayed.push({ node, thesis });
      return node;
    }
    for (const rect of plan.nodes) nodesById.set(rect.id, thesisNode(byId.get(rect.id), rect));
    edges.innerHTML = `<defs><marker id="${scope}-arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="10" markerHeight="10" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0 10 5 0 10Z" fill="var(--connector-color)"/></marker><marker id="${scope}-active-arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="10" markerHeight="10" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0 10 5 0 10Z" fill="var(--ink)"/></marker></defs>`;
    const outgoing = new Map();
    for (const edge of plan.edges) {
      if (!outgoing.has(edge.sourceId)) outgoing.set(edge.sourceId, []);
      outgoing.get(edge.sourceId).push(nodesById.get(edge.targetId));
    }
    for (const [sourceId, targets] of outgoing) connect(nodesById.get(sourceId), targets);
    edges.setAttribute(
      'width',
      Math.max(1, ...[...cards.children].map((c) => c.offsetLeft + c.offsetWidth)) + 80,
    );
    edges.setAttribute(
      'height',
      Math.max(1, ...[...cards.children].map((c) => c.offsetTop + c.offsetHeight)) + 80,
    );
    replay.hidden = !resolved.rootIds.length;
    setupReplay();
    if (animate) {
      const paths = new Map(
        [...edges.querySelectorAll('.edge')].map((path) => [path.dataset.target, path]),
      );
      void treeReveal.play({
        root: leading,
        steps: revealSequence(plan.edges).map((edge) => ({
          source: nodesById.get(edge.sourceId),
          target: nodesById.get(edge.targetId),
          path: paths.get(edge.targetId),
        })),
        restingCamera: treeCamera(),
        finalCards: [
          ...(trigger ? [{ node: trigger.element, path: paths.get('idea') }] : []),
          ...(action ? [{ node: action.element, path: paths.get('trigger') }] : []),
        ],
      });
    } else if (center) {
      if (spec.centerOn === 'tree') centerTree();
      else fit();
    }
  }
  function updateLeading() {
    if (!leading || !graph.leadingCard) return;
    const centerY = leading.offsetTop + leading.offsetHeight / 2;
    const replacement = graph.leadingCard({ width: leading.offsetWidth });
    replacement.classList.add('is-on');
    Object.assign(replacement.style, {
      left: leading.style.left,
      top: leading.style.top,
      width: leading.style.width,
      height: leading.style.height,
    });
    replacement.dataset.id = 'idea';
    leading.replaceWith(replacement);
    leading = replacement;
    fitLeading(leading, centerY);
    leading.addEventListener('mouseenter', () => highlight('idea'));
    leading.addEventListener('mouseleave', () => highlight(null));
    trigger?.setConfidence(graph.trigger.getConfidence());
  }
  function setupReplay() {
    scrub.max = String(dayDiff(start(), data.as_of));
    scrub.value = String(dayDiff(start(), day));
    replay.querySelector('[data-day]').textContent = day;
    replay
      .querySelectorAll('[data-range]')
      .forEach((button) =>
        button.setAttribute('aria-pressed', String(button.dataset.range === range)),
      );
  }
  function setDay(nextDay, fraction = dayDiff(start(), nextDay)) {
    treeReveal.cancel();
    day = nextDay;
    scrub.value = String(fraction);
    replay.querySelector('[data-day]').textContent = day;
    for (const { node, thesis } of displayed) {
      const x = calendarX(fraction, start(), data.as_of, CH.left, CH.W - CH.right),
        judgement = assessmentAt(thesis, day);
      node
        .querySelector('.js-clip')
        .setAttribute('width', fraction >= dayDiff(start(), data.as_of) ? CH.W : x);
      const dot = node.querySelector('.js-now');
      dot.style.display = judgement ? '' : 'none';
      dot.setAttribute('cx', x);
      if (judgement) dot.setAttribute('cy', chartStateY(thesis, judgement.rung));
      node
        .querySelectorAll('.axis-score')
        .forEach((axis) =>
          axis.classList.toggle('is-current', Number(axis.dataset.pos) === judgement?.rung),
        );
      node
        .querySelectorAll('.lane')
        .forEach((lane, i) => lane.classList.toggle('lane--cur', i + 1 === judgement?.rung));
      node.querySelector('.plot-badge').innerHTML = badgeHtml(thesis, judgement);
    }
    onDayChange(day, { start: start(), end: data.as_of });
    updateLeading();
  }
  scrub.addEventListener(
    'input',
    () => {
      stop();
      setDay(addDays(start(), Math.floor(Number(scrub.value))), Number(scrub.value));
    },
    { signal: events.signal },
  );
  replay.querySelectorAll('[data-range]').forEach((button) =>
    button.addEventListener(
      'click',
      () => {
        range = button.dataset.range;
        day = day < start() ? start() : day;
        onDayChange(day, { start: start(), end: data.as_of });
        render({ ...graph, day }, { center: false });
      },
      { signal: events.signal },
    ),
  );
  play.addEventListener(
    'click',
    () => {
      if (running) {
        stop();
        return;
      }
      running = true;
      play.textContent = '❚❚ Pause';
      const span = dayDiff(start(), data.as_of);
      let offset = Number(scrub.value) >= span ? 0 : Number(scrub.value),
        previous = performance.now();
      const tick = (now) => {
        if (!running || destroyed) return;
        offset += ((now - previous) / 1000) * Math.max(6, span / 8);
        previous = now;
        offset = Math.min(span, offset);
        setDay(addDays(start(), Math.floor(offset)), offset);
        if (offset >= span) stop();
        else frame = requestAnimationFrame(tick);
      };
      frame = requestAnimationFrame(tick);
    },
    { signal: events.signal },
  );
  stage.querySelectorAll('[data-zoom]').forEach((button) =>
    button.addEventListener(
      'click',
      () => {
        treeReveal.cancel();
        if (button.dataset.zoom === '2') fit();
        else {
          zoom = Math.max(
            0.35,
            Math.min(1.6, zoom * (button.dataset.zoom === '0' ? 1.15 : 1 / 1.15)),
          );
          apply();
        }
      },
      { signal: events.signal },
    ),
  );
  stage.addEventListener(
    'pointerdown',
    (event) => {
      treeReveal.cancel();
      if (event.button !== 0 || event.target.closest('button,input,a,select,label')) return;
      dragging = {
        x: event.clientX - pan.x,
        y: event.clientY - pan.y,
        startX: event.clientX,
        startY: event.clientY,
      };
      moved = false;
      stage.classList.add('is-dragging');
      event.preventDefault();
    },
    { signal: events.signal },
  );
  window.addEventListener(
    'pointermove',
    (event) => {
      if (!dragging) return;
      if (Math.hypot(event.clientX - dragging.startX, event.clientY - dragging.startY) > 3)
        moved = true;
      if (moved) {
        pan = { x: event.clientX - dragging.x, y: event.clientY - dragging.y };
        apply();
      }
    },
    { signal: events.signal },
  );
  const endDrag = () => {
    dragging = null;
    stage.classList.remove('is-dragging');
  };
  window.addEventListener('pointerup', endDrag, { signal: events.signal });
  window.addEventListener('pointercancel', endDrag, { signal: events.signal });
  stage.addEventListener(
    'click',
    (event) => {
      if (moved) {
        event.stopPropagation();
        event.preventDefault();
        moved = false;
      }
    },
    { capture: true, signal: events.signal },
  );
  stage.addEventListener(
    'wheel',
    (event) => {
      treeReveal.cancel();
      event.preventDefault();
      if (!event.ctrlKey && !event.metaKey) {
        pan = { x: pan.x - event.deltaX, y: pan.y - event.deltaY };
        apply();
        return;
      }
      const next = Math.max(0.35, Math.min(1.6, zoom * (event.deltaY < 0 ? 1.08 : 1 / 1.08))),
        r = stage.getBoundingClientRect(),
        x = event.clientX - r.left,
        y = event.clientY - r.top;
      pan = { x: x - ((x - pan.x) * next) / zoom, y: y - ((y - pan.y) * next) / zoom };
      zoom = next;
      apply();
    },
    { passive: false, signal: events.signal },
  );
  window.addEventListener('resize', () => treeReveal.cancel(), { signal: events.signal });
  return {
    render,
    setDay,
    fit,
    stop,
    updateLeading,
    get day() {
      return day;
    },
    destroy() {
      destroyed = true;
      stop();
      trigger?.destroy();
      action?.destroy();
      events.abort();
      stage.remove();
    },
  };
}
