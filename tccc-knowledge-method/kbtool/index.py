"""kbtool/index.py — BM25 + (optional) dense vector index for TCCC cards.

实现论文 §8.3 混合检索的索引侧:
  - BM25  稀疏索引: 处理缩写/装备名 (TQ/NPA/14G/EtCO2 等)
  - Dense 向量索引: 处理自然语言症状描述 (可选, 取决于环境是否安装 sentence-transformers)
  - Meta  元数据过滤: 按 module/applicable_phase/task_type/difficulty 切片

Usage:
    python -m kbtool.index <dist_dir>          # 默认只建 BM25
    python -m kbtool.index <dist_dir> --dense  # 同时建向量索引

输出:
    <dist_dir>/index/bm25.pkl
    <dist_dir>/index/meta.json
    <dist_dir>/index/dense.npz   (可选)
"""
from __future__ import annotations

import json
import pickle
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# rank_bm25 是轻量 pure-python 实现,无需 C 编译
try:
    from rank_bm25 import BM25Okapi
except ImportError:
    BM25Okapi = None  # type: ignore


# 中文 + 英文混合分词: 字符级 + 英文单词
TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+|[\u4e00-\u9fff]")


def tokenize(text: str) -> list[str]:
    if not text:
        return []
    return [t.lower() for t in TOKEN_PATTERN.findall(text)]


def card_to_text(card: dict[str, Any]) -> str:
    """把卡片折叠成一段可索引文本; 字段权重靠重复出现实现。"""
    parts: list[str] = []
    # 标题与核心问题各重复 2 次以提升权重
    for k in ("title", "core_question"):
        v = card.get(k, "")
        if v:
            parts.extend([v, v])
    for k in ("output_goal", "topic"):
        v = card.get(k, "")
        if v:
            parts.append(v)
    for k in ("trigger_conditions", "recognition_cues",
              "reassessment_points", "endpoints", "common_errors",
              "evaluation_points", "qa_seed_questions"):
        for v in card.get(k, []) or []:
            parts.append(str(v))
    for ka in card.get("key_actions", []) or []:
        if isinstance(ka, dict):
            for kk in ("action", "condition", "notes"):
                v = ka.get(kk)
                if v:
                    parts.append(str(v))
    for dp in card.get("decision_points", []) or []:
        if isinstance(dp, dict):
            for kk in ("condition", "next_action", "rationale"):
                v = dp.get(kk)
                if v:
                    parts.append(str(v))
    return " ".join(parts)


@dataclass
class IndexBundle:
    card_ids: list[str]
    bm25_path: str
    meta_path: str
    dense_path: str | None
    total: int

    def fmt(self) -> str:
        d = "+dense" if self.dense_path else ""
        return f"[index] cards={self.total} BM25 saved -> {self.bm25_path}{d}"


def _load_jsonl(p: Path) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    if not p.exists():
        raise FileNotFoundError(p)
    with p.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                cards.append(json.loads(line))
    return cards


def build_index(dist_dir: str, with_dense: bool = False) -> IndexBundle:
    dist = Path(dist_dir)
    cards_jsonl = dist / "cards.jsonl"
    cards = _load_jsonl(cards_jsonl)

    idx_dir = dist / "index"
    idx_dir.mkdir(parents=True, exist_ok=True)

    card_ids: list[str] = []
    corpus_tokens: list[list[str]] = []
    meta: dict[str, dict[str, Any]] = {}
    for c in cards:
        cid = c["card_id"]
        card_ids.append(cid)
        corpus_tokens.append(tokenize(card_to_text(c)))
        meta[cid] = {
            "title": c.get("title", ""),
            "module": c.get("module", ""),
            "task_type": c.get("task_type", ""),
            "applicable_phase": c.get("applicable_phase", []),
            "difficulty": c.get("difficulty", ""),
            "review_status": c.get("review_status", ""),
        }

    # 1) BM25
    if BM25Okapi is None:
        bm25_path = ""
        print("[warn] rank_bm25 未安装,跳过 BM25 索引 (pip install rank_bm25)",
              file=sys.stderr)
    else:
        bm25 = BM25Okapi(corpus_tokens)
        bm25_path = str(idx_dir / "bm25.pkl")
        with open(bm25_path, "wb") as f:
            pickle.dump({"bm25": bm25, "card_ids": card_ids}, f)

    # 2) 元数据
    meta_path = str(idx_dir / "meta.json")
    Path(meta_path).write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 3) Dense (可选)
    dense_path = None
    if with_dense:
        try:
            from sentence_transformers import SentenceTransformer
            import numpy as np
            model = SentenceTransformer("intfloat/multilingual-e5-base")
            texts = [card_to_text(c) for c in cards]
            embs = model.encode(texts, normalize_embeddings=True,
                                show_progress_bar=False)
            dense_path = str(idx_dir / "dense.npz")
            np.savez(dense_path, embeddings=embs, card_ids=np.array(card_ids))
        except ImportError:
            print("[warn] sentence-transformers/numpy 未安装,跳过 dense 索引",
                  file=sys.stderr)

    return IndexBundle(card_ids, bm25_path, meta_path, dense_path, len(cards))


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: python -m kbtool.index <dist_dir> [--dense]", file=sys.stderr)
        return 2
    with_dense = "--dense" in argv
    bundle = build_index(argv[1], with_dense=with_dense)
    print(bundle.fmt())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
