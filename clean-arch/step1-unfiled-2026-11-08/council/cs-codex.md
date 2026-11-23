**Two issues still block the send.** For example, an article could give a signing date two years away, and the revised schema would permit that date even though the standard caps the check date at 18 months.

- **Check date:** The schema says to use the date the item supports and applies the 18-month limit only when the item gives none. Apply the limit in both cases.
- **Transport errors:** The revision promises one recorded retry, but `send()` returns immediately on the first transport error. Either implement the stated retry and preserve both attempts, or revise the plan to say how an error affects the result.

The other changes address the main findings: the code now checks the opening conditions both ways, rejects empty or repeated new questions, preserves returned raw content, and reports skipped articles. Whether two statements describe the same obligation and whether an existing question covers it still need the planned human reading.

SEND WITH CHANGES