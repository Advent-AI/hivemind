**BLOCKER: the script can restart failures that were meant to stop the run.** It checks only for `status == "failed"`, so a provider refusal or spending-limit failure receives the same continuation as the cut network reply.

For draw 1, the recorded failure was the stated `IncompleteRead`, and the continuation starts after the first 50 completed articles. Its joined traces and library are stamped in the expected order.

Each segment also starts with a fresh copy of the limits. The original per-run spending and call limits therefore do not bound the combined draw across multiple segments.