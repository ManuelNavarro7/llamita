# 🦙 Llamita - Intelligent AI Assistant

A beautiful, text-based AI assistant that runs locally using Ollama. Llamita provides a clean, modern interface for chatting with your local AI models.

## ✨ Features

- **🤖 Local AI**: Runs completely offline using Ollama
- **💬 Conversation Memory**: Maintains context across messages
- **🎨 Beautiful UI**: Clean, modern interface with custom llama icon
- **🦙 Custom Icon**: Adorable llama emoji branding
- **📱 Native macOS App**: Properly packaged as a `.app` bundle
- **🔧 Easy Setup**: Simple installation and configuration

## 📋 Requirements

- **macOS** 10.13.0 or later
- **Python 3.11+**
- **Ollama** (for AI models)

## 🚀 Quick Start

### 1. Install Ollama
```bash
# Install Ollama
brew install ollama

# Start Ollama
ollama serve

# Download a model (optional)
ollama pull llama3:8b
```

### 2. Build Llamita
```bash
# Clone the repository
git clone https://github.com/yourusername/llamita.git
cd llamita

# Install dependencies
pip install -r requirements.txt

# Build the app
python3 setup.py py2app
```

### 3. Run Llamita
```bash
# Option 1: Double-click the app
open dist/Llamita.app

# Option 2: Use the launcher script
./Launch\ Llamita.command

# Option 3: Install to Applications
./install_llamita.sh
```

## 📁 Project Structure

```
llamita/
├── voice_assistant.py      # Main application logic
├── config.py              # Configuration settings
├── setup.py               # App packaging configuration
├── requirements.txt        # Python dependencies
├── Launch Llamita.command # Launcher script
├── install_llamita.sh     # Installation script
├── build_app.sh           # Build automation
├── create_icon.py         # Icon generation
├── llamita_icon.ico       # Custom icon
├── dist/
│   └── Llamita.app        # Built macOS app
└── README.md              # This file
```

## 🛠️ Development

### Prerequisites
```bash
# Install development dependencies
pip install py2app requests pillow
```

### Building the App
```bash
# Clean build
rm -rf build dist
python3 setup.py py2app

# The app will be created in dist/Llamita.app
```

### Running from Source
```bash
# Run directly with Python
python3 voice_assistant.py
```

## 🎨 Customization

### Changing the Icon
1. Replace `llamita_icon.ico` with your own icon
2. Run `python3 create_icon.py` to generate macOS format
3. Rebuild the app: `python3 setup.py py2app`

### Modifying the UI
Edit `voice_assistant.py` to customize:
- Window size and colors
- Button styles and layout
- Chat display formatting

### Configuration
Edit `config.py` to change:
- Ollama URL and model settings
- UI colors and styling
- System prompts

## 🔧 Troubleshooting

### App Won't Start
1. **Check Ollama**: Make sure `ollama serve` is running
2. **Check Models**: Ensure you have a model installed (`ollama list`)
3. **Permissions**: Make sure the app has proper permissions

### Build Issues
1. **Clean Build**: `rm -rf build dist && python3 setup.py py2app`
2. **Dependencies**: `pip install -r requirements.txt`
3. **Python Version**: Ensure you're using Python 3.11+

### Icon Issues
1. **Regenerate Icon**: `python3 create_icon.py`
2. **Check Format**: Ensure icon is in `.ico` format
3. **Rebuild**: `python3 setup.py py2app`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a Pull Request

## 📝 License

This project uses **dual licensing**:

- **Personal/Educational Use**: Free (MIT License) - see [LICENSE](LICENSE)
- **Commercial Use**: Paid license required - see [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md)

**For commercial use**, including integration into commercial products, enterprise deployments, or commercial distribution, a paid license is required. Please contact for pricing and terms.

## 🙏 Acknowledgments

- **Ollama** for providing the local AI infrastructure
- **Tkinter** for the GUI framework
- **py2app** for macOS app packaging
- **Pillow** for image processing

## 📞 Support

If you encounter any issues:
1. Check the [Issues](https://github.com/yourusername/llamita/issues) page
2. Create a new issue with detailed information
3. Include your macOS version and Python version

---

**Made with ❤️ and 🦙 by the Llamita team**
