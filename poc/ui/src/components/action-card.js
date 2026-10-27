import { element, ICON } from './dom.js';
import { cardHeaderHtml } from './primitives.js';
import { createSelect } from './select.js';
import { ACTION_SIZE, DEFAULT_ACTION_SETTINGS, readActionSettings } from '../model/market.js';
import { createPriceChart } from './price-chart.js';

/** Editable plan preview. This component displays prices and never submits an order. */
export function createActionCard({
  market = null,
  settings = DEFAULT_ACTION_SETTINGS,
  onChange = () => {},
} = {}) {
  let current = readActionSettings(settings);
  const events = new AbortController();
  const node = element(
    'section',
    'card card--action',
    `
    ${cardHeaderHtml('Action', '<span class="action__status"><span class="action__status-dot" aria-hidden="true"></span><span>Monitoring</span></span>')}
    <div class="card__body">
      <div class="action__row"><span>Buy</span><div class="action__product"></div><div class="action__order"></div><span>on</span><div class="action__venue"></div></div>
      <div class="action__row"><span>Invest</span><label class="action__allocation percentage-input"><input type="number" min="0" max="100" step="0.1" aria-label="Investment percentage" aria-description="Press Enter to save. Escape or clicking away cancels."><span>%</span></label><span>of</span><div class="action__wallet"></div></div>
      <div class="action__market"></div>
    </div>`,
  );
  node.setAttribute('aria-label', 'Action preview');
  node.style.width = `${ACTION_SIZE.width}px`;
  const single = (selector, value, label) =>
    createSelect(node.querySelector(selector), {
      options: [{ value, label: value }],
      value,
      label,
      onChange: () => {},
    });
  const selects = [
    single('.action__product', 'Spot', 'Product type'),
    single('.action__order', 'Market Order', 'Order type'),
    single('.action__venue', 'Hyperliquid', 'Venue'),
    single('.action__wallet', '0xas83....9832', 'Example wallet'),
  ];
  node.querySelector('.action__venue button').insertAdjacentHTML('afterbegin', ICON.hyperliquid);
  const allocationField = node.querySelector('.action__allocation');
  const allocation = allocationField.querySelector('input');
  const chart = createPriceChart(node.querySelector('.action__market'), {
    market,
    range: current.range,
    onRangeChange(range) {
      finishAllocation();
      notify({ ...current, range });
    },
  });
  function notify(next) {
    current = readActionSettings(next);
    onChange({ ...current });
  }
  allocation.value = current.allocation.toFixed(1);
  const changeAllocation = (value) => {
    const bounded = Math.round(Math.max(0, Math.min(100, value)) * 10) / 10;
    notify({ ...current, allocation: bounded });
  };
  function finishAllocation(commit = false) {
    if (commit && Number.isFinite(allocation.valueAsNumber))
      changeAllocation(allocation.valueAsNumber);
    allocation.value = current.allocation.toFixed(1);
    allocation.blur();
  }
  allocation.addEventListener(
    'keydown',
    (event) => {
      if (!['Enter', 'Escape'].includes(event.key)) return;
      event.preventDefault();
      event.stopPropagation();
      finishAllocation(event.key === 'Enter');
    },
    { signal: events.signal },
  );
  allocation.addEventListener(
    'blur',
    () => {
      allocation.value = current.allocation.toFixed(1);
    },
    { signal: events.signal },
  );
  document.addEventListener(
    'pointerdown',
    (event) => {
      if (document.activeElement === allocation && !allocationField.contains(event.target))
        finishAllocation();
    },
    { capture: true, signal: events.signal },
  );
  allocationField.addEventListener(
    'wheel',
    (event) => {
      event.preventDefault();
      event.stopPropagation();
      if (!event.deltaY) return;
      if (document.activeElement === allocation) {
        const draft = Number.isFinite(allocation.valueAsNumber)
          ? allocation.valueAsNumber
          : current.allocation;
        allocation.value = Math.max(
          0,
          Math.min(100, draft - Math.sign(event.deltaY) * 0.1),
        ).toFixed(1);
      } else {
        changeAllocation(current.allocation - Math.sign(event.deltaY) * 0.1);
        allocation.value = current.allocation.toFixed(1);
      }
    },
    { passive: false, signal: events.signal },
  );
  return {
    element: node,
    close() {
      finishAllocation();
      selects.forEach((select) => select.close());
      chart.clear();
    },
    destroy() {
      events.abort();
      chart.destroy();
      selects.forEach((select) => select.destroy());
      node.remove();
    },
  };
}
