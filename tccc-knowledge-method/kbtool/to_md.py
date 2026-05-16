"""kbtool/to_md.py — JSON 卡片 → MD+YAML 源格式 (论文 §4.2)

用途: 一次性把 JSON 卡片转成 MD+YAML,交给医学专家审核。
设计原则:
  - YAML front-matter 只放结构化字段 (机器关心,专家不必动)
  - Markdown 正文按 8 个固定小节排版 (专家关心)
  - 转换 100% 可逆,from_md.py 能 1:1 还原
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

META_FIELDS = [
    "card_id", "title", "version", "module", "topic",
    "task_type", "training_use", "difficulty", "applicable_phase",
    "evidence_level", "review_status", "reviewers",
    "created_at", "updated_at",
    "applicable_population",
    "related_cards",
    "source_refs",
]


def _yaml_dump(d: dict) -> str:
    return yaml.safe_dump(d, allow_unicode=True, sort_keys=False,
                          default_flow_style=False, width=120)


def _section(title: str, body: str) -> str:
    return f"\n## {title}\n\n{body.strip()}\n"


def _list(items: list, prefix: str = "- ") -> str:
    if not items:
        return "_(暂无)_"
    return "\n".join(f"{prefix}{x}" for x in items)


def _scene_block(card: dict) -> str:
    parts = []
    if card.get("applicable_scene"):
        parts.append("**适用场景**:\n" + _list(card["applicable_scene"]))
    if card.get("preconditions"):
        parts.append("**前置条件**:\n" + _list(card["preconditions"]))
    if card.get("exclusions"):
        parts.append("**不覆盖范围**:\n" + _list(card["exclusions"]))
    return "\n\n".join(parts) if parts else "_(暂无)_"


def _key_actions_table(actions):
    if not actions:
        return "_(暂无)_"
    rows = ["| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |",
            "|---|---|---|---|---|---|"]
    for a in actions:
        rows.append("| {} | {} | {} | {} | {} | {} |".format(
            a.get("step", ""),
            (a.get("action") or "").replace("|", "\\|"),
            a.get("priority", ""),
            (a.get("condition") or "").replace("|", "\\|"),
            a.get("time_target", ""),
            (a.get("notes") or "").replace("|", "\\|"),
        ))
    return "\n".join(rows)


def _decision_points(dps):
    if not dps:
        return "_(暂无)_"
    out = []
    for i, dp in enumerate(dps, 1):
        out.append(
            f"**{i}.**\n"
            f"- 如果(condition):{dp.get('condition','')}\n"
            f"- 则(next_action):{dp.get('next_action','')}\n"
            f"- 依据(rationale):{dp.get('rationale','')}\n"
            f"- 分支类型:`{dp.get('branch_type','')}`"
        )
    return "\n\n".join(out)


def _evidence(refs):
    if not refs:
        return "_(暂无)_"
    out = []
    for r in refs:
        block = (
            f"- **{r.get('source_id','')}** — {r.get('title','')} "
            f"({r.get('version','')})\n"
            f"  - 章节: `{r.get('section','')}`\n"
            f"  - 位置: `{r.get('locator','')}`"
        )
        if r.get("quote"):
            block += f"\n  - 原文引用:\n    > {r['quote']}"
        out.append(block)
    return "\n".join(out)


def card_to_md(card: dict) -> str:
    meta = {k: card[k] for k in META_FIELDS if k in card}
    yaml_block = _yaml_dump(meta).strip()

    body = []
    body.append(f"# {card.get('title','(未命名卡片)')}")
    body.append(_section("1. 核心问题", card.get("core_question", "_(暂无)_")))
    body.append(_section("2. 输出目标", card.get("output_goal", "_(暂无)_")))
    body.append(_section("3. 适用场景与边界", _scene_block(card)))

    cues_body = ""
    if card.get("trigger_conditions"):
        cues_body += "**触发条件**:\n" + _list(card["trigger_conditions"])
    if card.get("recognition_cues"):
        if cues_body:
            cues_body += "\n\n"
        cues_body += "**识别要点**:\n" + _list(card["recognition_cues"])
    if card.get("signs"):
        if cues_body:
            cues_body += "\n\n"
        cues_body += "**临床征象**:\n" + _list(card["signs"])
    body.append(_section("4. 触发与识别", cues_body or "_(暂无)_"))

    body.append(_section("5. 关键动作 / 流程",
                         _key_actions_table(card.get("key_actions") or [])))
    body.append(_section("6. 决策点",
                         _decision_points(card.get("decision_points") or [])))

    extras = []
    if card.get("reassessment_points"):
        extras.append("**复评要点**:\n" + _list(card["reassessment_points"]))
    if card.get("endpoints"):
        extras.append("**处置终点**:\n" + _list(card["endpoints"]))
    if card.get("contraindications_or_cautions"):
        extras.append("**禁忌 / 警示**:\n" +
                      _list(card["contraindications_or_cautions"]))
    if card.get("common_errors"):
        extras.append("**常见错误**:\n" + _list(card["common_errors"]))
    if card.get("documentation_requirements"):
        extras.append("**文书记录要求**:\n" +
                      _list(card["documentation_requirements"]))
    body.append(_section("7. 复评 / 终点 / 禁忌 / 错误",
                         "\n\n".join(extras) if extras else "_(暂无)_"))

    body.append(_section("8. 证据来源(展开)",
                         _evidence(card.get("source_refs") or [])))
    body.append(_section("9. 评分要点(LLM 评测)",
                         _list(card.get("evaluation_points") or [])))

    if card.get("notes"):
        body.append(_section("10. 备注", card["notes"]))

    return f"---\n{yaml_block}\n---\n\n" + "\n".join(body) + "\n"


def convert_file(src: Path, dst: Path) -> None:
    card = json.loads(src.read_text(encoding="utf-8"))
    dst.write_text(card_to_md(card), encoding="utf-8")


def main(argv):
    if len(argv) < 2:
        print("usage: python -m kbtool.to_md <in.json|in_dir> [out.md|out_dir]",
              file=sys.stderr)
        return 2
    src = Path(argv[1])
    if src.is_file():
        dst = Path(argv[2]) if len(argv) > 2 else src.with_suffix(".md")
        convert_file(src, dst)
        print(f"[to_md] {src} -> {dst}")
    elif src.is_dir():
        if len(argv) < 3:
            print("批量转换需要指定输出目录", file=sys.stderr)
            return 2
        outdir = Path(argv[2])
        outdir.mkdir(parents=True, exist_ok=True)
        n = 0
        for p in sorted(src.rglob("*.json")):
            convert_file(p, outdir / (p.stem + ".md"))
            n += 1
        print(f"[to_md] converted {n} files -> {outdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
