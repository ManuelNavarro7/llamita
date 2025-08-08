#!/usr/bin/env python3
"""
Test script for document processing feature
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_document_processor():
    """Test the document processor functionality"""
    print("🧪 Testing Document Processing Feature...")
    
    try:
        from document_processor import DocumentProcessor
        
        # Initialize processor
        processor = DocumentProcessor("test_documents")
        print("✅ Document processor initialized")
        
        # Test supported formats
        formats = processor.get_supported_formats()
        print(f"✅ Supported formats: {formats}")
        
        # Create a test document
        test_content = """
        This is a test document for Llamita.
        
        It contains information about:
        - Document processing features
        - AI assistant capabilities
        - User interface improvements
        
        The document processor should be able to:
        1. Extract text from various formats
        2. Create chunks for context
        3. Provide relevant information for queries
        """
        
        test_file = "test_document.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        print(f"✅ Created test document: {test_file}")
        
        # Process the document
        doc_id = processor.process_document(test_file)
        if doc_id:
            print(f"✅ Document processed successfully, ID: {doc_id}")
            
            # Test document context retrieval
            query = "What are the document processing features?"
            context = processor.get_document_context(query)
            print(f"✅ Document context retrieved for query: {query}")
            print(f"Context preview: {context[:100]}...")
            
            # List documents
            documents = processor.list_documents()
            print(f"✅ Found {len(documents)} documents")
            
            # Clean up
            processor.remove_document(doc_id)
            os.remove(test_file)
            print("✅ Test cleanup completed")
            
        else:
            print("❌ Failed to process test document")
            
    except ImportError as e:
        print(f"❌ Document processing not available: {e}")
        print("Install dependencies: pip install PyPDF2 python-docx pandas openpyxl")
    except Exception as e:
        print(f"❌ Error testing document processor: {e}")

def test_voice_assistant_integration():
    """Test voice assistant integration"""
    print("\n🧪 Testing Voice Assistant Integration...")
    
    try:
        import tkinter as tk
        from voice_assistant import VoiceAssistant
        
        # Create a minimal test window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        app = VoiceAssistant(root)
        print("✅ Voice assistant initialized with document processing")
        
        # Test document processor availability
        if hasattr(app, 'document_processor') and app.document_processor:
            print("✅ Document processor integrated successfully")
        else:
            print("⚠️ Document processor not available in voice assistant")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ Error testing voice assistant integration: {e}")

if __name__ == "__main__":
    print("🚀 Starting Document Processing Tests...\n")
    
    test_document_processor()
    test_voice_assistant_integration()
    
    print("\n✅ Document processing tests completed!")
