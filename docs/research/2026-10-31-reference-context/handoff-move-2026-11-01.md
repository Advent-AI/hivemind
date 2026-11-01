# 换机器续跑：带什么、多大、怎么同步（2026-11-01）

一句话：**代码和文档全在 GitHub 上，直接 clone 分支就有；数据不在 Git 里，一共要带 1 个 93 MB 的包**，解开放到仓库根目录，拷一个凭证文件，就能续跑三组种子 v2。

## 1. 代码：在 GitHub（`https://github.com/Advent-AI/hivemind.git`）

| 分支 | 是什么 | 状态 |
|---|---|---|
| `fix/extraction-quality-2026-10-28` | 跑抽取和端到端臂用的代码、标准页、金标、提示词、配置、种子 | 已推送，和 origin 一致；HEAD `17c7d5b` + 本次交接提交 |
| `fix/question-identity-r2` | R2（D248 第 2–3 条，合题）的代码，worktree `hivemind-identity-r2` | 已推送；比抽取分支多 1 个提交、少 5 个（R3 之后的），量 R2 之前要先合进抽取分支的最新提交 |
| `main` | 服务、UI、Idea 的最新代码；流水线还是旧的 `poc-v23` | 已推送；但**工作区有 27 个改过没提交的文件和 340 个没加进 Git 的文件（1.7 GB，`poc/reports/2026-10-25..27-*` 的研究输出）**，不是我这次的工作，没动。它们不影响续跑；若要带走，见 §5 |

进 Git 的部分（抽取分支的工作树 100 MB，pack 33 MB）里已经有：

- 标准页 `docs/prd/05-extraction-standard.html`；第 5 版金标 `docs/research/2026-10-29-ledger-standard/golden-v5/`（dev `6f9476bb…`、test `af2145cd…`，`golden-v5.sha256`）
- 提示词 `src/hivemind/prompts/`（role/categories/review v53…v66、placement-narrow-v2）；配置 `poc/config/poc-v69.json`（默认）、`poc-v83.json`（种子臂）、`poc-v84.json`（R3 抽取）
- 种子 `poc/seeds/nvda-2026-07-01.json`（v1）、`nvda-2026-07-01-v2.json`（v2，23 题）
- 比较和打分脚本：`docs/research/2026-10-31-reference-context/e2e_compare.py`、`r3_compare.py`、`r3_lost.py`；`docs/research/2026-10-29-ledger-standard/final-2026-10-30/final_scores.py`
- 本次新加的可移植启动脚本 `docs/research/2026-10-31-reference-context/run_seedv2.sh`（路径都从脚本位置算，不写死机器）

## 2. 数据：不在 Git，一个包

`~/hivemind-backups/run-move-2026-11-01.tar.gz`，**93 MB**，316 个文件，SHA-256
`c8ff99bab6ca01f82e1fe0bd7510c91966b9298d8e22d4ad74036c2ea06d966a`。路径相对仓库根目录，内容：

| 路径 | 是什么 | 解开后大小 |
|---|---|---|
| `poc/data/items-nvda-2026-07-01-10-27.sqlite` | **清理过的语料库**（D256：7-01 到 10-27 的 NVDA 文章，二进制规则和第二次抓取之后的那一版），所有跑法读的就是它；SHA-256 `57bc25441fea325b…` | 236 MB |
| `poc/data/e2e-v83-seed-d1..3` | 当前对照：poc-v83 + 种子 v1，三遍（10-31） | 75 MB |
| `poc/data/e2e-v83-seedv2-d1..3` | **要续跑的三组**：poc-v83 + 种子 v2，第 1 天停在 Jev HTTP 402 | 2 MB |
| `poc/data/e2e-v69-dev14-2026-10-31`、`-d2`、`-d3` | 不带种子的对照（poc-v69），三遍 | 61 MB |
| `poc/data/e2e-v69-seed-d1..3`、`e2e-v69-seed2-d1..3` | 种子 v1 在 poc-v69 下的两组三遍 | 82 MB |
| `poc/data/e2e-v82-dev14-2026-10-31` | 抽取 v71（参照架构）一遍，没采用 | 19 MB |
| `docs/research/2026-10-29-analyst-standard/loop-2026-10-29/Y5-v65-d1..3`、`Y6-v66-d1..3` | 抽取层 bench 的存档答案（R3 的对照和臂），`r3_compare.py`、`final_scores.py` 读 | 6 MB |

每个跑法文件夹里：`views.sqlite`（账本）、`archive.sqlite`（模型调用存档）、`replay.log`、`run.out`。

**没打进包、这台机器上还有的**（续跑不需要）：`.page.sqlite`（抓来的网页原文，169 MB，流水线不读）；语料库的两个早期状态和 TrueNorth 版（`.before-*.sqlite`、`-tn*.sqlite`，1.1 GB）；三个月旧跑法和封存账本（`english-v29/v34-*`、`sealed-2026-10-28-*`、`poc/data/service`，1.2 GB，UI 在放的就是它）；抽取 bench 的其余约 160 个答案存档（`loop-2026-10-29/`，334 MB）。都列在 `docs/research/2026-10-25-english/data-manifest.md`。

