#!/usr/bin/env python3
"""lhg-startup-legal 确定性审计：创业协议与股权结构体检。

扫描目标目录下的 *.md（协议文本）与 cap-table.json（股权结构），
按规则注册表逐项检查。零第三方依赖。

规则（rule_id / 级别 / 含义）：
  AGREE-CLAUSE-001  blocker  协议缺关键条款（争议解决/保密期限/竞业范围/违约责任）
  PLACEHOLDER-001   warning  协议含未填写占位符
  CAPTABLE-001      blocker  cap-table.json 股权比例加总不为 100%
  EQUITY-DEADLOCK-001 warning  股权僵局预警（50/50 或单一股东>=90%）
  NON-LAWYER-001    blocker  非律师意见声明缺失

用法：
  python3 startup_audit.py --target <目录> [--format json|text]
退出码：0=无问题，1=有 blocker，2=只有 warning。
"""

import argparse
import json
import os
import re
import sys

# ---------------- 规则注册表 ----------------
CLAUSE_KEYWORDS = [
    ("争议解决", "争议解决（管辖法院/仲裁机构）"),
    ("保密期限", "保密期限"),
    ("竞业范围", "竞业范围（地域+业务）"),
    ("违约责任", "违约责任"),
]
# 占位符模式：【】 ［］ ___ TODO XXX 待填写
PLACEHOLDER_PATTERNS = [
    "\u3010[^\u3011]*\u3011",
    "\u3014[^\u3015]*\u3015",
    "_{3,}",
    "TODO",
    "XXX",
    "\u5f85\u586b\u5199",
]
DISC = "\u975e\u5f8b\u5e08\u610f\u89c1"


class Finding(object):
    def __init__(self, rule_id, level, message, location=""):
        self.rule_id = rule_id
        self.level = level
        self.message = message
        self.location = location

    def to_dict(self):
        return {"rule_id": self.rule_id, "level": self.level,
                "message": self.message, "location": self.location}


def check_agreement_md(path, findings):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    missing = [label for kw, label in CLAUSE_KEYWORDS if kw not in text]
    if missing:
        findings.append(Finding(
            "AGREE-CLAUSE-001", "blocker",
            "协议缺关键条款：" + "、".join(missing), path))
    hits = []
    for pat in PLACEHOLDER_PATTERNS:
        for m in re.finditer(pat, text):
            hits.append(m.group(0)[:12])
    if hits:
        findings.append(Finding(
            "PLACEHOLDER-001", "warning",
            "协议含未填写占位符 %d 处：%s" % (len(hits), "、".join(hits[:5])), path))
    if DISC not in text:
        findings.append(Finding(
            "NON-LAWYER-001", "blocker",
            "协议/审查报告缺声明：须写明非律师意见、仅供参考", path))


def check_captable_json(path, findings):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return
    except ValueError as e:
        findings.append(Finding("CAPTABLE-001", "blocker",
                                "cap-table.json 不是合法 JSON：%s" % e, path))
        return
    rows = data if isinstance(data, list) else data.get("shareholders", [])
    if not rows:
        findings.append(Finding("CAPTABLE-001", "blocker",
                                "cap-table.json 为空：至少列出 1 位股东", path))
        return
    try:
        total = sum(float(r.get("share", 0)) for r in rows)
    except (TypeError, ValueError):
        findings.append(Finding("CAPTABLE-001", "blocker",
                                "cap-table.json 中 share 不是数字", path))
        return
    if abs(total - 100.0) > 0.01:
        findings.append(Finding(
            "CAPTABLE-001", "blocker",
            "股权比例加总为 %.2f%%，不为 100%%" % total, path))
    shares = [float(r.get("share", 0)) for r in rows]
    if len(shares) == 2 and any(abs(s - 50.0) < 0.01 for s in shares):
        findings.append(Finding(
            "EQUITY-DEADLOCK-001", "warning",
            "股权僵局预警：两股东 50/50 结构，一方不同意即僵局，建议一方多 1% 并配套表决机制",
            path))
    if any(s >= 90.0 for s in shares):
        findings.append(Finding(
            "EQUITY-DEADLOCK-001", "warning",
            "一人公司风险提示：单一股东持股 >=90%，注意财产混同的连带责任风险，请咨询律师",
            path))


def audit(target):
    findings = []
    for name in sorted(os.listdir(target)):
        p = os.path.join(target, name)
        if name.endswith(".md"):
            check_agreement_md(p, findings)
        elif name == "cap-table.json":
            check_captable_json(p, findings)
    return findings


def main():
    ap = argparse.ArgumentParser(description="lhg-startup-legal 创业协议与股权审计")
    ap.add_argument("--target", required=True, help="待审计目录")
    ap.add_argument("--format", choices=["json", "text"], default="text")
    args = ap.parse_args()
    if not os.path.isdir(args.target):
        print("目标目录不存在：" + args.target, file=sys.stderr)
        return 1
    findings = audit(args.target)
    blockers = sum(1 for f in findings if f.level == "blocker")
    warnings = sum(1 for f in findings if f.level == "warning")
    summary = {"blocker": blockers, "warning": warnings, "total": len(findings)}
    if args.format == "json":
        print(json.dumps({"summary": summary,
                          "findings": [f.to_dict() for f in findings]},
                         ensure_ascii=False, indent=2))
    else:
        print("创业协议审计：blocker=%d warning=%d" % (blockers, warnings))
        for f in findings:
            loc = " [%s]" % f.location if f.location else ""
            print("[%s] %s%s: %s" % (f.level.upper(), f.rule_id, loc, f.message))
        if not findings:
            print("全部通过。")
    if blockers:
        return 1
    if warnings:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
