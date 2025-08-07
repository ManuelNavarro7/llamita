#!/bin/bash

# Simple Voice Assistant Runner Script
# This script runs the voice assistant from the root directory

set -e  # Exit on any error

echo "🦙 Starting Llamita Voice Assistant (Simple Mode)"
echo "=================================================="

# Check if Ollama is running
echo "🤖 Checking Ollama status..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running. Please start Ollama first:"
    echo "   ollama serve"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Run the voice assistant with src directory in Python path
echo "🚀 Starting Llamita..."
echo ""
echo "💡 Tips:"
echo "   - Click 'Start Listening' to begin"
echo "   - Click 'Stop Speaking' to interrupt AI speech"
echo "   - Close the window to exit"
echo ""
PYTHONPATH=src python3 src/voice_assistant.py
