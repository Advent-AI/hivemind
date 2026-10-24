const PORT_INSET = 24;
const PORT_SPACING = 24;
const LANE_SPACING = 12;
const LEAD = 24;

/** Leave room for distinct bends, with a straight lead at both card edges. */
export function fanOutGap(count) {
  return Math.max(120, LEAD * 2 + Math.max(0, count - 1) * LANE_SPACING);
}

/** Round a horizontal–vertical–horizontal route without moving its endpoints. */
export function connectorPath(points) {
  const [start, bend, , end] = points;
  if (start.y === end.y) return `M${start.x},${start.y} H${end.x}`;
  const direction = Math.sign(end.y - start.y);
  const radius = Math.min(
    10,
    (bend.x - start.x) / 2,
    (end.x - bend.x) / 2,
    Math.abs(end.y - start.y) / 2,
  );
  return `M${start.x},${start.y} H${bend.x - radius} Q${bend.x},${start.y} ${bend.x},${start.y + direction * radius} V${end.y - direction * radius} Q${bend.x},${end.y} ${bend.x + radius},${end.y} H${end.x}`;
}

/** Route a fan-out between two card columns; preserve target identity. */
export function routeFanOut(source, targets) {
  const ordered = targets
    .map((target, index) => ({ target, index }))
    .sort((a, b) => a.target.top + a.target.height / 2 - b.target.top - b.target.height / 2);
  const center = source.top + source.height / 2;
  const spacing = Math.min(
    PORT_SPACING,
    Math.max(0, source.height - PORT_INSET * 2) / Math.max(1, targets.length - 1),
  );
  const routes = ordered.map(({ target, index }, rank) => {
    const start = {
      x: source.left + source.width,
      y: center + (rank - (targets.length - 1) / 2) * spacing,
    };
    const end = { x: target.left, y: target.top + target.height / 2 };
    return { start, end, index };
  });
  let upwardLane = 0;
  let downwardLane = routes.filter(({ start, end }) => end.y > start.y).length - 1;
  return routes.map(({ start, end, index }) => {
    const lane = end.y < start.y ? upwardLane++ : end.y > start.y ? downwardLane-- : 0;
    const bendX = start.x + LEAD + lane * LANE_SPACING;
    const points = [start, { x: bendX, y: start.y }, { x: bendX, y: end.y }, end];
    return { index, points, path: connectorPath(points) };
  });
}
