# FitEvidence · 运动循证学习 Skill

帮助用户学习**运动营养学**与**运动康复**知识，核心机制：每条结论追溯原始文献，每篇文献经过一套自研双维审核规则（类影响因子）评分，过滤掉结论不合理/证据不足的流行说法。

**本 Skill 是"指南 + 模板"型**：它只装操作指南、数据文件契约与内置示例数据；真正积累的知识库属于每个使用者——存在你自己的本地目录，或你自己的飞书多维表格里。

## 它解决什么问题

运动领域充斥着结论互相矛盾的信息（"拉伸防伤"、"练后 30 分钟必须补蛋白"…）。很多说法被博主和商家反复传播，但追溯文献后证据并不支持。FitEvidence 用一套**可复算的评分规则**给文献和主题结论打分，让"该信什么"有据可依。

## 核心机制

```
首次使用 → 初始化数据存储（询问用户：飞书多维表格 / 本地目录 / 内置示例）
之后提问 → 主题归一化 → 查知识库（命中即复用，不重复分析）
        → 未命中 → 检索文献（系统综述/RCT 优先）→ 逐篇分析
        → 双维评分（证据真实度 × 生活影响度）→ 入库 → 输出学习卡片
```

**综合分 = 0.65 × 证据真实度(A) + 0.35 × 生活影响度(B)**

| 分级 | 含义 |
| --- | --- |
| ≥80 | 强证据·可执行 |
| 60-79 | 推荐·有条件 |
| 40-59 | 证据不足·存疑 |
| <40 | 不靠谱·勿轻信 |

维度 A（真实度）：研究设计 30% + 方法学质量 25% + 可重复性 20% + 发表渠道 15% + 时效性 10%
维度 B（影响度）：效应量 35% + 人群适用 25% + 可操作性 20% + 成本风险 20%

## 数据存哪里（可配置后端）

| 后端 | 数据在哪 | 谁拥有 | 适用 |
| --- | --- | --- | --- |
| `local`（默认） | 本地 JSON（skill 内 `data/` 或自选目录） | 使用者本人 | 离线、零依赖、隐私优先 |
| `lark` | **用户自己的飞书多维表格**（两张表：papers / topics） | 使用者本人 | 可被网页/其他 Agent 调用、跨设备、可协作 |

- 初始化：`python scripts/init_storage.py --backend local|--backend lark …`（详见 SKILL.md 第 0 步）
- 飞书后端通过 CSV 交换：`python scripts/sync_lark.py export` 导出 → 用 lark-base 导入飞书；飞书导出 CSV 放回 `import/` 目录 → `sync_lark.py import` 拉回本地。
- **别人使用时会怎样**：别人安装同一 Skill，数据引导落在**他自己的**飞书账号/目录——不会读到你的数据，也互不干扰。这正是"绑定人"的轻量数据库形态。
- 同类可扩展后端（进阶）：SeaTable（开源、可自托管、SQL 接口）、Airtable、Notion、Google Sheets 等，均可走同一套 CSV 交换协议接入。

## 知识库（一次分析，永久复用）

内置示例数据：`data/papers.json`（19 篇文献，全部可溯源）+ `data/topics.json`（6 主题结论）。同一主题被分析过就不再重复分析，直接输出结论卡。

| 主题 | 综合分 | 分级 |
| --- | --- | --- |
| 肌酸补剂 | 87 | 强证据·可执行 |
| 蛋白粉必要性 | 90 | 强证据·可执行 |
| 冰敷 vs 热敷 | 88 | 强证据·可执行 |
| 泡沫轴 | 88 | 强证据·可执行 |
| 合成代谢窗口 | 34 | 不靠谱·勿轻信 |
| 拉伸防伤 | 34 | 不靠谱·勿轻信 |

## 使用方式

作为 AI Agent Skill 加载后，直接提问即可，例如：
- "肌酸真的有用吗？给我看证据"
- "拉伸能防伤吗？"
- "练后必须 30 分钟内吃蛋白吗？"

## 目录结构

```
fit-evidence/
├── SKILL.md                      # Agent 工作流（初始化 + 7 步流程 + 输出模板）
├── storage.json                  # 存储后端配置（backend / data_dir / lark 表 ID）
├── scripts/
│   ├── init_storage.py           # 数据存储初始化（选择 local / lark）
│   ├── score_paper.py            # 双维加权评分（可复算）
│   ├── build_knowledge_base.py   # 知识库汇总 + Markdown 视图生成
│   ├── sync_lark.py              # 本地 JSON ↔ 飞书多维表格 CSV 交换
│   └── storage.py                # 公共存储配置模块
├── templates/
│   ├── papers.schema.json        # papers 表字段契约（飞书建表用）
│   ├── topics.schema.json        # topics 表字段契约
│   ├── papers.empty.json         # 空库模板
│   └── topics.empty.json
├── references/
│   ├── scoring_rubric.md         # 评分细则（权威定义）
│   └── topics.md                 # 主题清单与关键词归一化
├── data/                         # 内置示例数据（可复制为用户初始库）
│   ├── papers.json
│   └── topics.json
└── knowledge_base.md             # 人读视图（脚本生成，勿手改）
```

## 数据维护

1. 新增文献：追加到数据目录 `papers.json`
2. `python scripts/score_paper.py`（自动评分回填）
3. 更新 `topics.json` 语义字段（bottom_line / action_advice / keywords）
4. `python scripts/build_knowledge_base.py`（重算主题分 + 刷新视图）
5. lark 后端：`python scripts/sync_lark.py export` + 导入飞书，保持云端一致

## 设计参照

评分规则参考牛津 CEBM 证据等级与 GRADE 框架，并加入"生活影响度"维度——这是本项目区别于现成影响因子的核心：期刊影响因子只反映平均被引量，FitEvidence 逐篇评估"能不能信 + 值不值得做"。

## License

MIT
