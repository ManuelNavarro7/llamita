#!/bin/bash

# Llamita Installation Verification Script
# This script checks if all components are properly installed

set -e  # Exit on any error

echo "🔍 Llamita Installation Verification"
echo "===================================="
echo ""

# Check Python
echo "🐍 Checking Python..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    echo "✅ Python found: $python_version"
else
    echo "❌ Python 3 not found. Please install Python 3.7+"
    exit 1
fi

# Check if src directory exists
echo "📁 Checking source files..."
if [ -d "src" ] && [ -f "src/voice_assistant.py" ] && [ -f "src/config.py" ]; then
    echo "✅ Source files found"
else
    echo "❌ Source files missing. Make sure you're in the correct directory"
    exit 1
fi

# Check Python dependencies
echo "📦 Checking Python dependencies..."
python3 -c "
import sys
import importlib

required_modules = ['tkinter', 'requests', 'json', 'threading', 'time', 'subprocess', 'os', 'datetime']

missing_modules = []
for module in required_modules:
    try:
        importlib.import_module(module)
    except ImportError:
        missing_modules.append(module)

if missing_modules:
    print(f'❌ Missing modules: {missing_modules}')
    print('Run: pip3 install -r requirements.txt')
    sys.exit(1)
else:
    print('✅ All required modules found')
"

# Check if scripts are executable
echo "🔧 Checking scripts..."
if [ -x "scripts/run_simple.sh" ] && [ -x "scripts/run_voice_assistant.sh" ]; then
    echo "✅ Scripts are executable"
else
    echo "⚠️  Making scripts executable..."
    chmod +x scripts/*.sh
    echo "✅ Scripts made executable"
fi

# Check Ollama
echo "🤖 Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama found"
else
    echo "❌ Ollama not found. Please install Ollama from https://ollama.ai"
    exit 1
fi

# Check if Ollama is running
echo "🔍 Checking if Ollama is running..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
    
    # Check for models
    models=$(curl -s http://localhost:11434/api/tags | python3 -c "import sys, json; data=json.load(sys.stdin); print('Available models:', [m['name'] for m in data.get('models', [])])")
    echo "📋 $models"
else
    echo "⚠️  Ollama is not running"
    echo "   Start Ollama with: ollama serve"
    echo "   Then download a model with: ollama pull llama3:8b"
fi

# Test the application
echo "🧪 Testing application..."
if PYTHONPATH=src python3 -c "import voice_assistant; print('✅ Application imports successfully')" 2>/dev/null; then
    echo "✅ Application test passed"
else
    echo "❌ Application test failed"
    echo "   Try running: PYTHONPATH=src python3 src/voice_assistant.py"
fi

echo ""
echo "🎉 Verification complete!"
echo ""
echo "If all checks passed, you can run Llamita with:"
echo "   ./scripts/run_simple.sh"
echo ""
echo "If you see any ❌ errors, please fix them before running Llamita."