## 3. 凭证：自己拷，不走 Git

`~/.config/hivemind/credentials.json`（权限 600），代码只认这个路径（`model.CREDENTIALS`）。里面是模型和 Jev（TypeSafe）的 key。**不要放进仓库、包、聊天或命令行参数。**

## 4. 在新机器上怎么做

```sh
# 1. 代码
git clone https://github.com/Advent-AI/hivemind.git
cd hivemind && git checkout fix/extraction-quality-2026-10-28
python3 --version          # 这里是 3.10；第三方包只有 tiktoken
pip install tiktoken

# 2. 数据：把包拷过来（scp / rsync / 网盘），先对哈希，再解到仓库根目录
shasum -a 256 run-move-2026-11-01.tar.gz     # 要等于 c8ff99ba…
tar -xzf run-move-2026-11-01.tar.gz -C /path/to/hivemind
shasum -a 256 poc/data/items-nvda-2026-07-01-10-27.sqlite   # 要以 57bc25441fea325b 开头

# 3. 凭证：把 ~/.config/hivemind/credentials.json 拷到新机器同一路径，chmod 600

# 4. 先过一遍 $0 的检查，再付费
python3 -m pytest tests -q                        # 255 passed（2026-11-01）；要写 tests，不然会收进 poc/reports 里旧研究的测试文件
python3 scripts/preflight.py --views poc/data/e2e-v83-seed-d1/views.sqlite

# 5. 续跑三组（各自开一个终端或后台；第一分钟盯 run.out，上次就是第 1 篇文章的匹配就报 402）
zsh docs/research/2026-10-31-reference-context/run_seedv2.sh 1
zsh docs/research/2026-10-31-reference-context/run_seedv2.sh 2
zsh docs/research/2026-10-31-reference-context/run_seedv2.sh 3
tail -f poc/data/e2e-v83-seedv2-d1/run.out        # 结束行 RUN-E2E-DONE

# 6. 跑完比：种子 v1 对 v2（design-seed-v2.md 里冻结的预测）
python3 docs/research/2026-10-31-reference-context/e2e_compare.py \
    control=poc/data/e2e-v83-seed-d1,poc/data/e2e-v83-seed-d2,poc/data/e2e-v83-seed-d3 \
    seedv2=poc/data/e2e-v83-seedv2-d1,poc/data/e2e-v83-seedv2-d2,poc/data/e2e-v83-seedv2-d3
```

续跑的规则（`scripts/replay.py`）：文件夹里已有账本就从最后一个完整的天之后接着跑；三组现在都停在第 1 天中间，直接运行即可，不用删。要从头来也行：把 `e2e-v83-seedv2-d*` 三个文件夹换个新日期名，脚本会新建。花费上限每组 3 美元（`--cap 3`）；种子 v1 的三组（同一窗口、同一配置）各花了不到 3 美元，所以上限不会先到。

## 5. 要不要把数据放 GitHub

**不建议放代码仓库。** 语料库 236 MB 超过 GitHub 单文件 100 MB 的限制，`.gitignore` 也把 `poc/data/` 排除了。三条路：

1. **包直接拷**（本文的做法）：93 MB，scp / rsync / 网盘，对哈希。最省事，我倾向这个。
2. 单独一个数据仓库用 Git LFS：免费额度 1 GB 存储、1 GB/月流量，这个包放得下；但每台机器要装 LFS，流量很快用完。
3. 对象存储（S3 / GCS）一个桶，`aws s3 cp`。要新建账号和权限，是你的事。

`main` 工作区那 27 个改过没提交的文件（AGENTS.md、DECISIONS.md、CURRENT_STATE.md、model.py、service.py、语料脚本等，10-25 到 10-30 的改动）不在任何分支上，换机器就没有了。要带走的话，一条命令提到一个新分支再推（我没做，等你说）：

```sh
cd /Users/lchingen/hivemind && git checkout -b wip/main-uncommitted-2026-11-01 && git add -u && git commit -m "WIP: main's uncommitted changes as of 2026-11-01" && git push -u origin wip/main-uncommitted-2026-11-01
```

那 340 个没加进 Git 的研究输出（1.7 GB）不建议进 Git；要留就 tar 到 `~/hivemind-backups/`。

## 6. 这台机器上没清、也不该清的

- `poc/data/` 全部 4.0 GB 原样在；没有删任何东西（规则：删存档数据要你的要求、备份、逐项列出、记日志）。
- 我这次在 `loop-2026-10-29/` 里放的三个本地符号链接 `Y6-v65-d1..3`（为了让 `final_scores.py Y6 v65 v66` 有对照）已经删掉；重现那张分数表要先建回去：`ln -s Y5-v65-d1 Y6-v65-d1`（d2、d3 同），结果在 `r3-final-scores-Y6.txt`。
