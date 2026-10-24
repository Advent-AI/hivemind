export function createDisclosures(root) {
  const active = new Set();
  const events = new AbortController();
  const heightTransitions = new WeakMap();
  function stopHeightTransition(element, settle = false) {
    const job = heightTransitions.get(element);
    if (job) {
      job.animation.onfinish = null;
      job.animation.cancel();
      heightTransitions.delete(element);
      active.delete(element);
      if (settle) job.settle();
    }
    element.style.height = '';
    element.style.overflow = '';
    element.classList.remove('is-animating');
  }
  function animateHeight(element, from, to, settle) {
    const finish = () => {
      settle();
      element.style.height = '';
      element.style.overflow = '';
      element.classList.remove('is-animating');
    };
    if (
      Math.abs(from - to) < 0.5 ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches
    ) {
      finish();
      return;
    }
    element.style.height = `${from}px`;
    element.style.overflow = 'hidden';
    element.classList.add('is-animating');
    const animation = element.animate([{ height: `${from}px` }, { height: `${to}px` }], {
      duration: 240,
      easing: 'cubic-bezier(0.2, 0, 0, 1)',
      fill: 'forwards',
    });
    const job = { animation, settle };
    heightTransitions.set(element, job);
    active.add(element);
    animation.onfinish = () => {
      if (heightTransitions.get(element) !== job) return;
      heightTransitions.delete(element);
      active.delete(element);
      animation.onfinish = null;
      animation.cancel();
      finish();
    };
  }
  function toggleDisclosure(element) {
    const expanded =
      element.dataset.expanded === undefined ? !element.open : element.dataset.expanded !== 'true';
    const summary = element.querySelector(':scope > summary');
    let content = element.querySelector(':scope > .disclosure-content');
    if (!content) {
      content = document.createElement('div');
      content.className = 'disclosure-content';
      const inner = document.createElement('div');
      inner.className = 'disclosure-content-inner';
      while (summary.nextSibling) inner.append(summary.nextSibling);
      content.append(inner);
      element.append(content);
    }
    const from = element.open ? content.getBoundingClientRect().height : 0;
    const summaryFrom = summary.getBoundingClientRect().height;
    element.querySelectorAll('.is-animating').forEach((child) => stopHeightTransition(child, true));
    element.classList.remove('is-closing');
    element.open = expanded;
    const summaryTo = summary.getBoundingClientRect().height;
    element.open = true;
    const to = expanded ? content.getBoundingClientRect().height : 0;
    element.dataset.expanded = String(expanded);
    element.classList.toggle('is-closing', !expanded);
    summary.setAttribute('aria-expanded', String(expanded));
    animateHeight(summary, summaryFrom, summaryTo, () => {});
    animateHeight(content, from, to, () => {
      element.open = expanded;
      element.classList.remove('is-closing');
    });
  }

  root.addEventListener(
    'click',
    (e) => {
      const summary = e.target.closest('summary');
      if (summary && summary.parentElement.matches('.detail-disclosure, .evidence-row')) {
        e.preventDefault();
        toggleDisclosure(summary.parentElement);
        return;
      }
      const button = e.target.closest('[data-assessment-toggle]');
      if (!button) return;
      const expanded = button.getAttribute('aria-expanded') !== 'true';
      const block = button.closest('.assessment'),
        text = block.querySelector('.assessment-copy');
      const from = text.getBoundingClientRect().height;
      stopHeightTransition(text);
      block.classList.toggle('is-expanded', expanded);
      const to = text.getBoundingClientRect().height;
      block.classList.add('is-expanded');
      button.setAttribute('aria-expanded', String(expanded));
      button.querySelector('.assessment-toggle-label').textContent = expanded
        ? 'Read less'
        : 'Read more';
      animateHeight(text, from, to, () => block.classList.toggle('is-expanded', expanded));
    },
    { signal: events.signal },
  );
  return {
    cancel() {
      for (const element of [...active]) stopHeightTransition(element, true);
    },
    destroy() {
      events.abort();
      for (const element of [...active]) stopHeightTransition(element, true);
    },
  };
}
