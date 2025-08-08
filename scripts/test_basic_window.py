#!/usr/bin/env python3
"""
Simple test to see if app bundle can create basic windows
"""

import tkinter as tk
import sys
import os

def test_basic_window():
    """Test if we can create a basic window"""
    print("🧪 Testing Basic Window Creation")
    print("================================")
    print(f"Python version: {sys.version}")
    print(f"Tkinter available: {tk.Tk}")
    print(f"Current directory: {os.getcwd()}")
    print("")
    
    try:
        # Create root window
        root = tk.Tk()
        root.title("Test Window")
        root.geometry("300x200")
        
        # Add a label
        label = tk.Label(root, text="🦙 Test Window\nIf you see this, basic window creation works!")
        label.pack(expand=True)
        
        print("✅ Basic window created successfully")
        print("📱 Window should be visible")
        print("⏰ Will close in 3 seconds...")
        
        # Close after 3 seconds
        root.after(3000, root.destroy)
        root.mainloop()
        
        print("✅ Test completed successfully")
        
    except Exception as e:
        print(f"❌ Error creating window: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_basic_window()
