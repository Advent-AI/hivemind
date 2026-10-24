import validate from './validate.generated.js';
import { isCalendarDay } from './dates.js';
import { SCORES } from './thesis.js';

export class ContractError extends Error {
  constructor(path, reason) {
    super(`${path}: ${reason}`);
    this.name = 'ContractError';
    this.path = path;
  }
}
function requireThat(condition, path, reason) {
  if (!condition) throw new ContractError(path, reason);
}
function unique(items, key, path) {
  const ids = new Set();
  items.forEach((item, index) => {
    const id = key(item);
    requireThat(!ids.has(id), `${path}/${index}`, `duplicate id ${id}`);
    ids.add(id);
  });
}
function dates(value, path = '') {
  if (Array.isArray(value)) value.forEach((child, index) => dates(child, `${path}/${index}`));
  else if (value && typeof value === 'object') {
    for (const [key, child] of Object.entries(value)) {
      if ((key === 'day' || key.endsWith('_day') || key === 'as_of') && typeof child === 'string')
        requireThat(isCalendarDay(child), `${path}/${key}`, 'invalid calendar date');
      else dates(child, `${path}/${key}`);
    }
  }
}
function freeze(value) {
  if (value && typeof value === 'object' && !Object.isFrozen(value)) {
    Object.values(value).forEach(freeze);
    Object.freeze(value);
  }
  return value;
}
/** Validate without changing the caller's data; return an owned, immutable snapshot. */
export function parseDataset(input) {
  if (!validate(input)) {
    const error = validate.errors[0];
    throw new ContractError(error.instancePath || '/', error.message);
  }
  const data = structuredClone(input);
  dates(data);
  data.days.forEach((day, i) => {
    requireThat(isCalendarDay(day), `/days/${i}`, 'invalid calendar date');
    requireThat(
      day <= data.as_of && (!i || day > data.days[i - 1]),
      `/days/${i}`,
      'days must ascend and not exceed as_of',
    );
  });
  unique(data.theses, (t) => t.id, '/theses');
  data.theses.forEach((thesis, i) => {
    const path = `/theses/${i}`;
    const scores = thesis.rungs.map((r) => r.score);
    requireThat(
      thesis.created_day <= data.as_of,
      `${path}/created_day`,
      'thesis is later than as_of',
    );
    requireThat(
      scores.length === 2
        ? scores.join('|') === 'Yes|No'
        : scores.length === 5 && SCORES.every((s) => scores.includes(s)),
      `${path}/rungs`,
      'expected Yes/No or five unique ordinal scores',
    );
    thesis.rungs.forEach((r, index) =>
      requireThat(
        r.position === index + 1,
        `${path}/rungs/${index}/position`,
        'positions must be contiguous and ordered',
      ),
    );
    unique(thesis.evidence, (e) => e.id, `${path}/evidence`);
    unique(thesis.judgements, (j) => j.id, `${path}/judgements`);
    const evidence = new Map(thesis.evidence.map((e) => [e.id, e]));
    thesis.evidence.forEach((e, index) =>
      requireThat(
        e.arrival_day <= data.as_of,
        `${path}/evidence/${index}/arrival_day`,
        'evidence is later than as_of',
      ),
    );
    thesis.judgements.forEach((j, index) => {
      requireThat(
        j.day <= data.as_of && j.day >= thesis.created_day,
        `${path}/judgements/${index}/day`,
        'judgement is outside the thesis snapshot',
      );
      requireThat(
        j.rung <= thesis.rungs.length,
        `${path}/judgements/${index}/rung`,
        'unknown state',
      );
      const previous = thesis.judgements[index - 1];
      requireThat(
        !previous || j.day > previous.day || (j.day === previous.day && j.seq >= previous.seq),
        `${path}/judgements/${index}`,
        'judgements must be ordered by day and sequence',
      );
      j.cited.forEach((id) =>
        requireThat(
          evidence.has(id) && evidence.get(id).arrival_day <= j.day,
          `${path}/judgements/${index}/cited`,
          `missing or future evidence ${id}`,
        ),
      );
    });
    for (const field of ['switches', 'dependencies']) {
      thesis[field].forEach((entry, index) =>
        requireThat(
          entry.day <= data.as_of,
          `${path}/${field}/${index}/day`,
          'entry is later than as_of',
        ),
      );
    }
    thesis.switches.forEach((entry, index) => {
      const previous = thesis.switches[index - 1];
      requireThat(
        !previous ||
          entry.day > previous.day ||
          (entry.day === previous.day && entry.seq >= previous.seq),
        `${path}/switches/${index}`,
        'switches must be ordered by day and sequence',
      );
    });
  });
  return freeze(data);
}
