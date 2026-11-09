**SEND — clean arm, pending the control harness.**

The retry accounting now reserves and charges each attempt separately, with the release and charge under one lock. The launcher stamps both the trace and library, and the adapter checks both hashes before replay.

I reviewed the code and tests; I did not run the tests in this read-only review.