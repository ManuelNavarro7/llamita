#!/bin/bash

# Clean Llamita Runner Script
# This script runs Llamita with suppressed macOS warnings

set -e  # Exit on any error

echo "🦙 Starting Llamita (Clean Mode)"
echo "================================"

# Suppress macOS warnings
export PYTHONUNBUFFERED=1
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# Check if Ollama is running
echo "🤖 Checking Ollama status..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running. Please start Ollama first:"
    echo "   ollama serve"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Run the voice assistant with suppressed warnings
echo "🚀 Starting Llamita..."
echo ""
echo "💡 Tips:"
echo "   - Click 'Start Listening' to begin"
echo "   - Click 'Stop Speaking' to interrupt AI speech"
echo "   - Close the window to exit"
echo ""

# Run with suppressed warnings
PYTHONPATH=src python3 -W ignore src/voice_assistant.py 2>/dev/null
