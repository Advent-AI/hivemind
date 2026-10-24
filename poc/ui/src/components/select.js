/** A themed, keyboard-accessible select with instance-local state and cleanup. */
let instanceCount = 0;
export function createSelect(root, { options, value, label, onChange }) {
  const events = new AbortController();
  const menuId = `hm-select-${++instanceCount}`;
  root.classList.add('type-filter');
  root.innerHTML = `<button type="button" class="detail-select type-filter__trigger" aria-haspopup="listbox" aria-expanded="false"><span></span><svg viewBox="0 0 16 16" aria-hidden="true"><path d="m4 6 4 4 4-4"/></svg></button><div class="type-filter__menu" role="listbox" hidden></div>`;
  const trigger = root.querySelector('button'),
    menu = root.querySelector('[role="listbox"]');
  trigger.setAttribute('aria-label', label);
  trigger.setAttribute('aria-controls', menuId);
  menu.id = menuId;
  menu.setAttribute('aria-label', label);
  const buttons = options.map((option) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'type-filter__option';
    button.tabIndex = -1;
    button.setAttribute('role', 'option');
    button.setAttribute('aria-selected', String(option.value === value));
    const text = document.createElement('span');
    text.textContent = option.label;
    button.append(text);
    const check = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    check.setAttribute('viewBox', '0 0 16 16');
    check.setAttribute('aria-hidden', 'true');
    check.innerHTML = '<path d="m3 8 3 3 7-7"/>';
    button.append(check);
    button.addEventListener(
      'click',
      () => {
        value = option.value;
        sync();
        close(true);
        onChange(value);
      },
      { signal: events.signal },
    );
    menu.append(button);
    return button;
  });
  function sync() {
    trigger.querySelector('span').textContent =
      options.find((o) => o.value === value)?.label || options[0].label;
    buttons.forEach((b, i) => b.setAttribute('aria-selected', String(options[i].value === value)));
  }
  function open() {
    menu.hidden = false;
    trigger.setAttribute('aria-expanded', 'true');
  }
  function close(focus = false) {
    if (menu.hidden) return false;
    menu.hidden = true;
    trigger.setAttribute('aria-expanded', 'false');
    if (focus) trigger.focus();
    return true;
  }
  trigger.addEventListener(
    'click',
    () => {
      if (menu.hidden) open();
      else close();
    },
    { signal: events.signal },
  );
  root.addEventListener(
    'keydown',
    (event) => {
      if (event.key === 'Escape') {
        if (close(true)) {
          event.preventDefault();
          event.stopPropagation();
        }
        return;
      }
      if (event.key === 'Tab') {
        close();
        return;
      }
      if (!['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      const wasClosed = menu.hidden;
      open();
      const current = buttons.indexOf(document.activeElement),
        selected = options.findIndex((o) => o.value === value);
      const next =
        event.key === 'Home'
          ? 0
          : event.key === 'End'
            ? buttons.length - 1
            : wasClosed || current < 0
              ? selected
              : (current + (event.key === 'ArrowDown' ? 1 : -1) + buttons.length) % buttons.length;
      buttons[Math.max(0, next)].focus();
    },
    { signal: events.signal },
  );
  root.addEventListener(
    'focusout',
    (event) => {
      if (!root.contains(event.relatedTarget)) close();
    },
    { signal: events.signal },
  );
  document.addEventListener(
    'pointerdown',
    (event) => {
      if (!root.contains(event.target)) close();
    },
    { signal: events.signal },
  );
  sync();
  return {
    close,
    destroy() {
      events.abort();
      root.replaceChildren();
    },
  };
}
