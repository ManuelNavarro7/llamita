#!/bin/bash

# Voice Assistant Stop Script
# This script stops the voice assistant and completely cleans up the virtual environment

echo "🛑 Stopping Llamita (Complete Cleanup)"
echo "========================================"

# Stop the voice assistant processes
echo "🔇 Stopping voice assistant..."
pkill -f "voice_assistant.py" 2>/dev/null || echo "No voice assistant processes found"

# Stop speech processes
echo "🔇 Stopping speech processes..."
pkill -f "say" 2>/dev/null || echo "No speech processes found"

# Stop voicebankingd
echo "🗣️ Stopping voicebankingd..."
pkill -f "voicebankingd" 2>/dev/null || echo "No voicebankingd process found"

# Deactivate virtual environment
echo "🔧 Deactivating virtual environment..."
deactivate 2>/dev/null || echo "Virtual environment already deactivated"

# Remove the virtual environment completely
echo "🧹 Removing virtual environment..."
if [ -d ".venv" ]; then
    rm -rf .venv
    echo "✅ Virtual environment removed"
else
    echo "✅ No virtual environment to remove"
fi

echo ""
echo "✅ Complete cleanup finished!"
echo ""
echo "🎯 Next time you run Llamita, it will:"
echo "   - Create a fresh virtual environment"
echo "   - Install dependencies from scratch"
echo "   - Work like a virtual machine"
echo ""
echo "To start again, run: ./run_voice_assistant.sh"
