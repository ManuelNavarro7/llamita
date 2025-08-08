#!/bin/bash

# Llamita Complete Installation Script
# This script installs everything needed to run Llamita, including Ollama

set -e  # Exit on any error

echo "🦙 Llamita Complete Installation Script"
echo "======================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS. Please install manually on other systems."
    exit 1
fi

print_info "Starting complete installation for Llamita..."

# Step 1: Check/Install Homebrew
echo ""
print_info "Step 1: Checking Homebrew..."
if ! command -v brew &> /dev/null; then
    print_warning "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    print_status "Homebrew installed successfully"
else
    print_status "Homebrew is already installed"
fi

# Step 2: Check/Install Python
echo ""
print_info "Step 2: Checking Python..."
if ! command -v python3 &> /dev/null; then
    print_warning "Python 3 not found. Installing Python..."
    brew install python
    print_status "Python installed successfully"
else
    python_version=$(python3 --version)
    print_status "Python found: $python_version"
fi

# Step 3: Check/Install Ollama
echo ""
print_info "Step 3: Checking Ollama..."
if ! command -v ollama &> /dev/null; then
    print_warning "Ollama not found. Installing Ollama..."
    
    # Try Homebrew first
    if brew install ollama 2>/dev/null; then
        print_status "Ollama installed via Homebrew"
    else
        print_warning "Homebrew installation failed, trying direct download..."
        
        # Download and install Ollama directly
        curl -fsSL https://ollama.ai/install.sh | sh
        print_status "Ollama installed via direct download"
    fi
else
    ollama_version=$(ollama --version)
    print_status "Ollama found: $ollama_version"
fi

# Step 4: Clone repository if not already in it
echo ""
print_info "Step 4: Setting up repository..."
if [ ! -f "src/voice_assistant.py" ] && [ ! -f "requirements.txt" ]; then
    print_info "Cloning Llamita repository..."
    git clone https://github.com/ManuelNavarro7/llamita.git
    cd llamita
    print_status "Repository cloned successfully"
else
    print_status "Repository already present"
fi

# Step 5: Install Python dependencies
echo ""
print_info "Step 5: Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    # Install only the packages that can be installed via pip
    pip3 install requests SpeechRecognition PyAudio py2app
    print_status "Python dependencies installed"
else
    print_warning "requirements.txt not found, installing basic dependencies..."
    pip3 install requests
    print_status "Basic Python dependencies installed"
fi

# Install document processing dependencies
echo ""
print_info "Step 5.5: Installing document processing dependencies..."
pip3 install PyPDF2>=3.0.0 python-docx>=0.8.11 pandas>=2.0.0 openpyxl>=3.1.0
print_status "Document processing dependencies installed"

# Step 6: Make scripts executable
echo ""
print_info "Step 6: Making scripts executable..."
chmod +x scripts/*.sh 2>/dev/null || true
print_status "Scripts made executable"

# Step 7: Start Ollama and download model
echo ""
print_info "Step 7: Starting Ollama and downloading model..."

# Check if Ollama is already running
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    print_status "Ollama is already running"
else
    print_info "Starting Ollama..."
    ollama serve > /dev/null 2>&1 &
    OLLAMA_PID=$!
    
    # Wait for Ollama to start
    print_info "Waiting for Ollama to start..."
    for i in {1..30}; do
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            print_status "Ollama started successfully"
            break
        fi
        if [ $i -eq 30 ]; then
            print_error "Ollama failed to start within 30 seconds"
            exit 1
        fi
        sleep 1
    done
fi

# Check for models
echo ""
print_info "Checking for available models..."
models=$(curl -s http://localhost:11434/api/tags | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    models = [m['name'] for m in data.get('models', [])]
    print('Available models:', models)
    if not models:
        print('No models found')
except:
    print('Could not parse models')
" 2>/dev/null)

if echo "$models" | grep -q "llama3:8b\|llama3.2:3b\|llama3.2:1b"; then
    print_status "Model already available"
else
    print_info "Downloading llama3:8b model (this may take a while)..."
    ollama pull llama3:8b
    print_status "Model downloaded successfully"
fi

# Step 8: Test the installation
echo ""
print_info "Step 8: Testing installation..."
if python3 -c "import tkinter; import requests; print('✅ Dependencies OK')" 2>/dev/null; then
    print_status "Python dependencies test passed"
else
    print_error "Python dependencies test failed"
    exit 1
fi

if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    print_status "Ollama connection test passed"
else
    print_error "Ollama connection test failed"
    exit 1
fi

# Step 9: Final verification
echo ""
print_info "Step 9: Running final verification..."
if [ -f "scripts/verify_installation.sh" ]; then
    ./scripts/verify_installation.sh
else
    print_warning "Verification script not found, skipping"
fi

echo ""
print_status "🎉 Installation completed successfully!"
echo ""
echo "🚀 To run Llamita:"
echo "   ./scripts/run_simple.sh"
echo ""
echo "📄 Document Processing:"
echo "   • Upload documents via the GUI"
echo "   • Ask questions about your files"
echo "   • Supported: PDF, DOCX, TXT, CSV, Excel"
echo ""
echo "💡 Tips:"
echo "   • Ollama is now running in the background"
echo "   • To stop Ollama: pkill ollama"
echo "   • To restart Ollama: ollama serve"
echo "   • To download more models: ollama pull <model-name>"
echo ""
echo "🦙 Happy chatting with Llamita! ✨"
