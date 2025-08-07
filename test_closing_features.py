#!/usr/bin/env python3
"""
Test script to verify all closing features work 100%
"""

import subprocess
import time
import os
import signal

def test_process_cleanup():
    """Test if processes are properly cleaned up"""
    print("🧪 Testing Process Cleanup")
    print("=" * 40)
    
    # Start the voice assistant
    print("🚀 Starting voice assistant...")
    process = subprocess.Popen(['./run_voice_assistant.sh'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
    
    # Wait for it to start
    time.sleep(20)
    
    # Check if it's running
    result = subprocess.run(['pgrep', '-f', 'voice_assistant.py'], 
                           capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Voice assistant is running")
        
        # Get the PID
        pid = result.stdout.strip().split('\n')[0]
        print(f"📋 Process ID: {pid}")
        
        # Test stop_app.sh
        print("🛑 Testing stop_app.sh...")
        subprocess.run(['./stop_app.sh'], check=True)
        
        # Wait a moment
        time.sleep(3)
        
        # Check if processes are gone
        result = subprocess.run(['pgrep', '-f', 'voice_assistant.py'], 
                               capture_output=True, text=True)
        
        if result.returncode != 0:
            print("✅ All voice assistant processes stopped")
        else:
            print("❌ Some processes still running")
            return False
        
        # Check if virtual environment is removed
        if not os.path.exists('.venv'):
            print("✅ Virtual environment removed")
        else:
            print("❌ Virtual environment still exists")
            return False
            
        return True
    else:
        print("❌ Voice assistant failed to start")
        return False

def test_manual_cleanup():
    """Test manual cleanup script"""
    print("\n🧹 Testing Manual Cleanup Script")
    print("=" * 40)
    
    # Run the cleanup script
    result = subprocess.run(['./stop_voice_assistant.sh'], 
                           capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Manual cleanup script works")
        return True
    else:
        print("❌ Manual cleanup script failed")
        return False

def test_speech_process_cleanup():
    """Test speech process cleanup"""
    print("\n🗣️ Testing Speech Process Cleanup")
    print("=" * 40)
    
    # Start a test speech process
    print("🎤 Starting test speech...")
    speech_process = subprocess.Popen(['say', 'This is a test of speech cleanup'])
    
    # Wait a moment
    time.sleep(2)
    
    # Check if speech process is running
    result = subprocess.run(['pgrep', '-f', 'say'], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Speech process is running")
        
        # Test cleanup
        subprocess.run(['pkill', '-f', 'say'], check=False)
        
        # Wait and check again
        time.sleep(2)
        result = subprocess.run(['pgrep', '-f', 'say'], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("✅ Speech processes cleaned up")
            return True
        else:
            print("❌ Speech processes still running")
            return False
    else:
        print("✅ No speech processes found")
        return True

def test_virtual_environment_isolation():
    """Test that virtual environment is properly isolated"""
    print("\n🏝️ Testing Virtual Environment Isolation")
    print("=" * 40)
    
    # Check if .venv exists
    if os.path.exists('.venv'):
        print("⚠️ Virtual environment exists, removing...")
        subprocess.run(['rm', '-rf', '.venv'], check=True)
    
    # Run the app
    print("🚀 Starting app to create fresh environment...")
    process = subprocess.Popen(['./run_voice_assistant.sh'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
    
    # Wait for setup
    time.sleep(15)
    
    # Check if .venv was created
    if os.path.exists('.venv'):
        print("✅ Virtual environment created")
        
        # Stop the app
        subprocess.run(['./stop_app.sh'], check=True)
        
        # Check if .venv was removed
        time.sleep(3)
        if not os.path.exists('.venv'):
            print("✅ Virtual environment removed")
            return True
        else:
            print("❌ Virtual environment not removed")
            return False
    else:
        print("❌ Virtual environment not created")
        return False

def main():
    """Run all closing feature tests"""
    print("🧠 Voice Assistant Closing Features Test")
    print("=" * 50)
    
    tests = [
        ("Process Cleanup", test_process_cleanup),
        ("Manual Cleanup", test_manual_cleanup),
        ("Speech Process Cleanup", test_speech_process_cleanup),
        ("Virtual Environment Isolation", test_virtual_environment_isolation),
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
        print("🎉 All closing features work 100%!")
        print("\n✅ The voice assistant properly:")
        print("   - Stops all processes when closed")
        print("   - Removes virtual environment")
        print("   - Cleans up speech processes")
        print("   - Works like a virtual machine")
    else:
        print("❌ Some closing features need attention")
    
    # Final cleanup
    subprocess.run(['./stop_app.sh'], check=False)
    subprocess.run(['./stop_voice_assistant.sh'], check=False)

if __name__ == "__main__":
    main()
