import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { ideaAnalysisHtml, ideaAnalysisSections } from '../src/idea/analysis.js';
import { fromIdeaResponse } from '../src/adapters/bundle.js';
import { esc } from '../src/components/dom.js';

const read = (name) =>
  JSON.parse(fs.readFileSync(new URL(`./fixtures/${name}.json`, import.meta.url), 'utf8'));
const stored = read('idea-card-v3');

test('D184/D210: the summary and every reading-step explanation and search query remain available', () => {
  const data = fromIdeaResponse(stored);
  const html = ideaAnalysisHtml(stored, data.theses);
  assert(html.includes(`<p class="detail-copy">${esc(stored.reading.summary)}</p>`));
  assert(stored.reading.parts.length > 0 && stored.reading.trace.length > 0);
  for (const part of stored.reading.parts) {
    assert(html.includes(esc(part.looks_for)));
    assert(html.includes(esc(part.why)));
  }
  for (const step of stored.reading.trace) {
    assert(html.includes(esc(step.query)));
    if (step.canonical) assert(html.includes(esc(step.canonical)));
  }
  const referenced = new Set([
    ...stored.reading.parts.flatMap((part) => [
      ...(part.direct || []),
      ...(part.driver || []),
      ...(part.context || []),
    ]),
  ]);
  for (const thesis of data.theses.filter((thesis) => referenced.has(thesis.id)))
    assert(html.includes(esc(thesis.question)));
  const responseText = html.match(/<pre class="analysis-json"[^>]*>([\s\S]*?)<\/pre>/)[1];
  const decoded = responseText.replace(
    /&(quot|amp|lt|gt|#39);/g,
    (_, name) => ({ quot: '"', amp: '&', lt: '<', gt: '>', '#39': "'" })[name],
  );
  assert.deepEqual(JSON.parse(decoded).reading, stored.reading);
});

test('D184: unavailable coverage and missing bundles are explicit; returned text stays escaped', () => {
  const none = ideaAnalysisHtml(read('idea-card-null'));
  assert(none.includes('No recorded thesis matches this idea. No analysis was generated.'));
  const empty = read('idea-card-empty');
  assert(ideaAnalysisHtml(empty).includes(esc(empty.reading.summary)));
  const unsafe = read('idea-composite-default');
  unsafe.reading.summary = '<script>bad</script>';
  unsafe.reading.parts[0].why = '<img src=x onerror=bad>';
  const html = ideaAnalysisHtml(unsafe);
  assert(html.includes('&lt;script&gt;bad&lt;/script&gt;'));
  assert(!html.includes('<script>') && !html.includes('<img'));
  assert(html.includes('(not loaded)'));
});

test('D214: overview, trace and response contain their requested content', () => {
  const data = fromIdeaResponse(stored);
  const sections = ideaAnalysisSections(stored, data.theses);
  assert(sections.overview.includes(esc(stored.reading.summary)));
  assert(
    !sections.overview.includes('analysis-search-step') &&
      !sections.overview.includes('analysis-json'),
  );
  assert(!sections.trace.includes('Search trace'));
  assert(!sections.trace.includes('analysis-candidates'));
  assert(sections.response.includes(esc(stored.reading.trace[0].query)));
  assert.equal(
    (sections.trace.match(/analysis-reading-part" open>/g) || []).length,
    stored.reading.parts.length,
  );
  assert(!sections.trace.includes('analysis-search-group'));
  assert(!sections.response.includes('detail-disclosure'));
  assert(sections.response.includes('aria-label="Idea response"'));
  const html = ideaAnalysisHtml(stored, data.theses);
  assert.equal((html.match(/role="tabpanel"/g) || []).length, 3);
  assert.equal((html.match(/ hidden>/g) || []).length, 2);
});
