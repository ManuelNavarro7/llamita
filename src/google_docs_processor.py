#!/usr/bin/env python3
"""
Google Docs and Sheets Processor for Llamita
Handles importing documents from Google Workspace
"""

import os
import tempfile
import subprocess
import requests
from typing import Optional, Dict, List
import json
import tkinter as tk
import tkinter.ttk as ttk

class GoogleDocsProcessor:
    def __init__(self):
        """Initialize Google Docs processor"""
        self.supported_export_formats = {
            'docs': ['pdf', 'docx', 'txt'],
            'sheets': ['pdf', 'xlsx', 'csv'],
            'slides': ['pdf', 'pptx']
        }
    
    def get_google_docs_info(self) -> Dict[str, str]:
        """Get information about Google Docs integration"""
        return {
            "title": "Google Docs & Sheets Integration",
            "description": "Import documents from Google Workspace",
            "supported_types": ["Google Docs", "Google Sheets", "Google Slides"],
            "export_formats": self.supported_export_formats,
            "instructions": [
                "1. Open your Google Doc/Sheet in browser",
                "2. Go to File > Download",
                "3. Choose PDF, DOCX, or XLSX format",
                "4. Upload the downloaded file to Llamita"
            ]
        }
    
    def validate_google_doc_url(self, url: str) -> Optional[str]:
        """
        Validate if a URL is a Google Doc/Sheet
        
        Args:
            url: The URL to validate
            
        Returns:
            Document type if valid, None otherwise
        """
        if not url.startswith('https://'):
            return None
        
        # Google Docs URLs
        if 'docs.google.com/document/' in url:
            return 'docs'
        elif 'docs.google.com/spreadsheets/' in url:
            return 'sheets'
        elif 'docs.google.com/presentation/' in url:
            return 'slides'
        
        return None
    
    def extract_doc_id_from_url(self, url: str) -> Optional[str]:
        """
        Extract document ID from Google Docs URL
        
        Args:
            url: Google Docs URL
            
        Returns:
            Document ID if found, None otherwise
        """
        try:
            # Extract ID from various Google Docs URL formats
            if '/document/d/' in url:
                # Format: https://docs.google.com/document/d/DOC_ID/edit
                parts = url.split('/document/d/')
                if len(parts) > 1:
                    doc_id = parts[1].split('/')[0]
                    return doc_id
            elif '/spreadsheets/d/' in url:
                # Format: https://docs.google.com/spreadsheets/d/SHEET_ID/edit
                parts = url.split('/spreadsheets/d/')
                if len(parts) > 1:
                    doc_id = parts[1].split('/')[0]
                    return doc_id
            elif '/presentation/d/' in url:
                # Format: https://docs.google.com/presentation/d/SLIDE_ID/edit
                parts = url.split('/presentation/d/')
                if len(parts) > 1:
                    doc_id = parts[1].split('/')[0]
                    return doc_id
        except Exception as e:
            print(f"Error extracting document ID: {e}")
        
        return None
    
    def get_export_url(self, doc_id: str, doc_type: str, format_type: str = 'pdf') -> str:
        """
        Generate export URL for Google Doc
        
        Args:
            doc_id: Document ID
            doc_type: Type of document (docs, sheets, slides)
            format_type: Export format (pdf, docx, xlsx, etc.)
            
        Returns:
            Export URL
        """
        base_urls = {
            'docs': 'https://docs.google.com/document/d/',
            'sheets': 'https://docs.google.com/spreadsheets/d/',
            'slides': 'https://docs.google.com/presentation/d/'
        }
        
        export_endpoints = {
            'docs': {
                'pdf': '/export?format=pdf',
                'docx': '/export?format=docx',
                'txt': '/export?format=txt'
            },
            'sheets': {
                'pdf': '/export?format=pdf',
                'xlsx': '/export?format=xlsx',
                'csv': '/export?format=csv'
            },
            'slides': {
                'pdf': '/export?format=pdf',
                'pptx': '/export?format=pptx'
            }
        }
        
        if doc_type not in base_urls or format_type not in export_endpoints[doc_type]:
            raise ValueError(f"Unsupported doc_type: {doc_type} or format: {format_type}")
        
        return f"{base_urls[doc_type]}{doc_id}{export_endpoints[doc_type][format_type]}"
    
    def download_google_doc(self, url: str, format_type: str = 'pdf') -> Optional[str]:
        """
        Download Google Doc as specified format
        
        Args:
            url: Google Docs URL
            format_type: Export format (pdf, docx, xlsx, etc.)
            
        Returns:
            Path to downloaded file, None if failed
        """
        try:
            # Validate URL
            doc_type = self.validate_google_doc_url(url)
            if not doc_type:
                print("❌ Invalid Google Docs URL")
                return None
            
            # Extract document ID
            doc_id = self.extract_doc_id_from_url(url)
            if not doc_id:
                print("❌ Could not extract document ID from URL")
                return None
            
            # Generate export URL
            export_url = self.get_export_url(doc_id, doc_type, format_type)
            
            # Download file
            print(f"📥 Downloading {doc_type} as {format_type}...")
            response = requests.get(export_url, timeout=30)
            
            if response.status_code == 200:
                # Create temporary file
                file_extension = format_type
                if format_type == 'docx':
                    file_extension = 'docx'
                elif format_type == 'xlsx':
                    file_extension = 'xlsx'
                elif format_type == 'pptx':
                    file_extension = 'pptx'
                
                temp_file = tempfile.NamedTemporaryFile(
                    suffix=f'.{file_extension}',
                    delete=False,
                    prefix='google_doc_'
                )
                
                temp_file.write(response.content)
                temp_file.close()
                
                print(f"✅ Downloaded to: {temp_file.name}")
                return temp_file.name
            else:
                print(f"❌ Failed to download: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error downloading Google Doc: {e}")
            return None
    
    def get_google_docs_instructions(self) -> str:
        """Get formatted instructions for Google Docs integration"""
        return """
📄 Google Docs & Sheets Integration

You can import documents from Google Workspace:

🔗 **Method 1: Direct URL (Limited)**
- Paste Google Docs URL in the upload dialog
- System will attempt to download and process

📁 **Method 2: Manual Export (Recommended)**
1. Open your Google Doc/Sheet in browser
2. Go to File > Download
3. Choose format:
   • Google Docs → PDF or DOCX
   • Google Sheets → PDF, XLSX, or CSV
   • Google Slides → PDF or PPTX
4. Upload the downloaded file to Llamita

✅ **Supported Formats:**
• Google Docs → PDF, DOCX, TXT
• Google Sheets → PDF, XLSX, CSV  
• Google Slides → PDF, PPTX

💡 **Tips:**
• PDF format works best for most documents
• XLSX/CSV for spreadsheet data analysis
• DOCX for editable document content
        """
    
    def process_google_doc_url(self, url: str, document_processor) -> Optional[str]:
        """
        Process Google Doc URL directly
        
        Args:
            url: Google Docs URL
            document_processor: DocumentProcessor instance
            
        Returns:
            Document ID if successful, None otherwise
        """
        try:
            # Try to download as PDF first (most reliable)
            downloaded_file = self.download_google_doc(url, 'pdf')
            
            if downloaded_file:
                # Process the downloaded file
                doc_id = document_processor.process_document(downloaded_file)
                
                # Clean up temporary file
                try:
                    os.unlink(downloaded_file)
                except:
                    pass
                
                return doc_id
            else:
                print("❌ Could not download Google Doc")
                return None
                
        except Exception as e:
            print(f"❌ Error processing Google Doc URL: {e}")
            return None


