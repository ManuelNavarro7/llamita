#!/usr/bin/env python3
"""
Document Processor for Llamita Voice Assistant
Handles document upload, parsing, and storage for AI context
"""

import os
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

# Document processing libraries
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

class DocumentProcessor:
    def __init__(self, storage_dir: str = "documents"):
        """
        Initialize the document processor
        
        Args:
            storage_dir: Directory to store processed documents
        """
        self.storage_dir = storage_dir
        self.documents = {}  # Store document metadata and content
        self.document_chunks = {}  # Store document chunks for context
        self.chunk_size = 1000  # Characters per chunk
        self.overlap = 200  # Overlap between chunks
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
        
        # Load existing documents (lazy loading to improve startup time)
        self._documents_loaded = False
    
    def load_documents(self):
        """Load existing documents from storage"""
        if self._documents_loaded:
            return
            
        metadata_file = os.path.join(self.storage_dir, "metadata.json")
        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    self.documents = json.load(f)
                
                # Load document chunks
                for doc_id in self.documents:
                    chunks_file = os.path.join(self.storage_dir, f"{doc_id}_chunks.json")
                    if os.path.exists(chunks_file):
                        with open(chunks_file, 'r', encoding='utf-8') as f:
                            self.document_chunks[doc_id] = json.load(f)
            except Exception as e:
                print(f"Error loading documents: {e}")
        
        self._documents_loaded = True
    
    def save_documents(self):
        """Save document metadata and chunks to storage"""
        try:
            # Save metadata
            metadata_file = os.path.join(self.storage_dir, "metadata.json")
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, indent=2, ensure_ascii=False)
            
            # Save chunks for each document
            for doc_id, chunks in self.document_chunks.items():
                chunks_file = os.path.join(self.storage_dir, f"{doc_id}_chunks.json")
                with open(chunks_file, 'w', encoding='utf-8') as f:
                    json.dump(chunks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving documents: {e}")
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported document formats"""
        formats = [".txt"]
        
        if PDF_AVAILABLE:
            formats.append(".pdf")
        
        if DOCX_AVAILABLE:
            formats.append(".docx")
        
        if PANDAS_AVAILABLE:
            formats.extend([".csv", ".xlsx", ".xls"])
        
        return formats
    
    def process_document(self, file_path: str) -> Optional[str]:
        """
        Process a document and extract its text content
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Document ID if successful, None otherwise
        """
        try:
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return None
            
            # Generate document ID
            doc_id = self._generate_doc_id(file_path)
            
            # Extract text based on file type
            text_content = self._extract_text(file_path)
            if not text_content:
                print(f"Could not extract text from: {file_path}")
                return None
            
            # Create document metadata
            doc_metadata = {
                "filename": os.path.basename(file_path),
                "filepath": file_path,
                "size": os.path.getsize(file_path),
                "uploaded_at": datetime.now().isoformat(),
                "content_length": len(text_content),
                "chunks_count": 0
            }
            
            # Store document
            self.documents[doc_id] = doc_metadata
            
            # Create chunks for context
            chunks = self._create_chunks(text_content)
            self.document_chunks[doc_id] = chunks
            doc_metadata["chunks_count"] = len(chunks)
            
            # Save to storage
            self.save_documents()
            
            print(f"Successfully processed document: {os.path.basename(file_path)}")
            print(f"Created {len(chunks)} chunks for context")
            
            return doc_id
            
        except Exception as e:
            print(f"Error processing document {file_path}: {e}")
            return None
    
    def _generate_doc_id(self, file_path: str) -> str:
        """Generate a unique document ID based on file content"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()[:16]
        except:
            # Fallback to filename-based ID
            return hashlib.md5(file_path.encode()).hexdigest()[:16]
    
    def _extract_text(self, file_path: str) -> Optional[str]:
        """Extract text content from various document formats"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == ".txt":
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif file_ext == ".pdf" and PDF_AVAILABLE:
                return self._extract_pdf_text(file_path)
            
            elif file_ext == ".docx" and DOCX_AVAILABLE:
                return self._extract_docx_text(file_path)
            
            elif file_ext in [".csv", ".xlsx", ".xls"] and PANDAS_AVAILABLE:
                return self._extract_spreadsheet_text(file_path)
            
            else:
                print(f"Unsupported file format: {file_ext}")
                return None
                
        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
            return None
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
        return text
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error extracting DOCX text: {e}")
        return text
    
    def _extract_spreadsheet_text(self, file_path: str) -> str:
        """Extract text from spreadsheet files"""
        text = ""
        try:
            df = pd.read_excel(file_path) if file_path.endswith(('.xlsx', '.xls')) else pd.read_csv(file_path)
            text = df.to_string(index=False)
        except Exception as e:
            print(f"Error extracting spreadsheet text: {e}")
        return text
    
    def _create_chunks(self, text: str) -> List[Dict]:
        """Create overlapping chunks from text for better context"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Try to break at a sentence boundary
            if end < len(text):
                # Look for sentence endings
                for i in range(end, max(start, end - 100), -1):
                    if text[i] in '.!?':
                        end = i + 1
                        break
            
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "start": start,
                    "end": end,
                    "length": len(chunk_text)
                })
            
            # Move start position with overlap
            start = end - self.overlap
            if start >= len(text):
                break
        
        return chunks
    
    def get_document_context(self, query: str, max_chunks: int = 3) -> str:
        """
        Get relevant document chunks for a query
        
        Args:
            query: The user's query
            max_chunks: Maximum number of chunks to return
            
        Returns:
            Relevant document context as string
        """
        if not self.documents:
            return ""
        
        # Simple keyword matching for now
        # In a more advanced implementation, you could use embeddings or semantic search
        query_words = query.lower().split()
        relevant_chunks = []
        
        for doc_id, chunks in self.document_chunks.items():
            doc_info = self.documents.get(doc_id, {})
            filename = doc_info.get("filename", "Unknown")
            
            for chunk in chunks:
                chunk_text = chunk["text"].lower()
                score = 0
                
                # Simple keyword scoring
                for word in query_words:
                    if word in chunk_text:
                        score += 1
                
                if score > 0:
                    relevant_chunks.append({
                        "doc_id": doc_id,
                        "filename": filename,
                        "chunk": chunk,
                        "score": score
                    })
        
        # Sort by relevance score and take top chunks
        relevant_chunks.sort(key=lambda x: x["score"], reverse=True)
        
        # Build context string
        context_parts = []
        for item in relevant_chunks[:max_chunks]:
            context_parts.append(f"From document '{item['filename']}':\n{item['chunk']['text']}\n")
        
        return "\n".join(context_parts)
    
    def list_documents(self) -> List[Dict]:
        """Get list of all uploaded documents"""
        # Ensure documents are loaded
        self.load_documents()
        
        return [
            {
                "id": doc_id,
                "filename": metadata.get("filename", "Unknown"),
                "uploaded_at": metadata.get("uploaded_at", ""),
                "size": metadata.get("size", 0),
                "chunks_count": metadata.get("chunks_count", 0)
            }
            for doc_id, metadata in self.documents.items()
        ]
    
    def remove_document(self, doc_id: str) -> bool:
        """Remove a document from storage"""
        try:
            if doc_id in self.documents:
                del self.documents[doc_id]
            
            if doc_id in self.document_chunks:
                del self.document_chunks[doc_id]
            
            # Remove chunk file
            chunks_file = os.path.join(self.storage_dir, f"{doc_id}_chunks.json")
            if os.path.exists(chunks_file):
                os.remove(chunks_file)
            
            self.save_documents()
            return True
        except Exception as e:
            print(f"Error removing document {doc_id}: {e}")
            return False
    
    def clear_all_documents(self):
        """Remove all documents"""
        self.documents.clear()
        self.document_chunks.clear()
        self.save_documents()


