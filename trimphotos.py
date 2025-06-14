import os
from PIL import Image
def trim_image(image_path, target_size, output_path):
    img = Image.open(image_path)
    original_width, original_height = img.size
    print(f"Original dimensions: {original_width}x{original_height}")
    scale = target_size / min(original_width, original_height)
    if scale >= 1:
        scale = 1
    print(f"Scale factor: {scale}")
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    print(f"Resized dimensions: {new_width}x{new_height}")
    left = (new_width - target_size) / 2
    top = (new_height - target_size) / 2
    right = (new_width + target_size) / 2
    bottom = (new_height + target_size) / 2
    left = max(left, 0)
    top = max(top, 0)
    right = min(right, new_width)
    bottom = min(bottom, new_height)
    print(f"Cropping box: left={left}, top={top}, right={right}, bottom={bottom}")
    img_cropped = img_resized.crop((left, top, right, bottom))
    img_cropped.save(output_path)
    print(f"Image saved as {output_path}")
def process_directory(directory, target_size):
    supported_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if any(filename.lower().endswith(ext) for ext in supported_extensions):
            output_path = os.path.join(directory, f"r{filename}")
            trim_image(file_path, target_size, output_path)
directory = input("Enter the directory path: ")
target_size = int(input("Enter the target size (for square): "))
process_directory(directory, target_size)
