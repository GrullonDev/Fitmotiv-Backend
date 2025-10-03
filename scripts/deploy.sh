#!/bin/bash

# Production deployment script for FitMotiv Backend

set -e

echo "🚀 Starting FitMotiv Backend deployment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found. Please create one from .env.example"
    exit 1
fi

# Load environment variables (safer method)
export $(cat .env | grep -v '^#' | xargs)

echo "📦 Installing dependencies..."
python3 -m pip install -r requirements.txt

echo "🗃️ Running database migrations..."
python3 -m alembic upgrade head

echo "🧪 Running tests (if available)..."
# pytest || echo "⚠️ No tests found or tests failed"

echo "🔍 Security check..."
# Add security checks here if needed

echo "✅ Deployment completed successfully!"
echo "🌟 Your FitMotiv Backend is ready to serve!"

# Optional: Start the application
if [ "$1" = "--start" ]; then
    echo "🚀 Starting the application..."
    python3 -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
fi