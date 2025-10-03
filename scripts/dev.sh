#!/bin/bash

# Development server script for FitMotiv Backend

echo "🚀 Starting FitMotiv Backend in development mode..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️ Warning: .env file not found. Using default settings..."
fi

# Start the development server
echo "🔥 Starting development server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"

python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000