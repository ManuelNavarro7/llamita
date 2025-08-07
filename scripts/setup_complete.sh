#!/bin/bash

echo "🦙 Complete Llamita Setup"
echo "========================="
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed."
    echo ""
    echo "📦 Installing Ollama..."
    echo "Please install Ollama from: https://ollama.ai"
    echo "Or run: brew install ollama"
    echo ""
    echo "After installing Ollama, run this script again."
    exit 1
fi

echo "✅ Ollama is installed"

# Start Ollama if not running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "🚀 Starting Ollama..."
    ollama serve &
    sleep 5
fi

# Check if model is already installed
MODEL_NAME=$(grep 'DEFAULT_MODEL' config.py | cut -d'"' -f2)
echo "📦 Checking for model: $MODEL_NAME"

if curl -s http://localhost:11434/api/tags | grep -q "$MODEL_NAME"; then
    echo "✅ Model $MODEL_NAME is already installed"
else
    echo "📥 Downloading model $MODEL_NAME..."
    echo "This may take a few minutes depending on your internet speed."
    ollama pull $MODEL_NAME
fi

# Make scripts executable
echo "🔧 Setting up scripts..."
chmod +x run_voice_assistant.sh
chmod +x "Launch Llamita.command"
chmod +x setup_lightweight_model.sh

# Test the setup
echo "🧪 Testing Llamita setup..."
if curl -s -X POST http://localhost:11434/api/generate \
   -H "Content-Type: application/json" \
   -d "{\"model\":\"$MODEL_NAME\",\"prompt\":\"Hello\",\"stream\":false}" > /dev/null 2>&1; then
    echo "✅ Everything is working!"
    echo ""
    echo "🎉 Llamita is ready to use!"
    echo ""
    echo "🚀 To start Llamita:"
    echo "   ./run_voice_assistant.sh"
    echo "   or double-click 'Launch Llamita.command'"
    echo ""
    echo "📁 This folder now contains everything needed:"
    echo "   ✅ Llamita application"
    echo "   ✅ Model downloaded and ready"
    echo "   ✅ All scripts and configuration"
    echo "   ✅ Setup instructions"
    echo ""
    echo "🔄 To share with others:"
    echo "   1. Copy this entire folder"
    echo "   2. They run: ./setup_complete.sh"
    echo "   3. That's it!"
else
    echo "❌ Something went wrong. Please check the error messages above."
fi
