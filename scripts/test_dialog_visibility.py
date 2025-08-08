#!/usr/bin/env python3
"""
Test script to check dialog visibility
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import tkinter as tk
from tkinter import messagebox
from document_processor import DocumentProcessor
from google_docs_processor import GoogleDocsProcessor, GoogleDocsUploadDialog

def test_dialog_visibility():
    """Test if the dialog is visible and has content"""
    print("🧪 Testing dialog visibility...")
    
    root = tk.Tk()
    root.title("Test Window")
    root.geometry("400x300")
    
    # Add a label to the main window
    label = tk.Label(root, text="Click the button to open dialog", font=("Helvetica", 14))
    label.pack(pady=50)
    
    def open_dialog():
        print("🔧 Opening dialog...")
        try:
            # Initialize processors
            doc_processor = DocumentProcessor()
            google_processor = GoogleDocsProcessor()
            
            # Create dialog
            dialog = GoogleDocsUploadDialog(root, doc_processor, google_processor)
            print("✅ Dialog created successfully")
            
        except Exception as e:
            print(f"❌ Error creating dialog: {e}")
            messagebox.showerror("Error", f"Failed to create dialog: {e}")
    
    # Add button to open dialog
    button = tk.Button(root, text="Open Upload Dialog", command=open_dialog, 
                      font=("Helvetica", 12), bg="#3498db", fg="white", padx=20, pady=10)
    button.pack(pady=20)
    
    print("🪟 Test window created. Click the button to test dialog.")
    root.mainloop()

if __name__ == "__main__":
    test_dialog_visibility()
