#!/usr/bin/env python3
"""
Demo script for Llamita's document processing feature
Shows how to use the feature programmatically
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def create_sample_documents():
    """Create sample documents for demonstration"""
    print("📄 Creating sample documents...")
    
    # Sample PDF content (simulated as text for demo)
    pdf_content = """
    Llamita AI Assistant - Technical Report
    
    Executive Summary:
    Llamita is an intelligent AI assistant designed for local deployment using Ollama.
    The system provides natural language interaction with support for document processing.
    
    Key Features:
    1. Local AI processing with Ollama
    2. Document upload and analysis
    3. Multi-format support (PDF, DOCX, TXT, CSV, Excel)
    4. Smart context retrieval
    5. Persistent document storage
    
    Technical Architecture:
    - Python-based GUI using tkinter
    - Document processing with PyPDF2, python-docx, pandas
    - Chunk-based text analysis
    - Keyword-based relevance scoring
    
    Performance Metrics:
    - Document processing: < 5 seconds for typical files
    - Context retrieval: < 1 second
    - Memory usage: ~50MB for 10 documents
    - Storage: ~1MB per document processed
    """
    
    # Sample spreadsheet content
    csv_content = """Name,Department,Salary,Performance
John Smith,Engineering,75000,Excellent
Sarah Johnson,Marketing,65000,Good
Mike Davis,Finance,80000,Excellent
Lisa Chen,HR,60000,Good
David Wilson,Engineering,85000,Outstanding
Emma Brown,Marketing,70000,Good
"""
    
    # Create sample files
    with open("sample_report.txt", "w", encoding="utf-8") as f:
        f.write(pdf_content)
    
    with open("sample_data.csv", "w", encoding="utf-8") as f:
        f.write(csv_content)
    
    print("✅ Created sample documents:")
    print("  - sample_report.txt (Technical report)")
    print("  - sample_data.csv (Employee data)")

def demo_document_processing():
    """Demonstrate document processing functionality"""
    print("\n🧪 Demonstrating Document Processing...")
    
    try:
        from document_processor import DocumentProcessor
        
        # Initialize processor
        processor = DocumentProcessor("demo_documents")
        
        # Process sample documents
        print("📄 Processing sample documents...")
        
        doc1_id = processor.process_document("sample_report.txt")
        doc2_id = processor.process_document("sample_data.csv")
        
        if doc1_id and doc2_id:
            print("✅ Documents processed successfully!")
            
            # Demo different types of queries
            queries = [
                "What are the key features of Llamita?",
                "What is the technical architecture?",
                "What are the performance metrics?",
                "Who are the employees in the Engineering department?",
                "What is the average salary?",
                "Who has excellent performance?"
            ]
            
            print("\n🔍 Testing different queries:")
            for query in queries:
                print(f"\nQuery: {query}")
                context = processor.get_document_context(query)
                if context:
                    print(f"Relevant context found: {len(context)} characters")
                    print(f"Preview: {context[:150]}...")
                else:
                    print("No relevant context found")
            
            # List documents
            documents = processor.list_documents()
            print(f"\n📚 Available documents: {len(documents)}")
            for doc in documents:
                print(f"  - {doc['filename']} ({doc['chunks_count']} chunks)")
            
            # Cleanup
            processor.remove_document(doc1_id)
            processor.remove_document(doc2_id)
            os.remove("sample_report.txt")
            os.remove("sample_data.csv")
            print("\n✅ Demo cleanup completed")
            
        else:
            print("❌ Failed to process sample documents")
            
    except ImportError as e:
        print(f"❌ Document processing not available: {e}")
        print("Install dependencies: pip install PyPDF2 python-docx pandas openpyxl")
    except Exception as e:
        print(f"❌ Error in demo: {e}")

def demo_voice_assistant_integration():
    """Demonstrate voice assistant integration"""
    print("\n🎤 Demonstrating Voice Assistant Integration...")
    
    try:
        import tkinter as tk
        from voice_assistant import VoiceAssistant
        
        # Create a minimal test window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        app = VoiceAssistant(root)
        
        # Test document processor integration
        if hasattr(app, 'document_processor') and app.document_processor:
            print("✅ Document processor integrated with voice assistant")
            
            # Test document context in AI responses
            test_query = "What are the key features?"
            context = app.document_processor.get_document_context(test_query)
            print(f"✅ Document context retrieval works: {len(context) if context else 0} characters")
        else:
            print("⚠️ Document processor not available in voice assistant")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ Error testing voice assistant integration: {e}")

def main():
    """Main demo function"""
    print("🚀 Llamita Document Processing Demo")
    print("=" * 50)
    
    # Create sample documents
    create_sample_documents()
    
    # Demo document processing
    demo_document_processing()
    
    # Demo voice assistant integration
    demo_voice_assistant_integration()
    
    print("\n🎉 Demo completed!")
    print("\n💡 To use the document processing feature:")
    print("1. Install dependencies: ./scripts/install_document_deps.sh")
    print("2. Start Llamita: python3 src/voice_assistant.py")
    print("3. Click '📄 Upload Documents' to upload your files")
    print("4. Ask questions about your documents!")

if __name__ == "__main__":
    main()
