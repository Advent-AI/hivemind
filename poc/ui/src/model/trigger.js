export const TRIGGER_SIZE = Object.freeze({ width: 320, height: 168 });
export const DEFAULT_TRIGGER_CONDITION = Object.freeze({ operator: '>', threshold: 70 });
export const TRIGGER_OPERATORS = Object.freeze([
  { value: '>', label: '>', description: 'Greater than' },
  { value: '>=', label: '≥', description: 'Greater than or equal to' },
  { value: '<', label: '<', description: 'Less than' },
  { value: '<=', label: '≤', description: 'Less than or equal to' },
  { value: '=', label: '=', description: 'Equal to' },
  { value: '!=', label: '≠', description: 'Not equal to' },
]);

/** A Trigger compares a displayed whole percentage with one bounded integer threshold. */
export function readTriggerCondition(condition = DEFAULT_TRIGGER_CONDITION) {
  if (
    !condition ||
    Object.keys(condition).sort().join(',') !== 'operator,threshold' ||
    !TRIGGER_OPERATORS.some((option) => option.value === condition.operator) ||
    !Number.isInteger(condition.threshold) ||
    condition.threshold < 0 ||
    condition.threshold > 100
  )
    throw new TypeError('A Trigger needs a supported comparison and an integer from 0 to 100');
  return { ...condition };
}

export function triggerMatches(condition, confidence) {
  const { operator, threshold } = readTriggerCondition(condition);
  if (confidence === null) return null;
  if (!Number.isFinite(confidence) || confidence < 0 || confidence > 100)
    throw new TypeError('Trigger confidence must be a percentage or null');
  const value = Math.round(confidence);
  switch (operator) {
    case '>':
      return value > threshold;
    case '>=':
      return value >= threshold;
    case '<':
      return value < threshold;
    case '<=':
      return value <= threshold;
    case '=':
      return value === threshold;
    case '!=':
      return value !== threshold;
  }
}
