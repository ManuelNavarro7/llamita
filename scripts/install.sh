#!/bin/bash

# Voice Assistant Installation Script for macOS
# This script automates the installation process

set -e  # Exit on any error

echo "🧠 Voice Assistant Installation Script"
echo "====================================="
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo "✅ Homebrew installed successfully"
else
    echo "✅ Homebrew is already installed"
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Installing Python..."
    brew install python
    echo "✅ Python installed successfully"
else
    echo "✅ Python 3 is already installed"
fi

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install Ollama from https://ollama.com/download"
    echo "After installing Ollama, run this script again."
    exit 1
else
    echo "✅ Ollama is already installed"
fi

# Install PortAudio
echo "📦 Installing PortAudio..."
brew install portaudio
echo "✅ PortAudio installed successfully"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt
echo "✅ Python dependencies installed successfully"

# Install document processing dependencies
echo "📦 Installing document processing dependencies..."
pip3 install PyPDF2>=3.0.0 python-docx>=0.8.11 pandas>=2.0.0 openpyxl>=3.1.0 Pillow>=10.0.0
echo "✅ Document processing dependencies installed successfully"

# Check if Ollama is running
echo "🔍 Checking if Ollama is running..."
if curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "✅ Ollama is running"
else
    echo "⚠️  Ollama is not running. Starting Ollama..."
    ollama serve &
    sleep 5
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo "✅ Ollama started successfully"
    else
        echo "❌ Failed to start Ollama. Please start it manually: ollama serve"
    fi
fi

# Check if llama3:8b model is available
echo "🔍 Checking for llama3:8b model..."
if ollama list | grep -q "llama3:8b"; then
    echo "✅ llama3:8b model is available"
else
    echo "📥 Downloading llama3:8b model (this may take a while)..."
    ollama pull llama3:8b
    echo "✅ llama3:8b model downloaded successfully"
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "To run the voice assistant:"
echo "  python3 voice_assistant.py"
echo ""
echo "To build the macOS app:"
echo "  python3 setup.py py2app"
echo ""
echo "📄 Document Processing:"
echo "  • Upload documents via the GUI"
echo "  • Ask questions about your files"
echo "  • Supported: PDF, DOCX, TXT, CSV, Excel"
echo ""
echo "Happy voice assisting! 🎤✨"
