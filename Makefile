# 🧪 Cats API - Development Commands
.PHONY: install test test-cov test-quick help clean dev

# Default target
help:
	@echo "🐱 Cats API - Available Commands:"
	@echo ""
	@echo "  make install      - Install dependencies from pyproject.toml"
	@echo "  make test-quick   - Run tests without coverage (fastest)"
	@echo "  make test         - Run all tests with coverage"
	@echo "  make test-cov     - Run tests with detailed coverage report"
	@echo "  make clean        - Clean cache files and build artifacts"
	@echo "  make dev          - Start development server"
	@echo "  make help         - Show this help message"
	@echo ""
	@echo "📋 Prerequisites:"
	@echo "  - Python 3.11+"
	@echo "  - docker-compose up mongodb -d"
	@echo ""

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	@pip install --upgrade pip
	@python -c "import tomllib; f=open('pyproject.toml','rb'); data=tomllib.load(f); f.close(); open('requirements.tmp','w').write('\n'.join(data['project']['dependencies']))"
	@pip install -r requirements.tmp
	@rm requirements.tmp
	@echo "✅ Dependencies installed!"

# Quick tests without coverage (fastest)
test-quick:
	@echo "⚡ Running Cats API Tests (Quick)..."
	@python -m pytest tests/ -v --tb=short
	@echo "✅ Tests completed!"

# All tests with coverage
test:
	@echo "🧪 Running Cats API Tests with Coverage..."
	@python -m pytest tests/ --cov=app --cov-report=term-missing -v
	@echo "✅ All tests passed!"

# Detailed coverage tests
test-cov:
	@echo "📊 Running Tests with Detailed Coverage..."
	@python -m pytest tests/ --cov=app --cov-report=term-missing --cov-report=term:skip-covered -v
	@echo "✅ Coverage tests complete!"

# Clean cache and build files
clean:
	@echo "🧹 Cleaning cache and build files..."
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/ 2>/dev/null || true
	@echo "✅ Cleanup complete!"

# Start development server
dev:
	@echo "🚀 Starting development server..."
	@uvicorn main:app --reload --host 0.0.0.0 --port 8000
