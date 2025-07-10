#!/bin/bash

# 🧪 Cats API Test Runner
echo "Running tests..."

python -m pytest tests/ --cov=app --cov-report=term-missing

echo "✅ Tests complete - workspace clean!"
