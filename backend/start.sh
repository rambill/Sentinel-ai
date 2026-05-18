#!/bin/bash
# SentinelAI Backend Startup Script (Linux/Mac)
# This script activates the virtual environment and starts the FastAPI server

echo "========================================"
echo "  SentinelAI Backend Server"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created!"
    echo ""
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
echo "🔄 Checking dependencies..."
if ! pip list | grep -q "fastapi"; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed!"
    echo ""
fi

# Start the server
echo ""
echo "========================================"
echo "  🚀 Starting FastAPI Server"
echo "========================================"
echo ""
echo "📍 Server URL: http://localhost:8000"
echo "📚 API Docs:   http://localhost:8000/docs"
echo "💚 Health:     http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
