"""kbtool/validate.py — schema and consistency checker for TCCC knowledge cards.

Implements论文 §4.4 一致性校验:
  1. ID 命名合规性
  2. 必填字段完整性 (20 个最小必填字段, 见 schema 规范 §5)
  3. 证据来源有效性 (source_refs 至少 1 条, 含 source_id/title/locator)
  4. 引用目标存在性 (related_cards 中的 ID 必须在仓库中存在)
  5. 受控词表一致性 (枚举值必须落在 vocab 中)

Usage:
    python -m kbtool.validate <source_dir>
    返回 exit code 0 表示全部通过,非 0 表示有违规。
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# ---- 受控词表 (与论文 §10 vocab.yaml 对齐) ------------------------------------
VOCAB = {
    "task_type": {
        "recognition", "procedure", "decision", "triage",
        "reassessment", "error_prevention", "documentation", "communication",
    },
    "training_use": {
        "fact_qa", "case_qa", "structured_decision", "ranking",
        "error_correction", "retrieval", "judge_eval",
    },
    "difficulty": {"basic", "intermediate", "advanced"},
    "applicable_phase": {
        "care_under_threat", "tactical_field_care", "tacevac",
        "prolonged_care_reference", "prolonged_casualty_care",
    },
    "evidence_level": {"guideline", "consensus", "expert_summary", "case_derived"},
    "review_status": {
        "draft", "internally_checked", "expert_reviewed",
        "approved", "deprecated",
    },
    "module": {
        "PHASE", "TRIAGE", "HEM", "AIR", "RESP", "CIRC", "HYP",
        "TBI", "EYE", "MON", "PAIN", "ABX", "WOUND", "BURN",
        "MSK", "EVAC",
        # PCC / ATP 扩展
        "PCC", "ATP",
    },
}

# ---- 必填字段 (schema 规范 §5) -----------------------------------------------
REQUIRED_FIELDS = [
    "card_id", "title", "version",
    "module", "topic", "task_type", "training_use", "difficulty", "applicable_phase",
    "core_question", "output_goal", "applicable_scene", "applicable_population",
    "exclusions", "evaluation_points",
    "source_refs", "evidence_level", "review_status",
    "created_at", "updated_at",
]

# ID 命名正则: 允许 HEM-001 / PCC-CIRC-001 / ATP-AIR-001 等
CARD_ID_PATTERN = re.compile(
    r"^(?:[A-Z]+-)?[A-Z]+-\d{3}$"
)

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class Violation:
    card_id: str
    file: str
    severity: str  # "error" | "warning"
    rule: str
    message: str

    def fmt(self) -> str:
        return f"[{self.severity.upper()}] {self.file}::{self.card_id} ({self.rule}) {self.message}"


def _load_card(p: Path) -> dict[str, Any] | None:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return {"__load_error__": str(e)}


def _check_one(card: dict[str, Any], path: Path, all_ids: set[str]) -> list[Violation]:
    violations: list[Violation] = []
    cid = card.get("card_id", "<unknown>")

    if "__load_error__" in card:
        return [Violation(cid, str(path), "error", "json_parse", card["__load_error__"])]

    # 1) ID 合规
    if not CARD_ID_PATTERN.match(cid):
        violations.append(Violation(cid, str(path), "error", "id_format",
                                    f"card_id 不符合正则 {CARD_ID_PATTERN.pattern}"))

    # 2) 必填字段
    for f in REQUIRED_FIELDS:
        if f not in card or card[f] in (None, "", []):
            violations.append(Violation(cid, str(path), "error", "required_field",
                                        f"缺少必填字段 `{f}`"))

    # 3) 证据来源
    refs = card.get("source_refs", [])
    if not isinstance(refs, list) or len(refs) == 0:
        violations.append(Violation(cid, str(path), "error", "evidence",
                                    "source_refs 必须 ≥ 1 条"))
    else:
        for i, r in enumerate(refs):
            for k in ("source_id", "title", "locator"):
                if k not in r or not r[k]:
                    violations.append(Violation(cid, str(path), "error", "evidence",
                                                f"source_refs[{i}] 缺字段 `{k}`"))

    # 4) related_cards 存在性 (仓库整体扫完一遍后再校验)
    for rc in card.get("related_cards", []) or []:
        if rc not in all_ids:
            violations.append(Violation(cid, str(path), "warning", "ref_target",
                                        f"related_cards `{rc}` 在仓库中未找到"))

    # 5) 受控词表
    if card.get("task_type") and card["task_type"] not in VOCAB["task_type"]:
        violations.append(Violation(cid, str(path), "error", "vocab",
                                    f"task_type=`{card['task_type']}` 不在词表"))
    if card.get("difficulty") and card["difficulty"] not in VOCAB["difficulty"]:
        violations.append(Violation(cid, str(path), "error", "vocab",
                                    f"difficulty=`{card['difficulty']}` 不在词表"))
    if card.get("evidence_level") and card["evidence_level"] not in VOCAB["evidence_level"]:
        violations.append(Violation(cid, str(path), "error", "vocab",
                                    f"evidence_level=`{card['evidence_level']}` 不在词表"))
    if card.get("review_status") and card["review_status"] not in VOCAB["review_status"]:
        violations.append(Violation(cid, str(path), "warning", "vocab",
                                    f"review_status=`{card['review_status']}` 不在词表"))
    if card.get("module") and card["module"] not in VOCAB["module"]:
        violations.append(Violation(cid, str(path), "warning", "vocab",
                                    f"module=`{card['module']}` 不在词表"))

    for tu in card.get("training_use", []) or []:
        if tu not in VOCAB["training_use"]:
            violations.append(Violation(cid, str(path), "error", "vocab",
                                        f"training_use 中 `{tu}` 不在词表"))
    for ph in card.get("applicable_phase", []) or []:
        if ph not in VOCAB["applicable_phase"]:
            violations.append(Violation(cid, str(path), "warning", "vocab",
                                        f"applicable_phase 中 `{ph}` 不在词表"))

    # 6) 日期格式
    for f in ("created_at", "updated_at"):
        v = card.get(f)
        if v and not DATE_PATTERN.match(str(v)):
            violations.append(Violation(cid, str(path), "warning", "date_format",
                                        f"{f}=`{v}` 不是 YYYY-MM-DD"))

    # 7) 禁忌卡片必须含 contraindications_or_cautions
    if card.get("task_type") == "error_prevention":
        if not card.get("contraindications_or_cautions"):
            violations.append(Violation(cid, str(path), "warning", "card_type_field",
                                        "error_prevention 卡建议含 contraindications_or_cautions"))

    # 8) 处置卡建议含 key_actions
    if card.get("task_type") == "procedure" and not card.get("key_actions"):
        violations.append(Violation(cid, str(path), "warning", "card_type_field",
                                    "procedure 卡建议含 key_actions"))

    return violations


def validate(source_dir: str) -> list[Violation]:
    """Walk source_dir, validate every *.json card, return all violations."""
    src = Path(source_dir)
    if not src.exists():
        return [Violation("-", str(src), "error", "io", "目录不存在")]

    files = sorted(src.rglob("*.json"))
    cards: list[tuple[Path, dict]] = []
    all_ids: set[str] = set()
    for p in files:
        c = _load_card(p)
        if c is None:
            continue
        cards.append((p, c))
        if isinstance(c, dict) and "card_id" in c:
            all_ids.add(c["card_id"])

    violations: list[Violation] = []
    for p, c in cards:
        violations.extend(_check_one(c, p, all_ids))

    # 重复 ID 检查
    seen: dict[str, list[str]] = {}
    for p, c in cards:
        if isinstance(c, dict):
            cid = c.get("card_id")
            if cid:
                seen.setdefault(cid, []).append(str(p))
    for cid, paths in seen.items():
        if len(paths) > 1:
            violations.append(Violation(cid, ",".join(paths), "error",
                                        "duplicate_id", f"卡片 ID 出现 {len(paths)} 次"))

    return violations


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: python -m kbtool.validate <source_dir>", file=sys.stderr)
        return 2
    src = argv[1]
    violations = validate(src)
    errors = [v for v in violations if v.severity == "error"]
    warnings = [v for v in violations if v.severity == "warning"]
    for v in violations:
        print(v.fmt())
    print(f"\n[validate] scanned: {len(list(Path(src).rglob('*.json')))} cards | "
          f"errors: {len(errors)} | warnings: {len(warnings)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
