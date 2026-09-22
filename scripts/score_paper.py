#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FitEvidence score_paper.py
按双维加权审核规则给文献打分：
  证据真实度 A（权重 0.65） × 生活影响度 B（权重 0.35） -> 综合分 0-100
  分级：>=80 strong(强证据·可执行) / 60-79 recommended(推荐·有条件)
        40-59 uncertain(证据不足·存疑) / <40 unreliable(不靠谱·勿轻信)

用法:
  python score_paper.py <analysis.json>            # 单篇评分，输出 JSON
  python score_paper.py --file <papers.json>       # 批量：为 papers.json 全部文献回填 score 字段
"""

import argparse
import json
import sys

# ---- 权重常量 ----
WEIGHTS_A = {"design": 0.30, "method": 0.25, "venue": 0.15, "repro": 0.20, "recency": 0.10}
WEIGHTS_B = {"effect": 0.35, "applicability": 0.25, "actionability": 0.20, "cost_risk": 0.20}
W_A, W_B = 0.65, 0.35

# ---- 枚举 -> 0-100 分值映射 ----
DESIGN_SCORE = {
    "systematic_review_meta_analysis": 100,  # RCT/队列的系统综述+Meta 分析
    "meta_analysis": 95,                     # 普通 Meta 分析
    "rct": 85,                               # 单一随机对照试验
    "guideline_consensus": 90,               # 专家共识/Delphi 声明
    "quasi_experimental": 65,                # 准实验/非随机对照
    "cohort": 55,                            # 队列研究
    "cross_sectional": 35,                   # 横断面/相关性研究
    "narrative_review": 30,                  # 叙述性综述
    "case_series": 20,                       # 病例系列/个案
    "expert_opinion": 10,                    # 专家意见/机制推测
}
VENUE_SCORE = {
    "peer_reviewed_top": 100,   # 顶级同行评审期刊（如 BMJ、Sports Med、Cochrane 库）
    "peer_reviewed": 85,        # 普通同行评审期刊
    "preprint": 60,             # 预印本
    "non_reviewed": 20,         # 非审稿平台/自媒体/商业网站
}
REPRO_SCORE = {
    "consistent": 100,   # 多项独立研究结论一致，被广泛引用
    "mixed": 50,         # 结论部分一致/有亚组差异
    "single": 60,        # 单篇支持，未见独立验证
    "contradicted": 30,  # 后续研究反驳
}
EFFECT_SCORE = {
    "large": 100,    # 效应大，足以显著改变结果/生活
    "moderate": 75,  # 效应中等，肉眼可见收益
    "small": 50,     # 效应小，真实但幅度有限
    "minimal": 20,   # 效应微乎其微，临床意义不足
    "none": 0,       # 无效应/阴性结果
}
APPLICABILITY_SCORE = {
    "general": 100,   # 普通人群可直接执行
    "partial": 70,    # 仅部分人群（如训练者/特定年龄）
    "specific": 40,   # 仅特定人群（如患者/运动员）
}
ACTIONABILITY_SCORE = {
    "clear": 100,   # 有明确剂量/频率/动作建议
    "vague": 70,    # 大致建议，无精确参数
    "unclear": 40,  # 无法转化为行动
}
COST_RISK_SCORE = {
    "low": 100,    # 低成本、低风险、普遍可得
    "medium": 70,  # 中等成本或一定风险/门槛
    "high": 30,    # 高成本、高风险或需专业监护
}


def _lookup(mapping, key, fallback=50):
    """安全查映射表；缺省/未知值给 50 分（中性）。"""
    if key is None:
        return fallback
    return mapping.get(str(key).strip().lower(), fallback)


def recency_score(years):
    """时效性：发表至今 <=3 年 100 分；<=5 年 90；<=10 年 70；更早 50（经典文献可在分析中人工豁免）。"""
    try:
        years = float(years)
    except (TypeError, ValueError):
        return 70
    if years <= 3:
        return 100
    if years <= 5:
        return 90
    if years <= 10:
        return 70
    return 50


def score_paper(p):
    """p: 含评分输入字段的文献 dict。返回评分结果 dict（不修改原 dict）。"""
    # 维度 A：证据真实度
    a_design = _lookup(DESIGN_SCORE, p.get("design"))
    a_method = float(p.get("method_quality", 50))
    a_venue = _lookup(VENUE_SCORE, p.get("venue"))
    a_repro = _lookup(REPRO_SCORE, p.get("reproducibility"))
    a_recency = recency_score(p.get("recency_years"))
    A = (WEIGHTS_A["design"] * a_design
         + WEIGHTS_A["method"] * a_method
         + WEIGHTS_A["venue"] * a_venue
         + WEIGHTS_A["repro"] * a_repro
         + WEIGHTS_A["recency"] * a_recency)

    # 维度 B：生活影响度
    b_effect = _lookup(EFFECT_SCORE, p.get("effect_size"))
    b_applic = _lookup(APPLICABILITY_SCORE, p.get("applicability"))
    b_action = _lookup(ACTIONABILITY_SCORE, p.get("actionability"))
    b_cost = _lookup(COST_RISK_SCORE, p.get("cost_risk"))
    B = (WEIGHTS_B["effect"] * b_effect
         + WEIGHTS_B["applicability"] * b_applic
         + WEIGHTS_B["actionability"] * b_action
         + WEIGHTS_B["cost_risk"] * b_cost)
    # 阴性结论（无效应）对生活无实质影响：B 维度强制低分，
    # 避免"方法学好但结论为无效果"的文献被算成高分。
    if str(p.get("effect_size", "")).strip().lower() == "none":
        B = 20.0

    total = round(W_A * A + W_B * B)
    return {
        "score_A": round(A),
        "score_B": round(B),
        "score_total": total,
        "grade": grade(total),
    }


def grade(total):
    if total >= 80:
        return "strong"
    if total >= 60:
        return "recommended"
    if total >= 40:
        return "uncertain"
    return "unreliable"


def _load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _dump_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def main():
    ap = argparse.ArgumentParser(description="FitEvidence 文献双维评分")
    ap.add_argument("input", nargs="?", help="单篇分析 JSON 文件路径")
    ap.add_argument("--file", help="批量模式：papers.json 路径，为每篇回填评分字段")
    args = ap.parse_args()

    if args.file:
        path = args.file
        data = _load_json(path)
        papers = data["papers"] if isinstance(data, dict) and "papers" in data else data
        for p in papers:
            s = score_paper(p)
            p.update(s)
            print("{0} [{1}] A={2} B={3} total={4} grade={5}".format(
                p.get("id", "?"), p.get("topic", "?"),
                s["score_A"], s["score_B"], s["score_total"], s["grade"]))
        _dump_json(path, data)
        print("已回填评分 -> {0}（{1} 篇）".format(path, len(papers)))
        return

    if args.input:
        p = _load_json(args.input)
        s = score_paper(p)
        print(json.dumps(s, ensure_ascii=False, indent=2))
        return

    ap.print_help()


if __name__ == "__main__":
    main()
