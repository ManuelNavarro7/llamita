#!/usr/bin/env python3
"""
Create a simple custom icon for Llamita
This generates a simple icon to replace the Python rocket
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_llamita_icon():
    """Create a simple llama icon"""
    # Create a 64x64 image with a dark background
    size = 64
    img = Image.new('RGBA', (size, size), (44, 62, 80, 255))  # Dark blue background
    draw = ImageDraw.Draw(img)
    
    # Draw a simple llama emoji-style icon
    # Body (light gray)
    draw.ellipse([10, 20, 54, 50], fill=(200, 200, 200, 255))
    
    # Head (light gray)
    draw.ellipse([20, 10, 44, 30], fill=(200, 200, 200, 255))
    
    # Ears (brown)
    draw.ellipse([15, 5, 25, 15], fill=(139, 69, 19, 255))
    draw.ellipse([39, 5, 49, 15], fill=(139, 69, 19, 255))
    
    # Eyes (black)
    draw.ellipse([25, 15, 30, 20], fill=(0, 0, 0, 255))
    draw.ellipse([34, 15, 39, 20], fill=(0, 0, 0, 255))
    
    # Nose (black)
    draw.ellipse([29, 22, 35, 28], fill=(0, 0, 0, 255))
    
    # Save the icon
    icon_path = "llamita_icon.png"
    img.save(icon_path)
    print(f"✅ Created custom icon: {icon_path}")
    return icon_path

if __name__ == "__main__":
    try:
        create_llamita_icon()
    except ImportError:
        print("⚠️ PIL not available, skipping icon creation")
        print("Install with: pip3 install Pillow")
    except Exception as e:
        print(f"❌ Error creating icon: {e}")
