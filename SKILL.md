---
name: fit-evidence
description: 运动营养学与运动康复的循证学习工具。当用户询问运动补剂（肌酸、蛋白粉）、训练营养（蛋白时机、合成代谢窗口）、运动恢复与康复（拉伸防伤、冰敷vs热敷、泡沫轴、肌肉酸痛/肌肉损伤）、以及任何"这个说法有没有文献支持/结论靠不靠谱/给我看证据"类问题时使用。工作方式：先查知识库（存储位置可配置：本地 JSON 或用户自己的飞书多维表格）命中即输出结论卡；未命中再检索文献、逐篇分析、按自研双维评分规则（证据真实度×生活影响度）评分入库。禁止凭印象回答运动营养/康复问题，必须引用可溯源文献。
---

# FitEvidence：运动循证知识助手

帮助用户学习运动营养学与运动康复知识，核心是"**每条结论都追溯到文献，每篇文献都过一遍审核规则**"。

**数据归属每个使用者**：Skill 只装指南、数据模板与内置示例。实际知识库存放在用户自选的位置——本地目录，或用户**自己的**飞书多维表格。任何人安装本 Skill，数据都落在他自己账号/目录下，互不干扰。

## 第 0 步：初始化数据存储（首次使用必做，之后跳过）

1. 读取 `storage.json`：
   - 已配置 `backend` → 按配置工作，跳到第 1 步。
   - 未配置 → **询问用户数据放哪**（这是指南型 Skill 的关键动作，不要默认跳过）：
     - **a) 飞书多维表格（推荐）**：数据在用户自己的飞书账号，可被网页/其他 Agent 调用，可跨设备；
     - **b) 本地目录**：离线、零依赖，可指定任意目录；
     - **c) 仅用内置示例数据**：skill 内 `data/`，开箱即用，后续可迁移。
2. 执行初始化：
   - b/c：`python scripts/init_storage.py --backend local [--data-dir <路径>] [--seed]`
     - 不指定 `--data-dir` = 用 skill 内 `data/`；指定目录时默认建空库，加 `--seed` 复制内置示例数据。
   - a：先用 lark-base 能力在用户飞书账号建**两张多维表格**（字段见 `templates/papers.schema.json`、`templates/topics.schema.json`），再回填：
     `python scripts/init_storage.py --backend lark --app-token <app_token> --papers-table-id <id> --topics-table-id <id>`
   - 想带内置示例数据到飞书：先 local+seed 初始化 → `python scripts/sync_lark.py export` 导出 CSV → 用 lark-base 把 CSV 导入飞书两张表。

## 工作流（按顺序执行）

### 第 1 步：主题归一化
- 用 `references/topics.md` 的关键词表把用户问题映射到主题 id。
- 命中主题 → 第 2 步查库；未命中 → 第 3 步新建主题。

### 第 2 步：查知识库（命中式复用，不重复分析）
- 按 `storage.json` 定位数据：
  - **local**：直接读数据目录的 `papers.json`、`topics.json`（目录由 `storage.json` 的 `data_dir` 解析，缺省 skill 内 `data/`）。
  - **lark**：用 lark-base 能力查飞书 `topics` 表 → 命中后从 `papers` 表取该主题文献明细；查询前可先 `python scripts/sync_lark.py import` 把云端数据拉回本地缓存再统一查。
- 找到主题且有 `score_total`/`grade` → 直接输出主题结论卡（见输出模板）。
- 未命中或记录为空 → 第 3 步。

### 第 3 步：检索文献
- 优先顺序：系统综述 / Meta 分析 > 随机对照试验 > 队列研究 > 专家共识（Cochrane、PubMed/PMC、权威期刊官网）。
- 每个主题至少 2-3 篇可溯源文献（真实 URL，禁止二手转述替代原文）。
- 同时收集**边界/反驳**文献（亚组无效、阴性结果），防止结论过度乐观。

### 第 4 步：逐篇分析
- 按 `references/scoring_rubric.md` 第 5 节字段逐篇填写（design / method_quality / venue / reproducibility / recency_years / effect_size / applicability / actionability / cost_risk / population / intervention / outcome / limitations / conclusion）。
- 追加到数据目录的 `papers.json`。

