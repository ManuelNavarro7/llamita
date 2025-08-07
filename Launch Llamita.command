#!/bin/bash

echo "🦙 Llamita Launcher"
echo "=================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 Script directory: $SCRIPT_DIR"

# Check if we're in the right directory
if [ ! -d "$SCRIPT_DIR/dist" ]; then
    echo "❌ dist folder not found in $SCRIPT_DIR"
    echo "Please run this script from the main Llamita directory"
    exit 1
fi

# Check if the app exists
if [ ! -d "$SCRIPT_DIR/dist/Llamita.app" ]; then
    echo "❌ Llamita.app not found in dist folder"
    echo "Please run './build_app.sh' first to build the app"
    exit 1
fi

echo "✅ Llamita.app found"

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

# Set the working directory to the app bundle
cd "$SCRIPT_DIR/dist/Llamita.app/Contents/Resources"

echo "🦙 Starting Llamita..."
echo "📁 Working directory: $(pwd)"

# Run the app with full error output
echo "🚀 Launching app..."
./../MacOS/Llamita 2>&1

echo "👋 Llamita exited"
