.PHONY: help install install-dev test test-cov lint format clean build upload dev-setup check security

help:
	@echo "AI Toolkit - 开发命令"
	@echo ""
	@echo "安装:"
	@echo "  make install       - 安装项目"
	@echo "  make install-dev   - 安装开发依赖"
	@echo "  make dev-setup     - 完整开发环境设置"
	@echo ""
	@echo "测试:"
	@echo "  make test          - 运行测试"
	@echo "  make test-cov      - 测试覆盖率"
	@echo ""
	@echo "代码质量:"
	@echo "  make lint          - 代码检查"
	@echo "  make format        - 格式化代码"
	@echo "  make check         - 完整检查"
	@echo "  make security      - 安全扫描"
	@echo ""
	@echo "构建:"
	@echo "  make clean         - 清理构建文件"
	@echo "  make build         - 构建发布包"
	@echo "  make upload        - 发布到 PyPI"
	@echo ""
	@echo "开发:"
	@echo "  make dev           - 开发模式运行"
	@echo "  make docs          - 生成文档"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

dev-setup:
	pip install -e ".[dev]"
	python3 -c "from ai_toolkit.core.api_manager import create_sample_config; create_sample_config()"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src/ai_toolkit --cov-report=html --cov-report=term

lint:
	flake8 src/ai_toolkit/
	mypy src/ai_toolkit/

format:
	black src/ tests/
	isort src/ tests/

check:
	black --check src/ tests/
	flake8 src/ai_toolkit/
	mypy src/ai_toolkit/
	pytest tests/ -v

security:
	bandit -r src/ai_toolkit/
	safety check

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

build: clean
	python3 -m build

upload: build
	twine upload dist/*

upload-test: build
	twine upload --repository testpypi dist/*

dev:
	python3 -m ai_toolkit.cli

docs:
	@echo "文档见 docs/ 目录"

# 快速开发循环
dev-loop: format lint test
	@echo "✅ 开发循环完成: 格式化 → 检查 → 测试"

# 发布前检查
pre-release: check test-cov security
	@echo "✅ 发布前检查完成"
