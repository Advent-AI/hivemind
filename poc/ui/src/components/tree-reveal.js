const TIMING = { idea: 360, line: 650, thesis: 280, pause: 140, finish: 650 };
const ease = (value) => value * value * (3 - 2 * value);
const mix = (from, to, amount) => from + (to - from) * amount;

/** Visit each root and its connected descendants in their existing display order. */
export function revealSequence(edges, rootId = 'idea') {
  const children = new Map();
  for (const edge of edges) {
    if (!children.has(edge.sourceId)) children.set(edge.sourceId, []);
    children.get(edge.sourceId).push(edge);
  }
  const sequence = [];
  function visit(id) {
    for (const edge of children.get(id) || []) {
      sequence.push(edge);
      visit(edge.targetId);
    }
  }
  visit(rootId);
  return sequence;
}

function tween(duration, update, signal) {
  return new Promise((resolve, reject) => {
    let frame;
    const started = performance.now();
    const abort = () => {
      cancelAnimationFrame(frame);
      reject(new DOMException('Tree reveal cancelled', 'AbortError'));
    };
    if (signal.aborted) return abort();
    signal.addEventListener('abort', abort, { once: true });
    const tick = (now) => {
      try {
        const progress = Math.min(1, (now - started) / duration);
        update(ease(progress));
        if (progress < 1) frame = requestAnimationFrame(tick);
        else {
          signal.removeEventListener('abort', abort);
          resolve();
        }
      } catch (error) {
        signal.removeEventListener('abort', abort);
        reject(error);
      }
    };
    frame = requestAnimationFrame(tick);
  });
}

/** Reveal one completed tree; cancellation settles visibility and preserves the current camera. */
export function createTreeReveal({ stage, readCamera, writeCamera }) {
  let active = null;
  const center = (node) => ({
    x: node.offsetLeft + node.offsetWidth / 2,
    y: node.offsetTop + node.offsetHeight / 2,
  });
  const cameraAt = (point) => ({
    x: stage.clientWidth / 2 - point.x,
    y: stage.clientHeight / 2 - point.y,
    zoom: 1,
  });
  function settle(run) {
    for (const node of run.nodes) {
      node.classList.add('is-on');
      node.style.opacity = '';
      node.style.transform = '';
      node.inert = false;
      node.removeAttribute('aria-hidden');
    }
    for (const path of run.paths) {
      path.style.opacity = '';
      path.style.strokeDasharray = '';
      path.style.strokeDashoffset = '';
      path.style.markerEnd = '';
    }
    // Commit the final appearance before restoring normal card transitions.
    void stage.offsetWidth;
    stage.classList.remove('is-revealing');
    delete stage.dataset.revealPhase;
    delete stage.dataset.revealNode;
  }
  function cancel() {
    if (!active) return;
    const run = active;
    active = null;
    run.controller.abort();
    settle(run);
  }
  async function play({ root, steps, restingCamera, finalCards = [] }) {
    cancel();
    const run = {
      nodes: [root, ...steps.map((step) => step.target), ...finalCards.map((card) => card.node)],
      paths: [...steps.map((step) => step.path), ...finalCards.map((card) => card.path)],
      controller: new AbortController(),
    };
    active = run;
    const signal = run.controller.signal;
    stage.classList.add('is-revealing');
    for (const node of run.nodes) {
      node.style.opacity = '0';
      node.inert = true;
      node.setAttribute('aria-hidden', 'true');
    }
    for (const path of run.paths) {
      path.style.opacity = '0';
      path.style.markerEnd = 'none';
    }
    const moveTo = (target, duration) => {
      const from = readCamera();
      return tween(
        duration,
        (p) =>
          writeCamera({
            x: mix(from.x, target.x, p),
            y: mix(from.y, target.y, p),
            zoom: mix(from.zoom, target.zoom, p),
          }),
        signal,
      );
    };
    const enter = async (node, duration, path = null) => {
      stage.dataset.revealPhase = 'card';
      stage.dataset.revealNode = node.dataset.id;
      await tween(
        duration,
        (p) => {
          node.style.opacity = String(p);
          node.style.transform = `translateY(${8 * (1 - p)}px)`;
          if (path) path.style.opacity = String(p);
        },
        signal,
      );
      node.classList.add('is-on');
      node.inert = false;
      node.removeAttribute('aria-hidden');
      if (path) path.style.markerEnd = '';
    };
    try {
      writeCamera(cameraAt(center(root)));
      await enter(root, TIMING.idea);
      const firstColumn = steps[0]?.target.offsetLeft;
      const columnWidth = Math.max(
        0,
        ...steps
          .filter(({ target }) => target.offsetLeft === firstColumn)
          .map(({ target }) => target.offsetWidth),
      );
      const columnX = firstColumn + columnWidth / 2;
      for (const { target, path } of steps) {
        const length = path.getTotalLength();
        const from = readCamera();
        const to = cameraAt({ x: columnX, y: center(target).y });
        path.style.strokeDasharray = String(length);
        path.style.strokeDashoffset = String(length);
        path.style.opacity = '1';
        stage.dataset.revealPhase = 'line';
        stage.dataset.revealNode = target.dataset.id;
        await tween(
          TIMING.line,
          (p) => {
            path.style.strokeDashoffset = String(length * (1 - p));
            writeCamera({
              x: mix(from.x, to.x, p),
              y: mix(from.y, to.y, p),
              zoom: mix(from.zoom, to.zoom, p),
            });
          },
          signal,
        );
        path.style.strokeDasharray = '';
        path.style.strokeDashoffset = '';
        path.style.markerEnd = '';
        await enter(target, TIMING.thesis);
        await tween(TIMING.pause, () => {}, signal);
      }
      stage.dataset.revealPhase = 'return';
      await moveTo(restingCamera, TIMING.finish);
      for (const card of finalCards) await enter(card.node, TIMING.thesis, card.path);
    } catch (error) {
      if (error.name !== 'AbortError') throw error;
    } finally {
      if (active === run) {
        active = null;
        settle(run);
      }
    }
  }
  return {
    play,
    cancel,
    get running() {
      return active !== null;
    },
  };
}
