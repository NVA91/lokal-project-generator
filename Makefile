.PHONY: help install dev test test-cov test-unit test-int lint format type clean run

.DEFAULT_GOAL := help

help:
	@echo "Lokal Project Generator - Development Commands"
	@echo ""
	@echo "  install        Install project dependencies"
	@echo "  dev            Install dev dependencies"
	@echo "  test           Run all tests"
	@echo "  test-cov       Run tests with coverage report"
	@echo "  test-unit      Run unit tests only"
	@echo "  test-int       Run integration tests only"
	@echo "  lint           Run linters (black, isort, flake8, mypy)"
	@echo "  format         Format code (black, isort)"
	@echo "  type           Run mypy type-checking"
	@echo "  clean          Remove build artifacts and caches"
	@echo "  cli            Run lokal CLI"
	@echo ""

install:
	@echo "Installing dependencies..."
	poetry install
	@echo "✅ Done!"

dev: install
	@echo "Installing dev dependencies..."
	poetry install --with dev
	@echo "✅ Done!"

test:
	@echo "Running all tests..."
	poetry run pytest -v

test-cov:
	@echo "Running tests with coverage..."
	poetry run pytest --cov=src/lokal --cov-report=term-missing --cov-report=html
	@echo "📊 Coverage report generated in htmlcov/index.html"

test-unit:
	@echo "Running unit tests..."
	poetry run pytest src/tests/unit -v

test-int:
	@echo "Running integration tests..."
	poetry run pytest src/tests/integration -v -m integration

lint:
	@echo "Linting code..."
	poetry run black --check src/
	poetry run isort --check-only src/
	poetry run flake8 src/ --max-line-length=100
	poetry run mypy src/lokal
	@echo "✅ All linters passed!"

format:
	@echo "Formatting code..."
	poetry run black src/
	poetry run isort src/
	@echo "✅ Done!"

type:
	@echo "Type checking..."
	poetry run mypy src/lokal --pretty

clean:
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov/ dist/ build/
	@echo "✅ Done!"

cli:
	@poetry run lokal
