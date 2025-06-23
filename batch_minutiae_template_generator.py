import os
import subprocess
import shutil

# Paths
input_folder = "./converted_images"
output_folder = "./templates"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop over all .png files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".png"):
        base_name = os.path.splitext(filename)[0]
        input_path = os.path.join(input_folder, filename)

        # Run mindtct
        command = [
            ".\\mindtct",
            input_path,
            os.path.join(input_folder, base_name),
        ]
        subprocess.run(command, check=True)

        # Move the .xyt file to templates folder
        xyt_file = os.path.join(input_folder, base_name + ".xyt")
        if os.path.exists(xyt_file):
            shutil.move(xyt_file, os.path.join(output_folder, base_name + ".xyt"))

        # Clean up other mindtct-generated files
        for ext in [
            ".brw",
            ".dm",
            ".lft",
            ".min",
            ".brf",
            ".wsq",
            ".ncm",
            ".map",
            ".qm",
        ]:
            generated_file = os.path.join(input_folder, base_name + ext)
            if os.path.exists(generated_file):
                os.remove(generated_file)

        print(f"Processed: {filename} -> templates/{base_name}.xyt")
