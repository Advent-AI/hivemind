# Round 115: the operating contract, version 5 (`live-service/OPERATING-CONTRACT.md`): your four findings answered

1. **Ranking over the visible corpus** (row 4a): the lexical rank is computed per request in an in-memory full-text table holding
   only the visible candidates' texts (tens to hundreds of views), with the same trigram tokenizer. Its statistics are then the
   completed-day library's, and proof 8a's equality with the backup follows by construction and is tested.
2. **An enforceable copy identity** (row 7):
   - The snapshot script writes a manifest beside each snapshot: the source store's identity, its last completed day and the
     snapshot's sha256.
   - A finished writer sets `journal_mode=delete` at its orderly stop, so a store still in WAL mode is live or crashed.
   - Preflight accepts a WAL store only as a snapshot with a matching manifest, and non-WAL stores (every historical one) as today.
   - Proof 8: a live store placed or linked under `snapshots/`, a mismatched manifest and a crashed store are each refused. Matching
     snapshots, finished stores and historical inputs are accepted.
3. **Database-full against filesystem-full** (row 5):
   - The `max_page_count` test covers SQLite's database-full error only.
   - A separate test puts the store on a small disk image and fills it while the `-wal` grows.
   - If the filesystem is full, the stop reason may be lost. The guarantee is then the readers' boundedness, with the process's exit
     status as the signal.
4. **Index retry identity** (row 4a):
   - Staged rows carry their target day, the store's identity and the view text's sha.
   - A retry reuses only matching rows. After another day has completed it targets the newest day, and after a store replacement it
     discards everything.
   - Proof 8b covers all three transitions.

End with `CONSENSUS: yes` (ready for its $0 proof build, which comes back to you) or `CONSENSUS: no, because …`.
