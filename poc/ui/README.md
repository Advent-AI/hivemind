# Thesis UI

Thesis 卡片、图、证据和详情的可复用组件。Idea 卡在 `src/idea/idea.js`：把用户的一句话 POST 给服务的 `/ideas`，用 `fromIdeaResponse` 进合同，再由 `graphOf` 保留服务给出的连接关系（D138）。被它取代的本地匹配演示（`legacy/idea.js`）已删除。

## 数据怎么进来

唯一规范是 [thesis.schema.json](src/model/thesis.schema.json)，版本为 `thesis-ui/1`。`parseDataset` 验证后复制并冻结数据，失败会抛出带字段路径的 `ContractError`，不会把半份数据画到页面。

现有 bundle 通过 `fromBundles` 转换一次。不要在卡片里重命名字段或猜 score。

```js
import {createThesisExplorer, fromBundles} from './src/index.js';
import './src/styles/index.css';

// agent 已选择 v3；此 GET 只读取数据，不调用模型。
const response = await fetch('/thesis-bundles?ids=v3,v1,v7&as_of=2026-08-15');
if (!response.ok) throw new Error(`Cannot load theses (${response.status})`);
const dataset = fromBundles(await response.json());

const explorer = createThesisExplorer(document.querySelector('#explorer'), {dataset});
explorer.showGraph({primaryId: 'v3', supportingIds: ['v1', 'v7']});
explorer.openThesis('v3');

// 新回复到达后：先验证，再替换。非法回复不会覆盖当前画面。
explorer.setDataset(nextDataset);
// 页面卸载时：移除 DOM、事件和动画。
explorer.destroy();
```

MCP 的同一入口是 `thesis_bundles({view_ids: ['v3','v1','v7'], as_of:'2026-08-15'})`。
`POST /ideas` 的回复可直接交给 `fromIdeaResponse(response)`，用 `graphOf(response)` 得到 `rootIds` 和 `branches[{sourceId,targetId}]`。所有选中的 Thesis 同级展示；关联 Thesis 的来源取自 `related[].via`，不用数组顺序推断。
这层 UI 不调用模型、不存密钥，也不替 agent 选择 Thesis。

请求的关系目标必须先加载，才能作为 `supportingIds` 显式展示。数据中未载入的关系引用可以保留，UI 不会凭空补出卡片。历史关闭状态按 `switches[].day` 计算，不按 due date 猜测。

## 组件与字段

| 组件 | 主要字段 |
|---|---|
| `createThesisCard` | question、rungs[].score/label、截至日期的 judgements |
| `ladderChart` / `bindHistoryChart` | 显式 score、judgements[].day/seq/rung、evidence[].arrival_day |
| `createThesisDetail` | 同一 Thesis 的快照、来源、开关历史、关系 |
| 证据列表 | one_line、quote、tier、source、original_who、replaced_by |
| `createCanvas` | 调用方给定的 rootIds、branches、可选 leading card；独立 Thesis 的 primaryId/supportingIds 入口仍可用 |

`day` 是证据的显示/来源日期；`arrival_day` 是它进入该 Thesis 的日期。日期回放和柱状图只读后者。
判断引用的证据必须存在，而且不能晚于判断日期。规范输入不接受未知字段、重复 id、无效日期或无效状态。
所有展示文本都会转义；来源仅允许 http/https 链接；不使用原生标题 hover tooltip。

两个实例可同时挂载：状态、事件、DOM id 和图表裁剪 id 都限定在各自实例。
宿主为容器提供高度；组件继承 [共享 theme tokens](../../web/design-system/tokens.css)，字体仍使用 Geist。

## 开发与验证

在仓库根目录运行：

```sh
npm ci --prefix poc/ui
python3 scripts/mock_build.py
npm --prefix poc/ui run lint
npm --prefix poc/ui run format:check
npm --prefix poc/ui test
npm --prefix poc/ui run test:mutations
python3 -m pytest tests -q
python3 docs/check.py
```

`poc/mock/index.template.html` 只保留页面骨架。生成的 `poc/mock/index.html` 内联 CSS、JS 和已验证数据，仍可单文件打开。
源数据、翻译缓存不会被构建修改。esbuild、Ajv、ESLint 和 Prettier 都仅用于构建/开发；浏览器运行独立验证函数。

`npm --prefix poc/ui run verify:page` 生成 `poc/ui/dist/verify.html`，用来在真实浏览器检查多个实例、非法更新、销毁和空历史。`dist` 与生成的 validator 不手工编辑。

数据和状态表详见 [设计记录](../../docs/poc/thesis-ui.md)。组件库本身不发请求、不调模型；只有 `src/idea/idea.js` 和页面入口 `src/bootstrap.js` 调用服务（地址默认 `http://127.0.0.1:8788`，可用 `<body data-api="…">` 指定）。
