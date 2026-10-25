// A small Markdown renderer for the PRD viewer: headings, paragraphs, lists (nested by two-space indent), tables,
// block quotes, fenced code, rules, and inline code, bold and links. Everything is escaped first; nothing else is
// interpreted. The PRDs in docs/prd are written in this subset.
(function () {
  'use strict';

  function escapeHtml(text) {
    return String(text).replace(/[&<>"']/g, (character) => (
      { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[character]));
  }

  function inline(text) {
    const codeSpans = [];
    const withoutCode = escapeHtml(text).replace(/`([^`]+)`/g, (match, code) => {
      codeSpans.push(code);
      return `\u0000${codeSpans.length - 1}\u0000`;
    });
    return withoutCode
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
      .replace(/\u0000(\d+)\u0000/g, (match, index) => `<code>${codeSpans[Number(index)]}</code>`);
  }

  const LIST_ITEM = /^(\s*)([-*]|\d+\.)\s+(.*)$/;
  const BLOCK_START = /^(#{1,4}\s|```|>|<!--|\s*([-*]|\d+\.)\s|\s*\|)/;

  function isTableSeparator(line) {
    return /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$/.test(line || '');
  }

  function tableCells(row) {
    return row.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map((cell) => cell.trim());
  }

  function render(markdown) {
    const lines = String(markdown).replace(/\r\n?/g, '\n').split('\n');
    const html = [];
    let index = 0;
    while (index < lines.length) {
      const line = lines[index];
      if (!line.trim()) { index += 1; continue; }
      if (/^<!--.*-->$/.test(line.trim())) { index += 1; continue; }   // hidden markers, e.g. generated blocks

      // Preserve explicit historical heading aliases without showing raw HTML.
      const anchor = line.trim().match(/^<a id="([^"<>\s]+)"><\/a>$/);
      if (anchor) {
        html.push(`<a id="${escapeHtml(anchor[1])}"></a>`);
        index += 1;
        continue;
      }

      if (/^```/.test(line)) {
        const body = [];
        index += 1;
        while (index < lines.length && !/^```/.test(lines[index])) { body.push(lines[index]); index += 1; }
        index += 1;
        html.push(`<pre><code>${escapeHtml(body.join('\n'))}</code></pre>`);
        continue;
      }

      const heading = line.match(/^(#{1,4})\s+(.*)$/);
      if (heading) {
        html.push(`<h${heading[1].length}>${inline(heading[2])}</h${heading[1].length}>`);
        index += 1;
        continue;
      }

      if (/^\s*(-{3,}|\*{3,})\s*$/.test(line)) { html.push('<hr>'); index += 1; continue; }

      if (/^>\s?/.test(line)) {
        const body = [];
        while (index < lines.length && /^>\s?/.test(lines[index])) { body.push(lines[index].replace(/^>\s?/, '')); index += 1; }
        html.push(`<blockquote>${body.filter((text) => text.trim()).map((text) => `<p>${inline(text)}</p>`).join('')}</blockquote>`);
        continue;
      }

      if (line.trim().startsWith('|') && isTableSeparator(lines[index + 1])) {
        const head = tableCells(line);
        const rows = [];
        index += 2;
        while (index < lines.length && lines[index].trim().startsWith('|')) { rows.push(tableCells(lines[index])); index += 1; }
        html.push('<div class="prd__table"><table>'
          + `<thead><tr>${head.map((cell) => `<th>${inline(cell)}</th>`).join('')}</tr></thead>`
          + `<tbody>${rows.map((row) => `<tr>${row.map((cell) => `<td>${inline(cell)}</td>`).join('')}</tr>`).join('')}</tbody>`
          + '</table></div>');
        continue;
      }

      if (LIST_ITEM.test(line)) {
        const stack = [];
        let out = '';
        while (index < lines.length && LIST_ITEM.test(lines[index])) {
          const [, spaces, marker, text] = lines[index].match(LIST_ITEM);
          const indent = spaces.length;
          const tag = /\d/.test(marker) ? 'ol' : 'ul';
          while (stack.length && indent < stack[stack.length - 1].indent) out += `</li></${stack.pop().tag}>`;
          const top = stack[stack.length - 1];
          if (!top || indent > top.indent) { out += `<${tag}>`; stack.push({ indent, tag }); } else { out += '</li>'; }
          out += `<li>${inline(text)}`;
          index += 1;
        }
        while (stack.length) out += `</li></${stack.pop().tag}>`;
        html.push(out);
        continue;
      }

      const body = [];
      while (index < lines.length && lines[index].trim() && !BLOCK_START.test(lines[index])) { body.push(lines[index].trim()); index += 1; }
      if (!body.length) { body.push(line.trim()); index += 1; }
      html.push(`<p>${inline(body.join(' '))}</p>`);
    }
    return html.join('\n');
  }

  window.HIVEMIND_MARKDOWN = { render };
})();
