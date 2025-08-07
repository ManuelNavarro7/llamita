#!/bin/bash

# Voice Assistant Runner Script
# This script creates a fresh virtual environment and runs the voice assistant
# Works like a virtual machine - isolated and self-contained

set -e  # Exit on any error

echo "🦙 Starting Llamita Voice Assistant (Virtual Environment Mode)"
echo "=============================================================="

# Remove existing virtual environment to ensure fresh start
if [ -d ".venv" ]; then
    echo "🧹 Removing existing virtual environment..."
    rm -rf .venv
fi

# Create fresh virtual environment
echo "🔧 Creating fresh virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ".venv/bin/activate"

# Install dependencies in the fresh environment
echo "📦 Installing dependencies in virtual environment..."
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

# Run the voice assistant from the src directory
echo "🚀 Starting Llamita..."
echo ""
echo "💡 Tips:"
echo "   - Click 'Start Listening' to begin"
echo "   - Click 'Stop Speaking' to interrupt AI speech"
echo "   - Close the window to exit"
echo ""
cd src && python3 voice_assistant.py
