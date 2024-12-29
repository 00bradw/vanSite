import os

# Directory containing the images
image_dir = "../assets/img/build"
output_file = "output.md"  # Output Markdown file

# Function to generate a figure block for each image
def generate_figure_block(image_path, caption=None):
    return f"""
<figure style="text-align: center;">
  <img src="{image_path}">
  <figcaption>{caption if caption else "Caption for the image."}</figcaption>
</figure>
"""

# Generate Markdown for each image in the directory
def generate_markdown(image_dir, output_file):
    markdown = []
    for filename in sorted(os.listdir(image_dir)):  # Sort alphabetically
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
            image_path = os.path.join(image_dir, filename).replace("\\", "/")
            caption = f"Description for {filename}"  # You can customize this
            markdown.append(generate_figure_block(image_path, caption))
    
    # Write the markdown content to the output file
    with open(output_file, "w") as f:
        f.write("\n".join(markdown))
    
    print(f"Markdown generated and saved to {output_file}")

# Run the script
generate_markdown(image_dir, output_file)
