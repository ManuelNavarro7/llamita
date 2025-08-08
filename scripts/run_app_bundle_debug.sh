#!/bin/bash

echo "🔍 Running App Bundle with Debug Output"
echo "======================================="
echo ""

if [ -d "dist/Llamita.app" ]; then
    echo "✅ App bundle found"
    echo "🚀 Running from terminal to see debug output..."
    echo ""
    
    # Run the app bundle from terminal to see output
    ./dist/Llamita.app/Contents/MacOS/Llamita
    
    echo ""
    echo "✅ App bundle execution completed"
    echo "Check the output above for any error messages"
    
else
    echo "❌ App bundle not found: dist/Llamita.app"
    echo "Build it first with: python3 setup.py py2app"
fi
