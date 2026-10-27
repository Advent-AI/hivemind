export const esc = (value) =>
  String(value ?? '').replace(
    /[&<>"']/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c],
  );
export const SEP = '<span class="sep">|</span>';
export const ICON = {
  action:
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m13 3-8 10h6l-1 8 9-11h-6l1-7Z"/></svg>',
  hyperliquid:
    '<svg class="action__logo" viewBox="0 0 144 144" aria-hidden="true"><path d="M144 71.6991C144 119.306 114.866 134.582 99.5156 120.98C86.8804 109.889 83.1211 86.4521 64.116 84.0456C39.9942 81.0113 37.9057 113.133 22.0334 113.133C3.5504 113.133 0 86.2428 0 72.4315C0 58.3063 3.96809 39.0542 19.736 39.0542C38.1146 39.0542 39.1588 66.5722 62.132 65.1073C85.0007 63.5379 85.4184 34.8689 100.247 22.6271C113.195 12.0593 144 23.4641 144 71.6991Z"/></svg>',
  trigger:
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h16l-6.5 7.5V20l-3-2v-6.5L4 4Z"/></svg>',
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
