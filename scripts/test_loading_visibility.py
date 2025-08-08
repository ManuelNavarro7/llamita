#!/usr/bin/env python3
"""
Test script to check if the loading screen is visible
"""

import tkinter as tk
import time
import threading

def test_loading_screen():
    """Test if the loading screen appears"""
    print("🧪 Testing Loading Screen Visibility")
    print("====================================")
    
    # Create root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Create a simple loading screen
    loading_window = tk.Toplevel(root)
    loading_window.title("🦙 Llamita - Loading...")
    loading_window.geometry("400x300")
    loading_window.configure(bg='#2c3e50')
    loading_window.resizable(False, False)
    
    # Make it visible
    loading_window.lift()
    loading_window.attributes('-topmost', True)
    loading_window.focus_force()
    
    # Add some content
    label = tk.Label(loading_window, text="🦙 Llamita", font=("Helvetica", 24, "bold"),
                     fg='#ecf0f1', bg='#2c3e50')
    label.pack(pady=50)
    
    status_label = tk.Label(loading_window, text="Testing loading screen...", 
                           font=("Helvetica", 12), fg='#ecf0f1', bg='#2c3e50')
    status_label.pack()
    
    print("✅ Loading screen created")
    print("📱 Window should be visible now")
    print("⏰ Will close in 5 seconds...")
    
    # Close after 5 seconds
    def close_test():
        time.sleep(5)
        loading_window.destroy()
        root.destroy()
        print("✅ Test completed")
    
    threading.Thread(target=close_test, daemon=True).start()
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    test_loading_screen()
