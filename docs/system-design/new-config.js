// The New design's Config module (the model settings a person chooses) and the dispatch step, the system's single entry.
// Edit the data at the top; the two drill-downs render it. Decisions D2-D4, D17, D18, D25, D27, D29, D31 and D41 in docs/DECISIONS.md. The texts
// are for a reader who did not follow the discussion: plain words, no field names.
(function () {
  'use strict';

  // What Config records: a version, its checksum and the model settings for reading text.
  const CONFIG_SCHEMA = [
    { item: 'Version', meaning: 'Every settings change creates a new version.', source: 'Created when settings change' },
    { item: 'Checksum', meaning: 'Calculated from the complete configuration and recorded with every model call, including extraction, matching, rejudgement and final verdicts, so the exact version can be traced.', source: 'Calculated by code' },
    { item: 'Model settings and search result count', meaning: 'Extraction has settings per category: model, prompt version, reasoning effort and temperature (lower temperature makes answers more stable). The thesis library has separate matching and rejudgement settings; final verdicts have their own. Config also sets the search result count, initially 10. Prompt content belongs to the extraction, thesis library and final-verdict modules. A settings version is immutable; a change creates a new one.', source: 'Chosen by a person' },
  ];

  // The dispatch tree. A branch asks one question; each child is one answer (`answer`). A child without children is
  // where the item ends up: `act` marks the one that processes it.
  const DISPATCH_TREE = {
    label: 'An item arrives', question: 'Is the item complete?', note: 'Check author, publication day, classification result and upstream ID.',
    children: [
      { answer: 'Incomplete', label: 'Return', note: 'This is an upstream problem; also place it in the human review pool.' },
      {
        answer: 'Complete', label: 'Check processing records', question: 'Has it been processed?', note: 'Use the upstream ID. An updated version is a new item with its own ID.',
        children: [
          { answer: 'Already processed', label: 'Skip', note: 'Do not pay again when upstream resends an item or a test reruns.' },
          {
            answer: 'Not processed', label: 'Read classification', question: 'What is the classification result?',
            children: [
              { answer: 'Invalid', label: 'Do not process', note: 'Record the reason; unresolved lookup entries go to the human review pool.' },
              { answer: 'Not source material', label: 'Do not process', note: 'For example, derived indicators we can calculate ourselves, or a file listing.' },
              { answer: 'Duplicate item', label: 'Merge with the original item', note: 'Record another source for the original item; do not process it again.' },
              { answer: 'Assigned to a category', label: 'Send to extraction', note: 'Include its category and sequence number; extraction reads each category differently.', act: true },
            ],
          },
        ],
      },
    ],
  };

  const TREE_NOTES = [
    'Grey boxes stop processing. The black box sends the item to extraction.',
    'Do not filter by subject here. Incoming items are already within the research universe, so dispatch does not decide which categories to process.',
    'Every category goes to extraction with its category-specific reading method; no manual selection. Extraction defines what each category yields.',
    'An unregistered publication series does not stop processing; also record it in the human review pool.',
    'Assign sequence numbers in arrival order, without using the computer clock. All later steps use that order.',
    'Processed means completed. Resume unfinished work from its recorded step rather than treating it as completed.',
  ];

  const RULES = [
    'Config owns human-selected model settings and the thesis search result count. Upstream classification supplies category, publication day and subjects. Code owns processing order and failure handling. The research universe owns subjects and tracked categories.',
    'Config does not set spending or concurrency limits.',
    'Any change creates a new version. Preserve old versions without modifying them.',
    'Missing required values or references to nonexistent model settings invalidate the entire version. It cannot process any item.',
  ];

  const OPEN = [
    'None currently.',
  ];

  function renderBranch(branch, escapeHtml, isRoot) {
    const isOutcome = !branch.children;
    const classes = ['org-node', isRoot ? 'org-node--root' : '', isOutcome ? (branch.act ? 'org-node--act' : 'org-node--leaf') : '']
      .filter(Boolean).join(' ');
    const box = `<div class="${classes}">`
      + (branch.answer ? `<span class="org-node__family">${escapeHtml(branch.answer)}</span>` : '')
      + `<span class="org-node__label">${escapeHtml(branch.label)}</span>`
      + (branch.question ? `<span class="org-node__question">${escapeHtml(branch.question)}</span>` : '')
      + (branch.note ? `<span class="org-node__note">${escapeHtml(branch.note)}</span>` : '')
      + '</div>';
    const below = isOutcome ? ''
      : `<ul>${branch.children.map((child) => `<li>${renderBranch(child, escapeHtml, false)}</li>`).join('')}</ul>`;
    return box + below;
  }

  // Scale the tree down, never up, so the whole of it is in view.
  function fitTree(container) {
    const frame = container.querySelector('.org');
    const tree = container.querySelector('.org-tree');
    tree.style.zoom = '1';
    tree.style.zoom = String(Math.min(1, (frame.clientWidth - 8) / tree.scrollWidth));
  }

  const design = window.HIVEMIND_DESIGNS.new;
  design.drilldowns = design.drilldowns || {};

  design.drilldowns.dispatch = {
    button: 'Explore dispatch: where each item goes',
    kicker: 'Dispatch · Details',
    size: 'full',
    render(container, context) {
      const escapeHtml = context.escapeHtml;

      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">Dispatch: route each item</h2>
          <p class="drill__intro">For each item, ask three questions in order: is it complete, has it been processed, and what is its classification? Each item has one destination. The research universe determines which categories arrive.</p>
          <div class="org"><div class="org-tree"><ul><li>${renderBranch(DISPATCH_TREE, escapeHtml, true)}</li></ul></div></div>
          <ul class="drill__rules">${TREE_NOTES.map((note) => `<li>${escapeHtml(note)}</li>`).join('')}</ul>
        </div>`;
      requestAnimationFrame(() => fitTree(container));
      window.addEventListener('resize', () => { if (container.isConnected) fitTree(container); });
    },
  };

  design.drilldowns.config = {
    button: 'Explore Config',
    kicker: 'Config · Details',
    size: 'full',
    render(container, context) {
      const escapeHtml = context.escapeHtml;
      const schemaRows = CONFIG_SCHEMA.map((row) => `<tr><td>${escapeHtml(row.item)}</td><td>${escapeHtml(row.meaning)}</td>`
        + `<td class="schema-table__quiet">${escapeHtml(row.source)}</td></tr>`).join('');

      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">Config: settings a person chooses</h2>
          <p class="drill__intro">Config owns human-selected settings: extraction settings per category, matching, rejudgement, final verdicts and the search result count. Extraction defines what each category yields and how prompts are assembled. The research universe defines subjects and tracked categories.</p>
          <div class="drill__columns drill__columns--schema">
            <section>
              <h3 class="drill__heading">Recorded settings</h3>
              <table class="schema-table schema-table--compact">
                <thead><tr><th>Item</th><th>Meaning</th><th>Source</th></tr></thead>
                <tbody>${schemaRows}</tbody>
              </table>
            </section>
            <section>
              <h3 class="drill__heading">Rules</h3>
              <ol class="drill__rules">${RULES.map((rule) => `<li>${escapeHtml(rule)}</li>`).join('')}</ol>
              <h3 class="drill__heading drill__heading--spaced">Open questions</h3>
              <ul class="drill__rules">${OPEN.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>
            </section>
          </div>
        </div>`;
    },
  };
})();
