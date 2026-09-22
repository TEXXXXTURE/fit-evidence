# FitEvidence 评分细则（Scoring Rubric）

本文件是自研文献审核规则（类影响因子）的唯一权威定义。Agent 在分析文献时严格按本细则填写评分输入字段，再由 `scripts/score_paper.py` 统一计算，保证评分可复算、口径一致。

## 1. 综合评分公式

```
综合分 = 0.65 × 证据真实度(A) + 0.35 × 生活影响度(B)
```

## 2. 维度 A：证据真实度（0-100）

| 子项 | 权重 | 评分要点 |
| --- | --- | --- |
| 研究设计 | 30% | 证据等级越高分越高（见下表） |
| 方法学质量 | 25% | 随机化/盲法/对照/样本量/流失率/统计方法/异质性 I²，由分析者按 0-100 人工评估 |
| 发表渠道 | 15% | 同行评审期刊 > 预印本 > 非审平台 |
| 可重复性 | 20% | 多项独立研究一致 > 单篇 > 结论被反驳 |
| 时效性 | 10% | 距发表 ≤3 年 100 分，≤5 年 90 分，≤10 年 70 分，更早 50 分（经典文献可在分析中注明豁免） |

### 2.1 研究设计分值映射（design 字段）

| 值 | 分值 | 含义 |
| --- | --- | --- |
| systematic_review_meta_analysis | 100 | RCT/队列的系统综述 + Meta 分析（最高级） |
| meta_analysis | 95 | 普通 Meta 分析 / 网络 Meta 分析 |
| guideline_consensus | 90 | 专家共识 / Delphi 声明 |
| rct | 85 | 单一随机对照试验 |
| quasi_experimental | 65 | 准实验 / 非随机对照 |
| cohort | 55 | 队列研究 |
| cross_sectional | 35 | 横断面 / 相关性研究 |
| narrative_review | 30 | 叙述性综述 |
| case_series | 20 | 病例系列 / 个案 |
| expert_opinion | 10 | 专家意见 / 机制推测 |

### 2.2 其他子项分值映射

| venue（渠道） | 分值 | reproducibility（可重复性） | 分值 |
| --- | --- | --- | --- |
| peer_reviewed_top（顶级期刊/Cochrane） | 100 | consistent（多篇一致+被引用） | 100 |
| peer_reviewed | 85 | single（单篇支持） | 60 |
| preprint | 60 | mixed（部分一致/亚组差异） | 50 |
| non_reviewed | 20 | contradicted（被反驳） | 30 |

## 3. 维度 B：生活影响度（0-100）

| 子项 | 权重 | 评分要点 |
| --- | --- | --- |
| 效应量/临床意义 | 35% | 效应是否大到值得改变生活方式 |
| 人群适用性 | 25% | 普通人能否直接执行 |
| 可操作性 | 20% | 是否有明确剂量/频率/动作建议 |
| 成本与风险 | 20% | 是否安全、便宜、低门槛 |

### 3.1 分值映射

| effect_size | 分值 | applicability | 分值 | actionability | 分值 | cost_risk | 分值 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| large | 100 | general | 100 | clear | 100 | low | 100 |
| moderate | 75 | partial | 70 | vague | 70 | medium | 70 |
| small | 50 | specific | 40 | unclear | 40 | high | 30 |
| minimal | 20 | | | | | | |
| none | 0 | | | | | | |

## 4. 结论分级

| 综合分 | grade | 含义 |
| --- | --- | --- |
| ≥80 | strong | 强证据·可执行 |
| 60-79 | recommended | 推荐·有条件 |
| 40-59 | uncertain | 证据不足·存疑 |
| <40 | unreliable | 不靠谱·勿轻信 |

## 5. 评分输入字段（Agent 分析每篇文献必须填写）

| 字段 | 说明 | 取值示例 |
| --- | --- | --- |
| design | 研究设计 | systematic_review_meta_analysis |
| method_quality | 方法学质量人工评估 | 0-100 |
| venue | 发表渠道 | peer_reviewed / peer_reviewed_top |
| reproducibility | 可重复性 | consistent / single / mixed / contradicted |
| recency_years | 距今年数 | 2 |
| effect_size | 效应量 | large / moderate / small / minimal / none |
| applicability | 人群适用性 | general / partial / specific |
| actionability | 可操作性 | clear / vague / unclear |
| cost_risk | 成本与风险 | low / medium / high |

## 6. 注意事项

- **阴性结果也要评分**：设计再好的研究若结论为"无效果"，A 维度仍按质量给分，但 B 维度（效应量 none）会拉低综合分，从而得到"证据充分但结论是不建议做"的正确输出。
- **人群边界必须在结论中写明**（如"女性亚组无显著效果"），不得用总体结论掩盖亚组差异。
- **引用必须可溯源**：每条文献记录必须带真实 URL（PubMed/PMC/Cochrane/期刊官网），禁止二手转述替代原文。
- 未知/缺失字段按 50 分中性处理，并在分析中注明缺口。
