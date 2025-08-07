#!/usr/bin/env python3
"""
Test script for stop speaking functionality
"""

import subprocess
import time
import threading

def test_stop_speaking():
    """Test the stop speaking functionality"""
    print("🧪 Testing Stop Speaking Functionality")
    print("=" * 40)
    
    # Test 1: Start speech and stop it
    print("1. Starting speech...")
    process = subprocess.Popen(['say', 'This is a test of the stop speaking functionality. This should be a long sentence to give us time to stop it.'])
    
    print("2. Waiting 2 seconds...")
    time.sleep(2)
    
    print("3. Stopping speech...")
    try:
        # Kill all say processes
        subprocess.run(['pkill', '-f', 'say'], check=False)
        process.terminate()
        try:
            process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            process.kill()
        print("✅ Speech stopped successfully!")
    except Exception as e:
        print(f"❌ Error stopping speech: {e}")
    
    # Test 2: Check if any say processes are still running
    print("\n4. Checking for remaining say processes...")
    result = subprocess.run(['pgrep', '-f', 'say'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"❌ Found remaining say processes: {result.stdout.strip()}")
    else:
        print("✅ No remaining say processes found!")
    
    print("\n🎉 Stop speaking test completed!")

if __name__ == "__main__":
    test_stop_speaking()
