# Idea progress timeline — D187

The pending header no longer contains Reading. The card lists actual task stages vertically, links completed nodes, and glimmers only the current node. New stages append on arrival. Reduced-motion settings disable animations. Completed cards retain the existing click-to-open analysis behaviour.

The Idea read function reports search, decomposition, candidate retrieval, mapping and optional summarisation at their actual boundaries. HTTP optionally streams these as NDJSON; the original JSON response remains supported. The browser adds Preparing the cards only when it starts fetching bundles. Prompts, model-call count, matching, scores and dates are unchanged.

## Verified

- Real HTTP test blocks only the fake external model: the client receives search and decompose before releasing the model, then receives the remaining stages and unchanged final shape.
- 155 Python tests and 37 UI tests pass. Twelve mutation checks pass, including dropping progress events and marking every node current. Lint and formatting pass.
- Arbitrary chunk/UTF-8 splits, missing final result, server errors and JSON fallback are covered. The existing request-number and abort checks exclude old callbacks.
- Browser: four connected nodes, no header chip, one current node with the glimmer animation; cancellation leaves Library visible, and the next request completes with no pending nodes. The screenshot uses the actual UI against a controlled recorded-response server; its hold is a test fixture, not a production timer.
- Actual API cached request returns search → decompose → retrieve → map → summarize → result, with three cached logical model calls, $0 charged estimate and 0.4 seconds reported. No model or embedding calls were made for this slice. The service archive stays at six model rows; all three source database hashes match the baseline.
- Final minified JavaScript is 152,748 bytes, below 200 KiB. Current-library validation measured 25.9 ms, below 200 ms.

`pending-preview.png` shows the requested state. `live-stream.ndjson` records the actual API stream. `preview.py` is only the local recorded-response UI fixture; its temporary server was stopped after verification. The normal API is running with the refreshed app at port 8002 / API 8788. Nothing was committed, pushed or deployed.
