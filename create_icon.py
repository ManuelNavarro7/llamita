#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# Create a 512x512 image with a blue background
img = Image.new('RGBA', (512, 512), (52, 152, 219, 255))
draw = ImageDraw.Draw(img)

# Try to use a system font, fallback to default
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 120)
except:
    font = ImageFont.load_default()

# Draw the llama emoji and text
text = "🦙"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

x = (512 - text_width) // 2
y = (512 - text_height) // 2
draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

# Save as PNG first
img.save("llamita_icon.png")

print("✅ Icon created: llamita_icon.png")

# Create iconset directory
os.makedirs("llamita.iconset", exist_ok=True)

# Generate different sizes
sizes = [16, 32, 64, 128, 256, 512]
for size in sizes:
    resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
    resized_img.save(f'llamita.iconset/icon_{size}x{size}.png')

print("✅ Icon sizes created in llamita.iconset/")