class DocumentUploadDialog:
    """GUI dialog for document upload"""
    
    def __init__(self, parent, document_processor: DocumentProcessor):
        self.parent = parent
        self.document_processor = document_processor
        self.result = None
        
        # Create dialog window with optimized settings
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Upload Document")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Optimize dialog performance
        self.dialog.resizable(False, False)  # Disable resizing for faster rendering
        self.dialog.update_idletasks()  # Force immediate update
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + parent.winfo_width()//2 - 250,
            parent.winfo_rooty() + parent.winfo_height()//2 - 200
        ))
        
        # Setup UI in background to avoid blocking
        self.dialog.after(10, self.setup_ui)
    
    def setup_ui(self):
        """Setup the upload dialog UI"""
        # Main frame
        main_frame = tk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="📄 Upload Document",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Supported formats (load in background to avoid delay)
        self.formats_label = tk.Label(
            main_frame,
            text="Loading supported formats...",
            font=("Helvetica", 10),
            fg="gray"
        )
        self.formats_label.pack(pady=(0, 20))
        
        # Update formats in background
        self.dialog.after(100, self.update_supported_formats)
        
        # File selection frame
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(
            file_frame,
            textvariable=self.file_path_var,
            font=("Helvetica", 12),
            state="readonly"
        )
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_button = tk.Button(
            file_frame,
            text="Browse",
            command=self.browse_file,
            font=("Helvetica", 10)
        )
        browse_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Upload button
        self.upload_button = tk.Button(
            main_frame,
            text="Upload Document",
            command=self.upload_document,
            font=("Helvetica", 12, "bold"),
            bg="#3498db",
            fg="white",
            state="disabled"
        )
        self.upload_button.pack(pady=(0, 20))
        
        # Progress and status
        self.status_label = tk.Label(
            main_frame,
            text="Select a document to upload",
            font=("Helvetica", 10),
            fg="gray"
        )
        self.status_label.pack()
        
        # Document list
        list_frame = tk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        list_label = tk.Label(
            list_frame,
            text="Uploaded Documents:",
            font=("Helvetica", 12, "bold")
        )
        list_label.pack(anchor=tk.W)
        
        # Create a frame for the listbox and scrollbar
        listbox_frame = tk.Frame(list_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.documents_listbox = tk.Listbox(
            listbox_frame,
            font=("Helvetica", 10)
        )
        self.documents_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.documents_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.documents_listbox.yview)
        
        # Remove button
        self.remove_button = tk.Button(
            list_frame,
            text="Remove Selected",
            command=self.remove_selected_document,
            font=("Helvetica", 10),
            bg="#e74c3c",
            fg="white"
        )
        self.remove_button.pack(pady=(10, 0))
        
        # Close button
        close_button = tk.Button(
            main_frame,
            text="Close",
            command=self.close_dialog,
            font=("Helvetica", 12)
        )
        close_button.pack(pady=(20, 0))
        
        # Update document list
        self.update_document_list()
    
    def update_supported_formats(self):
        """Update the supported formats display"""
        try:
            formats = self.document_processor.get_supported_formats()
            formats_text = "Supported formats: " + ", ".join(formats)
            self.formats_label.config(text=formats_text)
        except Exception as e:
            self.formats_label.config(text="Supported formats: .txt, .pdf, .docx, .csv, .xlsx, .xls")
    
    def browse_file(self):
        """Open file browser dialog"""
        # Use a more efficient approach for macOS
        try:
            # Show a simple message first
            self.status_label.config(text="Opening file browser...")
            self.dialog.update()
            
            # Use a basic dialog without file type filtering for speed
            file_path = filedialog.askopenfilename(
                title="Select Document",
                initialdir=os.path.expanduser("~/Documents")
            )
            
            # If user selects a file, validate it's supported
            if file_path:
                file_ext = os.path.splitext(file_path)[1].lower()
                supported_extensions = ['.txt', '.pdf', '.docx', '.csv', '.xlsx', '.xls']
                
                if file_ext not in supported_extensions:
                    import tkinter.messagebox as messagebox
                    messagebox.showwarning(
                        "Unsupported Format",
                        f"File format '{file_ext}' may not be supported.\nSupported formats: {', '.join(supported_extensions)}"
                    )
                else:
                    self.status_label.config(text=f"Selected: {os.path.basename(file_path)}")
                    
        except Exception as e:
            print(f"File dialog error: {e}")
            self.status_label.config(text="Error opening file browser")
            # Fallback to basic file dialog
            file_path = filedialog.askopenfilename(title="Select Document")
        
        if file_path:
            self.file_path_var.set(file_path)
            self.upload_button.config(state="normal")
            self.status_label.config(text=f"Selected: {os.path.basename(file_path)}")
    
    def upload_document(self):
        """Upload the selected document"""
        file_path = self.file_path_var.get()
        if not file_path:
            return
        
        # Validate file exists before processing
        if not os.path.exists(file_path):
            self.status_label.config(text="❌ File not found")
            return
        
        self.status_label.config(text="Processing document...")
        self.upload_button.config(state="disabled")
        
        # Process document in a separate thread with better error handling
        def process_thread():
            try:
                # Quick file size check
                file_size = os.path.getsize(file_path)
                if file_size > 50 * 1024 * 1024:  # 50MB limit
                    self.parent.after(0, lambda: self.status_label.config(
                        text="❌ File too large (max 50MB)"
                    ))
                    return
                
                doc_id = self.document_processor.process_document(file_path)
                if doc_id:
                    self.parent.after(0, lambda: self.status_label.config(
                        text=f"✅ Successfully uploaded: {os.path.basename(file_path)}"
                    ))
                    self.parent.after(0, self.update_document_list)
                else:
                    self.parent.after(0, lambda: self.status_label.config(
                        text="❌ Failed to process document"
                    ))
            except Exception as e:
                self.parent.after(0, lambda: self.status_label.config(
                    text=f"❌ Error: {str(e)[:50]}..."
                ))
            finally:
                self.parent.after(0, lambda: self.upload_button.config(state="normal"))
        
        # Use a more efficient threading approach
        import threading
        thread = threading.Thread(target=process_thread, daemon=True)
        thread.start()
    
    def update_document_list(self):
        """Update the document list display"""
        self.documents_listbox.delete(0, tk.END)
        documents = self.document_processor.list_documents()
        
        for doc in documents:
            display_text = f"{doc['filename']} ({doc['chunks_count']} chunks)"
            self.documents_listbox.insert(tk.END, display_text)
    
    def remove_selected_document(self):
        """Remove the selected document"""
        selection = self.documents_listbox.curselection()
        if not selection:
            return
        
        documents = self.document_processor.list_documents()
        if selection[0] < len(documents):
            doc_id = documents[selection[0]]["id"]
            
            if messagebox.askyesno("Remove Document", 
                                 f"Are you sure you want to remove '{documents[selection[0]]['filename']}'?"):
                if self.document_processor.remove_document(doc_id):
                    self.update_document_list()
                    self.status_label.config(text="Document removed successfully")
    
    def close_dialog(self):
        """Close the upload dialog"""
        self.dialog.destroy()
