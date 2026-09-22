#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FitEvidence 存储配置公共模块。

storage.json（位于 skill 根目录）描述数据存放在哪里：
  backend: "local" | "lark"
  local  -> data_dir 指向本地数据目录（缺省用 skill 内 data/）
  lark   -> 飞书多维表格：app_token + papers/topics 两张表的 table_id

所有脚本都通过本模块解析数据位置，实现"一份指南、多后端可配"。
"""

import json
import os

DEFAULT_CONFIG = {
    "backend": "local",
    "data_dir": None,
    "lark": {"app_token": "", "papers_table_id": "", "topics_table_id": ""},
    "updated_at": "",
}


def skill_dir_from_here():
    """本文件位于 <skill>/scripts/ 下，上级的上级即 skill 根目录。"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def config_path(skill_dir=None):
    return os.path.join(skill_dir or skill_dir_from_here(), "storage.json")


def load_config(skill_dir=None):
    """读取配置；文件缺失时返回默认（local + skill 内 data/），不自动创建。"""
    p = config_path(skill_dir)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            cfg = json.load(f)
        merged = dict(DEFAULT_CONFIG)
        merged.update(cfg)
        if isinstance(cfg.get("lark"), dict):
            lark = dict(DEFAULT_CONFIG["lark"])
            lark.update(cfg["lark"])
            merged["lark"] = lark
        return merged
    return dict(DEFAULT_CONFIG)


def save_config(cfg, skill_dir=None):
    p = config_path(skill_dir)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    return p


def resolve_data_dir(skill_dir=None, cfg=None):
    """local 后端：返回实际数据目录（用户指定 data_dir 或 skill 内 data/）。"""
    cfg = cfg or load_config(skill_dir)
    if cfg.get("backend") == "local" and cfg.get("data_dir"):
        return cfg["data_dir"]
    return os.path.join(skill_dir or skill_dir_from_here(), "data")


def papers_path(data_dir):
    return os.path.join(data_dir, "papers.json")


def topics_path(data_dir):
    return os.path.join(data_dir, "topics.json")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def dump_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
