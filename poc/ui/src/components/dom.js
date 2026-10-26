export const esc = (value) =>
  String(value ?? '').replace(
    /[&<>"']/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c],
  );
export const SEP = '<span class="sep">|</span>';
export const ICON = {
  scale:
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v17M7 21h10M4 7h16M6 7l-4 7h8L6 7Zm12 0-4 7h8l-4-7ZM2 14a4 4 0 0 0 8 0m4 0a4 4 0 0 0 8 0"/></svg>',
  idea: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 18h6M10 21h4M9 15.5c0-1.6-3-2.7-3-6a6 6 0 0 1 12 0c0 3.3-3 4.4-3 6H9Z"/></svg>',
  thesis:
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9l-6-6Z"/><path d="M14 3v6h6M8 13h8M8 17h5"/></svg>',
};
export function element(tag, className, html = '') {
  const node = document.createElement(tag);
  node.className = className;
  node.innerHTML = html;
  return node;
}
export function safeLink(uri, title, className = '') {
  try {
    const url = new URL(uri);
    if (!['http:', 'https:'].includes(url.protocol)) return esc(title);
    return `<a class="${esc(className)}" href="${esc(url.href)}" target="_blank" rel="noopener noreferrer">${esc(title)} ↗</a>`;
  } catch {
    return esc(title);
  }
}
