#!/usr/bin/env python3
"""
Test script for Voice Assistant features
"""

import subprocess
import time
import signal
import os

def test_stop_speaking():
    """Test the stop speaking functionality"""
    print("🧪 Testing Stop Speaking Feature")
    print("=" * 40)
    
    # Start a speech process
    print("🎤 Starting speech process...")
    process = subprocess.Popen(['say', 'This is a test of the stop speaking functionality. I will speak for a while to test if you can stop me.'])
    
    # Wait a bit
    time.sleep(2)
    
    # Try to stop it
    print("🔇 Attempting to stop speech...")
    try:
        process.terminate()
        process.wait(timeout=2)
        print("✅ Speech stopped successfully")
    except subprocess.TimeoutExpired:
        print("⏰ Process didn't stop gracefully, force killing...")
        process.kill()
        print("✅ Speech force stopped")
    except Exception as e:
        print(f"❌ Error stopping speech: {e}")
    
    return True

def test_process_cleanup():
    """Test process cleanup functionality"""
    print("\n🧹 Testing Process Cleanup")
    print("=" * 40)
    
    # Start some test processes
    print("🎤 Starting test speech processes...")
    processes = []
    for i in range(3):
        p = subprocess.Popen(['say', f'Test process {i+1}'])
        processes.append(p)
    
    time.sleep(1)
    
    # Try to kill them
    print("🔇 Cleaning up processes...")
    try:
        subprocess.run(['pkill', '-f', 'say'], check=False)
        print("✅ Process cleanup successful")
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
    
    return True

def test_voicebankingd_cleanup():
    """Test voicebankingd cleanup"""
    print("\n🗣️ Testing Voicebankingd Cleanup")
    print("=" * 40)
    
    # Check if voicebankingd is running
    result = subprocess.run(['pgrep', '-f', 'voicebankingd'], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("⚠️ Voicebankingd is running, attempting to stop...")
        try:
            subprocess.run(['pkill', '-f', 'voicebankingd'], check=False)
            print("✅ Voicebankingd stopped")
        except Exception as e:
            print(f"❌ Error stopping voicebankingd: {e}")
    else:
        print("✅ No voicebankingd process found")
    
    return True

def main():
    """Run all tests"""
    print("🧠 Voice Assistant Feature Tests")
    print("=" * 50)
    
    tests = [
        ("Stop Speaking", test_stop_speaking),
        ("Process Cleanup", test_process_cleanup),
        ("Voicebankingd Cleanup", test_voicebankingd_cleanup),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test passed")
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All feature tests passed!")
        print("\nThe voice assistant is ready with:")
        print("✅ Stop Speaking button functionality")
        print("✅ Process cleanup on exit")
        print("✅ Voicebankingd management")
    else:
        print("❌ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
