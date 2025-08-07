#!/usr/bin/env python3
"""
Test script to demonstrate Ollama error handling
"""

import requests
import sys
import os

# Add src to Python path
sys.path.insert(0, 'src')

def test_ollama_status():
    """Test Ollama status checking"""
    print("🧪 Testing Ollama Status Handling")
    print("=" * 40)
    
    # Test 1: Ollama not running
    print("\n1️⃣ Testing when Ollama is NOT running:")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        print(f"   ❌ Ollama is running (unexpected)")
    except requests.exceptions.ConnectionError:
        print("   ✅ Correctly detected: Ollama is not running")
    except requests.exceptions.Timeout:
        print("   ✅ Correctly detected: Ollama timeout")
    except Exception as e:
        print(f"   ✅ Correctly detected: {type(e).__name__}")
    
    # Test 2: Start Ollama and test again
    print("\n2️⃣ Starting Ollama...")
    os.system("ollama serve > /dev/null 2>&1 &")
    import time
    time.sleep(3)
    
    print("   Testing when Ollama IS running:")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            if models:
                model_names = [model.get('name', 'Unknown') for model in models]
                print(f"   ✅ Ollama is running with models: {', '.join(model_names)}")
            else:
                print("   ✅ Ollama is running but no models found")
        else:
            print(f"   ❌ Ollama error: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Stop Ollama and test again
    print("\n3️⃣ Stopping Ollama...")
    os.system("pkill ollama")
    time.sleep(2)
    
    print("   Testing when Ollama is stopped again:")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        print(f"   ❌ Ollama is still running (unexpected)")
    except requests.exceptions.ConnectionError:
        print("   ✅ Correctly detected: Ollama is not running")
    except Exception as e:
        print(f"   ✅ Correctly detected: {type(e).__name__}")
    
    print("\n🎉 Ollama error handling test completed!")
    print("\n💡 To test the full application:")
    print("   1. Start Ollama: ollama serve")
    print("   2. Run Llamita: ./scripts/run_simple.sh")
    print("   3. Try sending a message when Ollama is running/stopped")

if __name__ == "__main__":
    test_ollama_status()
