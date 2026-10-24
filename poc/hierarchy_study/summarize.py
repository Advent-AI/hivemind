"""Compute reproducible descriptive statistics; never score semantic correctness."""
import argparse
import json
from pathlib import Path
from statistics import mean

import study


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    root = Path(args.out)
    data = json.loads((root / 'input.json').read_text())
    total = len(data['snapshots'][-1]['theses'])
    rows = []
    for method in study.METHODS + ['E_argument-first']:
        samples = []
        for sample in [1, 2, 3]:
            folder = root / f'sample-{sample}'
            if method.startswith('E'):
                result = json.loads((folder / 'E_result.json').read_text())
                unused = result['unused_ids']
                groups = None
            else:
                result = json.loads((folder / f'{method}-heads.json').read_text())
                partition = json.loads((folder / f'{method}-partition.json').read_text())
                unused, groups = partition['unassigned'], len(partition['groups'])
            used = {ident for head in result['heads'] for claim in head['claims'] for ident in claim['view_ids']}
            records = []
            for path in folder.glob('*.json'):
                if path.name.endswith(('-heads.json', '-partition.json', '-checks.json')):
                    continue
                value = json.loads(path.read_text())
                if not isinstance(value, dict) or 'request' not in value:
                    continue
                own = path.stem.startswith(method)
                own |= method == 'C_global_llm' and path.stem == 'C_grouping'
                own |= method == 'D_incremental_llm' and path.stem.startswith('D_incremental-')
                if own:
                    records.append(value)
            agent = json.loads((folder / f'{method}-agent.json').read_text())
            checks = json.loads((folder / f'{method}-agent-checks.json').read_text())
            samples.append({
                'sample': sample, 'groups': groups,
                'heads': sum(head['status'] == 'main_thesis' for head in result['heads']),
                'insufficient': sum(head['status'] == 'insufficient' for head in result['heads']),
                'unassigned': len(unused), 'referenced_atomic': len(used),
                'agent_input_tokens': agent['input_tokens'], 'agent_references_valid': checks['valid'],
                'model_calls': len(records), 'estimated_usd': sum(record.get('estimated_usd', 0) for record in records),
                'input_tokens': sum(record.get('input_tokens', 0) for record in records),
                'output_tokens': sum(record.get('output_tokens', 0) for record in records),
                'model_seconds': sum(record.get('seconds', 0) for record in records),
            })
        rows.append({'method': method, 'samples': samples, 'total_estimated_usd': sum(s['estimated_usd'] for s in samples), 'mean_agent_input_tokens': mean(s['agent_input_tokens'] for s in samples), 'valid_agent_samples': sum(s['agent_references_valid'] for s in samples)})
    budget = json.loads((root / 'budget.json').read_text())
    summary = {'atomic_count': total, 'rows': rows, 'budget': budget, 'source_unchanged': study.digest(json.loads((root / 'manifest.json').read_text())['source']) == json.loads((root / 'manifest.json').read_text())['source_sha256']}
    study.write_json(root / 'summary.json', summary)
    text = ['# 实验描述统计', '', '这些数字描述规模、引用与重复性，不是语义准确率。费用按仓库价格估算，仅计本实验模型请求。', '', '| 方法 | 三个样本的总论点数 | 未归组/未使用数 | Agent 输入 token 均值 | 引用合法样本 | 三样本估算费用 |', '|---|---|---|---:|---:|---:|']
    for row in rows:
        samples = row['samples']
        text.append(f'| {row["method"]} | {" / ".join(str(s["heads"]) for s in samples)} | {" / ".join(str(s["unassigned"]) for s in samples)} | {row["mean_agent_input_tokens"]:.0f} | {row["valid_agent_samples"]}/3 | ${row["total_estimated_usd"]:.4f} |')
    text += ['', f'原始库指纹未变化：{summary["source_unchanged"]}。', f'登记模型请求：{len(budget["attempts"])}。估算用量：${budget["estimated_spent"]:.4f}。', '', '逐请求原始输出和 usage 在 sample-1/、sample-2/、sample-3/。']
    (root / 'metrics.md').write_text('\n'.join(text) + '\n')
    print('\n'.join(text))


if __name__ == '__main__':
    main()
