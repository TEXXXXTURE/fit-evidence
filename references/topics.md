# FitEvidence 主题清单与归一化

本文件用于两件事：
1. Agent 把用户问题**归一化**到主题（第 1 节关键词表）；
2. 提供每个主题的当前结论摘要（第 2 节），快速预览知识库覆盖范围。

## 1. 主题关键词表（问题 → 主题 id）

| 主题 id | 主题（中文） | 触发关键词 |
| --- | --- | --- |
| creatine | 肌酸补剂 | 肌酸、creatine、增肌补剂、肌酸有用吗 |
| protein_supplement | 蛋白粉必要性 | 蛋白粉、蛋白质补剂、蛋白补充、乳清蛋白、蛋白粉有必要吗 |
| protein_timing | 合成代谢窗口 | 合成代谢窗口、蛋白时机、练后蛋白、练后30分钟、anabolic window、protein timing |
| stretching | 拉伸防伤 | 拉伸、stretching、拉伸防伤、拉伸缓解酸痛、肌肉酸痛、DOMS |
| cold_heat_therapy | 冰敷vs热敷 | 冰敷、热敷、冷水浸泡、冰浴、冷疗、热疗、酸痛冷敷、cold water immersion |
| foam_rolling | 泡沫轴 | 泡沫轴、foam rolling、筋膜放松、自我筋膜释放、恢复工具 |

归一化规则：
- 命中关键词表 → 查 `data/topics.json` 对应主题，命中即输出结论卡（**不重新分析文献**）。
- 未命中 → 按 SKILL.md 工作流新建主题：检索 → 分析 → 评分 → 入库，并同步把新关键词补充到本表。

## 2. 主题结论摘要（当前知识库状态）

| 主题 | 综合分 | 分级 | 一句话结论 |
| --- | --- | --- | --- |
| creatine 肌酸补剂 | 待 build 生成 | strong（预期） | 肌酸是证据最充分的补剂之一：增力量、增瘦体重，但女性/患者人群效果不显著 |
| protein_supplement 蛋白粉必要性 | 待 build 生成 | recommended（预期） | 蛋白补剂有增益但非必需：每日蛋白 ≥1.6g/kg 后额外补充无更多收益 |
| protein_timing 合成代谢窗口 | 待 build 生成 | uncertain（预期） | 证据反驳"30 分钟窗口"：总蛋白量比时机重要 |
| stretching 拉伸防伤 | 待 build 生成 | uncertain（预期） | 拉伸不防伤、不显著缓解酸痛：被广泛传播但证据不足的说法 |
| cold_heat_therapy 冰敷vs热敷 | 待 build 生成 | recommended（预期） | 冷/热疗都能缓解酸痛；时机有差异，孰优无定论；频繁冷疗或削弱增肌 |
| foam_rolling 泡沫轴 | 待 build 生成 | recommended（预期） | 泡沫轴小幅缓解酸痛、表现恢复小改善；"加速重建"证据不足 |

> 注：综合分/分级以 `scripts/build_knowledge_base.py` 运行结果为准，本节摘要仅供 Agent 快速预览，输出时必须引用 topics.json 的实时数值。
