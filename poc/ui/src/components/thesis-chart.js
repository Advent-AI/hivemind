import { calendarX, dayDiff, addDays, fmtDay, isCalendarDay } from '../model/dates.js';
import {
  laneOf,
  stateText,
  judgementsUpTo,
  lastOf,
  dayRounds,
  changePoints,
  historyIndexAt,
} from '../model/thesis.js';
import { axisScore } from './primitives.js';

export const CH = { W: 406, left: 34, right: 18, top: 24, laneH: 22, barH: 52, plotGap: 36 };
export const chartStateY = (v, rung) =>
  CH.top + ((laneOf(v, rung) + 0.5) * CH.laneH * 5) / v.rungs.length;
function stepPath(points, y) {
  return points
    .map((p, k) => {
      if (!k) return `M${p.x},${y(p.rung)}`;
      const q = points[k - 1];
      if (p.rung === q.rung) return `L${p.x},${y(p.rung)}`;
      const s = Math.min(10, Math.max(2, p.x - q.x));
      return `L${p.x - s},${y(q.rung)} C${p.x - s / 2},${y(q.rung)} ${p.x - s / 2},${y(p.rung)} ${p.x},${y(p.rung)}`;
    })
    .join(' ');
}
function axisLabels(start, x, end) {
  if (start === end) return [{ day: start, text: fmtDay(start), anchor: 'middle', x: x(start) }];
  const placed = [
    { day: start, text: fmtDay(start), anchor: 'start', x: x(start) },
    { day: end, text: fmtDay(end), anchor: 'end', x: x(end) },
  ];
  const gap = 60;
  const candidates = [];
  const step = dayDiff(start, end) <= 45 ? 7 : 1;
  for (let d = addDays(start, step); d < end; d = addDays(d, step)) {
    if (step === 7 || d.endsWith('-01')) candidates.push(d);
  }
  for (const day of candidates)
    if (placed.every((p) => Math.abs(p.x - x(day)) >= gap))
      placed.push({ day, text: fmtDay(day), anchor: 'middle', x: x(day) });
  return placed.sort((a, b) => a.x - b.x);
}
export function ladderChart(
  v,
  { width = CH.W, start, end, day, scope = 'canvas', interactive = false },
) {
  const { left, right, top, laneH, barH, plotGap } = CH;
  const W = Number(width);
  if (!Number.isFinite(W) || W <= left + right)
    throw new TypeError('Chart width must be a finite number wider than its margins');
  if (![start, end, day].every(isCalendarDay) || start > end || day > end)
    throw new TypeError('Chart dates must form a valid loaded range');
  const stateBottom = top + laneH * 5,
    volumeTop = stateBottom + plotGap,
    baseY = volumeTop + barH,
    H = baseY + 24;
  const x = (date) => calendarX(date, start, end, left, W - right);
  const y = (r) => chartStateY(v, r);
  const all = v.judgements,
    ev = v.evidence,
    rounds = dayRounds(all);
  const atStart = judgementsUpTo(v, day);
  const cur = atStart.length ? lastOf(atStart).rung : null;
  const id = `clip-${scope}-${v.id}`.replace(/[^A-Za-z0-9_.:-]/g, '_');
  let s = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}"><defs><clipPath id="${id}"><rect class="js-clip" x="0" y="0" width="${day >= end ? W : x(day)}" height="${H}"/></clipPath></defs>`;
  s += `<text class="plot-title" x="${left - 31}" y="${top - 12}">AI score</text>`;
  s += `<rect class="volume-bg" x="${left}" y="${volumeTop}" width="${W - left - right}" height="${barH}" rx="3"/>`;
  for (const l of axisLabels(start, x, end))
    s += `${l.day === end && !interactive ? '' : `<line class="timeline-grid" x1="${l.x}" x2="${l.x}" y1="${top}" y2="${baseY}"/>`}<line class="ax-tick" x1="${l.x}" x2="${l.x}" y1="${baseY}" y2="${baseY + 4}"/><text class="timeline-date" x="${l.x}" y="${baseY + 20}" text-anchor="${l.anchor}">${l.text}</text>`;
  v.rungs.forEach((r, i) => {
    const p = i + 1;
    s += `<line class="lane ${p === cur ? 'lane--cur' : ''}" x1="${left}" x2="${W - right}" y1="${y(p)}" y2="${y(p)}"/>${axisScore(v, p, left - 18, y(p), cur)}`;
  });
  const byDay = {};
  for (const e of ev)
    if (e.arrival_day >= start && e.arrival_day <= end) (byDay[e.arrival_day] ||= []).push(e);
  const peak = Math.max(1, ...Object.values(byDay).map((a) => a.length));
  const unit = 10 ** Math.floor(Math.log10(peak)),
    scaleMax = Math.ceil(peak / unit) * unit;
  s += `<text class="plot-title" x="${left - 31}" y="${volumeTop - 12}">Evidence / day</text><text class="volume-scale" x="${left - 31}" y="${volumeTop + 4}" text-anchor="start">${scaleMax}</text><text class="volume-scale" x="${left - 31}" y="${baseY + 3}" text-anchor="start">0</text><line class="ax-tick" x1="${left}" x2="${W - right}" y1="${baseY}" y2="${baseY}"/>`;
  s += `<g clip-path="url(#${id})">`;
  const points = rounds
    .filter((r) => r.j.day >= start)
    .map((r) => ({ x: x(r.j.day), rung: r.j.rung }));
  const before = rounds.filter((r) => r.j.day < start);
  if (before.length) points.unshift({ x: x(start), rung: lastOf(before).j.rung });
  if (points.length) {
    points.push({ x: x(end), rung: lastOf(points).rung });
    s += `<path class="ribbon" d="${stepPath(points, y)}"/>`;
  }
  const bw = Math.max(1, Math.min(10, ((W - left - right) / (dayDiff(start, end) + 1)) * 0.72));
  for (const [day, evs] of Object.entries(byDay)) {
    const h = (evs.length / scaleMax) * barH,
      bx = Math.max(left, Math.min(W - right - bw, x(day) - bw / 2));
    s += `<rect class="evidence-bar" data-day="${day}" data-count="${evs.length}" x="${bx}" y="${baseY - h}" width="${bw}" height="${h}" rx="0.8"/>`;
  }
  const cpi = new Set(changePoints(all).map((c) => c.i));
  rounds.forEach(({ i, j }, k) => {
    if ((cpi.has(i) || k === 0) && j.day >= start)
      s += `<circle class="node" data-i="${i}" cx="${x(j.day)}" cy="${y(j.rung)}" r="3.5"/>`;
  });
  s += '</g>';
  if (!interactive)
    s += `<circle class="now-dot js-now" cx="${x(day)}" cy="${cur ? y(cur) : top}" r="3.5" style="display:${cur ? '' : 'none'}"/>`;
  if (interactive)
    s += `<g class="history-crosshair" visibility="hidden"><line class="history-guide-x" y1="${top}" y2="${baseY}"/><line class="history-guide-y" x1="${left}" x2="${W - right}"/><circle r="4.5"/></g><rect class="history-hitbox" x="${left - 6}" y="${top}" width="${W - left - right + 12}" height="${baseY - top}" tabindex="0" role="slider" aria-label="History date. Arrow keys to preview, Enter to select" aria-valuemin="0" aria-valuemax="${dayDiff(start, end)}" aria-valuenow="${dayDiff(start, day)}"/>`;
  return s + '</svg>';
}

