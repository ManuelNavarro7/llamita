#!/bin/bash

echo "🦙 Setting up lightweight models for Llamita"
echo "============================================="
echo ""

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama is not running. Please start Ollama first:"
    echo "   ollama serve"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "✅ Ollama is running"
echo ""

# Recommended lightweight models
echo "📦 Recommended lightweight models for Llamita:"
echo ""

echo "1. llama3.2:3b (RECOMMENDED) - Fast and capable"
echo "   Download: ollama pull llama3.2:3b"
echo "   Size: ~2GB"
echo ""

echo "2. llama3.2:1b - Ultra-fast"
echo "   Download: ollama pull llama3.2:1b"
echo "   Size: ~1GB"
echo ""

echo "3. gemma2:2b - Efficient and fast"
echo "   Download: ollama pull gemma2:2b"
echo "   Size: ~1.5GB"
echo ""

echo "4. phi3:mini - Microsoft's lightweight model"
echo "   Download: ollama pull phi3:mini"
echo "   Size: ~1.5GB"
echo ""

echo "🚀 Quick setup:"
echo "   ollama pull llama3.2:3b"
echo "   # Then update config.py to use 'llama3.2:3b'"
echo ""

echo "💡 Current model in config: $(grep 'DEFAULT_MODEL' config.py | cut -d'"' -f2)"
echo ""

# Test current model
echo "🧪 Testing current model..."
if curl -s -X POST http://localhost:11434/api/generate \
   -H "Content-Type: application/json" \
   -d '{"model":"llama3.2:3b","prompt":"Hello, how are you?","stream":false}' > /dev/null 2>&1; then
    echo "✅ Current model is working!"
else
    echo "⚠️ Current model not available. Please download a model first."
fi

echo ""
echo "🎯 To change models, edit config.py and change DEFAULT_MODEL"
echo "🦙 Then restart Llamita to use the new model!"
