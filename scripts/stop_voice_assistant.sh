#!/bin/bash

# Voice Assistant Process Cleanup Script
# This script stops any lingering voice assistant processes

echo "🧹 Voice Assistant Process Cleanup"
echo "=================================="
echo ""

# Stop Python voice assistant processes
echo "🔄 Stopping Python voice assistant processes..."
pkill -f "voice_assistant.py" 2>/dev/null || echo "No voice assistant Python processes found"

# Stop speech processes
echo "🔇 Stopping speech processes..."
pkill -f "say" 2>/dev/null || echo "No speech processes found"

# Stop voicebankingd
echo "🗣️ Stopping voicebankingd..."
pkill -f "voicebankingd" 2>/dev/null || echo "No voicebankingd process found"

# Stop any tkinter processes
echo "🖥️ Stopping GUI processes..."
pkill -f "tkinter" 2>/dev/null || echo "No tkinter processes found"

# Check if any processes are still running
echo ""
echo "🔍 Checking for remaining processes..."
if pgrep -f "voice_assistant" > /dev/null; then
    echo "⚠️ Some voice assistant processes are still running:"
    pgrep -f "voice_assistant" | xargs ps -p
else
    echo "✅ No voice assistant processes found"
fi

if pgrep -f "say" > /dev/null; then
    echo "⚠️ Some speech processes are still running:"
    pgrep -f "say" | xargs ps -p
else
    echo "✅ No speech processes found"
fi

echo ""
echo "🎉 Cleanup completed!"
echo ""
echo "If you still have issues, you can:"
echo "1. Restart your computer"
echo "2. Use Activity Monitor to manually kill processes"
echo "3. Check System Preferences > Security & Privacy > Privacy > Microphone"
