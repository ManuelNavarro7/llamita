# 🦙 Llamita Icons

This directory contains the icons for the Llamita Voice Assistant app.

## 📁 Icon Files

- **`llamita_icon.png`** - High-resolution PNG icon (512x512)
- **`llamita_icon.ico`** - Windows-compatible ICO format
- **`create_icon.py`** - Script to generate the icons

## 🎨 Icon Design

The Llamita icon features:
- **🦙 Llama/Alpaca mascot** - Represents the friendly, helpful nature of the assistant
- **💬 Speech bubble** - Indicates voice/speech capabilities
- **🌈 Gradient background** - Modern, appealing design
- **🎯 Clean, recognizable** - Easy to identify in dock/applications

## 🔧 Usage

The icons are automatically used when building the macOS app:

```bash
./build.sh
```

This will create `dist/Llamaita.app` with the custom icon.

## 🛠️ Regenerating Icons

To recreate the icons:

```bash
python3 create_icon.py
```

This requires the Pillow library:
```bash
pip install Pillow
```

## 📱 Icon Sizes

- **512x512** - High resolution for retina displays
- **ICO format** - Compatible with Windows and macOS
- **PNG format** - Web and general use

The icon will appear in:
- Dock when running
- Applications folder
- Finder
- Spotlight search
