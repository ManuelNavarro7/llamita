# 🚀 Quick Install Guide

This guide shows you how to install Llamita with just one command!

## 🎯 One-Command Installation

### From Any Directory:
```bash
curl -fsSL https://raw.githubusercontent.com/ManuelNavarro7/llamita/main/scripts/install_everything.sh | bash
```

**What this does:**
- ✅ Installs Homebrew (if needed)
- ✅ Installs Python (if needed)
- ✅ Installs Ollama (if needed)
- ✅ Clones the Llamita repository
- ✅ Installs Python dependencies
- ✅ Downloads AI models
- ✅ Starts Ollama automatically
- ✅ Tests everything works

## 📁 After Installation

The installer will clone the repository to your current directory. You can then:

```bash
# Navigate to the Llamita directory
cd llamita

# Run Llamita
./scripts/run_simple.sh
```

## 🔧 Alternative Methods

### If you want to clone manually first:
```bash
# Clone the repository
git clone https://github.com/ManuelNavarro7/llamita.git
cd llamita

# Run the installer from within the repo
curl -fsSL https://raw.githubusercontent.com/ManuelNavarro7/llamita/main/scripts/install_everything.sh | bash
```

### If you're already in the repository:
```bash
# Run the installer directly
./scripts/install_everything.sh
```

## 🛠️ Troubleshooting

### If you get "tkinter" errors:
This is normal! `tkinter` is a built-in Python module and doesn't need to be installed via pip.

### If you get "requirements.txt not found":
The installer will automatically clone the repository and install dependencies.

### If Ollama fails to start:
```bash
# Start Ollama manually
ollama serve

# Then run Llamita
./scripts/run_simple.sh
```

## 🎉 Success!

After running the installer, you should see:
```
🎉 Installation completed successfully!

🚀 To run Llamita:
   ./scripts/run_simple.sh
```

Then just run:
```bash
./scripts/run_simple.sh
```

## 💡 Tips

- The installer works from any directory
- It will automatically clone the repository if needed
- Ollama will be running in the background
- You can stop Ollama with `pkill ollama`
- You can restart Ollama with `ollama serve`

---

**That's it! One command to install everything! 🦙✨**
