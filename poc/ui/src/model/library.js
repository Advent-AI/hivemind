import { assessmentAt, groupsFor, isSuperseded, statusAt } from './thesis.js';

/** All filtering reads the same dated library; no group, score or edge is inferred. */
export function librarySelection(
  data,
  { day = data.as_of, group = '', object = '', status = '', query = '' } = {},
) {
  const words = query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  return data.theses
    .filter((t) => {
      if (
        t.created_day > day ||
        (object && t.object !== object) ||
        (status && statusAt(t, day) !== status)
      )
        return false;
      const groups = groupsFor(data, t.id, day);
      if (group === 'ungrouped' ? groups.length : group && !groups.some((g) => g.id === group))
        return false;
      const text = [
        t.question,
        t.object,
        t.looks_at,
        t.year,
        t.identity?.scope,
        ...groups.map((g) => g.name),
      ]
        .join(' ')
        .toLocaleLowerCase();
      return words.every((word) => text.includes(word));
    })
    .sort((a, b) => {
      const ad = assessmentAt(a, day)?.day || a.created_day;
      const bd = assessmentAt(b, day)?.day || b.created_day;
      return (
        bd.localeCompare(ad) ||
        b.created_seq - a.created_seq ||
        a.id.localeCompare(b.id, 'en', { numeric: true })
      );
    });
}
export function libraryCounts(data, day = data.as_of) {
  const theses = librarySelection(data, { day });
  const evidence = new Set(
    theses.flatMap((t) =>
      t.evidence.filter((e) => e.arrival_day <= day && !isSuperseded(e, day)).map((e) => e.id),
    ),
  );
  return {
    theses: theses.length,
    groups: data.groups.filter((g) => g.created_day <= day && g.members.some((m) => m.day <= day))
      .length,
    evidence: evidence.size,
  };
}
