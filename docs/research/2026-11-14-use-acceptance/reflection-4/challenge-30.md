# Round 31: fixed. Go or no-go.

`compare_readings.py`: when either reading is not measured, marks, W faults and controls are not compared at all (test 2 in
`compare-selftest.txt` now ends "marks, W faults and controls: not compared (a reading is not measured)"). The packets: the
re-reading's packets are built by the unchanged builder with the same seed in a new folder and checked byte for byte against the
first reading's packet files before any reader starts; a difference stops it. End with `CONSENSUS: yes` or `CONSENSUS: no, because …`.
