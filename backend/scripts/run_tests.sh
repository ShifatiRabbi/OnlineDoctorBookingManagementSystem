#!/bin/bash

# Exit on error
set -e

echo "🧪 Running Django Tests..."

# Set environment
export DJANGO_SETTINGS_MODULE=config.settings
export PYTHONPATH=.

# Run migrations
echo "🗄️ Running migrations..."
python manage.py migrate

# Run tests with coverage
echo "📊 Running tests with coverage..."
pytest --cov=. --cov-report=html --cov-report=xml -v

# Run linting
echo "🔍 Running linting..."
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

echo "✅ All tests passed!"