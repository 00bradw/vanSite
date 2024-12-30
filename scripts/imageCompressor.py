import os
import json
import random
import string
from PIL import Image
import shutil

def generate_random_name(length=8):
    """Generate a random alphanumeric string of fixed length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def clear_output_except_originals(output_folder, originals_folder_name='original'):
    """Clear all subdirectories and files in the output folder except the originals folder."""
    for item in os.listdir(output_folder):
        item_path = os.path.join(output_folder, item)
        if item != originals_folder_name:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)

def convert_to_webp(source_folder, output_folder, originals_folder_name='original', max_height=500):
    name_dict = {}

    # Ensure the originals folder is preserved
    originals_folder_path = os.path.join(output_folder, originals_folder_name)
    if not os.path.exists(originals_folder_path):
        os.makedirs(originals_folder_path)

    # Clear the output folder except for the originals folder
    clear_output_except_originals(output_folder, originals_folder_name)

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

                # Determine subdirectory structure and process accordingly
                relative_path = os.path.relpath(subdir, source_folder)
                output_dir = os.path.join(output_folder, relative_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                if 'adventures' in subdir:
                    # Generate a random name for the output file
                    random_name = generate_random_name() + '.webp'
                    name_dict[random_name] = original_name_dict.get(filename, filename)
                    output_path = os.path.join(output_dir, random_name)
                elif 'liveries' in subdir:
                    # Assign a random name without a dictionary
                    random_name = generate_random_name() + '.webp'
                    output_path = os.path.join(output_dir, random_name)
                else:
                    # Default handling for other folders
                    output_path = os.path.join(output_dir, filename.replace('.jpeg', '.webp').replace('.jpg', '.webp'))

                # Save the image as WebP
                img.save(output_path, 'WEBP')
                print(f"Converted {file_path} to {output_path}")

    # Save the new name dictionary for the adventures folder
    if name_dict:
        adventures_output_dir = "../_data"
        if not os.path.exists(adventures_output_dir):
            os.makedirs(adventures_output_dir)

        new_name_dict_path = os.path.join(adventures_output_dir, 'name_dict.json')
        with open(new_name_dict_path, 'w') as file:
            json.dump(name_dict, file, indent=4)

        print(f"Saved name dictionary at {new_name_dict_path}")

# Example usage
source_folder = '../assets/img/original'  # Update this path to your source folder
output_folder = '../assets/img'  # Update this path to your output folder
convert_to_webp(source_folder, output_folder, originals_folder_name='original')
