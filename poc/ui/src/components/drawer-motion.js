/** Slide a drawer without hiding it until its exit animation has completed. */
export function createDrawerMotion({ sheet, panel, scrim, onClosed }) {
  let targetOpen = false;
  let animations = [];
  let generation = 0;
  let destroyed = false;

  function cancel() {
    for (const animation of animations) {
      animation.onfinish = null;
      animation.cancel();
    }
    animations = [];
  }

  function setOpen(open, { immediate = false } = {}) {
    if (destroyed) return;
    if (targetOpen === open && ((!immediate && animations.length) || sheet.hidden === !open))
      return;
    const token = ++generation;
    targetOpen = open;
    if (open) sheet.hidden = false;
    const fromTransform = getComputedStyle(panel).transform;
    const fromOpacity = getComputedStyle(scrim).opacity;
    cancel();
    sheet.classList.toggle('is-open', open);
    sheet.inert = !open;

    const finish = () => {
      if (token !== generation || destroyed) return;
      cancel();
      sheet.classList.remove('is-transitioning');
      sheet.hidden = !open;
      if (!open) onClosed?.();
    };
    if (immediate || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      finish();
      return;
    }

    sheet.classList.add('is-transitioning');
    const options = {
      duration: 280,
      easing: 'cubic-bezier(0.2, 0, 0, 1)',
      fill: 'forwards',
    };
    const slide = panel.animate(
      [{ transform: fromTransform }, { transform: open ? 'translateX(0)' : 'translateX(100%)' }],
      options,
    );
    const fade = scrim.animate([{ opacity: fromOpacity }, { opacity: open ? 1 : 0 }], options);
    animations = [slide, fade];
    slide.onfinish = finish;
  }

  return {
    open() {
      setOpen(true);
    },
    close(options) {
      setOpen(false, options);
    },
    destroy() {
      destroyed = true;
      generation++;
      cancel();
      sheet.hidden = true;
      sheet.inert = true;
    },
  };
}
