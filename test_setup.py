#!/usr/bin/env python3
"""
Test script to verify Voice Assistant setup
"""

import sys
import subprocess
import requests
import speech_recognition as sr
import tkinter as tk

def test_python_version():
    """Test Python version"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is too old. Need 3.8+")
        return False

def test_dependencies():
    """Test if required packages are installed"""
    print("\n📦 Testing dependencies...")
    
    try:
        import speech_recognition
        print("✅ speech_recognition installed")
    except ImportError:
        print("❌ speech_recognition not installed")
        return False
    
    try:
        import requests
        print("✅ requests installed")
    except ImportError:
        print("❌ requests not installed")
        return False
    
    try:
        import tkinter
        print("✅ tkinter available")
    except ImportError:
        print("❌ tkinter not available")
        return False
    
    return True

def test_microphone():
    """Test microphone access"""
    print("\n🎤 Testing microphone...")
    try:
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        with microphone as source:
            print("✅ Microphone access successful")
            return True
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
        return False

def test_ollama():
    """Test Ollama connection"""
    print("\n🤖 Testing Ollama connection...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running and accessible")
            return True
        else:
            print(f"❌ Ollama returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        return False

def test_ollama_models():
    """Test if required models are available"""
    print("\n📚 Testing Ollama models...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [model['name'] for model in models]
            
            if 'llama3:8b' in model_names:
                print("✅ llama3:8b model is available")
                return True
            else:
                print("❌ llama3:8b model not found. Available models:")
                for model in model_names:
                    print(f"  - {model}")
                return False
        else:
            print("❌ Could not retrieve model list")
            return False
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return False

def test_text_to_speech():
    """Test macOS text-to-speech"""
    print("\n🗣️ Testing text-to-speech...")
    try:
        result = subprocess.run(['say', 'Test'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Text-to-speech is working")
            return True
        else:
            print(f"❌ Text-to-speech failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Text-to-speech timed out")
        return False
    except Exception as e:
        print(f"❌ Text-to-speech error: {e}")
        return False

def test_gui():
    """Test GUI creation"""
    print("\n🖥️ Testing GUI...")
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()
        print("✅ GUI creation successful")
        return True
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧠 Voice Assistant Setup Test")
    print("=============================")
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Microphone", test_microphone),
        ("Ollama Connection", test_ollama),
        ("Ollama Models", test_ollama_models),
        ("Text-to-Speech", test_text_to_speech),
        ("GUI", test_gui),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nTo run the voice assistant:")
        print("  python3 voice_assistant.py")
    else:
        print("❌ Some tests failed. Please check the issues above.")
        print("\nCommon solutions:")
        print("1. Install missing dependencies: pip3 install -r requirements.txt")
        print("2. Start Ollama: ollama serve")
        print("3. Download model: ollama pull llama3:8b")
        print("4. Grant microphone permissions in System Preferences")

if __name__ == "__main__":
    main()
