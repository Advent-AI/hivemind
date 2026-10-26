# Idea service startup smoke — October 26, 2026

The frontend reported “Cannot reach the service at http://127.0.0.1:8788” because only the static page server was running. The API port had no listener. No frontend or backend code change was needed.

Started the existing HTTP service on loopback port 8788 using its default English ledger, `poc-v9` configuration and `idea-v7` prompt. TLS connectivity and configured credential presence were checked without exposing secrets. Startup built the semantic search index for all 90 theses (10,145 embedding input tokens). The source ledger and items database remain read-only; index and Idea archive are under `poc/data/service-english/`.

Retried the user's exact submitted text, “Nvidia will beat earning next quarter”, through the browser. The API completed the two Idea model calls and the subsequent thesis-bundle request. The page rendered ten selected theses and explained that no stored thesis directly judges next-quarter earnings versus expectations. This is one operational smoke, not semantic quality or stability acceptance.

The required preflight ran on the existing English archive with a scratch copy of source items. It exited zero: 754 extraction answers, 250 matching records, 159 prompt enum checks. Its historical extraction refusals are not an Idea test and were not changed; the relevant current port failure was established before any model call. No ingestion or scoring work ran. All three protected source database hashes remain unchanged.

[Model-call measurements](result.json) and [working browser](working.png) are retained. The API remains running for the user's local session (PID 42222); the static page server is PID 40401. Runtime logs and pid file are in `/var/folders/lm/gw2hxzg52rd1brqm_bnlv6b00000gn/T/hivemind-idea-service-20261026-ie2uyb8m/`.
