#!/bin/bash

echo "🧪 Testing App Bundle Loading Screen"
echo "===================================="
echo ""

# Check if app bundle exists
if [ ! -d "dist/Llamita.app" ]; then
    echo "❌ App bundle not found. Building it first..."
    echo "Running: python3 setup.py py2app"
    python3 setup.py py2app
    echo ""
fi

if [ -d "dist/Llamita.app" ]; then
    echo "✅ App bundle found: dist/Llamita.app"
    echo ""
    
    echo "🔍 Checking app bundle contents..."
    echo "Main executable:"
    ls -la dist/Llamita.app/Contents/MacOS/
    echo ""
    
    echo "Python modules:"
    ls -la dist/Llamita.app/Contents/Resources/lib/python*/site-packages/ | head -10
    echo ""
    
    echo "🚀 Testing app bundle execution..."
    echo "Running: open dist/Llamita.app"
    echo "Expected: Should show loading screen"
    echo ""
    
    # Run the app bundle
    open dist/Llamita.app
    
    echo "⏰ App bundle launched. Check if loading screen appears."
    echo "If no loading screen appears, check Console.app for errors."
    echo ""
    
    echo "💡 Debugging tips:"
    echo "1. Open Console.app and filter for 'Llamita'"
    echo "2. Look for any error messages"
    echo "3. Check if PIL/Pillow is included in the bundle"
    echo "4. Try running from terminal: ./dist/Llamita.app/Contents/MacOS/Llamita"
    
else
    echo "❌ Failed to build app bundle"
    echo "Check the build output above for errors"
fi
