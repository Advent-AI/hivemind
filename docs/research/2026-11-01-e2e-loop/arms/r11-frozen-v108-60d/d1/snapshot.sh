#!/bin/sh
# Online copy of both databases (SQLite's backup API: consistent even while the run writes) into snapshots/<stamp>/.
R=/Users/lchingen/hivemind-run-v109-2026-11-04/docs/research/2026-11-01-e2e-loop/arms/r11-frozen-v108-60d/d1
S=$R/snapshots/$(date '+%Y-%m-%dT%H%M%S'); mkdir -p "$S"
for f in views archive; do sqlite3 "$R/$f.sqlite" ".backup '$S/$f.sqlite'" && echo "$f.sqlite → $S ($(sqlite3 "$S/$f.sqlite" 'pragma integrity_check'))"; done
cp "$R/run.out" "$S/run.out"
