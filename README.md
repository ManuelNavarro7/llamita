# 🦙 Llamita - Intelligent AI Assistant

A beautiful, text-based AI assistant that runs locally using Ollama. Llamita provides a clean, modern interface for chatting with your local AI models.

## 🚀 Quick Start

### Option 1: Manual Installation (Recommended)
```bash
# Clone the repository
git clone https://github.com/ManuelNavarro7/llamita.git
cd llamita

# Install dependencies
pip3 install -r requirements.txt

# Make scripts executable
chmod +x scripts/*.sh

# Start Ollama (in a separate terminal)
ollama serve

# Download a model (in another terminal)
ollama pull llama3:8b

# Run the app
./scripts/run_simple.sh
```

### Option 2: One-Command Installation (if GitHub allows)
```bash
# Try this first (may be rate limited)
curl -fsSL https://raw.githubusercontent.com/ManuelNavarro7/llamita/main/scripts/install_everything.sh | bash
```

### Option 3: Local Installation Script
```bash
# Download and run the local installer
curl -fsSL https://raw.githubusercontent.com/ManuelNavarro7/llamita/main/scripts/install_local.sh > install_llamita.sh
chmod +x install_llamita.sh
./install_llamita.sh
```

## 🔧 Alternative Run Methods

### Method 1: Simple Run (Recommended)
```bash
./scripts/run_simple.sh
```

### Method 2: Clean Run (No Warnings)
```bash
./scripts/run_clean.sh
```

### Method 3: Virtual Environment Run
```bash
./scripts/run_voice_assistant.sh
```

### Method 4: Direct Run
```bash
PYTHONPATH=src python3 src/voice_assistant.py
```

## 🛠️ Troubleshooting

### Common Issues:
- **"ModuleNotFoundError: No module named 'config'"** → Use `PYTHONPATH=src python3 src/voice_assistant.py`
- **"Ollama is not running"** → Start Ollama with `ollama serve`
- **Permission errors** → Run `chmod +x scripts/*.sh`
- **Missing dependencies** → Run `pip3 install -r requirements.txt`
- **GitHub rate limiting (429 error)** → Use manual installation instead

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
- **🎨 Beautiful UI** - Clean, modern interface with custom llama icon
- **📱 Native macOS App** - Properly packaged as a `.app` bundle
- **🔧 Easy Installation** - Multiple installation methods available

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
