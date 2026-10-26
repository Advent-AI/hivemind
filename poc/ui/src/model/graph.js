import { fanOutGap } from '../components/connectors.js';

export const CARD_WIDTH = 440;
const CARD = { width: CARD_WIDTH, height: 380, gap: 24, top: 40 };

/** Normalize legacy single-root callers and explicit Idea graphs before rendering. */
export function resolveGraph(spec, dataset) {
  const known = new Map(dataset.theses.map((thesis) => [thesis.id, thesis]));
  let rootIds, branches;
  if (spec.rootIds !== undefined) {
    if (spec.primaryId !== undefined || spec.supportingIds !== undefined)
      throw new TypeError('Use rootIds/branches or primaryId/supportingIds, not both');
    rootIds = spec.rootIds;
    branches = spec.branches ?? [];
  } else {
    rootIds = spec.primaryId ? [spec.primaryId] : [];
    const supporting =
      spec.supportingIds ??
      known
        .get(spec.primaryId)
        ?.dependencies.filter((edge) => edge.day <= dataset.as_of && known.has(edge.depends_on))
        .map((edge) => edge.depends_on)
        .slice(0, 4) ??
      [];
    branches = [...new Set(supporting)]
      .filter((id) => id !== spec.primaryId)
      .map((id) => ({ sourceId: spec.primaryId, targetId: id }));
  }
  if (!Array.isArray(rootIds) || !Array.isArray(branches))
    throw new TypeError('Graph rootIds and branches must be arrays');
  const roots = new Set();
  for (const id of rootIds) {
    if (typeof id !== 'string' || !known.has(id))
      throw new Error(`Load thesis ${id} before rendering it`);
    if (roots.has(id)) throw new Error(`Duplicate graph root: ${id}`);
    roots.add(id);
  }
  const targets = new Set();
  for (const edge of branches) {
    if (!edge || Object.keys(edge).sort().join(',') !== 'sourceId,targetId')
      throw new TypeError('A graph branch needs only sourceId and targetId');
    if (!roots.has(edge.sourceId))
      throw new Error(`Graph branch source is not a root: ${edge.sourceId}`);
    if (!known.has(edge.targetId))
      throw new Error(`Load thesis ${edge.targetId} before rendering it`);
    if (roots.has(edge.targetId) || targets.has(edge.targetId))
      throw new Error(`Graph branch target must have one parent: ${edge.targetId}`);
    targets.add(edge.targetId);
  }
  return { rootIds: [...rootIds], branches: branches.map((edge) => ({ ...edge })) };
}

/** Reserve a separate vertical block for each root and its actual related children. */
export function layoutGraph({ rootIds, branches }, hasLeading = false) {
  const children = new Map(
    rootIds.map((id) => [id, branches.filter((edge) => edge.sourceId === id)]),
  );
  const slots = rootIds.reduce((sum, id) => sum + Math.max(1, children.get(id).length), 0);
  const height = Math.max(CARD.height, slots * (CARD.height + CARD.gap) - CARD.gap);
  const rootLeft = hasLeading ? 40 + CARD.width + fanOutGap(rootIds.length) : 480;
  const childLeft =
    rootLeft +
    CARD.width +
    fanOutGap(Math.max(0, ...[...children.values()].map((list) => list.length)));
  const nodes = [];
  let top = CARD.top;
  for (const id of rootIds) {
    const related = children.get(id);
    const groupHeight = Math.max(1, related.length) * (CARD.height + CARD.gap) - CARD.gap;
    nodes.push({
      id,
      left: rootLeft,
      top: top + (groupHeight - CARD.height) / 2,
      width: CARD.width,
      height: CARD.height,
    });
    related.forEach((edge, index) =>
      nodes.push({
        id: edge.targetId,
        left: childLeft,
        top: top + index * (CARD.height + CARD.gap),
        width: CARD.width,
        height: CARD.height,
      }),
    );
    top += groupHeight + CARD.gap;
  }
  return {
    nodes,
    leading: hasLeading
      ? {
          id: 'idea',
          left: 40,
          top: CARD.top + (height - CARD.height) / 2,
          width: CARD.width,
          height: CARD.height,
        }
      : null,
    edges: [
      ...(hasLeading ? rootIds.map((targetId) => ({ sourceId: 'idea', targetId })) : []),
      ...branches.map((edge) => ({ ...edge })),
    ],
  };
}
