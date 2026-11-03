"""The model's own account of why gpt-6-luna keeps statements the reference rejects (product and benchmark figures, a partner's
or another company's own business). Same method and store as probe.py (stored conversation continued, one question each)."""
import concurrent.futures
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe  # noqa: E402

ASK = ("Which instruction led you to record {ids} as evidence? Quote the instruction text you followed. Then say whether any "
       "instruction tells you to leave such a statement out, and quote it if so.")
CASES = [
    ('j355-d1', 355, 'gnews:4249e0578b11cedf5a71ff08', 1, ASK.format(ids='e1 and e2 (the beamforming and link-adaptation throughput figures)')),
    ('j200-d1', 200, 'nvblog:open-models-icml-2026', 1, ASK.format(ids='e1 and e2 (papers accepted at ICML and papers citing NVIDIA GPUs)')),
    ('j381-d1', 381, 'gnews:784c556d2e58ed09dd8aa7fc', 1, ASK.format(ids='e1 and e2 (the Defense Department blacklisting of Hesai)')),
    ('j6-d1', 6, 'gnews:87607a311ad24b410c6ef85a', 1, ASK.format(ids='e3 and e4 (Intel\'s own quarterly revenue and EPS)')),
    ('j210-d1', 210, 'gnews:085b1e1a1543437edb9756d6', 1, ASK.format(ids='e4 and e5 (hyperscaler take-or-pay terms and AI debt-financing needs)')),
]

if __name__ == '__main__':
    conn = probe.store()
    done = {r[0] for r in conn.execute('select case_id from probes')}
    conn.close()
    with concurrent.futures.ThreadPoolExecutor(5) as pool:
        list(pool.map(probe.one, [c for c in CASES if c[0] not in done]))
    conn = probe.store()
    for case_id, reply, cost in conn.execute("select case_id, reply, cost_usd from probes where case_id like 'j%'"):
        print('=====', case_id, cost, '\n', (reply or '')[:1800])
