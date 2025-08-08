#!/bin/bash

echo "🧪 Testing Loading Screen in Different Environments"
echo "=================================================="
echo ""

# Test 1: Direct Python run
echo "Test 1: Direct Python run"
echo "Running: python3 src/voice_assistant.py"
echo "Expected: Should show loading screen"
echo ""

# Test 2: App bundle run
echo "Test 2: App bundle run"
if [ -d "dist/Llamita.app" ]; then
    echo "Running: open dist/Llamita.app"
    echo "Expected: Should show loading screen"
else
    echo "App bundle not found. Build it first with: python3 setup.py py2app"
fi
echo ""

# Test 3: Check dependencies
echo "Test 3: Checking dependencies"
echo "PIL/Pillow installed: $(python3 -c "import PIL; print('Yes')" 2>/dev/null || echo 'No')"
echo "Tkinter available: $(python3 -c "import tkinter; print('Yes')" 2>/dev/null || echo 'No')"
echo ""

echo "💡 If loading screen doesn't appear:"
echo "1. Make sure you're running the latest version"
echo "2. Check that all dependencies are installed"
echo "3. Try running directly with: python3 src/voice_assistant.py"
echo "4. Look for any error messages in the terminal"
