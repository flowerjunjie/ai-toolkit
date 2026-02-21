.PHONY: help install install-dev test lint format clean build upload docs

help:
	@echo "AI Toolkit - 可用命令:"
	@echo "  make install       - 安装项目"
	@echo "  make install-dev   - 安装开发依赖"
	@echo "  make test          - 运行测试"
	@echo "  make lint          - 代码检查"
	@echo "  make format        - 格式化代码"
	@echo "  make clean         - 清理构建文件"
	@echo "  make build         - 构建发布包"
	@echo "  make upload        - 发布到 PyPI"
	@echo "  make docs          - 生成文档"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pip install -e ".[rag]"

test:
	pytest tests/ -v

lint:
	flake8 src/ai_toolkit/
	mypy src/ai_toolkit/

format:
	black src/ai_toolkit/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

upload:
	twine upload dist/*

upload-test:
	twine upload --repository testpypi dist/

docs:
	@echo "文档待生成..."
