/** Shared drawer tabs; each drawer keeps ownership of its content and lazy rendering. */
export function createDetailTabs(root, { beforeSelect = () => {}, onSelect = () => {} } = {}) {
  const events = new AbortController();
  const buttons = () => [...root.querySelectorAll('[role="tab"]')];

  function select(id) {
    beforeSelect();
    for (const button of buttons()) {
      const selected = button.dataset.tab === id;
      button.setAttribute('aria-selected', String(selected));
      button.tabIndex = selected ? 0 : -1;
      root.querySelector(`[id="${button.getAttribute('aria-controls')}"]`).hidden = !selected;
    }
    onSelect(id);
    root.querySelector('.detail-content').scrollTop = 0;
  }

  root.addEventListener(
    'click',
    (event) => {
      const button = event.target.closest('[role="tab"]');
      if (button) select(button.dataset.tab);
    },
    { signal: events.signal },
  );
  root.addEventListener(
    'keydown',
    (event) => {
      const button = event.target.closest('[role="tab"]');
      if (!button || !['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      const tabs = buttons();
      const index = tabs.indexOf(button);
      const next =
        event.key === 'Home'
          ? 0
          : event.key === 'End'
            ? tabs.length - 1
            : (index + (event.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
      select(tabs[next].dataset.tab);
      tabs[next].focus();
    },
    { signal: events.signal },
  );

  return { select, destroy: () => events.abort() };
}
