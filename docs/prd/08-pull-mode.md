# Pull mode

> Status: scheduling and due-date freezing are decided (D54); remaining design is deferred. English edition: October 25, 2026 (D163).
> The earlier draft predates D41. Its verification conditions, premises, fallback reviews, driver merging/splitting and waiting requirements no longer apply.
> Design page: `docs/system-design.html` → New → Pull mode. Recorded decisions take precedence.

## Purpose

The only time-driven module: run at day-end or scheduled intervals to review and update theses, and freeze and close those that are due.

## Decided behaviour

- The incoming stream handles items without reading the calendar; pull mode owns time-driven work.
- Run at day-end or at scheduled intervals for an overall review and update.
- Freeze due theses at their current rung, without a separate result. Decisive information enters normally as evidence; freezing does not wait for it.
- Dependencies read the closing state and reasons. Further tracking uses a new successor thesis under the library's rules.
- Supply “now” externally: real time in production, replay time in tests. The system has no internal clock.
- Upstream delivery is distinct and must not be called pull mode.

## Example

Suppose NVDA FY2027 China revenue is due on the annual earnings date, illustrated as February 25, 2027. Published results show an 85% decline versus FY2026. The library rejudges it to “down at least 80%”. Day-end pull freezes that state and closes the thesis. Dependencies read the closing conclusion. An FY2028 successor continues tracking.

## Open questions

- Detailed day-end/scheduled execution and what the overall review does.
- Whether final verdict is separate. Claude proposed integrating it here because rejudgement already reads all evidence still in force; this is unapproved. Keep its Config settings meanwhile.
- The library's two proposals: unavailable answers/pending publication, and daily duplicate checks.
- Whether to fetch exact settlement numbers such as prices/XBRL, from the team's library or original source, and whether those enter through dispatch.

## Earlier draft: no longer used

The former design sent due theses to a final verdict after all pre-deadline publications were processed; reviewed weakened premises after seven days; and periodically merged/split drivers. D38/D41 removed those concepts; D54 removed the extra wait.

## Related decisions

- D12/D13: the stream does not read the calendar. D14: design the two modes separately.
- D29: earlier expiry final verdict, superseded by D54.
- D31: externally supplied “now”; the premise-lag fallback is obsolete.
- D54: scheduled overall review and due-date freezing without waiting.
