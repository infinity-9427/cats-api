# 🧪 Cats API - Custom Commands
.PHONY: test test-cov test-quick help

# Default target
help:
	@echo "🐱 Cats API - Available Commands:"
	@echo ""
	@echo "  make test-quick   - Run tests without coverage (fastest)"
	@echo "  make test         - Run all tests with coverage"
	@echo "  make test-cov     - Run tests with detailed coverage report"
	@echo "  make help         - Show this help message"
	@echo ""
	@echo "📋 Prerequisites:"
	@echo "  - pip install -r requirements.txt"
	@echo "  - docker-compose up mongodb -d"
	@echo ""

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
	@echo "📊 Running Tests with Detailed Coverage Report..."
	@python -m pytest tests/ --cov=app --cov-report=term-missing --cov-report=html -v
	@echo "✅ Coverage report generated in htmlcov/"
