#!/usr/bin/env python3
"""
Local Voice Assistant Desktop App for macOS
Powered by Ollama with offline speech recognition and macOS TTS
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json
import threading
import time
import subprocess
import sys
import os
from datetime import datetime

# Import document processor
try:
    from document_processor import DocumentProcessor, DocumentUploadDialog
    DOCUMENT_PROCESSING_AVAILABLE = True
except ImportError:
    DOCUMENT_PROCESSING_AVAILABLE = False
    print("⚠️ Document processing not available - install required dependencies")

# Import Google Docs processor
try:
    from google_docs_processor import GoogleDocsProcessor, GoogleDocsUploadDialog
    GOOGLE_DOCS_AVAILABLE = True
except ImportError:
    GOOGLE_DOCS_AVAILABLE = False
    print("⚠️ Google Docs integration not available - install required dependencies")
try:
    import config
except ImportError:
    # If config.py is not available, use default values
    class Config:
        WINDOW_WIDTH = 800
        WINDOW_HEIGHT = 600
        OLLAMA_URL = "http://localhost:11434/api/generate"
        DEFAULT_MODEL = "llama3:8b"
        COLORS = {
            'background': '#2c3e50',
            'secondary': '#34495e',
            'text': '#ecf0f1',
            'text_secondary': '#bdc3c7',
            'success': '#3498db',
            'warning': '#f39c12',
            'error': '#e74c3c',
            'info': '#3498db',
            'button_bg': '#3498db',
            'button_fg': 'white',
            'button_active': '#2980b9',
            'button_disabled': '#95a5a6'
        }
        SYSTEM_PROMPTS = {
            "default": "You are Llamita, a helpful AI assistant."
        }
    
    config = Config()

# Speech recognition import (disabled for now)
SPEECH_RECOGNITION_AVAILABLE = False

class VoiceAssistant:
    def __init__(self, root):
        try:
            print("🔧 Initializing Voice Assistant...")
            self.root = root
            self.root.title("🦙 Llamita")
            self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
            self.root.configure(bg=config.COLORS['background'])
            
            # Prevent window from closing immediately
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # Add a flag to prevent immediate closing
            self._closing = False
            
        except Exception as e:
            print(f"❌ Error in VoiceAssistant.__init__: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        # Set custom icon if available
        try:
            # First, try to clear any existing icon completely
            try:
                self.root.iconbitmap(default='')
                self.root.iconphoto(True, tk.PhotoImage())  # Set empty photo
                print("✅ Default icon cleared")
            except:
                pass
            
            # Find the repo root by looking for the assets directory
            def find_repo_root():
                current_dir = os.path.dirname(__file__)
                while current_dir != os.path.dirname(current_dir):  # Stop at filesystem root
                    if os.path.exists(os.path.join(current_dir, "assets", "icons", "llamita_icon.png")):
                        return current_dir
                    current_dir = os.path.dirname(current_dir)
                return None
            
            repo_root = find_repo_root()
            
            # Try multiple possible icon paths (prioritize existing assets)
            icon_paths = []
            
            # If we found the repo root, use it
            if repo_root:
                icon_paths.append(os.path.join(repo_root, "assets", "icons", "llamita_icon.png"))
            
            # Add fallback paths
            icon_paths.extend([
                os.path.join(os.getcwd(), "assets", "icons", "llamita_icon.png"),  # From current working directory
                "assets/icons/llamita_icon.png",  # Relative to current directory
                os.path.join(os.path.dirname(__file__), "llamita_icon.png"),  # Script directory
                os.path.join(os.path.dirname(sys.executable), "..", "Resources", "llamita_icon.png"),  # App bundle
                os.path.join(os.path.dirname(sys.executable), "..", "Resources", "llamita_icon.icns"),  # App bundle icns
            ])
            
            icon_loaded = False
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    if icon_path.endswith('.icns'):
                        # For .icns files, we can't use PhotoImage directly
                        # The icon is handled by the app bundle
                        print("✅ Custom icon available (handled by app bundle)")
                        icon_loaded = True
                        break
                    elif icon_path.endswith('.ico'):
                        # For .ico files, try to convert or use as is
                        try:
                            icon = tk.PhotoImage(file=icon_path)
                            self.root.iconphoto(True, icon)
                            print("✅ Custom ICO icon loaded")
                            icon_loaded = True
                            break
                        except:
                            print(f"⚠️ Could not load ICO icon: {icon_path}")
                            continue
                    else:
                        # PNG files
                        icon = tk.PhotoImage(file=icon_path)
                        self.root.iconphoto(True, icon)
                        print(f"✅ Custom icon loaded: {icon_path}")
                        icon_loaded = True
                        break
            
            if not icon_loaded:
                # Try additional methods to clear the Python icon
                try:
                    # Set a minimal 1x1 transparent icon
                    empty_icon = tk.PhotoImage(width=1, height=1)
                    self.root.iconphoto(True, empty_icon)
                    print("✅ Set minimal transparent icon")
                except:
                    pass
                print("⚠️ Could not find custom icon")
        except Exception as e:
            print(f"⚠️ Could not load custom icon: {e}")
            # Try to clear the default Python icon as fallback
            try:
                self.root.iconbitmap(default='')
                empty_icon = tk.PhotoImage(width=1, height=1)
                self.root.iconphoto(True, empty_icon)
                print("✅ Default icon cleared (fallback)")
            except:
                pass
        
        # Show loading screen first
        self.show_loading_screen()
        
        # Initialize basic components
        self.initialize_basic_components()
        
        print("✅ Window configured")
    
    def show_loading_screen(self):
        """Show loading screen with Llamita icon while initializing"""
        # Create loading window
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.title("🦙 Llamita - Loading...")
        self.loading_window.geometry("400x300")
        self.loading_window.configure(bg=config.COLORS['background'])
        self.loading_window.resizable(False, False)
        
        # Center the loading window
        self.loading_window.transient(self.root)
        self.loading_window.grab_set()
        
        # Try to load the Llamita icon
        icon_photo = None
        try:
            # Find icon path
            def find_icon_path():
                current_dir = os.path.dirname(__file__)
                while current_dir != os.path.dirname(current_dir):
                    icon_path = os.path.join(current_dir, "assets", "icons", "llamita_icon.png")
                    if os.path.exists(icon_path):
                        return icon_path
                    current_dir = os.path.dirname(current_dir)
                return None
            
            icon_path = find_icon_path()
            if icon_path:
                # Resize icon for loading screen (64x64)
                from PIL import Image, ImageTk
                img = Image.open(icon_path)
                img = img.resize((64, 64), Image.Resampling.LANCZOS)
                icon_photo = ImageTk.PhotoImage(img)
                print("✅ Loading screen icon loaded")
            else:
                print("⚠️ Could not find icon for loading screen")
        except Exception as e:
            print(f"⚠️ Error loading icon: {e}")
        
        # Create loading screen content
        main_frame = tk.Frame(self.loading_window, bg=config.COLORS['background'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        
        # Icon label
        if icon_photo:
            icon_label = tk.Label(main_frame, image=icon_photo, bg=config.COLORS['background'])
            icon_label.image = icon_photo  # Keep a reference
            icon_label.pack(pady=(0, 20))
        else:
            # Fallback to text icon
            icon_label = tk.Label(main_frame, text="🦙", font=("Helvetica", 48), 
                                fg=config.COLORS['text'], bg=config.COLORS['background'])
            icon_label.pack(pady=(0, 20))
        
        # Title
        title_label = tk.Label(main_frame, text="Llamita", font=("Helvetica", 24, "bold"),
                              fg=config.COLORS['text'], bg=config.COLORS['background'])
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(main_frame, text="AI Assistant", font=("Helvetica", 14),
                                fg=config.COLORS['text'], bg=config.COLORS['background'])
        subtitle_label.pack(pady=(0, 30))
        
        # Loading message
        self.loading_label = tk.Label(main_frame, text="Initializing...", font=("Helvetica", 12),
                                     fg=config.COLORS['text'], bg=config.COLORS['background'])
        self.loading_label.pack(pady=(0, 20))
        
        # Progress bar
        self.progress_var = tk.StringVar(value="⏳")
        progress_label = tk.Label(main_frame, textvariable=self.progress_var, font=("Helvetica", 16),
                                fg=config.COLORS['button_bg'], bg=config.COLORS['background'])
        progress_label.pack()
        
        # Start initialization in background
        self.root.after(100, self.initialize_with_loading)
    
    def initialize_with_loading(self):
        """Initialize components with loading progress updates"""
        try:
            # Step 1: Initialize basic components
            self.update_loading_status("Setting up components...", "⏳")
            self.root.after(500, self.step_2_initialize_processors)
        except Exception as e:
            print(f"❌ Error in initialization: {e}")
            self.hide_loading_screen()
    
    def step_2_initialize_processors(self):
        """Step 2: Initialize document processors"""
        try:
            # Initialize processors in background
            self.document_processor = None
            self.google_processor = None
            self._processors_ready = False
            
            def init_processors():
                try:
                    if DOCUMENT_PROCESSING_AVAILABLE:
                        self.document_processor = DocumentProcessor()
                        print("✅ Document processing initialized")
                    
                    if GOOGLE_DOCS_AVAILABLE:
                        self.google_processor = GoogleDocsProcessor()
                        print("✅ Google Docs integration initialized")
                    
                    self._processors_ready = True
                except Exception as e:
                    print(f"⚠️ Error initializing processors: {e}")
            
            # Start initialization in background
            import threading
            thread = threading.Thread(target=init_processors, daemon=True)
            thread.start()
            
            self.update_loading_status("Initializing AI components...", "⏳")
            self.root.after(800, self.step_3_setup_ui)
        except Exception as e:
            print(f"❌ Error in processor initialization: {e}")
            self.hide_loading_screen()
    
    def step_3_setup_ui(self):
        """Step 3: Setup UI components"""
        try:
            self.update_loading_status("Setting up interface...", "⏳")
            self.setup_ui()
            # Store reference to chat_text for later use
            self.chat_text = getattr(self, 'chat_text', None)
            self.update_loading_status("Cleaning up processes...", "⏳")
            self.root.after(500, self.step_4_finalize)
        except Exception as e:
            print(f"❌ Error in UI setup: {e}")
            self.hide_loading_screen()
    
    def step_4_finalize(self):
        """Step 4: Finalize initialization"""
        try:
            self.cleanup_previous_processes()
            self.update_loading_status("Ready!", "✅")
            self.root.after(500, self.hide_loading_screen)
        except Exception as e:
            print(f"❌ Error in finalization: {e}")
            self.hide_loading_screen()
    
    def update_loading_status(self, message, icon):
        """Update loading screen status"""
        try:
            self.loading_label.config(text=message)
            self.progress_var.set(icon)
        except Exception as e:
            print(f"⚠️ Error updating loading status: {e}")
    
    def hide_loading_screen(self):
        """Hide loading screen and show main interface"""
        try:
            if hasattr(self, 'loading_window') and self.loading_window:
                self.loading_window.destroy()
                self.loading_window = None
            print("✅ Loading screen hidden, main interface ready")
            
            # Add welcome messages after UI is ready
            self.root.after(100, self.add_welcome_messages)
        except Exception as e:
            print(f"⚠️ Error hiding loading screen: {e}")
    
    def add_welcome_messages(self):
        """Add welcome messages after UI is ready"""
        try:
            self.add_to_chat("Llamita: 🦙 Hello! I'm Llamita, your local AI assistant.")
            self.add_to_chat("Llamita: 💡 Type a message and press Enter to chat with me.")
            
            if DOCUMENT_PROCESSING_AVAILABLE:
                self.add_to_chat("Llamita: 📄 Upload documents and ask me questions about them!")
            
            self.add_to_chat("Llamita: Make sure Ollama is running with 'ollama serve' to chat with me!")
        except Exception as e:
            print(f"⚠️ Error adding welcome messages: {e}")
    
    def initialize_basic_components(self):
        """Initialize basic components without UI setup"""
        # Set up button style
        self.setup_button_style()
        
        # Initialize basic variables
        self.recognizer = None
        self.microphone = None
        self.voice_input_enabled = False
        self.is_listening = False
        self.ollama_url = config.OLLAMA_URL
        
        # Conversation context
        self.conversation_history = []
        self.max_history_length = 10
        
        # Voice input state (text responses only)
        self.voice_input_enabled = False
    
    def setup_button_style(self):
        """Setup custom button styling for rounded corners"""
        style = ttk.Style()
        style.theme_use('default')
        
        # Create custom button style
        style.configure('Rounded.TButton',
                       background=config.COLORS['button_bg'],
                       foreground=config.COLORS['button_fg'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Helvetica', 12, 'bold'),
                       relief='flat')
        
        style.map('Rounded.TButton',
                 background=[('active', config.COLORS['button_active']),
                           ('disabled', config.COLORS['button_disabled'])],
                 foreground=[('disabled', config.COLORS['button_disabled'])])
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg=config.COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🦙 Llamita",
            font=("Helvetica", 28, "bold"),
            fg=config.COLORS['text'],
            bg=config.COLORS['background']
        )
        title_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg=config.COLORS['secondary'], relief=tk.RAISED, bd=2)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = tk.Label(
            status_frame,
            text="Status: Ready (Text mode)",
            font=("Helvetica", 12),
            fg=config.COLORS['text'],
            bg=config.COLORS['secondary']
        )
        status_frame.pack_propagate(False)
        status_frame.configure(height=40)
        self.status_label.pack(expand=True)
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg=config.COLORS['background'])
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Document upload button (if available)
        if DOCUMENT_PROCESSING_AVAILABLE:
            button_text = "📄 Upload Documents"
            if GOOGLE_DOCS_AVAILABLE:
                button_text = "📄 Upload Documents + Google"
            
            self.upload_button = ttk.Button(
                control_frame,
                text=button_text,
                command=self.open_document_upload,
                style='Rounded.TButton'
            )
            self.upload_button.pack(side=tk.LEFT)
            # Add multiple click bindings for better responsiveness
            self.upload_button.bind('<Button-1>', lambda e: self.open_document_upload())
            self.upload_button.bind('<Double-Button-1>', lambda e: self.open_document_upload())
        
        # Clear conversation button with improved responsiveness
        self.clear_button = ttk.Button(
            control_frame,
            text="Clear Chat",
            command=self.clear_chat,
            style='Rounded.TButton'
        )
        self.clear_button.pack(side=tk.RIGHT)
        # Add multiple click bindings for better responsiveness
        self.clear_button.bind('<Button-1>', lambda e: self.clear_chat())
        self.clear_button.bind('<Double-Button-1>', lambda e: self.clear_chat())
        
        # Text input frame
        input_frame = tk.Frame(main_frame, bg=config.COLORS['background'])
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Text input label
        input_label = tk.Label(
            input_frame,
            text="Type your message:",
            font=("Helvetica", 12),
            fg=config.COLORS['text'],
            bg=config.COLORS['background']
        )
        input_label.pack(anchor=tk.W)
        
        # Text input entry with improved responsiveness
        self.input_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            bg=config.COLORS['secondary'],
            fg=config.COLORS['text'],
            insertbackground=config.COLORS['text'],
            relief=tk.SOLID,
            bd=2,
            highlightthickness=1,
            highlightcolor=config.COLORS['button_bg'],
            highlightbackground=config.COLORS['secondary']
        )
        self.input_entry.pack(fill=tk.X, pady=(5, 0))
        self.input_entry.bind('<Return>', self.send_message)
        self.input_entry.bind('<FocusIn>', self.on_input_focus)
        self.input_entry.bind('<FocusOut>', self.on_input_focus_out)
        
        # Set focus to input field immediately for better responsiveness
        self.input_entry.focus_set()
        
        # Send button with improved responsiveness
        self.send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            style='Rounded.TButton'
        )
        self.send_button.pack(pady=(10, 0))
        self.send_button.bind('<Button-1>', lambda e: self.send_message())
        self.send_button.bind('<Return>', lambda e: self.send_message())
        
        # Chat display frame
        chat_frame = tk.Frame(main_frame, bg=config.COLORS['background'])
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        # Chat display label
        chat_label = tk.Label(
            chat_frame,
            text="Conversation:",
            font=("Helvetica", 12),
            fg=config.COLORS['text'],
            bg=config.COLORS['background']
        )
        chat_label.pack(anchor=tk.W)
        
        # Chat text area
        self.chat_text = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Helvetica", 11),
            bg=config.COLORS['secondary'],
            fg=config.COLORS['text'],
            insertbackground=config.COLORS['text'],
            height=15
        )
        self.chat_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Add welcome message
        welcome_msg = "Llamita: Hello! I'm Llamita, your intelligent AI assistant. I'm here to help you with any questions, tasks, or conversations you might have. Simply type your message and I'll respond."
        
        if DOCUMENT_PROCESSING_AVAILABLE:
            welcome_msg += "\n\n📄 Document Feature: You can upload documents (PDF, DOCX, TXT, CSV, Excel) and I'll use them to answer your questions. Click 'Upload Documents' to get started!"
            
            if GOOGLE_DOCS_AVAILABLE:
                welcome_msg += "\n\n🌐 Google Docs & Sheets: You can also import documents directly from Google Workspace!"
        
        welcome_msg += "\n\nHow can I assist you today?"
        self.add_to_chat(welcome_msg)
        
        # Ensure input field has focus after UI setup
        self.root.after(100, self.ensure_input_focus)
        
        # Bind window focus events for better input responsiveness
        self.root.bind('<FocusIn>', lambda e: self.ensure_input_focus())
        self.root.bind('<Map>', lambda e: self.ensure_input_focus())
    
    # Voice input methods (disabled for simplified interface - uncomment for future use)
    """
    def toggle_voice_input(self):
        # Voice input functionality - disabled for simplified interface
        pass
    
    def start_listening(self):
        # Voice listening functionality - disabled for simplified interface
        pass
    
    def pause_listening(self):
        # Voice pause functionality - disabled for simplified interface
        pass
    
    def stop_conversation(self):
        # Voice stop functionality - disabled for simplified interface
        pass
    
    def stop_listening(self):
        # Voice stop functionality - disabled for simplified interface
        pass
    """
    
    def on_input_focus(self, event=None):
        """Handle input field focus in"""
        self.input_entry.config(highlightcolor=config.COLORS['button_bg'])
    
    def on_input_focus_out(self, event=None):
        """Handle input field focus out"""
        self.input_entry.config(highlightcolor=config.COLORS['secondary'])
    
    def ensure_input_focus(self):
        """Ensure input field has focus for better responsiveness"""
        try:
            self.input_entry.focus_set()
            self.input_entry.icursor(tk.END)
        except Exception as e:
            print(f"Focus setting error: {e}")
    
    def send_message(self, event=None):
        """Send a text message to the assistant"""
        text = self.input_entry.get().strip()
        if not text:
            return
        
        # Clear input and restore focus for better responsiveness
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus_set()
        
        # Add user message to chat
        self.add_to_chat(f"You: {text}")
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": text})
        
        # Get AI response with context
        self.update_status("Getting AI response...", "yellow")
        response = self.get_ollama_response_with_context(text)
        
        if response:
            self.add_to_chat(f"Llamita: {response}")
            # Add response to conversation history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Keep conversation history manageable
            if len(self.conversation_history) > self.max_history_length * 2:
                self.conversation_history = self.conversation_history[-self.max_history_length * 2:]
            
            self.update_status("Response received", "green")
        else:
            self.add_to_chat("Llamita: ❌ Sorry, I couldn't get a response. Please check that:")
            self.add_to_chat("   • Ollama is running (ollama serve)")
            self.add_to_chat("   • You have a model downloaded (ollama pull llama3:8b)")
            self.add_to_chat("   • Your internet connection is working")
            self.update_status("Failed to get response - check Ollama connection", "red")
    
    def cleanup_previous_processes(self):
        """Clean up any previous processes"""
        try:
            # Clean up any lingering processes if needed
            pass
        except Exception as e:
            print(f"Error cleaning up processes: {e}")
    

    
    def update_status(self, message, color="white"):
        """Update the status display"""
        self.status_label.config(text=f"Status: {message}", fg=color)
        self.root.update_idletasks()
    

    
    # Voice listening loop (disabled for simplified interface - uncomment for future use)
    """
    def listen_loop(self):
        # Voice listening functionality - disabled for simplified interface
        pass
    """
    
    def get_ollama_response_with_context(self, text):
        """Get response from Ollama with conversation context and document context"""
        try:
            # Build context from conversation history
            context_prompt = ""
            
            # Add system prompt
            system_prompt = config.SYSTEM_PROMPTS.get("default", "You are Llamita, a helpful AI assistant.")
            context_prompt += f"{system_prompt}\n\n"
            
            # Add document context if available
            if DOCUMENT_PROCESSING_AVAILABLE and self.document_processor:
                document_context = self.document_processor.get_document_context(text)
                if document_context:
                    context_prompt += f"Relevant document information:\n{document_context}\n\n"
                    print(f"📄 Added document context for query: {text[:50]}...")
            
            # Add conversation history
            for message in self.conversation_history:
                if message["role"] == "user":
                    context_prompt += f"User: {message['content']}\n"
                elif message["role"] == "assistant":
                    context_prompt += f"Llamita: {message['content']}\n"
            
            # Add current user message
            context_prompt += f"User: {text}\nLlamita:"
            
            # Prepare the request with context
            data = {
                "model": config.DEFAULT_MODEL,
                "prompt": context_prompt,
                "stream": False
            }
            
            # Send request to Ollama
            response = requests.post(
                self.ollama_url,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                print(f"❌ Ollama error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def get_ollama_response(self, text):
        """Get response from Ollama (legacy method - kept for compatibility)"""
        return self.get_ollama_response_with_context(text)
    

    

    
    def add_to_chat(self, message):
        """Add message to chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n\n"
        
        self.chat_text.insert(tk.END, formatted_message)
        self.chat_text.see(tk.END)
        
        # Update the display
        self.root.update_idletasks()
    

    
    def open_document_upload(self):
        """Open the document upload dialog"""
        # Check if processors are ready with better feedback
        if not self._processors_ready:
            messagebox.showinfo(
                "Initializing",
                "Document processing is still initializing. Please wait a moment and try again."
            )
            return
        
        if not self.document_processor:
            messagebox.showwarning(
                "Document Processing Unavailable",
                "Document processing is not available. Please install the required dependencies:\n\npip install PyPDF2 python-docx pandas openpyxl requests"
            )
            return
        
        try:
            if GOOGLE_DOCS_AVAILABLE and self.google_processor:
                # Use enhanced dialog with Google Docs support
                dialog = GoogleDocsUploadDialog(self.root, self.document_processor, self.google_processor)
            else:
                # Use basic dialog
                dialog = DocumentUploadDialog(self.root, self.document_processor)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to open upload dialog: {str(e)}"
            )
    
    def clear_chat(self):
        """Clear the chat display and conversation history"""
        self.chat_text.delete(1.0, tk.END)
        self.conversation_history.clear()
        self.add_to_chat("Llamita: Chat cleared. How can I help you?")
    
    def on_closing(self):
        """Handle window closing"""
        if not self._closing:
            self._closing = True
            print("🔄 Closing Llamita...")
            self.root.destroy()
            print("✅ Llamita closed successfully")

