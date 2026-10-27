export const ACTION_SIZE = { width: 440, height: 360 };
export const MARKET_RANGES = ['1D', '1W', '1M', '1Y'];
export const DEFAULT_ACTION_SETTINGS = { allocation: 5, range: '1Y' };
const DAY = 86400000;
const sessionDate = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York' });

export function readActionSettings(value = DEFAULT_ACTION_SETTINGS) {
  if (
    !value ||
    Object.keys(value).sort().join(',') !== 'allocation,range' ||
    !Number.isFinite(value.allocation) ||
    value.allocation < 0 ||
    value.allocation > 100 ||
    Math.abs(value.allocation * 10 - Math.round(value.allocation * 10)) > 1e-8 ||
    !MARKET_RANGES.includes(value.range)
  )
    throw new TypeError('Action settings need a 0–100 percentage in tenths and a chart range');
  return { ...value };
}

/** Read completed USD stock-price observations, with their actual source and cutoff. */
export function readMarketSnapshot(value) {
  if (
    !value ||
    Object.keys(value).sort().join(',') !==
      'asOf,assetClass,currency,daily,hourly,name,source,symbol' ||
    !/^[A-Z][A-Z0-9.-]{0,14}$/.test(value.symbol) ||
    typeof value.name !== 'string' ||
    !value.name.trim() ||
    value.currency !== 'USD' ||
    value.assetClass !== 'stock' ||
    value.source !== 'TrueNorth' ||
    typeof value.asOf !== 'string' ||
    !/^\d{4}-\d{2}-\d{2}T[\d:.]+Z$/.test(value.asOf) ||
    !Number.isFinite(Date.parse(value.asOf))
  )
    throw new TypeError('Invalid stock-price snapshot');
  const cutoff = Date.parse(value.asOf);
  const readPoints = (points) => {
    if (!Array.isArray(points)) throw new TypeError('Price history must be an array');
    return points.map((point, index) => {
      if (
        !Array.isArray(point) ||
        point.length !== 2 ||
        !Number.isSafeInteger(point[0]) ||
        point[0] <= 0 ||
        point[0] > cutoff ||
        !Number.isFinite(point[1]) ||
        point[1] <= 0 ||
        (index > 0 && point[0] <= points[index - 1][0])
      )
        throw new TypeError('Prices need increasing completed timestamps and positive values');
      return [...point];
    });
  };
  const hourly = readPoints(value.hourly),
    daily = readPoints(value.daily);
  if (hourly.length < 2 || daily.length < 2)
    throw new TypeError('Price history needs at least two hourly and daily observations');
  return { ...value, hourly, daily };
}

/** Anchor ranges to the newest observation, independently of the thesis replay date. */
export function marketWindow(snapshot, range) {
  if (!MARKET_RANGES.includes(range)) throw new TypeError('Unknown chart range');
  const latest = [snapshot.hourly.at(-1), snapshot.daily.at(-1)].sort((a, b) => a[0] - b[0]).at(-1);
  const history = range === '1Y' ? [...snapshot.daily] : snapshot.hourly;
  if (range === '1Y' && latest[0] > history.at(-1)[0]) history.push(latest);
  if (range === '1D') {
    const date = sessionDate.format(latest[0]);
    return history.filter(([time]) => sessionDate.format(time) === date);
  }
  const days = { '1W': 7, '1M': 30, '1Y': 365 }[range];
  return history.filter(([time]) => time >= latest[0] - days * DAY);
}

/** Map time and price to a bounded plot; preserve time gaps between sessions. */
export function priceGeometry(points, width = 390, height = 142) {
  if (!points.length) return null;
  const left = 2,
    right = width - 47,
    top = 12,
    bottom = height - 23;
  const values = points.map((point) => point[1]);
  const low = Math.min(...values),
    high = Math.max(...values);
  const padding = Math.max((high - low) * 0.12, high * 0.001);
  const min = low - padding,
    max = high + padding;
  const first = points[0][0],
    last = points.at(-1)[0];
  const mapped = points.map(([time, price]) => ({
    time,
    price,
    x: left + ((time - first) / (last - first || 1)) * (right - left),
    y: bottom - ((price - min) / (max - min)) * (bottom - top),
  }));
  return { mapped, left, right, top, bottom, min, max, width, height };
}
