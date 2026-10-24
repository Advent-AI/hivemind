/** Date helpers use explicit UTC calendar dates, never the machine's current day. */
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
export const dayDiff = (a, b) =>
  Math.round((Date.parse(`${b}T00:00:00Z`) - Date.parse(`${a}T00:00:00Z`)) / 86400000);
export function addDays(day, count) {
  const date = new Date(`${day}T00:00:00Z`);
  date.setUTCDate(date.getUTCDate() + count);
  return date.toISOString().slice(0, 10);
}
export const fmtDay = (day) => `${MONTHS[Number(day.slice(5, 7)) - 1]} ${Number(day.slice(8, 10))}`;
export const longDay = (day) => `${fmtDay(day)}, ${day.slice(0, 4)}`;
export function calendarX(day, start, end, left, right) {
  const span = dayDiff(start, end);
  if (!span) return (left + right) / 2;
  const offset = typeof day === 'number' ? day : dayDiff(start, day);
  return left + Math.min(1, Math.max(0, offset / span)) * (right - left);
}
export function isCalendarDay(day) {
  return (
    typeof day === 'string' &&
    /^\d{4}-\d{2}-\d{2}$/.test(day) &&
    Number.isFinite(Date.parse(`${day}T00:00:00Z`)) &&
    new Date(`${day}T00:00:00Z`).toISOString().slice(0, 10) === day
  );
}
