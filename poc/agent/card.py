"""The bet card: five lines beside a holding. What you bet, the question watched, the current judgement, the last
check (from the processing record), the exit condition."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind.views import store  # noqa: E402


def render(conn_views, conn_agent, user, view_id):
    v = store.view(conn_views, view_id)
    rungs = store.rungs_of(conn_views, view_id)
    state = store.current_state(conn_views, view_id)
    condition = conn_agent.execute('select * from conditions where user=? and view_id=? order by condition_id desc limit 1', (user, view_id)).fetchone()
    day, input_id = store.last_check(conn_views, view_id)
    lines = [
        f'你押的是什么：{condition["belief"] if condition and condition["belief"] else "（没写）"}',
        f'盯的问题：{v["question"]}（到期 {v["due_day"]}）',
        f'当前判断：第 {state["rung"]} 格 {rungs[state["rung"] - 1]["label"]}' if state else '当前判断：还没判',
        f'上次核对：{day or "还没有"}' + (f'，读的是 {input_id}' if input_id else ''),
        f'出场条件：判断掉到第 {condition["threshold_rung"]} 格「{rungs[condition["threshold_rung"] - 1]["label"]}」或更差，{condition["action"]}' if condition else '出场条件：（没设）',
    ]
    return '\n'.join(lines)