def main():
    """Main function"""
    try:
        # Suppress macOS warnings
        import os
        os.environ['PYTHONUNBUFFERED'] = '1'
        os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
        
        # Suppress specific macOS warnings
        import warnings
        warnings.filterwarnings("ignore", category=UserWarning)
        
        print("🚀 Starting Llamita Voice Assistant...")
        print("📱 Creating GUI window...")
        
        root = tk.Tk()
        print("✅ GUI window created")
        
        # Set a proper window icon to avoid the Python rocket
        try:
            # Try to set a custom icon
            root.iconbitmap(default='')  # Clear default icon
            root.title("🦙 Llamita - Voice Assistant")
        except:
            # If icon setting fails, just set the title
            root.title("🦙 Llamita - Voice Assistant")
        
        # Ensure window is visible and focused
        root.lift()
        root.attributes('-topmost', True)
        root.attributes('-topmost', False)
        root.focus_force()
        
        # Set window to stay on top briefly, then normal
        root.after(1000, lambda: root.attributes('-topmost', False))
        
        app = VoiceAssistant(root)
        print("✅ Voice Assistant initialized")
        
        # Handle window close
        def on_closing():
            print("🔄 Closing Llamita...")
            root.destroy()
            print("✅ Llamita closed successfully")
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        print("🎯 Starting main loop...")
        
        # Add a small delay to ensure window is properly initialized
        root.after(100, lambda: print("🪟 Window should be visible now"))
        
        # Prevent immediate closing
        root.after(500, lambda: root.focus_force())
        
        root.mainloop()
        print("👋 Llamita exited")
        
    except Exception as e:
        print(f"❌ Error in main: {e}")
        import traceback
        traceback.print_exc()
        # Try to show error in a message box if possible
        try:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Llamita Error", f"An error occurred: {e}")
        except:
            pass

if __name__ == "__main__":
    main()
