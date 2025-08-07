#!/bin/bash

# Voice Assistant Runner Script (Persistent Mode)
# This script uses an existing virtual environment if available
# Faster startup, but may have lingering issues

set -e  # Exit on any error

echo "🦙 Starting Llamita Voice Assistant (Persistent Mode)"
echo "====================================================="

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "🔧 Using existing virtual environment..."
else
    echo "🔧 Creating new virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ".venv/bin/activate"

# Install/upgrade dependencies
echo "📦 Checking dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if Ollama is running
echo "🤖 Checking Ollama status..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running. Please start Ollama first:"
    echo "   ollama serve"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Run the voice assistant
echo "🚀 Starting Llamita..."
echo ""
echo "💡 Tips:"
echo "   - Click 'Start Listening' to begin"
echo "   - Click 'Stop Speaking' to interrupt AI speech"
echo "   - Close the window to exit"
echo ""
python3 voice_assistant.py
