#!/bin/bash

echo "🦙 Llamita Development Launcher"
echo "=============================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
echo "📁 Project directory: $PROJECT_DIR"

# Change to project directory
cd "$PROJECT_DIR"

# Check if source files exist
if [ ! -f "src/voice_assistant.py" ]; then
    echo "❌ voice_assistant.py not found in src/ folder"
    exit 1
fi

echo "✅ Source files found"

# Check if Ollama is running
echo "🔍 Checking if Ollama is running..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
else
    echo "⚠️  Ollama is not running"
    echo "Starting Ollama..."
    ollama serve &
    sleep 3
fi

# Run the app in development mode
echo "🦙 Starting Llamita in development mode..."
echo "📁 Working directory: $(pwd)"

# Run the app directly with Python
python3 src/voice_assistant.py

echo "👋 Llamita exited"
