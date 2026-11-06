"""Whether a dropped 'fence' fact still reached the product ($0): for each window draw that dropped one, the same draw's ledger is searched
for a record carrying the fact's distinctive words and filed under a question that takes it. The test-article draws have no ledger."""
import sqlite3

RUNS = '/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-06-architecture-benchmark/runs'
CHECKS = [  # (packet case, dropped draws, distinctive words in the quote, questions that take it)
    (1, ['d2'], ['11.1 trillion', '11.1T'], ['v13', 'v4']), (2, ['d2'], ['north of $2T', '$2 trillion', '$2T'], ['v13', 'v4']),
    (5, ['d2'], ['27% CAGR'], ['v16']), (9, ['d1', 'd2', 'd3'], ['12.76'], ['v11']), (18, ['d2'], ['11.67'], ['v11']),
    (27, ['d3'], ['91 billion'], ['v1']), (23, ['d1', 'd2'], ['NVL576'], ['v18']), (29, ['d2'], ['NVL72x2'], ['v18']),
    (30, ['d1'], ['NVL72x2'], ['v18']), (31, ['d1'], ['CPO-NVSwitch', 'CPO NVSwitch'], ['v18'])]
reached = lost = 0
for case, draws, words, questions in CHECKS:
    for draw in draws:
        con = sqlite3.connect(f'file:{RUNS}/control-v108-{draw}/views.sqlite?mode=ro', uri=True)
        rows = con.execute('select e.created_from_input, group_concat(l.view_id) from evidence e left join evidence_links l using(evidence_id) where '
                           + ' or '.join(['e.quote like ?'] * len(words)) + ' group by e.evidence_id', [f'%{w}%' for w in words]).fetchall()
        right = [r for r in rows if r[1] and set(r[1].split(',')) & set(questions)]
        reached += bool(right); lost += not right
        print(f'#{case} {draw}: {len(rows)} records carry it, {len(right)} filed under {"/".join(questions)}')
print(f'reached from another article: {reached}; lost to the product: {lost}')
