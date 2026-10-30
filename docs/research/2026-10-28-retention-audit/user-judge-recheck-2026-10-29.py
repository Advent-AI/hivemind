"""Recount the old judge answers against the user's later, specific decisions.

The pointers and verdicts are manual readings. This is retrospective and
measures relevance/weight only, not citation, exact meaning, or correct pages.
"""
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = {
    'memory': 'gnews:fbce0469dbb5b33e2c34a0f5',
    'amd': 'gnews:55b3b854d30ecb73679c2088',
    'singapore': 'gnews:1eeceeb212a2c82c2e75e806',
    'financial': 'gnews:71df54965281684cc500960f',
    'policy': 'gnews:f9e7da6ddbf890fa64baf922',
}

# One row per user decision (6a/b/c separately), one cell per old answer.
# A non-negative number is the fact's index in its article; None is omitted.
# For the negative examples None is correct; index 0 is the case overview.
CASES = [
    ('1', 'financial', 'core', [None, None, None, None, None, 1], '收入增长预期；实验第三次还漏掉收入指标。'),
    ('2', 'financial', 'exclude', [None, None, None, None, None, None], '仅此 FY2028 每股收益预测排除。'),
    ('3', 'memory', 'core', [None, None, None, None, None, 4], 'SK hynix 长期短缺预测；实验第三次标次要。'),
    ('4', 'amd', 'colour', [1, 1, 1, 1, 1, 1], 'AMD 100 kW 机柜下的建模比较。'),
    ('5', 'singapore', 'exclude', [0, 0, 0, 0, 0, 0], '同案概况；其他事件不一概推论。'),
    ('6a', 'policy', 'colour', [0, 0, 0, 0, 0, 0], '开放权重模型联名信；三个子项按用户合并回答 B。'),
    ('6b', 'policy', 'colour', [None, None, None, None, None, None], '美国财长拟调查知识产权问题。'),
    ('6c', 'policy', 'colour', [None, None, None, None, None, 1], '白宫顾问对 Moonshot 的指称。'),
    ('7', 'financial', 'core', [0, 0, None, 0, 0, 0], '管理层对 2026／2027 云厂商支出的预测。'),
]


def main():
    outputs = []
    for stem in ('economic-judge-result', 'economic-judge-arm-result'):
        for sample in range(1, 4):
            name = f'{stem}-{sample}-2026-10-29.json'
            data = json.loads((HERE / name).read_text())
            articles = {a['input_id']: a for a in data['articles']}
            assert len(articles) == len(data['articles']) and set(SOURCES.values()) <= articles.keys()
            outputs.append((name, articles))
    reviews = []
    for user_id, source, expected, pointers, note in CASES:
        assert len(pointers) == len(outputs)
        cells = []
        for (name, articles), pointer in zip(outputs, pointers):
            facts = articles[SOURCES[source]]['facts']
            assert pointer is None or 0 <= pointer < len(facts)
            fact = facts[pointer] if pointer is not None else None
            actual = fact['weight'] if fact is not None else 'exclude'
            assert actual in ('core', 'colour', 'exclude')
            cells.append({'file': name, 'fact_index': pointer, 'actual_weight': actual,
                          'correct_relevance_and_weight': actual == expected,
                          'fact': fact, 'all_article_facts_if_absent': facts if fact is None else None})
        reviews.append({'user_question': user_id, 'source_input_id': SOURCES[source],
                        'expected_weight': expected, 'note': note, 'samples': cells})
    assert len(reviews) == 9 and len({c['user_question'] for c in reviews}) == 9
    counts = [sum(c['samples'][i]['correct_relevance_and_weight'] for c in reviews) for i in range(6)]
    out = {'scope': 'Nine specific user-decided items in old six-article dev judge experiment, rescored after the answers; not holdout or acceptance.',
           'criteria': 'For each item select or exclude as the user chose; if selected, agree on core versus colour. Does not prove meaning, citation or page.',
           'correct_per_sample': counts, 'denominator_per_sample': len(reviews), 'cases': reviews}
    with (HERE / 'user-judge-recheck-2026-10-29.json').open('x') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps({'correct_per_sample': counts, 'denominator': len(reviews)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
