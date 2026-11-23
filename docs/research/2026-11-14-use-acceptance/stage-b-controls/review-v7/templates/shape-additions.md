Two additions to the shape the brief gives:

1. `decisive_items` lists 2 to 6 distinct item ids from the packet.
2. For a question whose `unit` is `yes/no`, add the key `outcome_on_due_day`: the `label` of the one rung of that question that you expect to hold on its `due_day`, judged by each rung's own `condition`. It is "Yes" exactly when `implied_outcome.yes_no` is true. When `no_view` is true, set it to null. For a question whose `unit` is not `yes/no`, do not add this key.
