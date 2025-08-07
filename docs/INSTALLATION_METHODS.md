# 📦 Installation Methods Explained

This document explains the different ways to install Llamita and why certain components can't be installed via `requirements.txt`.

## 🤔 Why Can't Ollama Be in requirements.txt?

**`requirements.txt`** is specifically for Python packages that can be installed via pip. It cannot install:

- **System applications** (like Ollama)
- **Operating system packages** (like Homebrew)
- **Binary executables** (like the Ollama binary)

## 📋 What requirements.txt Contains

```txt
# Voice Assistant Dependencies
SpeechRecognition>=3.14.0
PyAudio>=0.2.14
py2app>=0.28.8
requests>=2.32.0
```

These are **Python packages only** that can be installed with `pip install`.

## 🚀 Installation Methods

### Method 1: One-Command Installation (Recommended)
```bash
curl -fsSL https://raw.githubusercontent.com/ManuelNavarro7/llamita/main/scripts/install_everything.sh | bash
```

**What this does:**
- ✅ Installs Homebrew (if needed)
- ✅ Installs Python (if needed)
- ✅ Installs Ollama (if needed)
- ✅ Installs Python dependencies from requirements.txt
- ✅ Downloads AI models
- ✅ Starts Ollama automatically
- ✅ Tests everything works

### Method 2: Manual Installation
```bash
# 1. Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Ollama
brew install ollama

# 3. Install Python dependencies
pip3 install -r requirements.txt

# 4. Start Ollama
ollama serve

# 5. Download model
ollama pull llama3:8b

# 6. Run Llamita
./scripts/run_simple.sh
```

### Method 3: Python Dependencies Only
```bash
pip3 install -r requirements.txt
```

**What this does:**
- ✅ Installs only Python packages
- ❌ Does NOT install Ollama
- ❌ Does NOT install system dependencies
- ❌ Does NOT start Ollama

## 🔧 What Each Component Does

### Python Dependencies (requirements.txt)
- **`requests`** - HTTP requests to Ollama API
- **`tkinter`** - GUI framework (usually pre-installed)
- **`SpeechRecognition`** - Voice recognition (optional)
- **`PyAudio`** - Audio processing (optional)
- **`py2app`** - Build macOS app (optional)

### System Dependencies (not in requirements.txt)
- **`Ollama`** - AI model server
- **`Homebrew`** - Package manager for macOS
- **`Python 3`** - Programming language runtime

## 🎯 Recommended Approach

For **new users**: Use the one-command installation
```bash
curl -fsSL https://raw.githubusercontent.com/ManuelNavarro7/llamita/main/scripts/install_everything.sh | bash
```

For **developers**: Use manual installation for more control
```bash
# Install system dependencies manually
brew install ollama python

# Install Python dependencies
pip3 install -r requirements.txt

# Start and configure Ollama manually
ollama serve
ollama pull llama3:8b
```

## 🛠️ Troubleshooting

### If requirements.txt installation fails:
```bash
# Try upgrading pip
pip3 install --upgrade pip

# Install dependencies one by one
pip3 install requests
pip3 install tkinter  # Usually pre-installed
```

### If Ollama installation fails:
```bash
# Try Homebrew installation
brew install ollama

# Or try direct download
curl -fsSL https://ollama.ai/install.sh | sh
```

### If Python installation fails:
```bash
# Install Python via Homebrew
brew install python

# Or download from python.org
```

## 💡 Best Practices

1. **Use the one-command installer** for the easiest experience
2. **Check system requirements** before manual installation
3. **Keep Ollama running** while using Llamita
4. **Update regularly** with `git pull` and `pip3 install -r requirements.txt`
5. **Use virtual environments** for development

## 🔄 Updating

### Update Python dependencies:
```bash
pip3 install -r requirements.txt --upgrade
```

### Update Ollama:
```bash
brew upgrade ollama
# or
curl -fsSL https://ollama.ai/install.sh | sh
```

### Update Llamita:
```bash
git pull origin main
```

---

**The one-command installer is the recommended method for most users! 🦙✨**
