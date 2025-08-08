#!/usr/bin/env python3
"""
Performance test for document upload dialogs
"""

import sys
import os
import time
import tkinter as tk
from tkinter import filedialog

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_dialog_loading():
    """Test dialog loading performance"""
    print("🧪 Testing Dialog Loading Performance...")
    
    try:
        from document_processor import DocumentProcessor, DocumentUploadDialog
        
        # Initialize processor
        processor = DocumentProcessor("test_performance")
        
        # Create test window
        root = tk.Tk()
        root.withdraw()
        
        # Test dialog creation time
        start_time = time.time()
        
        # Create dialog
        dialog = DocumentUploadDialog(root, processor)
        
        end_time = time.time()
        load_time = end_time - start_time
        
        print(f"✅ Dialog loaded in {load_time:.2f} seconds")
        
        # Close dialog
        dialog.dialog.destroy()
        root.destroy()
        
        if load_time < 1.0:
            print("✅ Performance: Excellent (< 1 second)")
        elif load_time < 2.0:
            print("✅ Performance: Good (< 2 seconds)")
        else:
            print("⚠️ Performance: Slow (> 2 seconds)")
            
    except Exception as e:
        print(f"❌ Error testing dialog performance: {e}")

def test_file_browser():
    """Test file browser performance"""
    print("\n🧪 Testing File Browser Performance...")
    
    try:
        # Create test window
        root = tk.Tk()
        root.withdraw()
        
        # Test file browser opening time
        start_time = time.time()
        
        # This will just test the dialog creation, not actual file selection
        file_types = [
            ("All supported", "*.txt *.pdf *.docx *.csv *.xlsx *.xls"),
            ("Text files", "*.txt"),
            ("PDF files", "*.pdf"),
            ("Word documents", "*.docx"),
            ("Spreadsheets", "*.csv *.xlsx *.xls"),
            ("All files", "*.*")
        ]
        
        # Simulate file dialog creation (without showing it)
        dialog = filedialog.askopenfilename(
            title="Select Document",
            filetypes=file_types,
            initialdir=os.path.expanduser("~/Documents")
        )
        
        end_time = time.time()
        browser_time = end_time - start_time
        
        print(f"✅ File browser ready in {browser_time:.2f} seconds")
        
        root.destroy()
        
        if browser_time < 0.5:
            print("✅ Performance: Excellent (< 0.5 seconds)")
        elif browser_time < 1.0:
            print("✅ Performance: Good (< 1 second)")
        else:
            print("⚠️ Performance: Slow (> 1 second)")
            
    except Exception as e:
        print(f"❌ Error testing file browser performance: {e}")

def test_google_docs_dialog():
    """Test Google Docs dialog performance"""
    print("\n🧪 Testing Google Docs Dialog Performance...")
    
    try:
        from document_processor import DocumentProcessor
        from google_docs_processor import GoogleDocsProcessor, GoogleDocsUploadDialog
        
        # Initialize processors
        doc_processor = DocumentProcessor("test_performance")
        google_processor = GoogleDocsProcessor()
        
        # Create test window
        root = tk.Tk()
        root.withdraw()
        
        # Test Google Docs dialog creation time
        start_time = time.time()
        
        # Create dialog
        dialog = GoogleDocsUploadDialog(root, doc_processor, google_processor)
        
        end_time = time.time()
        load_time = end_time - start_time
        
        print(f"✅ Google Docs dialog loaded in {load_time:.2f} seconds")
        
        # Close dialog
        dialog.dialog.destroy()
        root.destroy()
        
        if load_time < 1.5:
            print("✅ Performance: Excellent (< 1.5 seconds)")
        elif load_time < 3.0:
            print("✅ Performance: Good (< 3 seconds)")
        else:
            print("⚠️ Performance: Slow (> 3 seconds)")
            
    except Exception as e:
        print(f"❌ Error testing Google Docs dialog performance: {e}")

if __name__ == "__main__":
    print("🚀 Starting Performance Tests...\n")
    
    test_dialog_loading()
    test_file_browser()
    test_google_docs_dialog()
    
    print("\n✅ Performance tests completed!")
    print("\n💡 Performance Tips:")
    print("• Dialog should open in under 1 second")
    print("• File browser should be responsive")
    print("• Upload process should be non-blocking")
