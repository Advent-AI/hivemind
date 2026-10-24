import { ContractError, parseDataset } from '../model/contract.js';

const KINDS = {
  'Company view': 'Company thesis',
  'Company thesis': 'Company thesis',
  对象观点: 'Company thesis',
  'Theme view': 'Theme thesis',
  'Theme thesis': 'Theme thesis',
  主题观点: 'Theme thesis',
};
const TIERS = {
  Fact: 'Fact',
  发生的事: 'Fact',
  'Party statement': 'Party statement',
  当事人说的: 'Party statement',
  'Third-party view': 'Third-party view',
  第三方看法: 'Third-party view',
  Rumour: 'Rumour',
  传闻: 'Rumour',
};
const ORDINAL = ['+2', '+1', '0', '−1', '−2'];
function magnitude(condition) {
  return [...condition.matchAll(/(\d[\d,.]*)\s*(万亿|千亿|亿)/g)].map(
    (m) =>
      Number(m[1].replaceAll(',', '')) * (m[2] === '万亿' ? 10000 : m[2] === '千亿' ? 1000 : 1),
  );
}
function legacyScores(view) {
  if (view.rungs.every((r) => r.score)) return view.rungs.map((r) => r.score);
  if (view.rungs.length === 2) return ['Yes', 'No'];
  if (KINDS[view.kind] === 'Theme thesis') {
    const mean = (values) => values.reduce((sum, n) => sum + n, 0) / values.length;
    const first = mean(magnitude(view.rungs[0].condition_zh || view.rungs[0].condition));
    const last = mean(magnitude(view.rungs.at(-1).condition_zh || view.rungs.at(-1).condition));
    if (last > first) return [...ORDINAL].reverse();
  }
  return ORDINAL;
}
function source(value = {}, day = null) {
  return {
    title: value.title || '',
    publisher: value.publisher || '',
    category: value.category || '',
    uri: value.uri || value.source_uri || null,
    publication_day: value.publication_day || day,
  };
}
function array(value, path) {
  if (!Array.isArray(value)) throw new ContractError(path, 'expected an array');
  return value;
}
/** Compatibility boundary for mock JSON and POST /ideas view_bundle records. */
export function fromBundles(input, options = {}) {
  if (!input || !Array.isArray(input.views) || !Array.isArray(input.days))
    throw new ContractError('/', 'bundle payload needs views and days arrays');
  const sequenceDays = options.sequenceDays || input.sequence_days || {};
  const dated = (day, seq, path) => {
    const result = day || sequenceDays[seq];
    if (!result)
      throw new ContractError(path, 'missing event date; supply dated bundles or sequenceDays');
    return result;
  };
  const theses = input.views.map((v, vi) => {
    const path = `/views/${vi}`;
    if (!v || typeof v !== 'object') throw new ContractError(path, 'expected a thesis bundle');
    for (const key of ['rungs', 'judgements', 'evidence', 'dependencies', 'switches'])
      array(v[key], `${path}/${key}`);
    const scores = legacyScores(v);
    return {
      id: v.view_id,
      object: v.object,
      kind: KINDS[v.kind],
      looks_at: v.looks_at,
      question: v.question,
      due_day: v.due_day,
      created_seq: v.created_seq,
      created_day: dated(v.created_day, v.created_seq, `${path}/created_day`),
      created_from: source(v.created_from),
      rungs: v.rungs.map((r, i) => ({
        position: r.position,
        score: scores[i],
        label: r.label,
        condition: r.condition,
        ...(r.condition_zh ? { condition_zh: r.condition_zh } : {}),
      })),
      judgements: v.judgements
        .map((j, i) => ({
          id: j.id || `legacy:${v.view_id}:${i}`,
          day: j.day,
          seq: j.seq,
          rung: j.rung,
          changed: j.changed,
          why_changed: j.why_changed || '',
          reasons: j.reasons || '',
          cited: [...array(j.cited, `${path}/judgements/${i}/cited`)],
        }))
        .sort((a, b) => a.day.localeCompare(b.day) || a.seq - b.seq),
      evidence: v.evidence.map((e, i) => ({
        id: e.id,
        one_line: e.one_line,
        quote: e.quote,
        tier: TIERS[e.tier],
        speaker: e.speaker || '',
        original_who: e.original_who || '',
        day: e.day,
        arrival_day: dated(e.arrival_day, e.linked_seq, `${path}/evidence/${i}/arrival_day`),
        seq: e.seq,
        source: source(e.source, e.day),
        outlets: e.outlets,
        replaced_by: e.replaced_by,
        replaces: e.replaces,
      })),
      dependencies: v.dependencies.map((d, i) => ({
        depends_on: d.depends_on,
        direction: d.direction,
        wait_year: d.wait_year,
        day: dated(d.day, d.seq, `${path}/dependencies/${i}/day`),
      })),
      switches: v.switches
        .map((s, i) => {
          if (![true, false, 0, 1].includes(s.open))
            throw new ContractError(
              `${path}/switches/${i}/open`,
              'expected a boolean or SQLite 0/1',
            );
          return {
            day: dated(s.day, s.after_seq, `${path}/switches/${i}/day`),
            seq: s.after_seq,
            open: s.open === true || s.open === 1,
            reason: s.reason,
          };
        })
        .sort((a, b) => a.day.localeCompare(b.day) || a.seq - b.seq),
    };
  });
  return parseDataset({
    schema_version: 'thesis-ui/1',
    as_of: options.asOf || input.as_of || input.idea?.as_of || input.days.at(-1),
    days: [...input.days],
    theses,
  });
}
export function fromIdeaResponse(response) {
  return fromBundles(response, { asOf: response.idea.as_of });
}
