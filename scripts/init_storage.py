#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FitEvidence init_storage.py —— 初始化数据存储（首次使用必跑）

用法:
  python scripts/init_storage.py                        # 查看/保持当前配置
  python scripts/init_storage.py --backend local        # 本地 JSON 后端（默认，数据在 skill 内 data/）
  python scripts/init_storage.py --backend local --data-dir D:/my/fitdata [--seed]
                                                         # 本地后端 + 自定义目录（--seed 复制内置示例数据）
  python scripts/init_storage.py --backend lark [--app-token xxx --papers-table-id xxx --topics-table-id xxx]
                                                         # 飞书多维表格后端（表未建时打印建表指引）

设计意图：Skill 只装"指南 + 模板 + 种子示例"；数据归属每个使用者——
local 后端放自己的目录，lark 后端放自己飞书账号里的多维表格。
"""

import argparse
import json
import os
import shutil
import sys
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import storage  # noqa: E402

EMPTY_PAPERS = {"papers": []}
EMPTY_TOPICS = {"topics": []}


def _templates_dir(skill_dir):
    return os.path.join(skill_dir, "templates")


def _copy_empty(data_dir, skill_dir):
    """用 templates/ 下的空模板初始化数据文件。"""
    os.makedirs(data_dir, exist_ok=True)
    src_p = os.path.join(_templates_dir(skill_dir), "papers.empty.json")
    src_t = os.path.join(_templates_dir(skill_dir), "topics.empty.json")
    for src, dst in ((src_p, os.path.join(data_dir, "papers.json")),
                     (src_t, os.path.join(data_dir, "topics.json"))):
        if os.path.exists(src):
            shutil.copyfile(src, dst)
        else:
            with open(dst, "w", encoding="utf-8") as f:
                json.dump({"papers": []} if dst.endswith("papers.json") else {"topics": []},
                          f, ensure_ascii=False, indent=2)


def _seed_example(data_dir, skill_dir):
    """把 skill 内置示例数据（data/）复制为用户初始库。"""
    src_dir = os.path.join(skill_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    for name in ("papers.json", "topics.json"):
        src = os.path.join(src_dir, name)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(data_dir, name))
    print("已复制内置示例数据（{0} 篇文献）到 {1}".format(
        len(storage.load_json(os.path.join(data_dir, "papers.json")).get("papers", [])),
        data_dir))


def main():
    ap = argparse.ArgumentParser(description="FitEvidence 数据存储初始化")
    ap.add_argument("--backend", choices=["local", "lark"], default=None,
                    help="后端类型：local=本地 JSON；lark=飞书多维表格")
    ap.add_argument("--data-dir", default=None, help="local 后端的数据目录（缺省=skill 内 data/）")
    ap.add_argument("--seed", action="store_true",
                    help="local 后端：把内置示例数据复制为初始库（默认新建空库）")
    ap.add_argument("--app-token", default=None, help="lark 后端：飞书多维表格 app_token")
    ap.add_argument("--papers-table-id", default=None, help="lark 后端：papers 表的 table_id")
    ap.add_argument("--topics-table-id", default=None, help="lark 后端：topics 表的 table_id")
    args = ap.parse_args()

    skill_dir = storage.skill_dir_from_here()
    cfg = storage.load_config(skill_dir)

    if args.backend == "local":
        data_dir = args.data_dir or os.path.join(skill_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        has_papers = os.path.exists(storage.papers_path(data_dir))
        has_topics = os.path.exists(storage.topics_path(data_dir))
        if not (has_papers and has_topics):
            if args.seed or data_dir == os.path.join(skill_dir, "data"):
                _seed_example(data_dir, skill_dir)
            else:
                _copy_empty(data_dir, skill_dir)
        cfg["backend"] = "local"
        cfg["data_dir"] = data_dir
        cfg["updated_at"] = datetime.date.today().isoformat()
        storage.save_config(cfg, skill_dir)
        print("后端: local")
        print("数据目录: {0}".format(data_dir))
        print("配置已写入: {0}".format(storage.config_path(skill_dir)))
        return

    if args.backend == "lark":
        cfg["backend"] = "lark"
        if args.app_token:
            cfg["lark"]["app_token"] = args.app_token
        if args.papers_table_id:
            cfg["lark"]["papers_table_id"] = args.papers_table_id
        if args.topics_table_id:
            cfg["lark"]["topics_table_id"] = args.topics_table_id
        cfg["updated_at"] = datetime.date.today().isoformat()
        storage.save_config(cfg, skill_dir)
        print("后端: lark（飞书多维表格）")
        print("app_token={0}  papers_table_id={1}  topics_table_id={2}".format(
            cfg["lark"]["app_token"], cfg["lark"]["papers_table_id"], cfg["lark"]["topics_table_id"]))
        if not (cfg["lark"]["app_token"] and cfg["lark"]["papers_table_id"] and cfg["lark"]["topics_table_id"]):
            print("")
            print("提示：表尚未关联。请使用 lark-base 能力在用户的飞书账号下建两张多维表格：")
            print("  1) papers 表 —— 字段见 templates/papers.schema.json")
            print("  2) topics 表 —— 字段见 templates/topics.schema.json")
            print("  建好后把 app_token / 两个 table_id 回填到 storage.json，")
            print("  再用 `python scripts/sync_lark.py export` 把本地数据导入飞书。")
        print("配置已写入: {0}".format(storage.config_path(skill_dir)))
        return

    # 无 --backend：只读展示当前配置
    print("当前存储配置:")
    print(json.dumps(cfg, ensure_ascii=False, indent=2))
    print("数据目录(解析结果): {0}".format(storage.resolve_data_dir(skill_dir, cfg)))


if __name__ == "__main__":
    main()
