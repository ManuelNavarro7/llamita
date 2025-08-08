#!/bin/bash

# Create ICNS file for macOS app
# This script converts the PNG icon to ICNS format

set -e

echo "🦙 Creating ICNS icon for macOS app..."
echo "======================================="

# Check if PNG icon exists
if [ ! -f "assets/icons/llamita_icon.png" ]; then
    echo "❌ Error: assets/icons/llamita_icon.png not found"
    exit 1
fi

# Create iconset directory
echo "📁 Creating iconset directory..."
mkdir -p llamita.iconset

# Convert PNG to different sizes
echo "🔄 Converting icon to different sizes..."

# 16x16
sips -z 16 16 assets/icons/llamita_icon.png --out llamita.iconset/icon_16x16.png

# 32x32
sips -z 32 32 assets/icons/llamita_icon.png --out llamita.iconset/icon_16x16@2x.png

# 32x32
sips -z 32 32 assets/icons/llamita_icon.png --out llamita.iconset/icon_32x32.png

# 64x64
sips -z 64 64 assets/icons/llamita_icon.png --out llamita.iconset/icon_32x32@2x.png

# 128x128
sips -z 128 128 assets/icons/llamita_icon.png --out llamita.iconset/icon_128x128.png

# 256x256
sips -z 256 256 assets/icons/llamita_icon.png --out llamita.iconset/icon_128x128@2x.png

# 256x256
sips -z 256 256 assets/icons/llamita_icon.png --out llamita.iconset/icon_256x256.png

# 512x512
sips -z 512 512 assets/icons/llamita_icon.png --out llamita.iconset/icon_256x256@2x.png

# 512x512
sips -z 512 512 assets/icons/llamita_icon.png --out llamita.iconset/icon_512x512.png

# 1024x1024
sips -z 1024 1024 assets/icons/llamita_icon.png --out llamita.iconset/icon_512x512@2x.png

# Create ICNS file
echo "🎨 Creating ICNS file..."
iconutil -c icns llamita.iconset

# Move to assets directory
mv llamita.icns assets/icons/llamita_icon.icns

echo "✅ ICNS file created: assets/icons/llamita_icon.icns"
echo "🎉 Icon conversion complete!"