class GoogleDocsUploadDialog:
    """Enhanced upload dialog with Google Docs support"""
    
    def __init__(self, parent, document_processor, google_processor):
        self.parent = parent
        self.document_processor = document_processor
        self.google_processor = google_processor
        self.result = None
        
        # Create dialog window with optimized settings
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Documents")
        self.dialog.geometry("750x900")  # Much larger size to show all content without scrolling
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Optimize dialog performance
        self.dialog.resizable(True, True)  # Allow resizing for better UX
        self.dialog.update_idletasks()  # Force immediate update
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + parent.winfo_width()//2 - 375,
            parent.winfo_rooty() + parent.winfo_height()//2 - 450
        ))
        
        # Setup UI directly without scrollable frame
        self.setup_ui()
        
        # Focus on dialog
        self.dialog.focus_set()
        
        # Bind escape key to close
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_scrollable_frame(self):
        """Create a scrollable frame for the dialog content"""
        # Create main container
        self.main_container = tk.Frame(self.dialog)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create canvas with scrollbar
        self.canvas = tk.Canvas(self.main_container, bg='white')
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        # Configure canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to scroll
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def setup_ui(self):
        """Setup the upload dialog UI"""
        # Main frame
        main_frame = tk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Documents",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Storage stats (load immediately for faster response)
        try:
            stats = self.document_processor.get_storage_stats()
            stats_text = f"📊 Storage: {stats['total_documents']} docs, {stats['total_chunks']} chunks, {stats['total_size_mb']} MB"
        except Exception as e:
            stats_text = "📊 Storage: Loading..."
        
        self.stats_label = tk.Label(
            main_frame,
            text=stats_text,
            font=("Helvetica", 10),
            fg="gray"
        )
        self.stats_label.pack(pady=(0, 20))
        
        # Google Docs Section
        google_frame = tk.LabelFrame(main_frame, text="📄 Google Docs", font=("Helvetica", 12, "bold"), padx=15, pady=15)
        google_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Google Docs URL input
        url_label = tk.Label(google_frame, text="Google Docs URL:", font=("Helvetica", 10))
        url_label.pack(anchor=tk.W, pady=(0, 5))
        
        url_frame = tk.Frame(google_frame)
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.url_entry = tk.Entry(url_frame, font=("Helvetica", 10), width=50)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Import Google Doc button
        import_button = tk.Button(
            url_frame,
            text="Import Google Doc",
            command=self.import_google_doc,
            font=("Helvetica", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.RAISED,
            padx=15,
            pady=5
        )
        import_button.pack(side=tk.RIGHT)
        
        # Docs Info button
        info_button = tk.Button(
            google_frame,
            text="📋 Docs Info",
            command=self.show_docs_info,
            font=("Helvetica", 9),
            bg="#2196F3",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=3
        )
        info_button.pack(anchor=tk.W, pady=(5, 0))
        
        # Local Files Section
        local_frame = tk.LabelFrame(main_frame, text="💻 Local Files", font=("Helvetica", 12, "bold"), padx=15, pady=15)
        local_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Supported formats
        formats_label = tk.Label(local_frame, text="Supported formats: .txt, .pdf, .docx", font=("Helvetica", 9), fg="gray")
        formats_label.pack(anchor=tk.W, pady=(0, 10))
        
        # File selection
        file_frame = tk.Frame(local_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.file_entry = tk.Entry(file_frame, font=("Helvetica", 10))
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_button = tk.Button(
            file_frame,
            text="Browse",
            command=self.browse_file,
            font=("Helvetica", 10),
            bg="#FF9800",
            fg="white",
            relief=tk.RAISED,
            padx=15,
            pady=5
        )
        browse_button.pack(side=tk.RIGHT)
        
        # Upload button
        upload_button = tk.Button(
            local_frame,
            text="Upload Document",
            command=self.upload_document,
            font=("Helvetica", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.RAISED,
            padx=20,
            pady=8
        )
        upload_button.pack(pady=(5, 0))
        
        # Uploaded Documents Section
        docs_frame = tk.LabelFrame(main_frame, text="📚 Uploaded Documents", font=("Helvetica", 12, "bold"), padx=15, pady=15)
        docs_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Documents list
        self.documents_listbox = tk.Listbox(
            docs_frame,
            font=("Helvetica", 10),
            selectmode=tk.SINGLE,
            height=12  # Increased height for better visibility
        )
        self.documents_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Document info label
        self.doc_info_label = tk.Label(docs_frame, text="Select a document to view details", font=("Helvetica", 9), fg="gray")
        self.doc_info_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Action buttons frame
        action_frame = tk.Frame(docs_frame)
        action_frame.pack(fill=tk.X)
        
        # Remove selected button
        remove_button = tk.Button(
            action_frame,
            text="🗑️ Remove Selected",
            command=self.remove_selected_document,
            font=("Helvetica", 9),
            bg="#F44336",
            fg="white",
            relief=tk.RAISED,
            padx=10,
            pady=5
        )
        remove_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Remove all button
        remove_all_button = tk.Button(
            action_frame,
            text="🗑️ Remove All",
            command=self.remove_all_documents,
            font=("Helvetica", 9),
            bg="#FF5722",
            fg="white",
            relief=tk.RAISED,
            padx=10,
            pady=5
        )
        remove_all_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cleanup button
        cleanup_button = tk.Button(
            action_frame,
            text="🧹 Cleanup",
            command=self.cleanup_documents,
            font=("Helvetica", 9),
            bg="#9C27B0",
            fg="white",
            relief=tk.RAISED,
            padx=10,
            pady=5
        )
        cleanup_button.pack(side=tk.LEFT)
        
        # Close button
        close_button = tk.Button(
            main_frame,
            text="Close",
            command=self.dialog.destroy,
            font=("Helvetica", 10, "bold"),
            bg="#607D8B",
            fg="white",
            relief=tk.RAISED,
            padx=20,
            pady=8
        )
        close_button.pack(pady=(10, 0))
        
        # Load documents
        self.load_documents()
        
        # Bind double-click for document info
        self.documents_listbox.bind('<Double-Button-1>', self.show_document_info)
    
    def show_docs_info(self):
        """Show Google Docs instructions dialog"""
        info_dialog = tk.Toplevel(self.dialog)
        info_dialog.title("Google Docs Instructions")
        info_dialog.geometry("500x400")
        info_dialog.transient(self.dialog)
        info_dialog.grab_set()
        
        # Center the dialog
        info_dialog.geometry("+%d+%d" % (
            self.dialog.winfo_rootx() + self.dialog.winfo_width()//2 - 250,
            self.dialog.winfo_rooty() + self.dialog.winfo_height()//2 - 200
        ))
        
        # Main frame
        main_frame = tk.Frame(info_dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="📋 Google Docs Instructions",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Instructions text
        instructions = """
🔗 **How to Import Google Docs:**

1. **Get the URL**: Open your Google Doc and copy the URL from the address bar

2. **Paste the URL**: Paste the Google Docs URL into the input field above

3. **Import**: Click "Import Google Doc" to add it to your documents

4. **Supported Formats**:
   • Google Docs (.gdoc)
   • Google Sheets (.gsheet)
   • Google Slides (.gslides)

5. **Requirements**:
   • Document must be publicly accessible OR
   • You must be logged into the correct Google account

6. **Tips**:
   • Make sure the document is shared with appropriate permissions
   • Large documents may take a moment to process
   • You can import multiple documents

📝 **Note**: The document will be processed and added to your local storage for AI analysis.
        """
        
        text_widget = tk.Text(
            main_frame,
            font=("Helvetica", 10),
            wrap=tk.WORD,
            padx=10,
            pady=10,
            bg="#f5f5f5",
            relief=tk.SUNKEN
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, instructions)
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        close_button = tk.Button(
            main_frame,
            text="Close",
            command=info_dialog.destroy,
            font=("Helvetica", 10, "bold"),
            bg="#607D8B",
            fg="white",
            relief=tk.RAISED,
            padx=20,
            pady=8
        )
        close_button.pack(pady=(15, 0))
    
    def update_storage_stats(self):
        """Update storage statistics display"""
        try:
            stats = self.document_processor.get_storage_stats()
            stats_text = f"📊 Storage: {stats['total_documents']} docs, {stats['total_chunks']} chunks, {stats['total_size_mb']} MB"
            self.stats_label.config(text=stats_text)
        except Exception as e:
            self.stats_label.config(text="📊 Storage: Unable to load stats")
    
    def show_document_info(self, event=None):
        """Show detailed information about the selected document"""
        selection = self.documents_listbox.curselection()
        if not selection:
            return
        
        documents = self.document_processor.list_documents()
        if selection[0] < len(documents):
            doc_id = documents[selection[0]]["id"]
            doc_info = self.document_processor.get_document_info(doc_id)
            
            if doc_info:
                info_text = f"📄 {doc_info['filename']}\n"
                info_text += f"📅 Uploaded: {doc_info['uploaded_at']}\n"
                info_text += f"📊 Chunks: {doc_info['chunks_count']}\n"
                info_text += f"💾 Size: {round(doc_info['storage_size'] / 1024, 1)} KB\n"
                info_text += f"🔍 Type: {doc_info.get('file_type', 'Unknown')}"
                
                self.doc_info_label.config(text=info_text)
    
    def remove_all_documents(self):
        """Remove all documents with confirmation"""
        import tkinter.messagebox as messagebox
        if messagebox.askyesno("Remove All Documents", 
                             "Are you sure you want to remove ALL documents?\n\nThis action cannot be undone."):
            self.document_processor.clear_all_documents()
            self.update_document_list()
            self.update_storage_stats()
            self.doc_info_label.config(text="All documents removed")
            self.status_label.config(text="✅ All documents removed successfully")
    
    def cleanup_documents(self):
        """Clean up orphaned files"""
        try:
            self.document_processor.cleanup_orphaned_files()
            self.update_document_list()
            self.update_storage_stats()
            messagebox.showinfo("Cleanup Complete", "✅ Cleanup completed successfully")
        except Exception as e:
            messagebox.showerror("Cleanup Error", f"❌ Cleanup failed: {str(e)}")
    
    def cleanup_orphaned_files(self):
        """Clean up orphaned chunk files"""
        try:
            self.document_processor.cleanup_orphaned_files()
            self.update_document_list()
            self.update_storage_stats()
            messagebox.showinfo("Cleanup Complete", "✅ Cleanup completed successfully")
        except Exception as e:
            messagebox.showerror("Cleanup Error", f"❌ Cleanup failed: {str(e)}")
    
    def on_url_change(self, *args):
        """Callback for when the Google Docs URL entry changes"""
        url = self.url_var.get().strip()
        if url:
            self.import_button.config(state="normal")
            self.status_label.config(text="Enter a Google Docs URL to import")
        else:
            self.import_button.config(state="disabled")
            self.status_label.config(text="Select a document or enter a Google Docs URL")
    
    def import_google_doc(self):
        """Import document from Google Docs URL"""
        url = self.url_entry.get().strip() # Changed from self.url_var.get()
        if not url:
            self.status_label.config(text="Please enter a Google Docs URL")
            return
        
        self.status_label.config(text="Importing from Google Docs...")
        self.import_button.config(state="disabled")
        
        # Import in a separate thread
        def import_thread():
            try:
                doc_id = self.google_processor.process_google_doc_url(url, self.document_processor)
                if doc_id:
                    self.parent.after(0, lambda: self.status_label.config(
                        text="✅ Successfully imported from Google Docs"
                    ))
                    self.parent.after(0, self.update_document_list)
                    self.parent.after(0, lambda: self.url_entry.delete(0, tk.END)) # Changed from self.url_var.set("")
                else:
                    self.parent.after(0, lambda: self.status_label.config(
                        text="❌ Failed to import from Google Docs"
                    ))
            except Exception as e:
                self.parent.after(0, lambda: self.status_label.config(
                    text=f"❌ Error: {str(e)}"
                ))
            finally:
                self.parent.after(0, lambda: self.import_button.config(state="normal"))
        
        import threading
        threading.Thread(target=import_thread, daemon=True).start()
    
    def browse_file(self):
        """Open file browser dialog"""
        import tkinter.filedialog as filedialog
        
        # Use a simpler, faster approach
        try:
            # Start with a basic dialog for speed
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
                    
        except Exception as e:
            print(f"File dialog error: {e}")
            # Fallback to basic file dialog
            file_path = filedialog.askopenfilename(title="Select Document")
        
        if file_path:
            self.file_entry.delete(0, tk.END) # Changed from self.file_path_var.set(file_path)
            self.file_entry.insert(0, file_path) # Changed from self.file_path_var.set(file_path)
            self.upload_button.config(state="normal")
            self.status_label.config(text=f"Selected: {os.path.basename(file_path)}")
    
    def upload_document(self):
        """Upload the selected document"""
        file_path = self.file_entry.get() # Changed from self.file_path_var.get()
        if not file_path:
            return
        
        self.status_label.config(text="Processing document...")
        self.upload_button.config(state="disabled")
        
        # Process document in a separate thread
        def process_thread():
            try:
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
                    text=f"❌ Error: {str(e)}"
                ))
            finally:
                self.parent.after(0, lambda: self.upload_button.config(state="normal"))
        
        import threading
        threading.Thread(target=process_thread, daemon=True).start()
    
    def update_document_list(self):
        """Update the document list display"""
        self.documents_listbox.delete(0, tk.END)
        documents = self.document_processor.list_documents()
        
        for doc in documents:
            display_text = f"{doc['filename']} ({doc['chunks_count']} chunks)"
            self.documents_listbox.insert(tk.END, display_text)
    
    def remove_selected_document(self):
        """Remove the selected document"""
        import tkinter.messagebox as messagebox
        
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