/** Own one chart's pointer/keyboard state. Selection is reported, never written into the thesis. */
export function bindHistoryChart(host, { thesis, start, end, onSelect }) {
  const svg = host.querySelector('svg');
  const hitbox = svg.querySelector('.history-hitbox');
  const guide = svg.querySelector('.history-crosshair');
  const events = new AbortController();
  let pinned = null;
  let preview = null;

  function draw(day, index) {
    guide.setAttribute('visibility', day ? 'visible' : 'hidden');
    preview = day;
    if (!day) return;
    const judgement = thesis.judgements[index ?? historyIndexAt(thesis, day)];
    const resolved = judgement?.day || day;
    const x = calendarX(
      resolved,
      start,
      end,
      CH.left,
      Number(svg.getAttribute('width')) - CH.right,
    );
    const vertical = guide.querySelector('.history-guide-x');
    vertical.setAttribute('x1', x);
    vertical.setAttribute('x2', x);
    guide.setAttribute('data-pinned', String(Boolean(pinned && index !== undefined)));
    const horizontal = guide.querySelector('.history-guide-y'),
      dot = guide.querySelector('circle');
    horizontal.setAttribute('visibility', judgement ? 'visible' : 'hidden');
    dot.setAttribute('visibility', judgement ? 'visible' : 'hidden');
    if (judgement) {
      const y = chartStateY(thesis, judgement.rung);
      horizontal.setAttribute('y1', y);
      horizontal.setAttribute('y2', y);
      dot.setAttribute('cx', x);
      dot.setAttribute('cy', y);
    }
    const count = thesis.evidence.filter((e) => e.arrival_day === resolved).length;
    hitbox.setAttribute('aria-valuenow', String(dayDiff(start, resolved)));
    hitbox.setAttribute(
      'aria-valuetext',
      `${resolved} | ${judgement ? stateText(thesis, judgement.rung) : 'No assessment'} | ${count} evidence items`,
    );
  }
  function select(index, requestedDay) {
    pinned = { index, day: thesis.judgements[index]?.day || requestedDay };
    draw(pinned.day, index);
    onSelect(index, pinned.day);
  }
  function dateAt(event) {
    const rect = svg.getBoundingClientRect(),
      width = Number(svg.getAttribute('width'));
    const x = ((event.clientX - rect.left) * width) / rect.width;
    const fraction = Math.max(0, Math.min(1, (x - CH.left) / (width - CH.left - CH.right)));
    return addDays(start, Math.round(fraction * dayDiff(start, end)));
  }
  hitbox.addEventListener(
    'pointermove',
    (event) => {
      if (!pinned) draw(dateAt(event));
    },
    { signal: events.signal },
  );
  hitbox.addEventListener('pointerleave', () => draw(pinned?.day, pinned?.index), {
    signal: events.signal,
  });
  hitbox.addEventListener(
    'click',
    (event) => {
      const day = dateAt(event);
      hitbox.focus();
      select(historyIndexAt(thesis, day), day);
    },
    { signal: events.signal },
  );
  hitbox.addEventListener(
    'keydown',
    (event) => {
      if (['Enter', ' '].includes(event.key)) {
        event.preventDefault();
        const day = preview || pinned?.day || end;
        select(historyIndexAt(thesis, day), day);
        return;
      }
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      const offset = dayDiff(start, preview || pinned?.day || end);
      const next =
        event.key === 'Home'
          ? 0
          : event.key === 'End'
            ? dayDiff(start, end)
            : Math.max(
                0,
                Math.min(dayDiff(start, end), offset + (event.key === 'ArrowRight' ? 1 : -1)),
              );
      draw(addDays(start, next));
    },
    { signal: events.signal },
  );
  return {
    select,
    destroy() {
      events.abort();
      guide.setAttribute('visibility', 'hidden');
    },
  };
}
