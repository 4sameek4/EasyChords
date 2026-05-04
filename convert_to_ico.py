from PIL import Image

# Open the circular PNG
img = Image.open('Icon.png')

# Save as ICO
img.save('Icon.ico')
print("Icon.ico created successfully")
