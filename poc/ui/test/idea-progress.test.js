import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { advanceIdeaProgress, ideaProgressHtml } from '../src/idea/progress.js';
import { readIdea, readIdeaEvents } from '../src/idea/idea.js';

const card = JSON.parse(
  fs.readFileSync(new URL('./fixtures/idea-card-empty.json', import.meta.url), 'utf8'),
);

test('D187: each real stage appends one node, with only the latest marked current', () => {
  let stages = [];
  for (const stage of ['search', 'decompose', 'retrieve', 'map', 'summarize', 'cards']) {
    stages = advanceIdeaProgress(stages, stage);
    assert.equal(advanceIdeaProgress(stages, stage), stages);
    const html = ideaProgressHtml(stages);
    assert.equal((html.match(/<li /g) || []).length, stages.length);
    assert.equal((html.match(/aria-current="step"/g) || []).length, 1);
    assert(html.includes(`is-current" data-progress-stage="${stage}"`));
  }
  assert.throws(() => advanceIdeaProgress(stages, 'private-thought'), /Unknown/);
  assert.throws(() => advanceIdeaProgress(['map'], 'decompose'), /backwards/);
});

function stream(bytes, size = 17) {
  return new Response(
    new ReadableStream({
      start(controller) {
        for (let i = 0; i < bytes.length; i += size) controller.enqueue(bytes.slice(i, i + size));
        controller.close();
      },
    }),
    { headers: { 'Content-Type': 'application/x-ndjson; charset=utf-8' } },
  );
}

test('D187: streamed stages survive split UTF-8 and preserve the stored final response', async () => {
  const progress = [];
  const events = [
    { type: 'progress', stage: 'search' },
    { type: 'progress', stage: 'decompose' },
    { type: 'result', data: card },
  ];
  const wire = new TextEncoder().encode(events.map((event) => JSON.stringify(event)).join('\n'));
  assert.deepEqual(await readIdeaEvents(stream(wire, 1), (stage) => progress.push(stage)), card);
  assert.deepEqual(progress, ['search', 'decompose']);
});

test('D187: a failed or interrupted stream never becomes a completed card', async () => {
  const encode = (value) => new TextEncoder().encode(value);
  await assert.rejects(
    readIdeaEvents(
      stream(encode('{"type":"error","status":502,"message":"Model unavailable"}')),
      () => {},
    ),
    (error) => error.status === 502 && error.message === 'Model unavailable',
  );
  await assert.rejects(
    readIdeaEvents(stream(encode('{"type":"progress","stage":"search"}\n')), () => {}),
    /stopped before returning/,
  );
  await assert.rejects(
    readIdeaEvents(stream(encode('not JSON')), () => {}),
    /invalid analysis/,
  );
});

test('D187: the same client negotiates progress and accepts a legacy JSON response', async (t) => {
  t.mock.method(globalThis, 'fetch', async (url, options) => {
    assert.equal(options.headers.Accept, 'application/x-ndjson');
    return new Response(JSON.stringify(card), { headers: { 'Content-Type': 'application/json' } });
  });
  assert.deepEqual(await readIdea('http://example.test', 'A revenue idea'), card);
});
