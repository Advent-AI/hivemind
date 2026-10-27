import { element } from './dom.js';
import { cardHeaderHtml } from './primitives.js';
import { createSelect } from './select.js';
import {
  DEFAULT_TRIGGER_CONDITION,
  TRIGGER_OPERATORS,
  TRIGGER_SIZE,
  readTriggerCondition,
  triggerMatches,
} from '../model/trigger.js';

// Range positions share the native 14px handle's 7px inset at each end.
const scalePosition = (value) => `calc(${value}% + ${((50 - value) * 0.14).toFixed(2)}px)`;

/** Editable confidence condition; the host owns persistence and supplies the current assessment. */
export function createTriggerCard({
  condition = DEFAULT_TRIGGER_CONDITION,
  confidence = null,
  onChange = () => {},
} = {}) {
  let current = readTriggerCondition(condition);
  triggerMatches(current, confidence);
  const events = new AbortController();
  const node = element(
    'section',
    'card card--trigger',
    `${cardHeaderHtml('Trigger', '<span class="chip trigger__status" role="status"></span>')}
    <div class="card__body">
      <div class="trigger__condition"><span class="trigger__label">If</span><div class="trigger__metric"></div><div class="trigger__operator"></div><label class="trigger__threshold percentage-input"><input type="number" min="0" max="100" step="1" aria-label="Confidence threshold"><span aria-hidden="true">%</span></label></div>
      <div class="trigger__scale">
        <input class="trigger__slider" type="range" min="0" max="100" step="1" aria-label="Adjust confidence threshold">
        <span class="trigger__current-marker" aria-hidden="true"></span>
        <div class="trigger__current"><span>Current value:</span><span class="trigger__confidence"></span></div>
      </div>
    </div>`,
  );
  node.setAttribute('aria-label', 'Idea confidence Trigger');
  node.style.width = `${TRIGGER_SIZE.width}px`;
  const number = node.querySelector('input[type="number"]');
  const slider = node.querySelector('input[type="range"]');
  const scale = node.querySelector('.trigger__scale');
  const currentMarker = node.querySelector('.trigger__current-marker');
  const status = node.querySelector('.trigger__status');
  const metric = createSelect(node.querySelector('.trigger__metric'), {
    options: [{ value: 'ai-confidence', label: 'AI confidence' }],
    value: 'ai-confidence',
    label: 'Trigger metric',
    onChange: () => {},
  });
  const operatorRoot = node.querySelector('.trigger__operator');
  const operator = createSelect(operatorRoot, {
    options: TRIGGER_OPERATORS,
    value: current.operator,
    label: 'Confidence comparison',
    onChange: (value) => change({ ...current, operator: value }),
  });
  operatorRoot.querySelectorAll('[role="option"]').forEach((option, index) => {
    option.setAttribute('aria-label', TRIGGER_OPERATORS[index].description);
  });

  function sync() {
    const matched = triggerMatches(current, confidence);
    number.value = slider.value = String(current.threshold);
    slider.style.setProperty('--trigger-progress', scalePosition(current.threshold));
    scale.style.setProperty('--trigger-current', scalePosition(Math.round(confidence ?? 50)));
    currentMarker.hidden = confidence === null;
    slider.setAttribute('aria-valuetext', `${current.threshold}%`);
    operatorRoot
      .querySelector('button')
      .setAttribute(
        'aria-label',
        `Confidence comparison: ${TRIGGER_OPERATORS.find((option) => option.value === current.operator).description.toLowerCase()}`,
      );
    status.textContent = matched === null ? 'No confidence' : matched ? 'Met' : 'Not met';
    status.classList.toggle('chip--ink', matched === true);
    node.dataset.matched = matched === null ? 'unavailable' : String(matched);
    node.querySelector('.trigger__confidence').textContent =
      confidence === null ? 'Unavailable' : `${Math.round(confidence)}%`;
  }
  function change(next) {
    current = readTriggerCondition(next);
    sync();
    onChange({ ...current });
  }
  const bounded = (value) => Math.max(0, Math.min(100, Math.round(value)));
  for (const input of [number, slider]) {
    input.addEventListener(
      'input',
      () => {
        if (Number.isFinite(input.valueAsNumber))
          change({ ...current, threshold: bounded(input.valueAsNumber) });
      },
      { signal: events.signal },
    );
  }
  for (const control of [number.closest('label'), slider]) {
    control.addEventListener(
      'wheel',
      (event) => {
        event.preventDefault();
        event.stopPropagation();
        if (event.deltaY)
          change({ ...current, threshold: bounded(current.threshold - Math.sign(event.deltaY)) });
      },
      { passive: false, signal: events.signal },
    );
  }
  number.addEventListener('blur', sync, { signal: events.signal });
  sync();
  return {
    element: node,
    setConfidence(value) {
      triggerMatches(current, value);
      confidence = value;
      sync();
    },
    close() {
      metric.close();
      operator.close();
    },
    destroy() {
      events.abort();
      metric.destroy();
      operator.destroy();
      node.remove();
    },
  };
}
