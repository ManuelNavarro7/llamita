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

# Step 3: Install Python dependencies
print_status "Step 3: Installing Python dependencies..."

if ! pip3 show py2app &> /dev/null; then
    print_warning "Installing py2app..."
    pip3 install py2app
fi

if ! pip3 show requests &> /dev/null; then
    print_warning "Installing requests..."
    pip3 install requests
fi

print_success "Dependencies installed!"

# Step 4: Build the app
print_status "Step 4: Building Llamita app..."

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

# Step 5: Install to Applications
print_status "Step 5: Installing to Applications..."

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

# Step 6: Create desktop alias
print_status "Step 6: Creating desktop shortcut..."

# Remove existing alias if it exists
rm -f ~/Desktop/Llamita

# Create new alias
ln -sf /Applications/Llamita.app ~/Desktop/Llamita

print_success "Desktop shortcut created!"

# Step 7: Final instructions
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
echo "💡 To uninstall later, run: ./scripts/uninstall_llamita.sh"
echo ""
print_success "Installation completed successfully!"
