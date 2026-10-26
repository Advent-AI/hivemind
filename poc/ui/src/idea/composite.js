import { assessmentAt, score } from '../model/thesis.js';
import { isCalendarDay } from '../model/dates.js';

function shape(value, keys, name) {
  if (
    !value ||
    typeof value !== 'object' ||
    Array.isArray(value) ||
    Object.keys(value).sort().join(',') !== [...keys].sort().join(',')
  )
    throw new TypeError(`Invalid ${name} shape`);
}

function numericScore(thesis, position) {
  const value = score(thesis, position);
  if (!['+2', '+1', '0', '−1', '−2', 'Yes', 'No'].includes(value))
    throw new TypeError('Unsupported composite input score');
  return value === 'Yes' ? 2 : value === 'No' ? -2 : Number(value.replace('−', '-'));
}

/** Apply one fixed basket to the dated assessments, preserving missing values and coverage. */
function history(drivers, dataset, asOf, weighted = false) {
  const byId = new Map(dataset.theses.map((thesis) => [thesis.id, thesis]));
  const start = dataset.days[0] || asOf;
  const dates = new Set([start, asOf]);
  for (const driver of drivers)
    for (const judgement of byId.get(driver.thesis_id).judgements)
      if (judgement.day >= start && judgement.day <= asOf) dates.add(judgement.day);
  const series = [...dates].sort().map((day) => {
    const contributions = drivers.map((driver) => {
      const thesis = byId.get(driver.thesis_id);
      const judgement = assessmentAt(thesis, day);
      const raw = judgement ? numericScore(thesis, judgement.rung) : null;
      return { ...driver, score: raw, signed: raw === null ? null : raw * driver.direction };
    });
    const active = contributions.filter((entry) => entry.signed !== null);
    const sum = active.reduce(
      (total, entry) => total + entry.signed * (weighted ? entry.weight_percent / 100 : 1),
      0,
    );
    for (const entry of contributions)
      entry.contribution =
        entry.signed === null
          ? null
          : entry.signed * (weighted ? entry.weight_percent / 100 : 1 / active.length);
    return {
      day,
      value: weighted
        ? drivers.length && active.length === drivers.length
          ? sum
          : null
        : active.length
          ? sum / active.length
          : null,
      scored: active.length,
      total: drivers.length,
      contributions,
    };
  });
  return { start, series };
}

/** Default API plan: interpret its supporting ladder end using the card's existing score scale. */
export function prepareIdeaComposite(card, dataset) {
  const plan = card.reading?.composite;
  if (!plan) return null;
  const positiveOnly = plan.version === 'idea-composite/4';
  const weighted =
    ['idea-composite/3', 'idea-composite/4'].includes(plan.version) && plan.method === 'weighted';
  const excluded = positiveOnly ? [] : plan.excluded;
  shape(
    plan,
    [
      'version',
      'method',
      'as_of',
      'drivers',
      ...(positiveOnly ? [] : ['excluded']),
      ...(plan.target ? ['target'] : []),
    ],
    'Idea composite',
  );
  if (
    (!weighted && !(plan.version === 'idea-composite/2' && plan.method === 'equal_weight')) ||
    !isCalendarDay(plan.as_of) ||
    plan.as_of !== card.idea.as_of ||
    plan.as_of !== dataset.as_of ||
    !Array.isArray(plan.drivers) ||
    !Array.isArray(excluded) ||
    (positiveOnly && (!plan.target || card.related?.length))
  )
    throw new TypeError('Invalid Idea composite');
  if (plan.target) {
    shape(plan.target, ['outcome', 'direction'], 'composite target');
    if (
      typeof plan.target.outcome !== 'string' ||
      !plan.target.outcome.trim() ||
      !['higher', 'lower', 'unclear'].includes(plan.target.direction)
    )
      throw new TypeError('Invalid composite target');
    if (plan.target.direction === 'unclear' && plan.drivers.length)
      throw new TypeError('An unclear composite cannot have scored drivers');
  }
  const selected = new Set((card.reading.chosen || []).map((entry) => entry.view_id));
  const byId = new Map(dataset.theses.map((thesis) => [thesis.id, thesis]));
  const used = new Set();
  const identify = (entry) => {
    const thesis = byId.get(entry.thesis_id);
    if (
      !thesis ||
      !selected.has(thesis.id) ||
      used.has(thesis.id) ||
      thesis.question !== entry.question
    )
      throw new TypeError('Composite entries must identify unique connected theses');
    if (typeof entry.reason !== 'string' || !entry.reason.trim())
      throw new TypeError('Composite entries require a reason');
    used.add(thesis.id);
    return thesis;
  };
  const drivers = plan.drivers.map((entry) => {
    shape(
      entry,
      [
        'thesis_id',
        'question',
        'label',
        'supporting_end',
        'reason',
        ...(weighted ? ['weight_percent', 'weight_reason'] : []),
      ],
      'Idea driver',
    );
    const thesis = identify(entry);
    if (
      !['first', 'last'].includes(entry.supporting_end) ||
      typeof entry.label !== 'string' ||
      !entry.label.trim()
    )
      throw new TypeError('An Idea driver needs a supporting end and label');
    if (
      weighted &&
      (!Number.isInteger(entry.weight_percent) ||
        entry.weight_percent < 1 ||
        entry.weight_percent > 100 ||
        typeof entry.weight_reason !== 'string' ||
        !entry.weight_reason.trim())
    )
      throw new TypeError('An Idea driver needs 1–100 impact percent and a reason');
    const first = numericScore(thesis, thesis.rungs[0].position);
    if (Math.abs(first) !== 2)
      throw new TypeError('A composite scale must have an explicit endpoint');
    const direction = Math.sign(first) * (entry.supporting_end === 'first' ? 1 : -1);
    return { ...entry, direction };
  });
  for (const entry of excluded) {
    shape(
      entry,
      ['thesis_id', 'question', 'reason', ...(weighted ? ['weight_percent'] : [])],
      'excluded Idea thesis',
    );
    identify(entry);
    if (weighted && entry.weight_percent !== 0)
      throw new TypeError('An excluded thesis must have zero impact');
  }
  if (used.size !== selected.size)
    throw new TypeError('Every connected thesis needs a composite disposition');
  if (
    weighted &&
    drivers.reduce((total, driver) => total + driver.weight_percent, 0) !==
      (drivers.length ? 100 : 0)
  )
    throw new TypeError('Idea impact weights must sum to 100');
  return { ...plan, excluded, drivers, ...history(drivers, dataset, plan.as_of, weighted) };
}

