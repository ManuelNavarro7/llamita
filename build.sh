#!/bin/bash

# Voice Assistant Build Script for macOS
# This script builds the macOS .app bundle

set -e  # Exit on any error

echo "🏗️ Voice Assistant Build Script"
echo "=============================="
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is designed for macOS only"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if py2app is installed
if ! python3 -c "import py2app" &> /dev/null; then
    echo "📦 Installing py2app..."
    pip3 install py2app
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist
echo "✅ Cleaned previous builds"

# Run tests first
echo "🧪 Running setup tests..."
python3 test_setup.py

# Build the app
echo "🏗️ Building the app..."
python3 setup.py py2app

    # Check if build was successful
    if [ -d "dist/Llamita.app" ]; then
        echo "✅ Build successful!"
        echo ""
        echo "📱 Your app is ready at: dist/Llamita.app"
        echo ""
        echo "To run the app:"
        echo "  open 'dist/Llamita.app'"
        echo ""
        echo "To copy to Applications:"
        echo "  cp -r 'dist/Llamita.app' /Applications/"
    echo ""
    echo "🎉 Happy voice assisting! 🎤✨"
else
    echo "❌ Build failed. Check the error messages above."
    exit 1
fi
