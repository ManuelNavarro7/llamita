# 🦙 Llamita Setup Instructions

## Quick Start (for sharing with others)

### 1. Install Ollama
```bash
# macOS
brew install ollama

# Or download from: https://ollama.ai
```

### 2. Download a Model
```bash
# Start Ollama
ollama serve

# Download a model (in another terminal)
ollama pull llama3:8b
```

### 3. Run Llamita
```bash
# Make scripts executable
chmod +x run_voice_assistant.sh
chmod +x "Launch Llamita.command"

# Run Llamita
./run_voice_assistant.sh
```

## 🎯 What Works Offline:
- ✅ Text input/output
- ✅ AI responses
- ✅ Chat history
- ✅ All GUI features

## 🌐 What Needs Internet:
- ⚠️ Voice input (optional feature)

## 📁 Files Included:
- `voice_assistant.py` - Main application
- `config.py` - Configuration
- `run_voice_assistant.sh` - Run script
- `Launch Llamita.command` - macOS launcher
- `requirements.txt` - Python dependencies

## 🚀 Features:
- **100% Local AI** - No cloud dependencies
- **Text-based chat** - Works offline
- **Optional voice input** - Requires internet
- **Modern UI** - Clean, professional interface
- **Customizable** - Easy to modify and extend

## 💡 Tips:
- Change models in `config.py`
- Add custom prompts in `config.py`
- Modify colors and styling in `config.py`
