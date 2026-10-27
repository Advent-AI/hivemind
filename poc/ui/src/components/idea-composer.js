/** Keep the Idea draft anchored to the canvas while its entry control opens and folds. */
export function createIdeaComposer({ root, form, input, launcher }) {
  const events = new AbortController();
  const entry = form.parentElement;

  function setOpen(open) {
    form.hidden = !open;
    launcher.hidden = open;
    launcher.setAttribute('aria-expanded', String(open));
    root.dataset.composer = open ? 'open' : 'collapsed';
  }
  function open() {
    setOpen(true);
    input.focus();
  }
  function close() {
    setOpen(false);
  }

  launcher.addEventListener('click', open, { signal: events.signal });
  document.addEventListener(
    'pointerdown',
    (event) => {
      if (!root.hidden && !form.hidden && !entry.contains(event.target)) close();
    },
    { signal: events.signal },
  );
  form.addEventListener(
    'keydown',
    (event) => {
      if (event.key !== 'Escape') return;
      event.preventDefault();
      close();
      launcher.focus();
    },
    { signal: events.signal },
  );

  return { open, close, destroy: () => events.abort() };
}