/** An explicit trial basket; directions and representative selection are never inferred here. */
export function prepareCompositeTrial(trials, card, dataset) {
  const matching = trials.filter(
    (trial) => trial.idea_text === card.idea.text && trial.as_of === card.idea.as_of,
  );
  if (!matching.length) return null;
  if (matching.length !== 1)
    throw new TypeError('A response needs exactly one matching composite trial');
  const plan = matching[0];
  shape(plan, ['version', 'idea_text', 'as_of', 'note', 'drivers'], 'composite trial');
  if (
    plan.version !== 'idea-composite/1' ||
    !isCalendarDay(plan.as_of) ||
    plan.as_of !== dataset.as_of ||
    typeof plan.note !== 'string' ||
    !Array.isArray(plan.drivers) ||
    !plan.drivers.length
  )
    throw new TypeError('Invalid composite trial');
  const selected = new Set((card.reading?.chosen || []).map((entry) => entry.view_id));
  if (plan.drivers.some((driver) => !selected.has(driver.thesis_id))) return null;
  const used = new Set();
  const byId = new Map(dataset.theses.map((thesis) => [thesis.id, thesis]));
  const drivers = plan.drivers.map((driver) => {
    shape(driver, ['thesis_id', 'question', 'label', 'direction', 'reason'], 'composite driver');
    const thesis = byId.get(driver.thesis_id);
    if (
      !thesis ||
      thesis.question !== driver.question ||
      !selected.has(thesis.id) ||
      used.has(thesis.id)
    )
      throw new TypeError('A composite driver must identify one unique connected thesis');
    if (
      ![1, -1].includes(driver.direction) ||
      ![driver.label, driver.reason].every((text) => typeof text === 'string' && text.trim())
    )
      throw new TypeError('A composite driver needs an explicit direction and explanation');
    used.add(thesis.id);
    return { ...driver };
  });
  return {
    ...plan,
    drivers,
    ...history(drivers, dataset, plan.as_of),
    excluded: [...selected].filter((id) => !used.has(id)),
  };
}

export function compositeAt(trial, day) {
  return (
    trial.series.findLast((point) => point.day <= day) || {
      day,
      value: null,
      scored: 0,
      total: trial.drivers.length,
      contributions: [],
    }
  );
}

/** Rank display copies by impact, retaining incoming order for ties or unweighted entries. */
export function byImpactWeight(entries, weightOf = (entry) => entry.weight_percent) {
  return [...entries].sort((a, b) => (weightOf(b) ?? 0) - (weightOf(a) ?? 0));
}

export function confidenceFromScore(value) {
  if (value === null) return null;
  if (!Number.isFinite(value) || value < -2 || value > 2)
    throw new TypeError('Confidence requires a score from −2 to +2');
  return 50 + 25 * value;
}

export function confidenceHistory(composite) {
  return composite.series.map((point) => ({
    day: point.day,
    value: confidenceFromScore(point.value),
  }));
}

export function formatConfidence(value, decimals = 0) {
  return value === null ? '—' : `${value.toFixed(decimals)}%`;
}
