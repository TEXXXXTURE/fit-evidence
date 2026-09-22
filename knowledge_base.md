# FitEvidence 知识库（自动生成，勿手改）

> 由 `scripts/build_knowledge_base.py` 生成 · 更新于 2026-09-22
> 评分口径：综合分 = 0.65×证据真实度(A) + 0.35×生活影响度(B)，详见 references/scoring_rubric.md

## 一、主题结论总览

| 主题 | 方向 | 问题 | 综合分 | 分级 | 一句话结论 |
| --- | --- | --- | --- | --- | --- |
| 肌酸补剂 | 正向主张 | 肌酸真的能增肌吗？值得吃吗？ | 87 | 强证据·可执行 | 肌酸是目前证据最充分的运动补剂之一：联合抗阻训练可显著提升力量与瘦体重，多数健康成人安全有效。但收益存在人群边界——女性与疾病人群（如癌症患者）未观察到显著效果，不能无差别宣传。 |
| 蛋白粉必要性 | 正向主张 | 蛋白粉是必须的吗？不喝蛋白粉会少长肌肉吗？ | 90 | 强证据·可执行 | 蛋白补剂能小幅增强抗阻训练的肌肉与力量增益，但前提是日常饮食蛋白不足；当每日蛋白达到约 1.6g/kg 后，额外补充不再增加收益。饮食能吃够蛋白时，蛋白粉并非必需品——其必要性常被营销夸大。 |
| 冰敷vs热敷 | 正向主张 | 运动后酸痛该冰敷还是热敷？ | 88 | 强证据·可执行 | 冷疗（冷水浸泡/冰敷）与热疗（热敷包）均能缓解运动后酸痛，证据等级中等；时机存在差异：24h 内热敷包止痛评分最高、冷水浸泡亦有效，48h 后冷冻疗法排名上升。冷热孰优尚无定论；且频繁冷疗可能削弱长期增肌适应，需权衡。 |
| 泡沫轴 | 正向主张 | 泡沫轴有用吗？能加速恢复吗？ | 88 | 强证据·可执行 | 证据中等：泡沫轴能小幅减轻运动后主观酸痛（24-72h），并带来小幅表现恢复改善；但“加速肌肉重建/机制性恢复”证据不足。性价比高、风险低，可作为酸痛管理工具。 |
| 合成代谢窗口 | 反面主张(神话) | 练后 30 分钟内必须吃蛋白吗？错过窗口会白练吗？ | 34 | 不靠谱·勿轻信 | 证据明确反驳“30 分钟合成代谢窗口”神话：控制总蛋白摄入后，训练前后的蛋白时机对增肌无显著影响；关键是全天总蛋白足够。 |
| 拉伸防伤 | 反面主张(神话) | 拉伸能预防运动损伤或缓解酸痛吗？ | 34 | 不靠谱·勿轻信 | 高质量系统综述（含 Cochrane）与国际专家共识一致：拉伸对减轻运动后肌肉酸痛无临床意义，对预防全因损伤无明显效果。“拉伸防伤”是被广泛传播但证据不足的说法。 |

## 二、文献明细

### 肌酸补剂（creatine）

