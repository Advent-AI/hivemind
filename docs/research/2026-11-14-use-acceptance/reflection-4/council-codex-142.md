**Yes: build and run proof 2f**, with the successful case exercising the bundle path as well as the Idea submission.

The proposed 409 stub matches the API’s status, JSON body and content type. The page requests a stream, but `readIdea` handles a non-200 JSON response before trying to decode stream events. [API mapping](/Users/lchingen/hivemind/scripts/hivemind_api.py:44), [page reader](/Users/lchingen/hivemind/poc/ui/src/idea/idea.js:25).

For case A, use a card with at least one selected or related question and `card.idea.as_of == L`. Assert that `/thesis-bundles` receives `as_of=L`, returns a valid fixture at L, and that the resulting card and its dated chart or question are displayed. Otherwise an empty selection skips `readBundles`, leaving that path unexercised. [Idea flow](/Users/lchingen/hivemind/poc/ui/src/bootstrap.js:193), [bundle reader](/Users/lchingen/hivemind/poc/ui/src/idea/idea.js:221).

For case B, the listed checks make “nothing else breaks” concrete for this test: the error is visible, the library remains usable, a second submission is sent, and no uncaught error occurs. Report that scope rather than claiming all page behavior was checked.

I checked the saved proof-10 result and output; they support the reported pause and poll counts, with MCP limited to module-level calls. I did not rerun it. [Proof 10 result](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/live-service/PROOF10-RESULT.md).

CONSENSUS: yes