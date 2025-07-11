# 🧪 Cats API - Custom Commands
.PHONY: test test-cov help

# Default target
help:
	@echo "🐱 Cats API - Available Commands:"
	@echo ""
	@echo "  make test         - Run all functional tests (100% pass rate)"
	@echo "  make test-cov     - Run tests with detailed coverage"
	@echo "  make help         - Show this help message"
	@echo ""

# All functional tests
test:
	@echo "🧪 Running Cats API Functional Tests..."
	@.venv/bin/python -m pytest tests/ -v
	@echo "✅ All tests passed - 100% success rate!"

# Detailed coverage tests
test-cov:
	@echo "📊 Running Tests with Detailed Coverage..."
	@.venv/bin/python -m pytest tests/ --cov=app --cov-report=term-missing -v
	@echo "✅ Coverage tests complete!"
