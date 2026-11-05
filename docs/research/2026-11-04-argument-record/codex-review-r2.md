**仍有实质缺口，第二稿还不能直接据此实现。** 例如：即使卡片只引用一条证据，这条证据附带的转载关系仍能不断增长，输入并没有随之固定下来。

1. **决策一致性：上一轮结论漏出了输入清单。**  
   设计 §3 只列上一张卡片，§4 的卡片却不含上一轮档位。这样无法可靠判断“是否改变”，而这个结果会触发其他问题重判。应明确保留上一轮结论供比较；现有要求见 [PRD:89](/Users/lchingen/hivemind/docs/prd/06-views.md:89)，实际输入见 [judging.py:157](/Users/lchingen/hivemind/src/hivemind/views/judging.py:157)，传播见 [judging.py:332](/Users/lchingen/hivemind/src/hivemind/views/judging.py:332)。首轮对输出一致性的回答因此还不完整。

   修订保留新旧两条、独立来源交给模型判断、事务失败先回滚，这三项回答成立。未发现新增第二套问题状态、删除原始证据或直接修改冻结文件的要求；v8 仍须按 D354、D359 另开版本。

2. **状态与恢复：还缺三个明确约定。**  
   - **§6“换配置会拒绝续跑”并非所有入口成立。** `--workers 1` 不使用并行日清单，可以绕过该检查。半天 v7、半天 v8 时，已提交的判断仍会被跳过。见 [入口](/Users/lchingen/hivemind/scripts/replay.py:58)、[跳过条件](/Users/lchingen/hivemind/src/hivemind/views/judging.py:300)。这是首轮回答中的事实错误。
   - **§6 漏了“等待的依赖题终于建立”。** 它即使尚未判断，也会让依赖它的问题重新进入判断队列，并非只有“依赖结论变了”才触发。需要覆盖新到证据为空、依赖尚无判断编号的情况。见 [writing.py:60](/Users/lchingen/hivemind/src/hivemind/views/writing.py:60)。
   - **§4、§6 只明确保存依赖结论版本，没有明确主题结论版本。** 公司题可能先读旧主题结论，主题随后才判断；不能用当天最后的主题结论解释前面的卡片。依赖顺序优先于主题优先，见 [judging.py:309](/Users/lchingen/hivemind/src/hivemind/views/judging.py:309)。主题引用也应绑定实际读到的判断编号。

3. **读取方与检查：预检还缺历史上下文，旧库读取也未写清。**  
   **§5、§10 不能只把存档回答交给当前检查。** 检查仍从数据库读取“最新结论”和当前依赖。内存验证中，一份当时正确的“维持第 2 档”回答，被后来的第 3 档误判成违规变档。必须按原请求之前的状态检查，包括上一张卡片。见 [judging.py:210](/Users/lchingen/hivemind/src/hivemind/views/judging.py:210)、[judging.py:226](/Users/lchingen/hivemind/src/hivemind/views/judging.py:226)。

   §5 还须规定旧库没有 `arguments` 表时返回“无卡片”，因为历史库通过[只读连接](/Users/lchingen/hivemind/src/hivemind/views/store.py:216)打开，不能靠读取时建表。读取清单另漏了 [条件事件扫描](/Users/lchingen/hivemind/poc/agent/conditions.py:44)，它直接读取判断及引用；保留旧字段后未见必然破坏，但应列入核对。评分程序确实可以不改，前提是保留种子身份、日期、档位及档位边界，见 [scorer:40](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py:40)。

4. **大小：§7 的收窄仍不充分，§6 的首次升级“有界”不成立。**  
   `same_as` 会带出不断增加的关联编号，[store.py:425](/Users/lchingen/hivemind/src/hivemind/views/store.py:425)生成它，[judging.py:134](/Users/lchingen/hivemind/src/hivemind/views/judging.py:134)全部打印。内存构造验证：同样只显示一条证据，关联编号从 1 个增至 1,000 个，请求从 592 字节增至 6,484 字节。因此连“老证据部分不再随时间增长”也尚未保证。

   首次升级沿用的 v7 窗口按**判断次数**划分，不按天数；不足五次时包含全部有效证据，见 [judging.py:47](/Users/lchingen/hivemind/src/hivemind/views/judging.py:47)。一天的新增量、依赖和主题数量也没有硬上限。当前可以承诺限制卡片理由及直接引用数量，不能承诺请求整体有界。

5. **不做周期更新：结论正确。**  
   未发现需要在没有新判断时重写论证正文的情况。关闭、重开、主题退出使用范围，应更新展示状态及引用标记，保留当时的卡片；依赖绑定属于信息变化，应走正常判断，不需要定时重写。依据 [D356](/Users/lchingen/hivemind/docs/DECISIONS.md:3734)。

本次未修改文件，未调用付费模型；验证仅使用只读检查和内存计算。

