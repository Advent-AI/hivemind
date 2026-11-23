**No-go:** version 8 detects the replacements named in its tests, but checking the path before and after opening does not prove which file SQLite opened.

For example, the path can name A at the first check, B when SQLite opens it, and A again at the second check. Both checks match A’s lock, while the connection has opened B. The same gap applies to the writer’s create/open sequence. This is a counterexample to the contract’s guarantee, not a reproduced failure in this repository. [Contract, file identity](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md:138).

Before building, either specify a way to bind the opened SQLite database to the locked file and prove that case, or narrow the operating contract to forbid path replacement while a store is being opened or used, with the limits of detection stated. Add the A → B → A case to the proof if the stronger guarantee remains.

One other check belongs in proof 8: after a crashed writer leaves committed data in a WAL, copy the store through a hard-link alias and compare it with a copy through the original path. Sharing the main file’s inode does not by itself establish that SQLite will find the same path-named WAL sidecars. Refuse that alias if the comparison cannot be guaranteed. [Contract, aliases and copies](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md:135).

The shared lock-folder lifecycle now states the manual-deletion limitation honestly, and the changed-text restoration test is included. P1 remains proposed; these would be test-store proofs, not authorization for live operation. [Contract](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md:124).

CONSENSUS: no, because the identity checks do not establish which file SQLite opened, and copying a WAL store through a hard-link alias remains unproved.