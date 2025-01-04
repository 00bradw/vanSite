import os
import json
import random
import string
import argparse
from PIL import Image
import shutil
from moviepy.editor import VideoFileClip
from moviepy.video.fx import resize

def clear_output_except_originals(output_folder, originals_folder_name='original', specific_folder=None):
    """Clear all subdirectories and files in the output folder except the originals folder or specific folder."""
    for item in os.listdir(output_folder):
        item_path = os.path.join(output_folder, item)
        if item != originals_folder_name and (specific_folder is None or item == specific_folder):
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)

def convert_to_webp_and_resize_mp4(source_folder, output_folder, originals_folder_name='original', max_height=800, specific_folder=None):
    name_dict = {}

    # Ensure the originals folder is preserved
    originals_folder_path = os.path.join(output_folder, originals_folder_name)
    if not os.path.exists(originals_folder_path):
        os.makedirs(originals_folder_path)

    # Clear the specific output folder or entire folder
    if specific_folder:
        clear_output_except_originals(output_folder, originals_folder_name, specific_folder)
    else:
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
        relative_path = os.path.relpath(subdir, source_folder)

        if specific_folder and specific_folder not in relative_path:
            continue

        for filename in files:
            file_path = os.path.join(subdir, filename)

            # Process image files (e.g., .jpg, .jpeg, .png, .heic)
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.heic')):
                img = Image.open(file_path)

                # Convert HEIC to RGB if necessary
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                # Resize the image if necessary
                if img.height > max_height:
                    aspect_ratio = img.width / img.height
                    new_height = max_height
                    new_width = int(new_height * aspect_ratio)
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)

                # Determine subdirectory structure and process accordingly
                output_dir = os.path.join(output_folder, relative_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                output_path = os.path.join(output_dir, filename.rsplit('.', 1)[0] + '.webp')

                # Save the image as WebP
                img.save(output_path, 'WEBP')
                print(f"Converted {file_path} to {output_path}")

            # Process video files (.mp4)
            elif filename.lower().endswith('.mp4'):
                clip = VideoFileClip(file_path)
                output_dir = os.path.join(output_folder, relative_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # Resize the video to reduce file size
                resized_clip = resize.resize(clip, height=max_height)

                output_path = os.path.join(output_dir, filename)

                # Save the resized MP4
                resized_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
                print(f"Resized {file_path} to {output_path}")

    # Save the new name dictionary for the adventures folder
    if name_dict:
        adventures_output_dir = "../_data"
        if not os.path.exists(adventures_output_dir):
            os.makedirs(adventures_output_dir)

        new_name_dict_path = os.path.join(adventures_output_dir, 'name_dict.json')
        with open(new_name_dict_path, 'w') as file:
            json.dump(name_dict, file, indent=4)

        print(f"Saved name dictionary at {new_name_dict_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert images to webp and resize videos.")
    parser.add_argument('--folder', type=str, help="Specify a subdirectory within the source folder to process.")
    parser.add_argument('--source', type=str, default='../assets/img/original', help="Source folder path.")
    parser.add_argument('--output', type=str, default='../assets/img', help="Output folder path.")
    args = parser.parse_args()

    convert_to_webp_and_resize_mp4(args.source, args.output, originals_folder_name='original', specific_folder=args.folder)
