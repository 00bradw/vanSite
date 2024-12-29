import os
from PIL import Image

def convert_to_webp(source_folder, output_folder, max_height=800):
    # Walk through the source directory
    for subdir, dirs, files in os.walk(source_folder):
        for filename in files:
            if filename.lower().endswith((".jpg", ".jpeg")):
                # Construct the full file path
                file_path = os.path.join(subdir, filename)
                # Open the image
                img = Image.open(file_path)

                # Resize the image if necessary
                if img.height > max_height:
                    aspect_ratio = img.width / img.height
                    new_height = max_height
                    new_width = int(new_height * aspect_ratio)
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)

                # Create corresponding subdirectory structure in output_folder
                relative_path = os.path.relpath(subdir, source_folder)
                output_dir = os.path.join(output_folder, relative_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # Save the image as WebP in the corresponding output folder
                output_path = os.path.join(output_dir, filename.replace('.jpeg', '.webp').replace('.jpg', '.webp'))
                img.save(output_path, 'WEBP')

                print(f"Converted {file_path} to {output_path}")

# Example usage
source_folder = '../assets/img/original'  # Update this path to your source folder
output_folder = '../assets/img'  # Update this path to your output folder
convert_to_webp(source_folder, output_folder)
