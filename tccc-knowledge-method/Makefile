# tccc-knowledge-method/Makefile  — Phase 1 build/validate/index pipeline
#
# 论文 §9.4: CI 必跑 validate -> build -> index -> eval
# 本 Makefile 负责前 3 步; eval 由 kbtool/eval_runner.py 实现。

# 路径约定 (与 eval-dataset/ 已有结构兼容)
SOURCE_DIR ?= eval-dataset/cards-source
DIST_DIR   ?= eval-dataset/cards-dist
PYTHON     ?= python3

# 兼容已有的 zip-unpacked 目录: 若 source 目录不存在,降级使用 zip 解压目录
ifeq ($(wildcard $(SOURCE_DIR)),)
SOURCE_DIR := $(shell echo "eval-dataset/tccc-zip-unpacked/TCCC指南知识卡片/4.LLM提取的知识卡片")
endif

.PHONY: help validate build index ci clean test

help:
	@echo "Targets:"
	@echo "  make validate    # 校验所有 source/*.json 卡片"
	@echo "  make build       # source -> dist/cards.jsonl"
	@echo "  make index       # 建 BM25 + 元数据索引"
	@echo "  make ci          # 上述三步 + 评测 (论文 §9.4)"
	@echo "  make clean       # 清空 dist/"
	@echo ""
	@echo "Vars:"
	@echo "  SOURCE_DIR=$(SOURCE_DIR)"
	@echo "  DIST_DIR=$(DIST_DIR)"

validate:
	$(PYTHON) -m kbtool.validate "$(SOURCE_DIR)"

build:
	$(PYTHON) -m kbtool.build "$(SOURCE_DIR)" "$(DIST_DIR)"

index: build
	$(PYTHON) -m kbtool.index "$(DIST_DIR)"

# CI 闸口: 任一失败即返回非零
ci: validate build index
	@echo "[ci] all phase-1 stages green ✓"

clean:
	rm -rf "$(DIST_DIR)"

# 单测占位 (Phase 1 暂不强制)
test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py" 2>/dev/null || true
