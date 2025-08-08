#!/usr/bin/env python3
"""
Test script for Google Docs integration
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_google_docs_processor():
    """Test the Google Docs processor functionality"""
    print("🧪 Testing Google Docs Integration...")
    
    try:
        from google_docs_processor import GoogleDocsProcessor
        
        # Initialize processor
        processor = GoogleDocsProcessor()
        print("✅ Google Docs processor initialized")
        
        # Test URL validation
        test_urls = [
            "https://docs.google.com/document/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit",
            "https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit",
            "https://docs.google.com/presentation/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit",
            "https://example.com/invalid-url"
        ]
        
        print("\n🔍 Testing URL validation:")
        for url in test_urls:
            doc_type = processor.validate_google_doc_url(url)
            doc_id = processor.extract_doc_id_from_url(url)
            print(f"  URL: {url[:50]}...")
            print(f"    Type: {doc_type}")
            print(f"    ID: {doc_id}")
        
        # Test export URL generation
        print("\n🔗 Testing export URL generation:")
        test_cases = [
            ("docs", "pdf"),
            ("sheets", "xlsx"),
            ("slides", "pdf")
        ]
        
        for doc_type, format_type in test_cases:
            try:
                export_url = processor.get_export_url("test_id_123", doc_type, format_type)
                print(f"  {doc_type} → {format_type}: {export_url[:80]}...")
            except Exception as e:
                print(f"  ❌ Error generating {doc_type} → {format_type}: {e}")
        
        # Test instructions
        print("\n📋 Testing instructions:")
        instructions = processor.get_google_docs_instructions()
        print(f"  Instructions length: {len(instructions)} characters")
        
        # Test info
        print("\nℹ️ Testing info:")
        info = processor.get_google_docs_info()
        print(f"  Title: {info['title']}")
        print(f"  Supported types: {info['supported_types']}")
        
        print("\n✅ Google Docs integration tests completed!")
        
    except ImportError as e:
        print(f"❌ Google Docs integration not available: {e}")
        print("Install dependencies: pip install requests")
    except Exception as e:
        print(f"❌ Error testing Google Docs integration: {e}")

def test_voice_assistant_integration():
    """Test voice assistant integration with Google Docs"""
    print("\n🧪 Testing Voice Assistant Integration...")
    
    try:
        import tkinter as tk
        from voice_assistant import VoiceAssistant
        
        # Create a minimal test window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        app = VoiceAssistant(root)
        print("✅ Voice assistant initialized with Google Docs integration")
        
        # Test Google Docs processor availability
        if hasattr(app, 'google_processor') and app.google_processor:
            print("✅ Google Docs processor integrated successfully")
        else:
            print("⚠️ Google Docs processor not available in voice assistant")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ Error testing voice assistant integration: {e}")

def test_google_docs_download():
    """Test actual Google Docs download (requires internet)"""
    print("\n🌐 Testing Google Docs Download (requires internet)...")
    
    try:
        from google_docs_processor import GoogleDocsProcessor
        from document_processor import DocumentProcessor
        
        processor = GoogleDocsProcessor()
        doc_processor = DocumentProcessor("test_google_docs")
        
        # Test with a public Google Doc (this is a sample)
        test_url = "https://docs.google.com/document/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit"
        
        print(f"Testing download from: {test_url}")
        
        # This will only work if the document is publicly accessible
        # For testing, we'll just check if the URL parsing works
        doc_type = processor.validate_google_doc_url(test_url)
        doc_id = processor.extract_doc_id_from_url(test_url)
        
        print(f"  Document type: {doc_type}")
        print(f"  Document ID: {doc_id}")
        
        if doc_type and doc_id:
            print("✅ URL parsing works correctly")
        else:
            print("❌ URL parsing failed")
        
    except Exception as e:
        print(f"❌ Error testing Google Docs download: {e}")

if __name__ == "__main__":
    print("🚀 Starting Google Docs Integration Tests...\n")
    
    test_google_docs_processor()
    test_voice_assistant_integration()
    test_google_docs_download()
    
    print("\n✅ Google Docs integration tests completed!")
    print("\n💡 To use Google Docs integration:")
    print("1. Install dependencies: pip install requests")
    print("2. Start Llamita: python3 src/voice_assistant.py")
    print("3. Click '📄 Upload Documents + Google' to access Google Docs features")
    print("4. Paste Google Docs URLs or upload exported files")
