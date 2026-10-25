# 运行后修正：请求里的编号约束漏传

本轮已经结束；不重新采样，不覆盖原答，不把此修正当作本轮成功。

范围：本轮 5 次归组抽取请求全部只把 thread_ids 的元素声明为 string。实际产生 11 个引用，grouped-2/item1 的 4 个引用不在已展示或声明集合，其余 7 个合法。运行器的写入前检查正确拒绝了这一整份回答。

机制：原隔离 retained_membership.extraction_schema(offered) 把本地 t 编号及展示的 g 编号写进 pattern；移到当前 keyed schema 时，我漏了这个约束。服务端 schema 允许 g3/g4，后续代码却禁止它，造成请求和检查不一致。不是证明编号表示本身不可行。

最便宜的验证：把应有的 pattern 对本轮全部 11 个原始引用重放，4 个非法引用全部从 wire-valid 变成 wire-invalid，另 7 个不变，见 schema-repair-proof.json。这只证明请求约束收紧到原合同，不证明模型会改答正确，更不恢复 grouped-2 的业务内容。

修正：schema 显式接收 offered，把合法编号空间写进请求；运行前检查仍验证 t 编号确实有本次声明，不按名称猜测或修补引用。旧 runner 在 run-original.py，原 manifest 和付费记录保持不变。新的代码未做付费验证。

状态/读者变化：只变请求 schema 的元素约束；原答、候选、组 writer、成员、证据形状和读者不变。未展示的 g 编号在模型边界和写入前均不合法；本地 t 编号仍需已声明。这个修正不改变业务验收，不扩展 PRD。
