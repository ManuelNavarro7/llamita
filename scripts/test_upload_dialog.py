#!/usr/bin/env python3
"""
Test script for upload dialog functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import tkinter as tk
from tkinter import messagebox
from document_processor import DocumentProcessor, DocumentUploadDialog
from google_docs_processor import GoogleDocsProcessor, GoogleDocsUploadDialog

def test_basic_dialog():
    """Test the basic document upload dialog"""
    print("Testing basic document upload dialog...")
    
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    try:
        # Initialize document processor
        doc_processor = DocumentProcessor()
        
        # Create dialog
        dialog = DocumentUploadDialog(root, doc_processor)
        
        print("✅ Basic dialog created successfully")
        
    except Exception as e:
        print(f"❌ Error creating basic dialog: {e}")
        return False
    
    finally:
        root.destroy()
    
    return True

def test_google_docs_dialog():
    """Test the Google Docs upload dialog"""
    print("Testing Google Docs upload dialog...")
    
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    try:
        # Initialize processors
        doc_processor = DocumentProcessor()
        google_processor = GoogleDocsProcessor()
        
        # Create dialog
        dialog = GoogleDocsUploadDialog(root, doc_processor, google_processor)
        
        print("✅ Google Docs dialog created successfully")
        
    except Exception as e:
        print(f"❌ Error creating Google Docs dialog: {e}")
        return False
    
    finally:
        root.destroy()
    
    return True

def main():
    """Main test function"""
    print("🧪 Testing upload dialog functionality...")
    
    # Test basic dialog
    basic_success = test_basic_dialog()
    
    # Test Google Docs dialog
    google_success = test_google_docs_dialog()
    
    if basic_success and google_success:
        print("✅ All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
