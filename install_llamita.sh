#!/bin/bash

echo "🦙 Installing Llamita to Applications"
echo "====================================="
echo ""

# Check if the app exists
if [ ! -d "dist/Llamita.app" ]; then
    echo "❌ Llamita.app not found in dist/ folder"
    echo "Please run './build_app.sh' first to build the app"
    exit 1
fi

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Warning: Ollama is not installed"
    echo "Llamita requires Ollama to work. Please install it from:"
    echo "https://ollama.ai"
    echo ""
    echo "Or run: brew install ollama"
    echo ""
    read -p "Continue with installation anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install to Applications
echo "📦 Installing Llamita to Applications..."
cp -r dist/Llamita.app /Applications/

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Llamita installed successfully!"
    echo ""
    echo "🎉 You can now find Llamita in your Applications folder"
    echo "🚀 Launch it from Spotlight (Cmd+Space) or Applications folder"
    echo ""
    echo "📋 To start Ollama (required for Llamita to work):"
    echo "   ollama serve"
    echo ""
    echo "📋 To download a model:"
    echo "   ollama pull llama3:8b"
    echo ""
    echo "🦙 Enjoy using Llamita!"
else
    echo "❌ Installation failed. Please check permissions."
    echo "Try running with sudo if needed."
fi
