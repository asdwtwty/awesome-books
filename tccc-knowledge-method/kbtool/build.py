"""kbtool/build.py — Convert source JSON cards to publish-format JSONL.

实现论文 §4.3 发布格式: 把 source/*.json 合并为 dist/cards.jsonl,
为下游索引/检索/评测提供单文件统一语料。

构建前自动跑 validate(); 任何 error 级别违规直接阻断。

Usage:
    python -m kbtool.build <source_dir> <dist_dir>
"""
from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from .validate import Violation, validate


@dataclass
class BuildReport:
    total_cards: int
    output_jsonl: str
    elapsed_sec: float
    violations: list[Violation]

    def fmt(self) -> str:
        e = sum(1 for v in self.violations if v.severity == "error")
        w = sum(1 for v in self.violations if v.severity == "warning")
        return (f"[build] cards={self.total_cards} -> {self.output_jsonl} "
                f"({self.elapsed_sec:.2f}s) errors={e} warnings={w}")


def build(source_dir: str, dist_dir: str) -> BuildReport:
    t0 = time.time()
    src = Path(source_dir)
    dist = Path(dist_dir)
    dist.mkdir(parents=True, exist_ok=True)

    # 1. 校验
    violations = validate(source_dir)
    errors = [v for v in violations if v.severity == "error"]
    if errors:
        report = BuildReport(0, "", time.time() - t0, violations)
        return report

    # 2. 合并为 cards.jsonl
    output = dist / "cards.jsonl"
    cards: list[dict] = []
    for p in sorted(src.rglob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            # 注入构建元数据
            d["_source_file"] = str(p.relative_to(src))
            d["_built_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            cards.append(d)
        except json.JSONDecodeError:
            continue

    with output.open("w", encoding="utf-8") as f:
        for c in cards:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    # 3. 写 manifest
    manifest = {
        "schema_version": "1.0",
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_cards": len(cards),
        "by_module": _count_by_module(cards),
    }
    (dist / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return BuildReport(len(cards), str(output), time.time() - t0, violations)


def _count_by_module(cards: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for c in cards:
        m = c.get("module", "UNKNOWN")
        out[m] = out.get(m, 0) + 1
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("usage: python -m kbtool.build <source_dir> <dist_dir>", file=sys.stderr)
        return 2
    report = build(argv[1], argv[2])
    print(report.fmt())
    errors = [v for v in report.violations if v.severity == "error"]
    if errors:
        print("\n--- ERRORS ---")
        for v in errors:
            print(v.fmt())
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
