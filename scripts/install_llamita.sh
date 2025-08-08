#!/bin/bash

# Llamita Installation Script
# This script installs Ollama (if needed), builds Llamita, and installs it to Applications

set -e  # Exit on any error

echo "🦙 Llamita Installation Script"
echo "=============================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the llamita directory
if [ ! -f "setup.py" ]; then
    print_error "Please run this script from the llamita directory"
    exit 1
fi

# Step 1: Check and install Ollama
print_status "Step 1: Checking Ollama installation..."

if ! command -v ollama &> /dev/null; then
    print_warning "Ollama not found. Installing Ollama..."
    
    # Install Ollama using the official method
    curl -fsSL https://ollama.ai/install.sh | sh
    
    if command -v ollama &> /dev/null; then
        print_success "Ollama installed successfully!"
    else
        print_error "Failed to install Ollama. Please install it manually from https://ollama.ai"
        exit 1
    fi
else
    print_success "Ollama is already installed"
fi

# Step 2: Start Ollama and download a model
print_status "Step 2: Setting up Ollama and downloading a model..."

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    print_warning "Starting Ollama..."
    ollama serve &
    sleep 5  # Wait for Ollama to start
fi

# Check if we have any models
if ! ollama list | grep -q .; then
    print_warning "No models found. Downloading llama3:8b..."
    ollama pull llama3:8b
    print_success "Model downloaded successfully!"
else
    print_success "Models are already available"
fi

# Step 3: Check and install Python
print_status "Step 3: Checking Python installation..."

if ! command -v python3 &> /dev/null; then
    print_warning "Python 3 not found. Installing Python..."
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        print_warning "Homebrew not found. Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    # Install Python 3
    print_warning "Installing Python 3..."
    brew install python@3.11
    
    if command -v python3 &> /dev/null; then
        print_success "Python 3 installed successfully!"
    else
        print_error "Failed to install Python. Please install it manually from https://python.org"
        exit 1
    fi
else
    print_success "Python 3 is already installed"
fi

# Step 4: Install Python dependencies
print_status "Step 4: Installing Python dependencies..."

if ! pip3 show py2app &> /dev/null; then
    print_warning "Installing py2app..."
    pip3 install py2app
fi

if ! pip3 show requests &> /dev/null; then
    print_warning "Installing requests..."
    pip3 install requests
fi

# Install document processing dependencies (optional but recommended)
print_warning "Installing document processing dependencies..."
pip3 install PyPDF2>=3.0.0 python-docx>=0.8.11 pandas>=2.0.0 openpyxl>=3.1.0

print_success "Dependencies installed!"

# Step 5: Build the app
print_status "Step 5: Building Llamita app..."

# Clean previous builds
rm -rf build dist

# Build the app
python3 setup.py py2app

if [ -d "dist/Llamita.app" ]; then
    print_success "App built successfully!"
else
    print_error "Failed to build the app"
    exit 1
fi

# Step 6: Install to Applications
print_status "Step 6: Installing to Applications..."

# Remove existing app if it exists
if [ -d "/Applications/Llamita.app" ]; then
    print_warning "Removing existing Llamita app..."
    sudo rm -rf /Applications/Llamita.app
fi

# Copy to Applications
sudo cp -R dist/Llamita.app /Applications/

if [ -d "/Applications/Llamita.app" ]; then
    print_success "Llamita installed to Applications!"
else
    print_error "Failed to install to Applications"
    exit 1
fi

# Step 7: Create desktop alias
print_status "Step 7: Creating desktop shortcut..."

# Remove existing alias if it exists
rm -f ~/Desktop/Llamita

# Create new alias
ln -sf /Applications/Llamita.app ~/Desktop/Llamita

print_success "Desktop shortcut created!"

# Step 8: Final instructions
echo ""
echo "🎉 Installation Complete!"
echo "========================"
echo ""
echo "✅ Llamita has been installed to:"
echo "   - Applications: /Applications/Llamita.app"
echo "   - Desktop: ~/Desktop/Llamita"
echo ""
echo "🚀 You can now:"
echo "   - Double-click the Llamita icon on your Desktop"
echo "   - Find Llamita in your Applications folder"
echo "   - Drag it to your Dock for quick access"
echo ""
echo "📄 Document Processing:"
echo "   • Upload documents via the GUI"
echo "   • Ask questions about your files"
echo "   • Supported: PDF, DOCX, TXT, CSV, Excel"
echo ""
echo "💡 To uninstall later, run: ./scripts/uninstall_llamita.sh"
echo ""
print_success "Installation completed successfully!"
