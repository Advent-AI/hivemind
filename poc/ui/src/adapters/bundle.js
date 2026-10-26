import { ContractError, parseDataset } from '../model/contract.js';

// The canonical English ledger values (D163) and the legacy spellings of earlier ledgers and exports.
const KINDS = {
  asset: 'Company thesis',
  'Company view': 'Company thesis',
  'Company thesis': 'Company thesis',
  对象观点: 'Company thesis',
  theme: 'Theme thesis',
  'Theme view': 'Theme thesis',
  'Theme thesis': 'Theme thesis',
  主题观点: 'Theme thesis',
};
const TIERS = {
  fact: 'Fact',
  Fact: 'Fact',
  发生的事: 'Fact',
  party_statement: 'Party statement',
  'Party statement': 'Party statement',
  当事人说的: 'Party statement',
  third_party_view: 'Third-party view',
  'Third-party view': 'Third-party view',
  第三方看法: 'Third-party view',
  rumour: 'Rumour',
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
// A rung's representative amount: its numeric bounds when the ledger carries them (every English-library rung does),
// else the magnitudes written in its condition (legacy ledgers; condition_zh is the untranslated text).
function representative(rung) {
  const lo = typeof rung.lo === 'number' ? rung.lo : null;
  const hi = typeof rung.hi === 'number' ? rung.hi : null;
  if (lo !== null || hi !== null)
    return lo !== null && hi !== null ? (lo + hi) / 2 : lo !== null ? lo : hi;
  const values = magnitude(rung.condition_zh || rung.condition);
  return values.length ? values.reduce((sum, n) => sum + n, 0) / values.length : NaN;
}
function legacyScores(view) {
  if (view.rungs.every((r) => r.score)) return view.rungs.map((r) => r.score);
  if (view.rungs.length === 2) return ['Yes', 'No'];
  if (KINDS[view.kind] === 'Theme thesis') {
    const first = representative(view.rungs[0]);
    const last = representative(view.rungs.at(-1));
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
      year: v.year ?? null,
      identity: v.identity ?? null,
      successions: v.successions ?? [],
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
        ...(typeof r.lo === 'number' ? { lo: r.lo } : {}),
        ...(typeof r.hi === 'number' ? { hi: r.hi } : {}),
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
        original_date: e.original_day || '',
        event_time: e.event_time || '',
        day: e.day,
        arrival_day: dated(e.arrival_day, e.linked_seq, `${path}/evidence/${i}/arrival_day`),
        seq: e.seq,
        source: source(e.source, e.day),
        outlets: e.outlets,
        sources: (e.sources || []).map((s) => ({
          input_id: s.input_id,
          day: s.day,
          arrival_day: s.arrival_day,
          source: source(s.source, s.day),
        })),
        replaced_by: e.replaced_by ? { ...e.replaced_by, day: e.replaced_by.day ?? null } : null,
        replaces: e.replaces,
      })),
      dependencies: v.dependencies.map((d, i) => ({
        depends_on: d.depends_on,
        direction: d.direction,
        wait_year: d.wait_year,
        wait_chain_view_id: d.wait_chain_view_id ?? null,
        resolutions: d.resolutions ?? [],
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
    schema_version: 'thesis-ui/2',
    coverage: input.coverage || 'selection',
    groups: input.groups ?? [],
    as_of: options.asOf || input.as_of || input.idea?.as_of || input.days.at(-1),
    days: [...input.days],
    theses,
  });
}
export function fromIdeaResponse(response) {
  return fromBundles(response, { asOf: response.idea.as_of });
}