| 文献 | 设计 | 年份 | A真实度 | B影响度 | 综合 | 分级 | 结论 | 局限 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Effects of Creatine Supplementation and Resistance Training on Muscle Strength Gains in Adults <50 Years of Age: A Systematic Review and Meta-Analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC11547435/) | systematic_review_meta_analysis | 2024 | 95 | 91 | 94 | 强证据·可执行 | 肌酸联合抗阻训练在 <50 岁成人中带来比单纯训练更大的上下肢力量增益；男性效果显著，女性未达显著。 | 女性亚组未观察到显著力量改善; 多数受试者已有训练基础，新手外推需谨慎 |
| [Creatine supplementation and resistance training: a comparison between novice and experienced lifters - a systematic review and dose-response meta-analysis](https://www.tandfonline.com/doi/pdf/10.1080/15502783.2025.2586523) | systematic_review_meta_analysis | 2025 | 95 | 91 | 94 | 强证据·可执行 | 汇总 61 项试验：肌酸显著增加 FFM +1.39kg（95%CI 1.07-1.70）与体重 +0.89kg，新手获益大于有经验者。 | 存在发表偏倚可能; 剂量-反应模型存在一定异质性 |
| [Performance-Enhancing Drugs in Healthy Athletes: An Umbrella Review of Systematic Reviews and Meta-analyses](https://pmc.ncbi.nlm.nih.gov/articles/PMC11346223/) | meta_analysis | 2024 | 92 | 91 | 92 | 强证据·可执行 | 伞形综述确认：肌酸在抗阻训练期间可安全增加总/瘦体重与力量，改善高强度短时表现；对脂肪量无影响。 | 伞形综述覆盖多种补剂，肌酸条目为汇总结论; 长期安全性证据仍有限 |
| [Creatine Supplementation in Patients With Cancer: A Systematic Review and Meta-Analysis](https://onlinelibrary.wiley.com/doi/10.1002/rco2.70044) | systematic_review_meta_analysis | 2026 | 93 | 20 | 67 | 推荐·有条件 | 在癌症患者中未观察到肌酸对肌肉力量的显著效果（SMD -0.05, p=0.65）——提示肌酸收益存在明确的人群边界。 | 仅纳入 5 项研究; 患者人群异质性大; 样本量小 |

### 蛋白粉必要性（protein_supplement）

| 文献 | 设计 | 年份 | A真实度 | B影响度 | 综合 | 分级 | 结论 | 局限 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [A systematic review, meta-analysis and meta-regression of the effect of protein supplementation on resistance training-induced gains in muscle mass and strength in healthy adults](https://pubmed.ncbi.nlm.nih.gov/28698222/) | systematic_review_meta_analysis | 2017 | 94 | 91 | 93 | 强证据·可执行 | 蛋白补剂显著增强长期抗阻训练的力量与肌肉增益；但年龄越大效果越低、训练经验越多效果越高，且蛋白摄入 >1.6g/kg/天 后不再额外增加 FFM。 | 多数研究为补剂 vs 安慰剂设计，可能高估补剂的必要性; 2017 年发表，时效性一般 |
| [Systematic review and meta-analysis of protein intake to support muscle mass and function in healthy adults](https://pmc.ncbi.nlm.nih.gov/articles/PMC8978023/) | systematic_review_meta_analysis | 2022 | 93 | 82 | 89 | 强证据·可执行 | 增加每日蛋白摄入仅带来 LBM 与下肢力量的小幅额外增益——蛋白补剂的作用被营销严重夸大。 | 效应量小; 对握力效果不明确，功能表现影响甚微 |
| [Which Protein-Based Dietary Supplements Most Effectively Enhance Fat-Free Mass and Strength Gains in Healthy Adults Undergoing Resistance Training? A Network Meta-Analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC12862422/) | meta_analysis | 2026 | 93 | 82 | 89 | 强证据·可执行 | 网络 Meta 分析显示乳清与胶原蛋白是仅有的对增肌/力量有效的蛋白补剂，其余蛋白源无显著差异。 | 网络分析以间接比较为主; 效应量小 |

### 合成代谢窗口（protein_timing）

| 文献 | 设计 | 年份 | A真实度 | B影响度 | 综合 | 分级 | 结论 | 局限 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Does Protein Ingestion Timing Affect Exercise-Induced Adaptations? A Systematic Review with Meta-Analysis](https://pubmed.ncbi.nlm.nih.gov/40647175/) | systematic_review_meta_analysis | 2025 | 94 | 20 | 68 | 推荐·有条件 | 蛋白摄入时机不显著改变训练诱导的瘦体重变化；上下肢力量可能反应不同，需更多研究。再次否定“练后 30 分钟必须补蛋白”。 | 腿举一项亚组分析提示练前略优（2 研究 53 人，亚组交互 p=0.07 不显著）; 上下肢力量反应差异证据不足 |
| [The effect of protein timing on muscle strength and hypertrophy: a meta-analysis](https://consensus.app/questions/protein-supplementation-timing/) | meta_analysis | 2013 | 88 | 20 | 64 | 推荐·有条件 | 控制总蛋白摄入后，训练前后的蛋白时机对力量与肥大无显著影响；总蛋白摄入是效应量最强预测因子，反驳“30 分钟合成代谢窗口”。 | 2013 年发表，时效性弱; 纳入研究多为补剂 vs 安慰剂且总蛋白未匹配（Beale 评论指出） |

### 拉伸防伤（stretching）

| 文献 | 设计 | 年份 | A真实度 | B影响度 | 综合 | 分级 | 结论 | 局限 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Stretching to prevent or reduce muscle soreness after exercise（Cochrane 系统综述）](https://www.cochrane.org/zh-hant/evidence/CD004577_stretching-prevent-or-reduce-muscle-soreness-after-exercise) | systematic_review_meta_analysis | 2011 | 92 | 20 | 67 | 推荐·有条件 | 随机试验证据显示：拉伸（无论训练前、后或前后）对健康成人运动后肌肉酸痛的减轻不具临床重要性。 | 部分原始研究质量中等; 主要结局为酸痛而非损伤发生率（防伤结论需另看） |
| [Exercise Programs to Reduce the Risk of Musculoskeletal Injuries in Military Personnel: A Systematic Review and Meta-Analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC7586796/) | systematic_review_meta_analysis | 2020 | 91 | 20 | 66 | 推荐·有条件 | 低质量证据显示静态拉伸不降低肌肉骨骼损伤风险——拉伸作为“防伤手段”缺乏支持。 | 人群为军事人员，外推需谨慎; GRADE 评估为低质量证据 |
| [Practical recommendations on stretching exercise: A Delphi consensus statement of international research experts](https://pmc.ncbi.nlm.nih.gov/articles/PMC12305623/) | guideline_consensus | 2026 | 90 | 20 | 65 | 推荐·有条件 | 国际专家共识：多数系统综述不支持拉伸对全因损伤的预防效果；“拉伸防伤”属于被高估的常见说法。 | 共识性质（非定量证据）; 最新综述提示拉伸降低肌肉损伤风险但伴随骨/关节损伤风险升高 |

### 冰敷vs热敷（cold_heat_therapy）

| 文献 | 设计 | 年份 | A真实度 | B影响度 | 综合 | 分级 | 结论 | 局限 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Cold-water immersion for preventing and treating muscle soreness after exercise（Cochrane 系统综述）](https://www.cochrane.org/ru/evidence/CD008262_cold-water-immersion-preventing-and-treating-muscle-soreness-after-exercise) | systematic_review_meta_analysis | 2012 | 92 | 91 | 92 | 强证据·可执行 | 冷水浸泡显著减轻运动后 24h（SMD -0.55）与 48h（SMD -0.66）的肌肉酸痛。 | 原始研究异质性较高; 2012 年发表，时效性弱 |
| [Impact of different doses of cold water immersion (duration and temperature variations) on recovery from acute exercise-induced muscle damage: a network meta-analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC11897523/) | meta_analysis | 2026 | 92 | 91 | 92 | 强证据·可执行 | 10-15min/11-15°C 的冷水浸泡对减轻肌肉酸痛最有效；10-15min/5-10°C 对生化指标（CK）恢复最有效。 | 网络分析以间接证据为主; 频繁冷疗可能削弱长期增肌适应，需另行权衡 |
| [Heat and cold therapy reduce pain in patients with delayed onset muscle soreness: A systematic review and meta-analysis of 32 randomized controlled trials](https://pubmed.ncbi.nlm.nih.gov/33493991/) | systematic_review_meta_analysis | 2021 | 83 | 91 | 86 | 强证据·可执行 | 冷、热疗法在运动后 1h 内应用均能有效减轻 DOMS 疼痛 24h；热敷包与冷水浸泡效果最好，冷热孰优尚无定论。 | 需更多高质量研究确定冷热孰优; 效应依赖应用时机（1h 内最佳） |
| [Effect of cold and heat therapies on pain relief in patients with delayed onset muscle soreness: A network meta-analysis](https://pubmed.ncbi.nlm.nih.gov/34636405/) | meta_analysis | 2021 | 81 | 91 | 84 | 强证据·可执行 | 运动后 24h 内热敷包止痛最有效，其次交替水疗；48h 内热敷包仍居首，48h 后冷冻疗法排名升至第一。 | 纳入研究质量有限; 结论等级中等以下 |

### 泡沫轴（foam_rolling）

| 文献 | 设计 | 年份 | A真实度 | B影响度 | 综合 | 分级 | 结论 | 局限 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Preventive effect of foam rolling on muscle soreness after exercise: A systematic review and meta-analysis](https://pubmed.ncbi.nlm.nih.gov/39593540/) | systematic_review_meta_analysis | 2024 | 93 | 82 | 89 | 强证据·可执行 | 泡沫轴对运动后肌肉酸痛有一定缓解作用（SMD -0.38），但幅度有限。 | 效应量小; 多数研究仅覆盖短期观察 |
| [Effect of Self-Myofascial Release with Foam Rolling on Delayed Onset Muscle Soreness (DOMS): A Systematic Review](https://revistamentor.ec/index.php/mentor/article/view/10758/11033) | systematic_review_meta_analysis | 2026 | 92 | 82 | 88 | 强证据·可执行 | 2020-2025 年文献显示泡沫轴自我筋膜放松在运动后 48-72h 显著减轻 DOMS，与既有 Meta 分析一致。 | 仅纳入 5 项实验研究，样本量小; 期刊影响力一般 |
| [A Meta-Analysis of the Effects of Foam Rolling on Performance and Recovery](https://scispace.com/pdf/a-meta-analysis-of-the-effects-of-foam-rolling-on-2uwja4ym57.pdf) | meta_analysis | 2019 | 90 | 82 | 87 | 强证据·可执行 | 泡沫轴小幅减轻肌肉疼痛感知（g≈0.47），对冲刺与力量恢复有小幅改善，但“加速肌肉重建”证据不足。 | 表现改善幅度小（冲刺 +3.1%、力量 +3.9%）; 对跳跃表现影响可忽略; 作用机制不清 |
