#!/bin/bash

# Isolated Voice Assistant Setup
# This script sets up everything needed without affecting your system Python

set -e  # Exit on any error

echo "🏝️ Isolated Voice Assistant Setup"
echo "================================="
echo "This setup won't affect your system Python installation"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found."
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

# Check if Homebrew is available for PortAudio
if ! command -v brew &> /dev/null; then
    echo "⚠️  Homebrew not found. Installing PortAudio manually..."
    echo "Please install Homebrew first:"
    echo "/bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Install PortAudio (required for microphone access)
echo "📦 Installing PortAudio..."
brew install portaudio

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install Ollama from:"
    echo "https://ollama.com/download"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Check if Ollama is running
echo "🤖 Checking Ollama status..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running. Starting Ollama..."
    ollama serve &
    sleep 5
    
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "❌ Failed to start Ollama. Please start it manually:"
        echo "ollama serve"
        exit 1
    fi
fi

# Check if required model is available
echo "📚 Checking for llama3:8b model..."
if ! ollama list | grep -q "llama3:8b"; then
    echo "📥 Downloading llama3:8b model (this may take a while)..."
    ollama pull llama3:8b
fi

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "🎯 Your system is now ready for isolated voice assistant operation."
echo ""
echo "To run the voice assistant:"
echo "  ./run_voice_assistant.sh"
echo ""
echo "To stop and clean up:"
echo "  ./stop_app.sh"
echo ""
echo "💡 The app will create a fresh virtual environment each time it runs,"
echo "   just like a virtual machine!"
