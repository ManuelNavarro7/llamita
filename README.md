# 🦙 Llamita - Intelligent AI Assistant

A beautiful, text-based AI assistant that runs locally using Ollama. Llamita provides a clean, modern interface for chatting with your local AI models.

## 🚀 Quick Start

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

## 🔧 Alternative Installation Methods

### Method 1: Simple Run (Recommended)
```bash
./scripts/run_simple.sh
```

### Method 2: Virtual Environment Run
```bash
./scripts/run_voice_assistant.sh
```

### Method 3: Direct Run
```bash
PYTHONPATH=src python3 src/voice_assistant.py
```

## 🛠️ Troubleshooting

### Common Issues:
- **"ModuleNotFoundError: No module named 'config'"** → Use `PYTHONPATH=src python3 src/voice_assistant.py`
- **"Ollama is not running"** → Start Ollama with `ollama serve`
- **Permission errors** → Run `chmod +x scripts/*.sh`
- **Missing dependencies** → Run `pip3 install -r requirements.txt`

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
- **[License Information](docs/LICENSE)** - Licensing terms
- **[Commercial License](docs/COMMERCIAL_LICENSE.md)** - Commercial use terms

## 🎯 Features

- **🤖 Local AI** - Runs completely offline using Ollama
- **💬 Conversation Memory** - Maintains context across messages
- **🎨 Beautiful UI** - Clean, modern interface with custom llama icon
- **📱 Native macOS App** - Properly packaged as a `.app` bundle

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
