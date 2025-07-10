# 🧪 Cats API - Custom Commands
.PHONY: test test-quick test-coverage help

# Default target
help:
	@echo "🐱 Cats API - Available Commands:"
	@echo ""
	@echo "  make test         - Run full test suite with coverage"
	@echo "  make test-quick   - Run tests without coverage (faster)"
	@echo "  make test-cov     - Run tests with detailed coverage"
	@echo "  make help         - Show this help message"
	@echo ""

# Full test suite with coverage
test:
	@echo "🧪 Running Cats API Tests (Full Suite)..."
	@python -m pytest tests/ --cov=app --cov-report=term-missing
	@echo "✅ Tests complete - workspace clean!"

# Quick tests without coverage
test-quick:
	@echo "⚡ Running Quick Tests..."
	@python -m pytest tests/ -q
	@echo "✅ Quick tests complete!"

# Detailed coverage tests
test-cov:
	@echo "📊 Running Tests with Detailed Coverage..."
	@python -m pytest tests/ --cov=app --cov-report=term-missing -v
	@echo "✅ Coverage tests complete!"
