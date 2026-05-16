"""kbtool/from_md.py — MD+YAML 源格式 → JSON 卡片 (论文 §4.3)

用途: 把专家审核后的 MD+YAML 文件转回 JSON 入库。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml


def _split_front_matter(text: str):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    fm = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")
    meta = yaml.safe_load(fm) or {}
    return meta, body


def _split_sections(body: str):
    sections = {}
    pat = re.compile(r"^## +(.+?)\s*$", re.MULTILINE)
    matches = list(pat.finditer(body))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        sec = body[m.end():end].strip()
        title = m.group(1).strip()
        sections[title] = sec
    return sections


def _bullets(text: str):
    out = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith(("- ", "* ")):
            v = line[2:].strip()
            v = re.sub(r"^\*\*[^*]+\*\*[::]\s*", "", v)
            if v and v != "_(暂无)_":
                out.append(v)
    return out


def _bullets_under(text: str, leader: str):
    pat = re.compile(rf"\*\*{re.escape(leader)}\*\*[::]?\s*\n((?:- .+\n?)+)")
    m = pat.search(text)
    if not m:
        return []
    return _bullets(m.group(1))


def _parse_table(text: str):
    lines = [l for l in text.splitlines() if l.strip().startswith("|")]
    if len(lines) < 3:
        return []
    headers = [h.strip() for h in lines[0].strip("|").split("|")]
    out = []
    for row in lines[2:]:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        d = dict(zip(headers, cells))
        rec = {}
        if "步骤" in d and d["步骤"]:
            try:
                rec["step"] = int(d["步骤"])
            except ValueError:
                rec["step"] = d["步骤"]
        if "动作" in d:
            rec["action"] = d["动作"]
        if "优先级" in d:
            rec["priority"] = d["优先级"]
        if "条件" in d:
            rec["condition"] = d["条件"]
        if "时间目标" in d:
            rec["time_target"] = d["时间目标"]
        if "备注" in d:
            rec["notes"] = d["备注"]
        out.append(rec)
    return out


def _parse_decision_points(text: str):
    out = []
    blocks = re.split(r"\n(?=\*\*\d+\.\*\*)", text.strip())
    for blk in blocks:
        if not blk.strip():
            continue
        d = {}
        for line in blk.splitlines():
            line = line.strip().lstrip("- ")
            for tag, key in (
                ("如果(condition)", "condition"),
                ("则(next_action)", "next_action"),
                ("依据(rationale)", "rationale"),
                ("分支类型", "branch_type"),
            ):
                if line.startswith(tag):
                    val = line[len(tag):].lstrip("::").strip().strip("`")
                    d[key] = val
        if d:
            out.append(d)
    return out


def md_to_card(text: str) -> dict:
    meta, body = _split_front_matter(text)
    sections = _split_sections(body)
    card = dict(meta)

    for tag, key in (
        ("1. 核心问题", "core_question"),
        ("2. 输出目标", "output_goal"),
        ("10. 备注", "notes"),
    ):
        if tag in sections:
            card[key] = sections[tag].strip()
            if card[key] == "_(暂无)_":
                card[key] = ""

    def _set_if(key, value):
        # 只有非空才写,保持与原 JSON 的 sparseness 一致
        if value:
            card[key] = value

    if "3. 适用场景与边界" in sections:
        s3 = sections["3. 适用场景与边界"]
        _set_if("applicable_scene",
                _bullets_under(s3, "适用场景") or meta.get("applicable_scene"))
        _set_if("preconditions", _bullets_under(s3, "前置条件"))
        _set_if("exclusions", _bullets_under(s3, "不覆盖范围"))

    if "4. 触发与识别" in sections:
        s4 = sections["4. 触发与识别"]
        _set_if("trigger_conditions", _bullets_under(s4, "触发条件"))
        _set_if("recognition_cues", _bullets_under(s4, "识别要点"))
        _set_if("signs", _bullets_under(s4, "临床征象"))

    if "5. 关键动作 / 流程" in sections:
        _set_if("key_actions", _parse_table(sections["5. 关键动作 / 流程"]))

    if "6. 决策点" in sections:
        _set_if("decision_points",
                _parse_decision_points(sections["6. 决策点"]))

    if "7. 复评 / 终点 / 禁忌 / 错误" in sections:
        s7 = sections["7. 复评 / 终点 / 禁忌 / 错误"]
        for leader, key in (
            ("复评要点", "reassessment_points"),
            ("处置终点", "endpoints"),
            ("禁忌 / 警示", "contraindications_or_cautions"),
            ("常见错误", "common_errors"),
            ("文书记录要求", "documentation_requirements"),
        ):
            _set_if(key, _bullets_under(s7, leader))

    if "9. 评分要点(LLM 评测)" in sections:
        _set_if("evaluation_points",
                _bullets(sections["9. 评分要点(LLM 评测)"]))

    if "source_refs" in meta:
        card["source_refs"] = meta["source_refs"]

    return card


def convert_file(src: Path, dst: Path) -> None:
    text = src.read_text(encoding="utf-8")
    card = md_to_card(text)
    dst.write_text(json.dumps(card, ensure_ascii=False, indent=2),
                   encoding="utf-8")


def main(argv):
    if len(argv) < 2:
        print("usage: python -m kbtool.from_md <in.md|in_dir> [out.json|out_dir]",
              file=sys.stderr)
        return 2
    src = Path(argv[1])
    if src.is_file():
        dst = Path(argv[2]) if len(argv) > 2 else src.with_suffix(".json")
        convert_file(src, dst)
        print(f"[from_md] {src} -> {dst}")
    elif src.is_dir():
        if len(argv) < 3:
            print("批量转换需要指定输出目录", file=sys.stderr)
            return 2
        outdir = Path(argv[2])
        outdir.mkdir(parents=True, exist_ok=True)
        n = 0
        for p in sorted(src.rglob("*.md")):
            convert_file(p, outdir / (p.stem + ".json"))
            n += 1
        print(f"[from_md] converted {n} files -> {outdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
