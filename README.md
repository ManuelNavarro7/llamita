# 🦙 Llamita - Intelligent AI Assistant

A beautiful, text-based AI assistant that runs locally using Ollama. Llamita provides a clean, modern interface for chatting with your local AI models.

## 🚀 Quick Start (macOS)

### 1. Clone and Build
```bash
# Clone the repository
git clone https://github.com/ManuelNavarro7/llamita.git
cd llamita

# Build the macOS app
python3 setup.py py2app
```

### 2. Run the App
```bash
# Run the app
open dist/Llamita.app
```

### 3. Set Up Ollama (First Time Only)
```bash
# Start Ollama (in a separate terminal)
ollama serve

# Download a model (in another terminal)
ollama pull llama3:8b
```

That's it! 🎉 Your Llamita app is ready to use.

## 🔧 Alternative Run Methods

### Direct Python Run (for development)
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run directly
PYTHONPATH=src python3 src/voice_assistant.py
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