### 第 5 步：评分（机器计算，保证可复算）
```bash
python scripts/score_paper.py           # 自动按 storage.json 定位当前库并回填
python scripts/score_paper.py --file <papers.json>   # 指定文件
python scripts/score_paper.py <单篇.json>            # 单篇试算
```
- 综合分 = 0.65×证据真实度(A) + 0.35×生活影响度(B)，回填 score_A / score_B / score_total / grade。
- 分级：strong(≥80) / recommended(60-79) / uncertain(40-59) / unreliable(<40)。

### 第 6 步：入库并刷新视图
- 更新数据目录 `topics.json` 的语义字段（bottom_line / action_advice / keywords），数值交给脚本：
```bash
python scripts/build_knowledge_base.py [--data-dir <目录>]
```
- 脚本按主题"主张方向"重算主题综合分（positive=文献总分均值；negative=100-均值），刷新 `key_papers`，生成人读视图 `knowledge_base.md`（写在数据目录上一级）。

### 第 7 步：输出学习卡片 + 同步飞书（若 lark 后端）
- 按下方模板输出；未命中新主题时同步在 `references/topics.md` 补关键词。
- lark 后端：`python scripts/sync_lark.py export` 生成 CSV → 用 lark-base 把新增/更新记录导入飞书两张表，保证云端库一致。

## 输出模板（主题结论卡）

```
## 【主题中文名】—— 分级标签（综合分 XX）
**问题**：……
**一句话结论**：bottom_line
**行动建议**：action_advice
**证据支撑**（n 篇，可溯源）：
| 文献 | 设计 | 年份 | 真实度 | 影响度 | 综合 | 分级 | 结论 |
|---|---|---|---|---|---|---|---|
| [标题](url) | …… | …… | A | B | total | …… | …… |
**需要注意**：limitations（人群边界 / 争议点）
```

- 分级标签用中文：强证据·可执行 / 推荐·有条件 / 证据不足·存疑 / 不靠谱·勿轻信。
- 必须把"边界条件"（女性/患者无效、阴性结果）写进结论，不得用总体结论掩盖亚组差异。

## 数据存储：可配置后端

| 后端 | 数据在哪 | 谁拥有 | 适用 |
| --- | --- | --- | --- |
| `local`（默认） | 本地 JSON（skill 内 `data/` 或自选目录） | 使用者本人 | 离线、零依赖、隐私优先 |
| `lark` | 用户自己的飞书多维表格（两张表：papers / topics） | 使用者本人 | 可被网页/其他 Agent 调用、跨设备、可协作 |

- 配置存在 `storage.json`；切换后端只需重跑 `scripts/init_storage.py --backend …`。
- 数据文件契约（字段定义）：`templates/papers.schema.json`、`templates/topics.schema.json`；空库模板 `templates/*.empty.json`。
- 同类可扩展后端（进阶，README 有说明）：SeaTable（自托管、开源、SQL 接口）等 Airtable 类产品，走同一套 CSV 交换协议。

## 数据维护约定

- **唯一数据源**：数据目录的 `papers.json` + `topics.json`（local 后端即最终库；lark 后端为本地缓存+云端主库，以 sync 对齐）。`knowledge_base.md` 由脚本生成，禁止手改。
- 新增文献流程：追加 papers.json → `python scripts/score_paper.py` → 更新 topics.json 语义字段 → `python scripts/build_knowledge_base.py` → （lark）`sync_lark.py export` + 导入飞书。
- 知识库随 GitHub 仓库版本管理（默认库），跨会话复用；同一主题已被分析过就不要再分析一遍。
- 若使用者在自己的目录/飞书表维护库，其数据不属于仓库，不随 GitHub 同步——这正是"绑定人"的设计。

## 规则参考

- 评分细则：`references/scoring_rubric.md`
- 主题清单与关键词：`references/topics.md`
- 数据文件契约：`templates/papers.schema.json`、`templates/topics.schema.json`
- 数据文件：数据目录 `papers.json`、`topics.json`、`knowledge_base.md`
