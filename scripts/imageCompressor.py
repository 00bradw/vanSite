import os
import json
import random
import string
from PIL import Image

def generate_random_name(length=8):
    """Generate a random alphanumeric string of fixed length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def convert_to_webp(source_folder, output_folder, max_height=800):
    name_dict = {}

    # Define path to name_dict.json
    name_dict_path = os.path.join(source_folder, 'adventures', 'name_dict.json')

    # Check if name_dict.json exists and load it
    if os.path.exists(name_dict_path):
        with open(name_dict_path, 'r') as file:
            original_name_dict = json.load(file)
    else:
        original_name_dict = {}

    # Walk through the source directory
    for subdir, dirs, files in os.walk(source_folder):
        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg')):
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

                # Check if the image is in the "adventures" folder
                if 'adventures' in subdir:
                    # Generate a random name for the output file
                    random_name = generate_random_name() + '.webp'
                    name_dict[random_name] = original_name_dict.get(filename, filename)

                    # Set output directory to adventures' corresponding folder
                    relative_path = os.path.relpath(subdir, source_folder)
                    output_dir = os.path.join(output_folder, relative_path)
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)

                    # Save the image with the random name
                    output_path = os.path.join(output_dir, random_name)
                else:
                    # Create corresponding subdirectory structure in output_folder
                    relative_path = os.path.relpath(subdir, source_folder)
                    output_dir = os.path.join(output_folder, relative_path)
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)

                    # Save the image with the original name as WebP
                    output_path = os.path.join(output_dir, filename.replace('.jpeg', '.webp').replace('.jpg', '.webp'))

                img.save(output_path, 'WEBP')

                print(f"Converted {file_path} to {output_path}")

    # Save the new name dictionary for adventures folder
    if name_dict:
        adventures_output_dir = os.path.join(output_folder, 'adventures')
        if not os.path.exists(adventures_output_dir):
            os.makedirs(adventures_output_dir)

        new_name_dict_path = os.path.join(adventures_output_dir, 'name_dict.json')
        with open(new_name_dict_path, 'w') as file:
            json.dump(name_dict, file, indent=4)

        print(f"Saved name dictionary at {new_name_dict_path}")

# Example usage
source_folder = '../assets/img/original'  # Update this path to your source folder
output_folder = '../assets/img'  # Update this path to your output folder
convert_to_webp(source_folder, output_folder)