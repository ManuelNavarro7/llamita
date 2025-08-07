# 🦙 Llamita Installation Guide

This guide will help you install and run Llamita on macOS. Follow these steps carefully to avoid common issues.

## 📋 Prerequisites

Before installing Llamita, make sure you have:

- **macOS** (tested on macOS 10.15+)
- **Python 3.7+** (usually pre-installed on macOS)
- **Homebrew** (for installing dependencies)
- **Git** (for cloning the repository)

## 🚀 Step-by-Step Installation

### Step 1: Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Ollama
```bash
# Install Ollama using Homebrew
brew install ollama

# Or download from: https://ollama.ai
```

### Step 3: Clone the Repository
```bash
# Clone the repository
git clone https://github.com/ManuelNavarro7/llamita.git
cd llamita
```

### Step 4: Install Python Dependencies
```bash
# Install required Python packages
pip3 install -r requirements.txt
```

### Step 5: Make Scripts Executable
```bash
# Make all scripts executable
chmod +x scripts/*.sh
```

### Step 6: Start Ollama and Download a Model
```bash
# Start Ollama (run this in a separate terminal and keep it running)
ollama serve

# Download a model (run this in another terminal)
ollama pull llama3:8b
```

### Step 7: Run Llamita
```bash
# Run Llamita using the simple method (recommended)
./scripts/run_simple.sh
```

## 🔧 Alternative Run Methods

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

### Issue 1: "ModuleNotFoundError: No module named 'config'"
**Solution:**
```bash
# Run with PYTHONPATH set to include the src directory
PYTHONPATH=src python3 src/voice_assistant.py
```

### Issue 2: "Ollama is not running"
**Solution:**
```bash
# Start Ollama in a separate terminal
ollama serve
```

### Issue 3: "Permission denied" when running scripts
**Solution:**
```bash
# Make scripts executable
chmod +x scripts/*.sh
```

### Issue 4: "No module named 'SpeechRecognition'"
**Solution:**
```bash
# Install missing dependencies
pip3 install -r requirements.txt
```

### Issue 5: "PortAudio not found"
**Solution:**
```bash
# Install PortAudio using Homebrew
brew install portaudio
```

### Issue 6: "Python not found"
**Solution:**
```bash
# Install Python using Homebrew
brew install python
```

### Issue 7: "Model not found"
**Solution:**
```bash
# Download the model
ollama pull llama3:8b

# Or use a different model
ollama pull llama3.2:3b
```

## 🎯 Quick Test

To test if everything is working:

1. **Check Ollama:**
   ```bash
   curl -s http://localhost:11434/api/tags
   ```

2. **Check Python:**
   ```bash
   python3 --version
   ```

3. **Check Dependencies:**
   ```bash
   python3 -c "import tkinter; import requests; print('✅ Dependencies OK')"
   ```

4. **Run Llamita:**
   ```bash
   ./scripts/run_simple.sh
   ```

## 📁 File Structure

After installation, your directory should look like this:
```
llamita/
├── src/
│   ├── voice_assistant.py  # Main application
│   └── config.py          # Configuration
├── scripts/
│   ├── run_simple.sh      # Simple run script
│   └── run_voice_assistant.sh  # Virtual environment script
├── docs/
├── requirements.txt
└── README.md
```

## 🔄 Updating Llamita

To update to the latest version:

```bash
# Pull the latest changes
git pull origin main

# Reinstall dependencies (if needed)
pip3 install -r requirements.txt

# Run the updated version
./scripts/run_simple.sh
```

## 🎉 Success!

If you see the Llamita GUI window, congratulations! You've successfully installed Llamita.

**Next steps:**
- Try typing a message and pressing Enter
- Explore the configuration options in `src/config.py`
- Check out the documentation in the `docs/` folder

## 📞 Need Help?

If you're still having issues:

1. **Check the logs** - Look for error messages in the terminal
2. **Verify Ollama** - Make sure `ollama serve` is running
3. **Check dependencies** - Ensure all Python packages are installed
4. **Try the troubleshooting steps** above
5. **Open an issue** on GitHub with your error message

---

**Happy chatting with Llamita! 🦙✨**
