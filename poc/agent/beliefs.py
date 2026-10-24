"""Belief → view: one model call that reads a user's sentence and the object's open questions (as of the views
database it is given, for example the day-0 snapshot) and answers which question the sentence bets on, how the
sentence and the question differ, or 'none' with the three nearest questions. No state is shown, so the mapping
cannot be pulled by where the judgement currently stands."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import model  # noqa: E402
from hivemind.views import store  # noqa: E402

SCHEMA = {
    'type': 'object', 'additionalProperties': False, 'required': ['view_id', 'difference', 'nearest', 'why'],
    'properties': {'view_id': {'type': 'string'}, 'difference': {'type': 'string'},
                   'nearest': {'type': 'array', 'items': {'type': 'string'}}, 'why': {'type': 'string'}},
}

SYSTEM = """你是 agent 的落题员。用户说了一句话（一个看法、一条新闻、一个人的帖子、一种感觉）。下面是这家公司和相关主题现在开着的问题（每个问题有答案区间和到期日，不给当前判断）。
判断这句话押的是哪个问题。用户的话几乎都不带日期，常常说的是股价会涨会跌、或者转述别人的看法；股价本身不是问题，但推动股价的那件事是。把这句话落到它实际在押的那个问题上：
- 押的是其中一个：view_id 写它的编号；difference 用人话说清用户的原话和这个问题差在哪，包括他说的比问题宽、窄、或没有日期（比如「你说的是需求撑到年底，这个问题问的是全年收入涨多少；需求撑住但价格跌了，收入也可能不达标」；「你说的是中国市场迟早放开，这个问题问的是今年年底前 H200 能不能获准进口，他没说什么时候，这个问题有日期」）。
- 只有当这句话根本不是关于公司业务或世界会怎样的事（审美、梦、对人的评价、该不该拆股这类公司动作），或者它押的那件事列出的问题里确实没有（比如列表里没有关于融资担保、市场份额的问题），才写 none；nearest 列最接近的三个编号，difference 说清缺的是哪个问题。
不要替用户发明问题，只在列出的里面选。"""


def map_sentence(conn_views, archive, cfg, sentence, object_ids, *, transport=None):
    shown = []
    for object_id in object_ids:
        for view_id in store.views_of_object(conn_views, object_id):
            shown.append(view_id)
        for view_id in list(shown):
            for dep in store.dependencies_of(conn_views, view_id):
                if dep['resolved_to'] and dep['resolved_to'] not in shown and store.is_open(conn_views, dep['resolved_to']):
                    shown.append(dep['resolved_to'])
    lines = []
    for view_id in shown:
        v = store.view(conn_views, view_id)
        rungs = ' / '.join(f'{r["label"]}：{r["condition"]}' for r in store.rungs_of(conn_views, view_id))
        lines.append(f'- {view_id}（{v["object_id"]}，看的是「{v["looks_at"]}」，到期 {v["due_day"]}）：{v["question"]}\n    答案区间：{rungs}')
    user = f'用户的话：「{sentence}」\n\n开着的问题：\n' + ('\n'.join(lines) if lines else '（没有）') + '\n\n按 JSON schema 回答。'
    answer = model.call(archive, cfg, cfg.matching, SYSTEM, user, SCHEMA, 'belief', 'belief', transport=transport)
    data = answer.data
    view_id = data['view_id'].strip()
    if view_id not in shown:
        view_id = None
    settlement_day = store.view(conn_views, view_id)['due_day'] if view_id else None
    return {'sentence': sentence, 'view_id': view_id, 'difference': data['difference'], 'nearest': [n for n in data['nearest'] if n in shown][:3],
            'why': data['why'], 'settlement_day': settlement_day, 'shown': shown, 'call_id': answer.call_id, 'cost': answer.cost_usd}
