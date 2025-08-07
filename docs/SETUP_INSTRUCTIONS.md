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
chmod +x scripts/run_simple.sh
chmod +x scripts/run_voice_assistant.sh

# Run Llamita (choose one method):
# Method 1: Simple run (recommended)
./scripts/run_simple.sh

# Method 2: Virtual environment run
./scripts/run_voice_assistant.sh

# Method 3: Direct run
PYTHONPATH=src python3 src/voice_assistant.py
```

## 🔧 Troubleshooting

### If you get "ModuleNotFoundError: No module named 'config'"
```bash
# Run with PYTHONPATH set
PYTHONPATH=src python3 src/voice_assistant.py
```

### If you get "Ollama is not running"
```bash
# Start Ollama in a separate terminal
ollama serve
```

### If you get permission errors
```bash
# Make scripts executable
chmod +x scripts/*.sh
```

### If Python dependencies are missing
```bash
# Install dependencies
pip3 install -r requirements.txt
```

## 🎯 What Works Offline:
- ✅ Text input/output
- ✅ AI responses
- ✅ Chat history
- ✅ All GUI features

## 🌐 What Needs Internet:
- ⚠️ Voice input (optional feature)

## 📁 Files Included:
- `src/voice_assistant.py` - Main application
- `src/config.py` - Configuration
- `scripts/run_simple.sh` - Simple run script
- `scripts/run_voice_assistant.sh` - Virtual environment run script
- `requirements.txt` - Python dependencies

## 🚀 Features:
- **100% Local AI** - No cloud dependencies
- **Text-based chat** - Works offline
- **Optional voice input** - Requires internet
- **Modern UI** - Clean, professional interface
- **Customizable** - Easy to modify and extend

## 💡 Tips:
- Change models in `src/config.py`
- Add custom prompts in `src/config.py`
- Modify colors and styling in `src/config.py`
- Use `./scripts/run_simple.sh` for quick testing
