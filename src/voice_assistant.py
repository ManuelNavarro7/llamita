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
        
        # Configure button style for rounded corners
        self.setup_button_style()
        
        print("✅ Window configured")
    
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
        
        # Initialize components (voice disabled)
        self.recognizer = None
        self.microphone = None
        self.voice_input_enabled = False
        
        self.is_listening = False
        self.ollama_url = config.OLLAMA_URL
        
        # Conversation context
        self.conversation_history = []
        self.max_history_length = 10  # Keep last 10 exchanges for context
        
        # Voice input state (text responses only)
        self.voice_input_enabled = False
        
        # Document processing
        if DOCUMENT_PROCESSING_AVAILABLE:
            self.document_processor = DocumentProcessor()
            print("✅ Document processing initialized")
        else:
            self.document_processor = None
            print("⚠️ Document processing not available")
        
        print("🖥️ Setting up UI...")
        self.setup_ui()
        print("✅ UI setup complete")
        
        print("🧹 Cleaning up previous processes...")
        self.cleanup_previous_processes()
        print("✅ Process cleanup complete")
        print("🎉 Voice Assistant ready!")
    
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
            self.upload_button = ttk.Button(
                control_frame,
                text="📄 Upload Documents",
                command=self.open_document_upload,
                style='Rounded.TButton'
            )
            self.upload_button.pack(side=tk.LEFT)
        
        # Clear conversation button
        self.clear_button = ttk.Button(
            control_frame,
            text="Clear Chat",
            command=self.clear_chat,
            style='Rounded.TButton'
        )
        self.clear_button.pack(side=tk.RIGHT)
        
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
        
        # Text input entry
        self.input_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            bg=config.COLORS['secondary'],
            fg=config.COLORS['text'],
            insertbackground=config.COLORS['text']
        )
        self.input_entry.pack(fill=tk.X, pady=(5, 0))
        self.input_entry.bind('<Return>', self.send_message)
        
        # Send button
        self.send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            style='Rounded.TButton'
        )
        self.send_button.pack(pady=(10, 0))
        
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
        
        welcome_msg += "\n\nHow can I assist you today?"
        self.add_to_chat(welcome_msg)
    
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
    
    def send_message(self, event=None):
        """Send a text message to the assistant"""
        text = self.input_entry.get().strip()
        if not text:
            return
        
        # Clear input
        self.input_entry.delete(0, tk.END)
        
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
        if DOCUMENT_PROCESSING_AVAILABLE and self.document_processor:
            dialog = DocumentUploadDialog(self.root, self.document_processor)
        else:
            messagebox.showwarning(
                "Document Processing Unavailable",
                "Document processing is not available. Please install the required dependencies:\n\npip install PyPDF2 python-docx pandas openpyxl"
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
        
        # Add welcome message
        app.add_to_chat("Llamita: 🦙 Hello! I'm Llamita, your local AI assistant.")
        app.add_to_chat("Llamita: 💡 Type a message and press Enter to chat with me.")
        
        if DOCUMENT_PROCESSING_AVAILABLE:
            app.add_to_chat("Llamita: 📄 Upload documents and ask me questions about them!")
        
        app.add_to_chat("Llamita: Make sure Ollama is running with 'ollama serve' to chat with me!")
        
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
