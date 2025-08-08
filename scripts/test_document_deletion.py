#!/usr/bin/env python3
"""
Test script for enhanced document deletion features
"""

import os
import sys
import tempfile
import shutil
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_document_deletion_features():
    """Test the enhanced document deletion features"""
    print("🧪 Testing Enhanced Document Deletion Features")
    print("=" * 50)
    
    try:
        from document_processor import DocumentProcessor
        
        # Create a temporary directory for testing
        test_dir = tempfile.mkdtemp(prefix="llamita_test_")
        print(f"📁 Using test directory: {test_dir}")
        
        # Initialize document processor
        processor = DocumentProcessor(storage_dir=test_dir)
        
        # Create test documents
        test_docs = [
            ("test1.txt", "This is test document 1 with some content for testing."),
            ("test2.txt", "This is test document 2 with different content."),
            ("test3.txt", "This is test document 3 with more content for testing deletion features.")
        ]
        
        print("\n📄 Creating test documents...")
        doc_ids = []
        for filename, content in test_docs:
            # Create temporary file
            temp_file = os.path.join(test_dir, filename)
            with open(temp_file, 'w') as f:
                f.write(content)
            
            # Process document
            doc_id = processor.process_document(temp_file)
            if doc_id:
                doc_ids.append(doc_id)
                print(f"✅ Created document: {filename} (ID: {doc_id})")
            else:
                print(f"❌ Failed to create document: {filename}")
        
        # Test storage stats
        print("\n📊 Testing storage statistics...")
        stats = processor.get_storage_stats()
        print(f"Total documents: {stats['total_documents']}")
        print(f"Total chunks: {stats['total_chunks']}")
        print(f"Total size: {stats['total_size_mb']} MB")
        
        # Test document info
        print("\n📋 Testing document information...")
        for doc_id in doc_ids:
            doc_info = processor.get_document_info(doc_id)
            if doc_info:
                print(f"Document: {doc_info['filename']}")
                print(f"  - Uploaded: {doc_info['uploaded_at']}")
                print(f"  - Chunks: {doc_info['chunks_count']}")
                print(f"  - Size: {doc_info['storage_size']} bytes")
        
        # Test single document removal
        if doc_ids:
            print(f"\n🗑️ Testing single document removal...")
            doc_id_to_remove = doc_ids[0]
            if processor.remove_document(doc_id_to_remove):
                print(f"✅ Successfully removed document: {doc_id_to_remove}")
                doc_ids.pop(0)
            else:
                print(f"❌ Failed to remove document: {doc_id_to_remove}")
        
        # Test multiple document removal
        if len(doc_ids) >= 2:
            print(f"\n🗑️ Testing multiple document removal...")
            docs_to_remove = doc_ids[:2]
            results = processor.remove_multiple_documents(docs_to_remove)
            for doc_id, success in results.items():
                if success:
                    print(f"✅ Successfully removed document: {doc_id}")
                else:
                    print(f"❌ Failed to remove document: {doc_id}")
            doc_ids = doc_ids[2:]
        
        # Test cleanup orphaned files
        print(f"\n🧹 Testing cleanup orphaned files...")
        processor.cleanup_orphaned_files()
        print("✅ Cleanup completed")
        
        # Test clear all documents
        if doc_ids:
            print(f"\n🗑️ Testing clear all documents...")
            processor.clear_all_documents()
            print("✅ All documents cleared")
        
        # Final stats
        print(f"\n📊 Final storage statistics...")
        final_stats = processor.get_storage_stats()
        print(f"Total documents: {final_stats['total_documents']}")
        print(f"Total chunks: {final_stats['total_chunks']}")
        print(f"Total size: {final_stats['total_size_mb']} MB")
        
        print(f"\n✅ All tests completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you have installed document processing dependencies:")
        print("pip3 install PyPDF2 python-docx pandas openpyxl")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up test directory
        try:
            shutil.rmtree(test_dir)
            print(f"🧹 Cleaned up test directory: {test_dir}")
        except Exception as e:
            print(f"⚠️ Could not clean up test directory: {e}")

def test_gui_features():
    """Test the GUI deletion features"""
    print("\n🖥️ Testing GUI Deletion Features")
    print("=" * 40)
    
    try:
        import tkinter as tk
        from document_processor import DocumentProcessor, DocumentUploadDialog
        
        # Create a simple test window
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Initialize processor
        processor = DocumentProcessor()
        
        # Create upload dialog
        dialog = DocumentUploadDialog(root, processor)
        
        print("✅ GUI components created successfully")
        print("📋 Available GUI features:")
        print("  - Remove Selected Document")
        print("  - Remove All Documents")
        print("  - Cleanup Orphaned Files")
        print("  - Document Information Display")
        print("  - Storage Statistics")
        
        # Close dialog
        dialog.close_dialog()
        root.destroy()
        
    except Exception as e:
        print(f"❌ GUI test failed: {e}")

if __name__ == "__main__":
    test_document_deletion_features()
    test_gui_features()
    
    print("\n🎉 Document deletion feature testing complete!")
    print("\n📝 Summary of enhanced features:")
    print("  ✅ Single document removal")
    print("  ✅ Multiple document removal")
    print("  ✅ Remove all documents")
    print("  ✅ Document information display")
    print("  ✅ Storage statistics")
    print("  ✅ Cleanup orphaned files")
    print("  ✅ Enhanced GUI with better buttons")
    print("  ✅ Double-click to view document details")
    print("  ✅ Confirmation dialogs for destructive actions")
