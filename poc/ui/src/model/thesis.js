export const SCORES = ['+2', '+1', '0', '−1', '−2'];
export const score = (thesis, position) =>
  thesis.rungs.find((r) => r.position === position)?.score ?? '—';
export const rungLabel = (thesis, position) => {
  const state = thesis.rungs.find((r) => r.position === position);
  return state && state.label !== state.score ? state.label : '';
};
export const stateText = (thesis, position) =>
  `${score(thesis, position)} ${rungLabel(thesis, position)}`.trim();
export const stateTone = (value) =>
  ['+2', '+1', 'Yes'].includes(value)
    ? 'state--positive'
    : ['−1', '−2', 'No'].includes(value)
      ? 'state--negative'
      : 'state--neutral';
export const laneOf = (thesis, position) =>
  (thesis.rungs.length === 2 ? ['Yes', 'No'] : SCORES).indexOf(score(thesis, position));
export const lastOf = (array) => array.at(-1);
export const judgementsUpTo = (thesis, day) => thesis.judgements.filter((j) => j.day <= day);
export function assessmentAt(thesis, day) {
  return lastOf(judgementsUpTo(thesis, day)) ?? null;
}
export function historyIndexAt(thesis, day) {
  return thesis.judgements.findLastIndex((j) => j.day <= day);
}
export function statusAt(thesis, day) {
  if (day < thesis.created_day) return 'Not open yet';
  const last = lastOf(thesis.switches.filter((s) => s.day <= day));
  return last && !last.open ? 'Closed' : 'Open';
}
export function snapshotThesis(thesis, day) {
  return {
    ...thesis,
    judgements: judgementsUpTo(thesis, day),
    evidence: thesis.evidence
      .filter((e) => e.arrival_day <= day)
      .map((e) => ({
        ...e,
        sources: e.sources.filter((s) => s.arrival_day <= day),
        replaced_by: e.replaced_by?.day && e.replaced_by.day > day ? null : e.replaced_by,
      })),
    dependencies: dependenciesAt(thesis, day),
    successions: thesis.successions.filter((s) => s.day <= day),
    switches: thesis.switches.filter((s) => s.day <= day),
  };
}
export function dependenciesAt(thesis, day) {
  return thesis.dependencies
    .filter((d) => d.day <= day)
    .map((d) => ({
      ...d,
      depends_on: d.resolutions.filter((r) => r.day <= day).at(-1)?.target ?? d.depends_on,
      resolutions: d.resolutions.filter((r) => r.day <= day),
    }));
}
export const isSuperseded = (evidence, day) =>
  Boolean(evidence.replaced_by?.day && evidence.replaced_by.day <= day);
export const groupsFor = (dataset, thesisId, day) =>
  dataset.groups.filter(
    (g) => g.created_day <= day && g.members.some((m) => m.thesis_id === thesisId && m.day <= day),
  );
export function relatedTheses(thesis, dataset, day) {
  const ids = new Set(dependenciesAt(thesis, day).map((d) => d.depends_on));
  for (const other of dataset.theses) {
    if (dependenciesAt(other, day).some((d) => d.depends_on === thesis.id)) ids.add(other.id);
  }
  return dataset.theses.filter((t) => ids.has(t.id) && t.created_day <= day);
}
export function dayRounds(judgements) {
  const rounds = [];
  for (let i = 0; i < judgements.length; i++) {
    const judgement = judgements[i];
    if (rounds.at(-1)?.j.day === judgement.day) rounds[rounds.length - 1] = { i, j: judgement };
    else rounds.push({ i, j: judgement });
  }
  return rounds;
}
export function changePoints(judgements) {
  const points = [];
  let previous = null;
  for (const { i, j } of dayRounds(judgements)) {
    if (previous !== null && j.rung !== previous) points.push({ i, from: previous, to: j.rung, j });
    previous = j.rung;
  }
  return points;
}
export function humanise(thesis, text) {
  return String(text ?? '')
    .replace(
      /\bview(s?)\b/gi,
      (word, plural) => (word[0] === 'V' ? 'Thes' : 'thes') + (plural ? 'es' : 'is'),
    )
    .replace(/\brung (\d)\b/gi, (_, n) => `state ${score(thesis, Number(n))}`)
    .replace(/\brungs\b/gi, 'states')
    .replace(/\brung\b/gi, 'state');
}
