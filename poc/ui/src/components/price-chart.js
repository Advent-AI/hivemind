import { esc } from './dom.js';
import { MARKET_RANGES, readMarketSnapshot, marketWindow, priceGeometry } from '../model/market.js';

const priceFormat = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});
const timestampFormat = new Intl.DateTimeFormat('en-US', {
  timeZone: 'America/New_York',
  year: 'numeric',
  month: 'short',
  day: 'numeric',
  hour: 'numeric',
  minute: '2-digit',
  timeZoneName: 'short',
});
const dateFormat = new Intl.DateTimeFormat('en-US', {
  timeZone: 'America/New_York',
  month: 'short',
  day: 'numeric',
});
const timeFormat = new Intl.DateTimeFormat('en-US', {
  timeZone: 'America/New_York',
  hour: 'numeric',
  minute: '2-digit',
});

/** Own the captured-price display and inspection; the host retains the selected range. */
export function createPriceChart(root, { market, range, onRangeChange }) {
  let snapshot = null,
    geometry = null,
    selected = null,
    svg = null,
    crosshair = null,
    cursorDot = null;
  try {
    snapshot = readMarketSnapshot(market);
  } catch {
    // Missing prices leave the surrounding Action editable.
  }
  const events = new AbortController();
  root.innerHTML = `
    <div class="action__instrument"></div>
    <div class="action__quote-row"><div><strong class="action__price"></strong><span class="action__change"></span></div><div class="action__ranges" aria-label="Price chart range">${MARKET_RANGES.map((value) => `<button type="button" data-market-range="${value}" aria-pressed="false">${value}</button>`).join('')}</div></div>
    <div class="action__plot"></div>`;
  const plot = root.querySelector('.action__plot');
  const quote = root.querySelector('.action__price');
  const change = root.querySelector('.action__change');
  const buttons = [...root.querySelectorAll('[data-market-range]')];
  root.querySelector('.action__instrument').textContent =
    `${snapshot?.symbol ?? 'NVDA'}-USDC | Hyperliquid-Spot`;

  function showPoint(point = geometry?.mapped.at(-1)) {
    if (!point || !geometry) return;
    quote.textContent = priceFormat.format(point.price);
    const percent = (point.price / geometry.mapped[0].price - 1) * 100;
    change.textContent = `${percent >= 0 ? '+' : '−'}${Math.abs(percent).toFixed(2)}%`;
    crosshair.toggleAttribute('hidden', selected === null);
    crosshair.setAttribute('transform', `translate(${point.x} 0)`);
    cursorDot.setAttribute('cy', point.y);
  }
  function clear() {
    selected = null;
    showPoint();
  }
  function draw() {
    selected = null;
    buttons.forEach((button) =>
      button.setAttribute('aria-pressed', String(button.dataset.marketRange === range)),
    );
    geometry = snapshot ? priceGeometry(marketWindow(snapshot, range)) : null;
    if (!geometry) {
      quote.textContent = '—';
      change.textContent = '';
      plot.innerHTML = '<p class="action__empty">Price data unavailable</p>';
      return;
    }
    const { mapped, left, right, top, bottom, min, max, width, height } = geometry;
    const path = mapped
      .map((point, index) => `${index ? 'L' : 'M'}${point.x.toFixed(2)},${point.y.toFixed(2)}`)
      .join(' ');
    const ticks = [0, 0.5, 1]
      .map((fraction) => {
        const y = top + fraction * (bottom - top);
        return `<line class="action__grid" x1="${left}" x2="${right}" y1="${y}" y2="${y}"/><text x="${width - 1}" y="${y + 3}" text-anchor="end">${(max - fraction * (max - min)).toFixed(2)}</text>`;
      })
      .join('');
    const tickFormat = range === '1D' ? timeFormat : dateFormat;
    const dates = [0, Math.floor((mapped.length - 1) / 2), mapped.length - 1]
      .map(
        (index, order) =>
          `<text x="${mapped[index].x}" y="${height - 3}" text-anchor="${['start', 'middle', 'end'][order]}">${esc(tickFormat.format(mapped[index].time))}</text>`,
      )
      .join('');
    plot.innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img" tabindex="0" aria-label="${esc(snapshot.symbol)} ${range} stock-price reference in USD. ${esc(snapshot.source)}, as of ${esc(timestampFormat.format(mapped.at(-1).time))}. Use arrow keys to inspect prices.">
      ${ticks}<path class="action__area" d="${path} L${right},${bottom} L${left},${bottom} Z"/>
      <path class="action__line" d="${path}"/><circle class="action__last" cx="${mapped.at(-1).x}" cy="${mapped.at(-1).y}" r="2.5"/>
      <g class="action__crosshair" hidden><line y1="${top}" y2="${bottom}"/><circle r="3"/></g>${dates}</svg>`;
    svg = plot.querySelector('svg');
    crosshair = svg.querySelector('.action__crosshair');
    cursorDot = crosshair.querySelector('circle');
    showPoint();
  }
  buttons.forEach((button) =>
    button.addEventListener(
      'click',
      () => {
        const next = button.dataset.marketRange;
        onRangeChange(next);
        range = next;
        draw();
      },
      { signal: events.signal },
    ),
  );
  plot.addEventListener('pointerdown', (event) => event.stopPropagation(), {
    signal: events.signal,
  });
  plot.addEventListener(
    'pointermove',
    (event) => {
      if (!geometry) return;
      const transform = svg.getScreenCTM();
      const x = (event.clientX - transform.e) / transform.a;
      selected = geometry.mapped.reduce(
        (best, point, i) =>
          Math.abs(point.x - x) < Math.abs(geometry.mapped[best].x - x) ? i : best,
        0,
      );
      showPoint(geometry.mapped[selected]);
    },
    { signal: events.signal },
  );
  plot.addEventListener('pointerleave', clear, { signal: events.signal });
  plot.addEventListener('focusout', clear, { signal: events.signal });
  plot.addEventListener(
    'keydown',
    (event) => {
      if (!geometry || !['ArrowLeft', 'ArrowRight', 'Home', 'End', 'Escape'].includes(event.key))
        return;
      event.preventDefault();
      event.stopPropagation();
      if (event.key === 'Escape') {
        clear();
        return;
      }
      selected =
        event.key === 'Home'
          ? 0
          : event.key === 'End'
            ? geometry.mapped.length - 1
            : Math.max(
                0,
                Math.min(
                  geometry.mapped.length - 1,
                  (selected ?? geometry.mapped.length - 1) + (event.key === 'ArrowLeft' ? -1 : 1),
                ),
              );
      showPoint(geometry.mapped[selected]);
    },
    { signal: events.signal },
  );
  draw();
  return { clear, destroy: () => events.abort() };
}
