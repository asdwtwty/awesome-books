# kbtool — Phase 1 工具集

> 配套论文 §9 原型实现方案
> 状态: Phase 1 (build / validate / index) 已完成
> 后续: Phase 2-5 在论文 §12.3 路线图

## 文件清单

| 文件 | 实现章节 | 行为 |
|---|---|---|
| `validate.py` | §4.4 一致性校验 | ID 命名 / 必填字段 / 证据 / 词表 / 引用目标 |
| `build.py`    | §4.3 发布格式  | source/*.json → dist/cards.jsonl + manifest |
| `index.py`    | §8.3 混合检索  | BM25 (必装) + 向量 (可选) + 元数据 |

## 安装依赖

```bash
pip install rank_bm25                       # BM25 (必装)
pip install sentence-transformers numpy     # 向量索引 (可选)
```

## 快速开始

```bash
# 进入仓库
cd tccc-knowledge-method/

# 1. 校验现有 24 张 HEM 卡片
make validate

# 2. 构建发布格式
make build

# 3. 建索引 (默认 BM25)
make index

# 4. 一键跑完 Phase 1 全流程
make ci
```

## 默认路径

- `SOURCE_DIR`:卡片源目录,默认指向已有的 zip-unpacked 卡片
- `DIST_DIR`:发布产物目录,默认 `eval-dataset/cards-dist/`

可用环境变量覆盖:`make ci SOURCE_DIR=path/to/cards`

## 校验规则总表 (validate.py)

| 规则 ID | 严重度 | 含义 |
|---|---|---|
| `id_format`        | error   | card_id 必须匹配 `^(?:[A-Z]+-)?[A-Z]+-\d{3}$` |
| `required_field`   | error   | 20 项必填字段 (schema 规范 §5) |
| `evidence`         | error   | source_refs ≥ 1, 含 source_id/title/locator |
| `vocab`            | error   | task_type/difficulty/evidence_level 必须在 VOCAB |
| `duplicate_id`     | error   | card_id 全仓库唯一 |
| `ref_target`       | warning | related_cards 引用的 ID 需存在 |
| `card_type_field`  | warning | procedure 卡建议有 key_actions 等 |

## 退出码

- `0`:全部通过
- `1`:存在 error 级违规 (CI 闸口阻断 PR)
- `2`:命令行参数错误
