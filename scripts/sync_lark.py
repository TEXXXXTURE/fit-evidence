#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FitEvidence sync_lark.py —— 本地 JSON 与飞书多维表格之间的数据交换

设计：脚本不直接持有飞书凭证，改用"CSV 交换"方式——
  export: 本地 papers.json/topics.json -> <data_dir>/import/papers.import.csv / topics.import.csv
           （表头=飞书表字段名，Agent 用 lark-base 能力把 CSV 导入飞书多维表格）
  import: 飞书导出的 CSV（放到 <data_dir>/import/）-> 合并回 papers.json / topics.json

用法:
  python scripts/sync_lark.py export [--data-dir <dir>]
  python scripts/sync_lark.py import [--data-dir <dir>]

字段契约见 templates/*.schema.json；list 字段在 CSV 中用 "|" 分隔（limitations、keywords、key_papers）。
"""

import argparse
import csv
import json
import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import storage  # noqa: E402

LIST_FIELDS = {
    "papers": {"limitations"},
    "topics": {"keywords", "key_papers"},
}
NUM_FIELDS = {
    "papers": {"year", "method_quality", "recency_years", "score_A", "score_B", "score_total"},
    "topics": {"score_total"},
}


def _import_dir(data_dir):
    d = os.path.join(data_dir, "import")
    os.makedirs(d, exist_ok=True)
    return d


def _row_from_paper(p):
    row = dict(p)
    row["limitations"] = "|".join(p.get("limitations", []))
    return row


def _row_from_topic(t):
    row = dict(t)
    for f in ("keywords", "key_papers"):
        if isinstance(t.get(f), list):
            row[f] = "|".join(str(x) for x in t[f])
    return row


def export(data_dir):
    imp = _import_dir(data_dir)
    wrote = []

    pp = storage.papers_path(data_dir)
    if os.path.exists(pp):
        data = storage.load_json(pp)
        papers = data.get("papers", [])
        fields = sorted({k for p in papers for k in _row_from_paper(p).keys()})
        out = os.path.join(imp, "papers.import.csv")
        with open(out, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for p in papers:
                w.writerow(_row_from_paper(p))
        wrote.append((out, len(papers)))

    tp = storage.topics_path(data_dir)
    if os.path.exists(tp):
        data = storage.load_json(tp)
        topics = data.get("topics", [])
        fields = sorted({k for t in topics for k in _row_from_topic(t).keys()})
        out = os.path.join(imp, "topics.import.csv")
        with open(out, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for t in topics:
                w.writerow(_row_from_topic(t))
        wrote.append((out, len(topics)))

    if not wrote:
        print("未找到数据文件，请先运行 scripts/init_storage.py 初始化。")
        return
    for path, n in wrote:
        print("已导出 {0} 条 -> {1}".format(n, path))
    print("下一步：用 lark-base 能力把这两份 CSV 导入用户的飞书多维表格（papers 表 / topics 表）。")


def _coerce(row, kind):
    """CSV 行 -> JSON 值（list 用 | 分隔还原；数字字段转 int）。"""
    out = {}
    for k, v in row.items():
        if v is None or v == "":
            continue
        if k in LIST_FIELDS.get(kind, set()):
            out[k] = [x.strip() for x in v.split("|") if x.strip()]
        elif k in NUM_FIELDS.get(kind, set()):
            try:
                out[k] = int(float(v))
            except ValueError:
                out[k] = v
        else:
            out[k] = v
    return out


def import_csv(data_dir, kind):
    imp = _import_dir(data_dir)
    path = os.path.join(imp, "{0}.import.csv".format(kind))
    if not os.path.exists(path):
        print("未找到 {0}，请先放入飞书导出的 CSV（或运行 export 生成模板）。".format(path))
        return None
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            rows.append(_coerce(row, kind))
    return rows


def merge_papers(data_dir, rows):
    pp = storage.papers_path(data_dir)
    data = storage.load_json(pp) if os.path.exists(pp) else {"papers": []}
    papers = data.get("papers", [])
    by_id = {p.get("id"): p for p in papers}
    added = 0
    for r in rows:
        if not r.get("id"):
            continue
        if r["id"] in by_id:
            by_id[r["id"]].update(r)
        else:
            papers.append(r)
            added += 1
    data["papers"] = papers
    storage.dump_json(pp, data)
    print("papers.json：更新 {0} 条、新增 {1} 条（合计 {2}）".format(len(rows) - added, added, len(papers)))


def merge_topics(data_dir, rows):
    tp = storage.topics_path(data_dir)
    data = storage.load_json(tp) if os.path.exists(tp) else {"topics": []}
    topics = data.get("topics", [])
    by_id = {t.get("id"): t for t in topics}
    added = 0
    for r in rows:
        if not r.get("id"):
            continue
        if r["id"] in by_id:
            by_id[r["id"]].update(r)
        else:
            topics.append(r)
            added += 1
    data["topics"] = topics
    storage.dump_json(tp, data)
    print("topics.json：更新 {0} 条、新增 {1} 条（合计 {2}）".format(len(rows) - added, added, len(topics)))


def main():
    ap = argparse.ArgumentParser(description="FitEvidence 本地JSON <-> 飞书多维表格 数据交换")
    ap.add_argument("action", choices=["export", "import"], help="export=本地->CSV；import=CSV->本地")
    ap.add_argument("--data-dir", default=None, help="数据目录（缺省按 storage.json 解析）")
    args = ap.parse_args()

    skill_dir = storage.skill_dir_from_here()
    cfg = storage.load_config(skill_dir)
    data_dir = args.data_dir or storage.resolve_data_dir(skill_dir, cfg)

    if args.action == "export":
        export(data_dir)
    else:
        rows_p = import_csv(data_dir, "papers")
        rows_t = import_csv(data_dir, "topics")
        if rows_p:
            merge_papers(data_dir, rows_p)
        if rows_t:
            merge_topics(data_dir, rows_t)
        if not rows_p and not rows_t:
            print("没有可导入的数据。")
            return
        print("提示：导入后建议运行 `python scripts/build_knowledge_base.py` 刷新主题分与视图。")


if __name__ == "__main__":
    main()
