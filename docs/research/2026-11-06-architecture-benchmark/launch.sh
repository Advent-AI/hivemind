#!/bin/zsh
# Launch the benchmark's paid draws (benchmark-design.md, "What runs"): three split and three control window draws at once, then the six test-article
# draws. Each draw runs detached under caffeinate (the r10 draws were suspended for five hours when the laptop slept), with its run.out and pid file
# in its own new folder. Refuses to start if the design's hashes do not verify or a draw folder exists.
set -e
REPOSITORY="$(cd "$(dirname "$0")/../../.." && pwd)"
BENCH="$REPOSITORY/docs/research/2026-11-06-architecture-benchmark"
cd "$REPOSITORY"
shasum -a 256 -c "$BENCH/benchmark-design.sha256" > /dev/null || { echo "design hashes do not verify" >&2; exit 2 }
uptime
curl -s -o /dev/null -w "openai reachable: %{http_code}\n" --max-time 10 https://api.openai.com/v1/models
typeset -A CONFIGS
CONFIGS=(split-v3 poc/config/poc-split-v3.json control-v108 poc/config/poc-v108.json)
for name in split-v3 control-v108 test-split test-control; do
  for draw in 1 2 3; do
    folder="$BENCH/runs/$name-d$draw"
    test ! -e "$folder" || { echo "exists: $folder; every draw starts in a new folder" >&2; exit 2 }
  done
done
for arm in split-v3 control-v108; do
  for draw in 1 2 3; do
    folder="$BENCH/runs/$arm-d$draw"
    mkdir -p "$folder"
    nohup caffeinate -i env PYTHONPATH="$REPOSITORY/src" python3 "$BENCH/bench_run.py" --config "$REPOSITORY/${CONFIGS[$arm]}" --run-folder "$folder" \
        > "$folder/run.out" 2>&1 &
    echo $! > "$folder/run.pid"
    echo "launched $arm d$draw pid $(cat $folder/run.pid)"
  done
done
for arm in split control; do
  for draw in 1 2 3; do
    folder="$BENCH/runs/test-$arm-d$draw"
    mkdir -p "$folder"
    nohup caffeinate -i env PYTHONPATH="$REPOSITORY/src" python3 "$BENCH/bench_test_articles.py" --arm $arm --draw $draw > "$folder/run.out" 2>&1 &
    echo $! > "$folder/run.pid"
    echo "launched test $arm d$draw pid $(cat $folder/run.pid)"
  done
done
