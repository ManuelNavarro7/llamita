#!/bin/bash

echo "🦙 Building Llamita macOS App"
echo "=============================="
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is for macOS only"
    exit 1
fi

# Check if Python is installed
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

# Create a simple icon if it doesn't exist
if [ ! -f "assets/icons/llamita_icon.icns" ]; then
    echo "🎨 Creating default icon..."
    python3 assets/icons/create_icon.py
    
    # Convert to ICNS (macOS icon format)
    if command -v iconutil &> /dev/null; then
        echo "🔄 Converting to ICNS format..."
        iconutil -c icns assets/icons/llamita.iconset
        rm -rf assets/icons/llamita.iconset
        echo "✅ Icon converted to ICNS format"
    else
        echo "⚠️ Could not convert to ICNS, using PNG"
        mv assets/icons/llamita_icon.png assets/icons/llamita_icon.icns
    fi
fi

# Build the app
echo "🔨 Building Llamita app..."
python3 setup.py py2app

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Llamita app built successfully!"
    echo ""
    echo "📁 App location: dist/Llamita.app"
    echo ""
    echo "🚀 To run the app:"
    echo "   open dist/Llamita.app"
    echo ""
    echo "📋 To install to Applications:"
    echo "   cp -r dist/Llamita.app /Applications/"
    echo ""
    echo "🎉 Llamita is now a proper macOS app!"
else
    echo "❌ Build failed. Please check the error messages above."
    exit 1
fi
