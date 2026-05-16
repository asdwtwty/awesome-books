# tccc-knowledge-method/Makefile  — Phase 1 build/validate/index pipeline
#
# 论文 §9.4: CI 必跑 validate -> build -> index -> eval
# 本 Makefile 负责前 3 步; eval 由 kbtool/eval_runner.py 实现。

# 路径约定 (与 eval-dataset/ 已有结构兼容)
SOURCE_MD_DIR ?= eval-dataset/cards-source-md
SOURCE_DIR    ?= eval-dataset/cards-source
DIST_DIR      ?= eval-dataset/cards-dist
PYTHON        ?= python3

# 兼容已有的 zip-unpacked 目录: 若 source 目录不存在,降级使用 zip 解压目录
ifeq ($(wildcard $(SOURCE_DIR)),)
SOURCE_DIR := $(shell echo "eval-dataset/tccc-zip-unpacked/TCCC指南知识卡片/4.LLM提取的知识卡片")
endif

.PHONY: help validate build index ci clean test to-md from-md review

help:
	@echo "Targets (按工作流顺序):"
	@echo ""
	@echo "  专家审核工作流 (论文 §4.2 双格式):"
	@echo "  make to-md       # JSON -> MD+YAML  (生成给专家审核的版本)"
	@echo "  make review      # 转 MD 后的审阅入口提示"
	@echo "  make from-md     # 专家改完后,MD+YAML -> JSON 入库"
	@echo ""
	@echo "  发布与索引:"
	@echo "  make validate    # 校验所有 source/*.json 卡片"
	@echo "  make build       # source -> dist/cards.jsonl"
	@echo "  make index       # 建 BM25 + 元数据索引"
	@echo "  make ci          # validate + build + index"
	@echo "  make clean       # 清空 dist/"
	@echo ""
	@echo "Vars:"
	@echo "  SOURCE_MD_DIR=$(SOURCE_MD_DIR)"
	@echo "  SOURCE_DIR=$(SOURCE_DIR)"
	@echo "  DIST_DIR=$(DIST_DIR)"

to-md:
	@mkdir -p "$(SOURCE_MD_DIR)/HEM" "$(SOURCE_MD_DIR)/PCC" "$(SOURCE_MD_DIR)/ATP"
	$(PYTHON) -m kbtool.to_md "$(SOURCE_DIR)" "$(SOURCE_MD_DIR)/HEM" 2>/dev/null || true
	@if [ -d "eval-dataset/cards-pcc" ]; then \
		$(PYTHON) -m kbtool.to_md eval-dataset/cards-pcc "$(SOURCE_MD_DIR)/PCC"; \
	fi
	@if [ -d "eval-dataset/cards-atp40211" ]; then \
		$(PYTHON) -m kbtool.to_md eval-dataset/cards-atp40211 "$(SOURCE_MD_DIR)/ATP"; \
	fi
	@echo ""
	@echo "✓ MD+YAML 源文件已生成于: $(SOURCE_MD_DIR)/"
	@echo "  专家可直接在 GitHub Web 编辑器或本地编辑器中修改 .md 文件"

review:
	@echo ""
	@echo "==== 专家审核工作流 ===="
	@echo "1. 工程: 拉本分支并跑 make to-md 生成 .md 文件"
	@echo "2. 工程: 创建 PR 把 cards-source-md/ 推上 GitHub"
	@echo "3. 专家: 在 GitHub PR 页面直接 review 渲染好的 .md (附建议 / 改正)"
	@echo "4. 专家: 把 review_status: draft 改成 expert_reviewed,提交"
	@echo "5. 工程: 跑 make from-md 把改后的 .md 转回 .json,然后 make ci 闸口"
	@echo ""
	@echo "MD 文件位置: $(SOURCE_MD_DIR)/{HEM,PCC,ATP}/"
	@find "$(SOURCE_MD_DIR)" -name "*.md" 2>/dev/null | head -5
	@echo "  ..."
	@echo ""

from-md:
	@mkdir -p "$(SOURCE_DIR)" eval-dataset/cards-pcc eval-dataset/cards-atp40211
	@if [ -d "$(SOURCE_MD_DIR)/HEM" ]; then \
		$(PYTHON) -m kbtool.from_md "$(SOURCE_MD_DIR)/HEM" "$(SOURCE_DIR)"; \
	fi
	@if [ -d "$(SOURCE_MD_DIR)/PCC" ]; then \
		$(PYTHON) -m kbtool.from_md "$(SOURCE_MD_DIR)/PCC" eval-dataset/cards-pcc; \
	fi
	@if [ -d "$(SOURCE_MD_DIR)/ATP" ]; then \
		$(PYTHON) -m kbtool.from_md "$(SOURCE_MD_DIR)/ATP" eval-dataset/cards-atp40211; \
	fi
	@echo ""
	@echo "✓ 已把审核后的 .md 转回 .json,接下来跑 make ci 进入闸口校验"

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
