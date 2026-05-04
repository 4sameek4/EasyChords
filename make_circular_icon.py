from PIL import Image, ImageDraw

# Open the original icon
icon_path = "Icon.jpg"
img = Image.open(icon_path)

# Convert to RGBA
img = img.convert('RGBA')

# Resize to square with high quality (256x256 as base)
size = 256
img_cropped = img.resize((size, size), Image.Resampling.LANCZOS)

# Create a new image with transparent background
circular_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))

# Create circular mask with high quality
mask = Image.new('L', (size, size), 0)
draw = ImageDraw.Draw(mask)
# Draw circle slightly smaller to avoid edge artifacts
draw.ellipse([0, 0, size-1, size-1], fill=255)

# Paste the image using the circular mask
circular_img.paste(img_cropped, (0, 0), mask)

# Save as PNG with transparency
circular_img.save('Icon.png')
print("High-quality circular PNG created: Icon.png")

# Create multi-resolution ICO for better display at different sizes
sizes_list = [16, 32, 48, 64, 128, 256]
ico_images = []
for sz in sizes_list:
    resized = circular_img.resize((sz, sz), Image.Resampling.LANCZOS)
    ico_images.append(resized)

# Save as multi-resolution ICO
ico_images[0].save('Icon.ico', sizes=[(s, s) for s in sizes_list])
print(f"Multi-resolution Icon.ico created with sizes: {sizes_list}")
