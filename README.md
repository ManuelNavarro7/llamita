# 🦙 Llamita - Intelligent AI Assistant

A beautiful, text-based AI assistant that runs locally using Ollama. Llamita provides a clean, modern interface for chatting with your local AI models.

## 🚀 Quick Start (macOS)

### Option 1: One-Command Installation (Recommended)
```bash
# Clone the repository
git clone https://github.com/ManuelNavarro7/llamita.git
cd llamita

# Install Python dependencies first
pip3 install -r requirements.txt

# Run the installation script
./scripts/install_llamita.sh
```

This will:
- ✅ Install Python 3 (if not already installed)
- ✅ Install Ollama (if not already installed)
- ✅ Download a model (llama3:8b)
- ✅ Build the macOS app
- ✅ Install to Applications folder
- ✅ Create a desktop shortcut

### Option 2: Manual Installation
```bash
# Clone the repository
git clone https://github.com/ManuelNavarro7/llamita.git
cd llamita

# Install Python dependencies first
pip3 install -r requirements.txt

# Build the macOS app
python3 setup.py py2app

# Run the app
open dist/Llamita.app
```

### Set Up Ollama (First Time Only)
```bash
# Start Ollama (in a separate terminal)
ollama serve

# Download a model (in another terminal)
ollama pull llama3:8b
```

### Install Document Processing (Optional)
```bash
# Install document processing dependencies
./scripts/install_document_deps.sh
```

This enables:
- 📄 PDF document processing
- 📝 Word document (.docx) support
- 📊 Spreadsheet (.csv, .xlsx) analysis
- 📋 Text file (.txt) processing
- 🌐 Google Docs & Sheets integration

That's it! 🎉 Your Llamita app is ready to use.

## 🦙 First Run Experience

When you run Llamita for the first time, you'll see a beautiful loading screen with the Llamita icon. This takes about 1-2 minutes and ensures all components are properly initialized.

**What happens during loading:**
- 🔧 Setting up components...
- 🤖 Initializing AI components...
- 🖥️ Setting up interface...
- 🧹 Cleaning up processes...
- ✅ Ready!

**If you see dependency warnings:** Don't worry! The app will still work, but document processing features won't be available until you install the optional dependencies.

**If the loading screen doesn't appear:**
1. Make sure you're running the latest version
2. Try running directly: `python3 src/voice_assistant.py`
3. Check the terminal for any error messages
4. Test loading screen visibility: `python3 scripts/test_loading_visibility.py`

## 📄 Document Processing

Llamita can now process and answer questions about your documents!

### Upload Documents
1. Start Llamita
2. Click "📄 Upload Documents + Google" button
3. Choose your method:
   - **Local Files**: Select files from your computer
   - **Google Docs**: Paste Google Docs/Sheets URLs
4. Ask questions about your documents

### Google Docs & Sheets Integration
- **Direct URL Import**: Paste Google Docs URLs to import automatically
- **Manual Export**: Download from Google Workspace and upload
- **Supported**: Google Docs, Google Sheets, Google Slides
- **Formats**: PDF, DOCX, XLSX, CSV, PPTX

### Example Questions
- "What does the document say about [topic]?"
- "Summarize the main points"
- "What are the key findings?"
- "Can you explain the data in the spreadsheet?"

### Supported Formats
- **PDF Documents** (.pdf)
- **Word Documents** (.docx)
- **Text Files** (.txt)
- **Spreadsheets** (.csv, .xlsx, .xls)
- **Google Workspace** (Docs, Sheets, Slides)

## 🔧 Alternative Run Methods

### Direct Python Run (for development)
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run directly
PYTHONPATH=src python3 src/voice_assistant.py
```

> **💡 Note:** On first run, you'll see a beautiful loading screen with the Llamita icon while the app initializes. This takes about 1-2 minutes and ensures everything works perfectly!
```

### Using Scripts
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Run with script
./scripts/run_simple.sh
```

## 🛠️ Troubleshooting

### Common Issues:
- **"Ollama is not running"** → Start Ollama with `ollama serve`
- **"icon file must exist"** → Make sure you cloned the full repository
- **App won't start** → Check that Ollama is running and you have a model downloaded

## 🗑️ Uninstall

To completely remove Llamita from your system:

```bash
# Run the uninstall script
./scripts/uninstall_llamita.sh
```

This will remove:
- ✅ Llamita from Applications folder
- ✅ Desktop shortcut
- ✅ Build files
- ✅ All references to Llamita

**Note**: Ollama and models are NOT removed (you might want to keep them for other projects).

## 📁 Project Structure

```
llamita/
├── src/                    # Source code
│   ├── voice_assistant.py  # Main application
│   └── config.py          # Configuration
├── scripts/                # Build and utility scripts  
├── docs/                   # Documentation
├── assets/                 # Assets and resources
└── dist/                   # Built macOS app
```

## 📖 Documentation

- **[Full Documentation](docs/README.md)** - Complete setup and usage guide
- **[Setup Instructions](docs/SETUP_INSTRUCTIONS.md)** - Detailed installation guide
- **[Installation Guide](docs/INSTALLATION_GUIDE.md)** - Comprehensive installation guide
- **[Quick Install Guide](docs/QUICK_INSTALL.md)** - Quick installation methods
- **[License Information](docs/LICENSE)** - Licensing terms
- **[Commercial License](docs/COMMERCIAL_LICENSE.md)** - Commercial use terms

## 🎯 Features

- **🤖 Local AI** - Runs completely offline using Ollama
- **💬 Conversation Memory** - Maintains context across messages
- **📄 Document Processing** - Upload and ask questions about PDF, DOCX, TXT, CSV, Excel files
- **🎨 Beautiful UI** - Clean, modern interface with custom llama icon
- **📱 Native macOS App** - Properly packaged as a `.app` bundle
- **🚀 Easy Setup** - Simple 3-step installation process

## 📝 License

This project uses **dual licensing**:
- **Personal/Educational Use**: Free
- **Commercial Use**: Paid license required ($1 USD)

See [docs/LICENSE](docs/LICENSE) and [docs/COMMERCIAL_LICENSE.md](docs/COMMERCIAL_LICENSE.md) for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a Pull Request

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/ManuelNavarro7/llamita/issues)
- **Commercial Inquiries**: manuel.navarro.work@gmail.com

---

**Made with ❤️ and 🦙 by the Llamita team**
