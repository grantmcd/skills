#!/bin/bash
set -e

echo "🔍 Running Quality Checks..."

# Python Linting and Formatting
echo "🐍 Checking Python scripts with ruff..."
ruff check .
ruff format --check .

# HTML/JS Formatting
echo "✨ Checking UI files with prettier..."
npx prettier --check "**/ui/*.html"

echo "✅ All quality checks passed!"
