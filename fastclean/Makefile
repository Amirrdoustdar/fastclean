.PHONY: help install install-dev test lint format clean build templates

help:
	@echo "Available commands:"
	@echo "  make install      - Install package"
	@echo "  make install-dev  - Install with dev dependencies"
	@echo "  make templates    - Create Jinja2 templates"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make build        - Build package"

install:
	@echo "📦 Installing fastclean..."
	pip install -e .
	@echo "✅ Installation complete!"

install-dev:
	@echo "📦 Installing with dev dependencies..."
	pip install -e ".[dev]"
	pre-commit install
	@echo "✅ Dev installation complete!"

templates:
	@echo "🎨 Creating templates..."
	python build_templates.py
	@echo "✅ Templates created!"

test:
	@echo "🧪 Running tests..."
	pytest -v --cov=src --cov-report=html

lint:
	@echo "🔍 Linting code..."
	flake8 src tests
	mypy src

format:
	@echo "✨ Formatting code..."
	black src tests
	isort src tests

clean:
	@echo "🧹 Cleaning up..."
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .mypy_cache/ htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"

build:
	@echo "📦 Building package..."
	python -m build
	@echo "✅ Build complete!"
