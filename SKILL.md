---
name: fit-evidence
description: 运动营养学与运动康复的循证学习工具。当用户询问运动补剂（肌酸、蛋白粉）、训练营养（蛋白时机、合成代谢窗口）、运动恢复与康复（拉伸防伤、冰敷vs热敷、泡沫轴、肌肉酸痛/肌肉损伤）、以及任何"这个说法有没有文献支持/结论靠不靠谱/给我看证据"类问题时使用。工作方式：先查内置文献知识库（data/topics.json）命中即输出结论卡；未命中再检索文献、逐篇分析、按自研双维评分规则（证据真实度×生活影响度）评分入库。禁止凭印象回答运动营养/康复问题，必须引用可溯源文献。
---

# FitEvidence：运动循证知识助手

帮助用户学习运动营养学与运动康复知识，核心是"**每条结论都追溯到文献，每篇文献都过一遍审核规则**"。

## 工作流（按顺序执行）

### 第 1 步：主题归一化
- 用 `references/topics.md` 的关键词表把用户问题映射到主题 id。
- 命中主题 → 进入第 2 步查库；未命中 → 进入第 3 步新建主题。

### 第 2 步：查知识库（命中式复用，不重复分析）
- 读取 `data/topics.json`，找到对应主题记录。
- 有 `score_total` 与 `grade` → 直接输出主题结论卡（见输出模板），引用 `key_papers` 明细（从 `data/papers.json` 取）。
- 未命中或库中记录为空 → 进入第 3 步。
- 数据文件缺失时按第 3 步新建。

### 第 3 步：检索文献
- 检索优先顺序：系统综述 / Meta 分析 > 随机对照试验 > 队列研究 > 专家共识（Cochrane、PubMed/PMC、权威期刊官网）。
- 每个主题至少收集 2-3 篇可溯源文献（真实 URL，禁止二手转述替代原文）。
- 同时注意收集**边界/反驳**文献（亚组无效、阴性结果），防止结论过度乐观。

### 第 4 步：逐篇分析
- 按 `references/scoring_rubric.md` 第 5 节字段逐篇填写分析（design / method_quality / venue / reproducibility / recency_years / effect_size / applicability / actionability / cost_risk / population / intervention / outcome / limitations / conclusion）。
- 把新文献追加到 `data/papers.json` 的 `papers` 数组。

### 第 5 步：评分（机器计算，保证可复算）
```bash
python scripts/score_paper.py --file data/papers.json
```
- 脚本按 综合分 = 0.65×证据真实度(A) + 0.35×生活影响度(B) 回填每篇的 score_A / score_B / score_total / grade。
- 分级：strong(≥80) / recommended(60-79) / uncertain(40-59) / unreliable(<40)。

### 第 6 步：入库并刷新视图
- 更新 `data/topics.json` 对应主题的语义字段（bottom_line / action_advice / keywords），数值部分交给脚本：
```bash
python scripts/build_knowledge_base.py
```
- 脚本按主题"主张方向"重算主题综合分（positive=文献总分均值；negative=100-均值，高质量反面证据=说法越不可信），刷新 `key_papers`、生成人读视图 `knowledge_base.md`。

### 第 7 步：输出学习卡片
按下方模板输出；未命中新主题时同步在 `references/topics.md` 补充关键词。

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
- 必须把"边界条件"（如女性/患者无效、阴性结果）写进结论，不得用总体结论掩盖亚组差异。

## 数据维护约定
- `data/papers.json` 与 `data/topics.json` 是**唯一数据源**；`knowledge_base.md` 由脚本生成，禁止手改。
- 新增文献流程：追加 papers.json → 运行 score_paper.py → 更新 topics.json 语义字段 → 运行 build_knowledge_base.py。
- 知识库随仓库版本管理，跨会话复用；同一主题已被分析过就不要再分析一遍。

## 规则参考
- 评分细则：`references/scoring_rubric.md`
- 主题清单与关键词：`references/topics.md`
- 数据文件：`data/papers.json`、`data/topics.json`、`knowledge_base.md`
