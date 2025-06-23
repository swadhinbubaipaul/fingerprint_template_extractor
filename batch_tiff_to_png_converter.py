import os
from PIL import Image

# Source and destination folders
source_folder = "./images"
destination_folder = "./converted_images"

# Create destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Loop through all TIFF files in the source folder
for filename in os.listdir(source_folder):
    if filename.lower().endswith(".tif") or filename.lower().endswith(".tiff"):
        tif_path = os.path.join(source_folder, filename)

        # Open and convert the image
        with Image.open(tif_path) as img:
            img_gray = img.convert("L")  # Convert to grayscale

            # Save as PNG in the destination folder
            new_filename = os.path.splitext(filename)[0] + ".png"
            png_path = os.path.join(destination_folder, new_filename)
            img_gray.save(png_path)

        print(f"Converted: {filename} -> converted_image/{new_filename}")
