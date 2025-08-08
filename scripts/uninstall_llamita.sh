#!/bin/bash

# Llamita Uninstall Script
# This script removes Llamita from Applications, Desktop, and cleans up

set -e  # Exit on any error

echo "🗑️  Llamita Uninstall Script"
echo "============================"
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

# Function to check if file/directory exists and remove it
safe_remove() {
    if [ -e "$1" ]; then
        print_status "Removing: $1"
        rm -rf "$1"
        print_success "Removed: $1"
    else
        print_warning "Not found: $1"
    fi
}

echo "This script will remove Llamita from your system."
echo ""

# Ask for confirmation
read -p "Are you sure you want to uninstall Llamita? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Uninstall cancelled"
    exit 0
fi

echo ""
print_status "Starting uninstall process..."

# Step 1: Remove from Applications
print_status "Step 1: Removing from Applications..."
safe_remove "/Applications/Llamita.app"

# Step 2: Remove desktop alias
print_status "Step 2: Removing desktop shortcut..."
safe_remove "$HOME/Desktop/Llamita"

# Step 3: Remove from Dock (if present)
print_status "Step 3: Checking Dock..."
if defaults read com.apple.dock persistent-apps | grep -q "Llamita"; then
    print_warning "Llamita found in Dock. Please remove it manually by dragging it out of the Dock."
else
    print_success "Llamita not found in Dock"
fi

# Step 4: Remove build files (if in llamita directory)
if [ -f "setup.py" ]; then
    print_status "Step 4: Cleaning build files..."
    safe_remove "build"
    safe_remove "dist"
    print_success "Build files cleaned!"
else
    print_warning "Not in llamita directory - skipping build file cleanup"
fi

# Step 5: Remove from Spotlight index
print_status "Step 5: Updating Spotlight index..."
sudo mdutil -E /Applications > /dev/null 2>&1 || true

# Step 6: Final cleanup
print_status "Step 6: Final cleanup..."

# Remove any remaining references
if [ -d "$HOME/.Trash/Llamita.app" ]; then
    print_status "Cleaning Trash..."
    rm -rf "$HOME/.Trash/Llamita.app"
fi

echo ""
echo "🎉 Uninstall Complete!"
echo "====================="
echo ""
print_success "Llamita has been completely removed from your system!"
echo ""
echo "✅ Removed from:"
echo "   - Applications folder"
echo "   - Desktop shortcut"
echo "   - Build files (if in llamita directory)"
echo ""
echo "💡 Note:"
echo "   - Ollama and models were NOT removed (you might want to keep them)"
echo "   - If you added Llamita to Dock, please remove it manually"
echo "   - If you want to remove Ollama too, run: brew uninstall ollama"
echo ""
print_success "Uninstall completed successfully!"
