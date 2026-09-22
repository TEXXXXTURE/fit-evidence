#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FitEvidence build_knowledge_base.py
从 data/papers.json 汇总生成:
  1) data/topics.json 的自动数值部分（主题综合分=该主题文献总分均值、分级、key_papers、updated_at；
     语义字段 bottom_line / action_advice 由人工/Agent 维护，脚本只更新数值，不覆盖语义）
  2) knowledge_base.md 人读视图（主题结论总览 + 文献明细表）

用法:
  python build_knowledge_base.py [--skill-dir <FitEvidence 目录>]
"""

import argparse
import json
import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import storage  # noqa: E402

GRADE_LABEL = {
    "strong": "强证据·可执行",
    "recommended": "推荐·有条件",
    "uncertain": "证据不足·存疑",
    "unreliable": "不靠谱·勿轻信",
}
GRADE_ORDER = {"strong": 0, "recommended": 1, "uncertain": 2, "unreliable": 3}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def dump_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def build(skill_dir, data_dir=None):
    data_dir = data_dir or storage.resolve_data_dir(skill_dir)
    papers_path = os.path.join(data_dir, "papers.json")
    topics_path = os.path.join(data_dir, "topics.json")
    # 人读视图写到"数据目录的上一级"，保证任何后端位置下都能找到
    view_path = os.path.join(os.path.dirname(os.path.abspath(data_dir)), "knowledge_base.md")

    papers_data = load_json(papers_path)
    papers = papers_data["papers"] if isinstance(papers_data, dict) else papers_data
    topics_data = load_json(topics_path)
    topics = topics_data["topics"] if isinstance(topics_data, dict) else topics_data

    today = datetime.date.today().isoformat()

    by_topic = {}
    for p in papers:
        by_topic.setdefault(p.get("topic", "other"), []).append(p)

    for t in topics:
        tid = t["id"]
        t_papers = by_topic.get(tid, [])
        if t_papers:
            totals = [p.get("score_total", 0) for p in t_papers]
            mean = round(sum(totals) / len(totals))
            # 主张方向：positive=主题主张成立（分越高越可信）；
            # negative=主题主张是神话/被高质量证据反驳（高质量反面证据 -> 分越低越不可信）。
            direction = str(t.get("claim_direction", "positive")).strip().lower()
            score = mean if direction == "positive" else 100 - mean
            t["score_total"] = score
            t["grade"] = _grade_from_total(score)
            t["key_papers"] = [p["id"] for p in t_papers]
        else:
            t["score_total"] = 0
            t["grade"] = ""
            t["key_papers"] = []
        t["updated_at"] = today

    dump_json(topics_path, topics_data)

    # ---- 生成人读视图 ----
    lines = []
    lines.append("# FitEvidence 知识库（自动生成，勿手改）")
    lines.append("")
    lines.append("> 由 `scripts/build_knowledge_base.py` 生成 · 更新于 {0}".format(today))
    lines.append("> 评分口径：综合分 = 0.65×证据真实度(A) + 0.35×生活影响度(B)，详见 references/scoring_rubric.md")
    lines.append("")
    lines.append("## 一、主题结论总览")
    lines.append("")
    lines.append("| 主题 | 方向 | 问题 | 综合分 | 分级 | 一句话结论 |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for t in sorted(topics, key=lambda x: GRADE_ORDER.get(x.get("grade", "unreliable"), 9)):
        g = GRADE_LABEL.get(t.get("grade", ""), t.get("grade", "-"))
        direction_label = "正向主张" if str(t.get("claim_direction", "positive")).strip().lower() != "negative" else "反面主张(神话)"
        lines.append("| {0} | {1} | {2} | {3} | {4} | {5} |".format(
            t.get("topic_zh", t["id"]), direction_label, t.get("question", ""),
            t.get("score_total", 0), g, t.get("bottom_line", "").replace("|", "/")))
    lines.append("")

    lines.append("## 二、文献明细")
    lines.append("")
    for t in topics:
        t_papers = by_topic.get(t["id"], [])
        if not t_papers:
            continue
        lines.append("### {0}（{1}）".format(t.get("topic_zh", t["id"]), t["id"]))
        lines.append("")
        lines.append("| 文献 | 设计 | 年份 | A真实度 | B影响度 | 综合 | 分级 | 结论 | 局限 |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for p in sorted(t_papers, key=lambda x: x.get("score_total", 0), reverse=True):
            g = GRADE_LABEL.get(p.get("grade", ""), p.get("grade", "-"))
            lines.append("| {0} | {1} | {2} | {3} | {4} | {5} | {6} | {7} | {8} |".format(
                "[{0}]({1})".format(p.get("title", p.get("id", "?")), p.get("url", "")),
                p.get("design", ""), p.get("year", ""),
                p.get("score_A", ""), p.get("score_B", ""), p.get("score_total", ""),
                g, p.get("conclusion", "").replace("|", "/"),
                "; ".join(p.get("limitations", [])).replace("|", "/")))
        lines.append("")

    with open(view_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("已更新 topics.json（{0} 个主题）并生成 {1}".format(len(topics), view_path))


def _grade_from_total(total):
    if total >= 80:
        return "strong"
    if total >= 60:
        return "recommended"
    if total >= 40:
        return "uncertain"
    return "unreliable"


def main():
    ap = argparse.ArgumentParser(description="FitEvidence 知识库生成")
    ap.add_argument("--skill-dir", default=None, help="FitEvidence skill 目录（默认自动定位到本脚本上级）")
    ap.add_argument("--data-dir", default=None, help="数据目录（缺省按 storage.json 解析，local 默认 skill 内 data/）")
    args = ap.parse_args()
    skill_dir = args.skill_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    build(skill_dir, args.data_dir)


if __name__ == "__main__":
    main()
