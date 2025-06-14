import sys
from PIL import Image
import os


def convert_image_to_png(image_path):
    try:
        # Get the directory and base filename of the input file
        dir_name = os.path.dirname(image_path)
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(dir_name, f"{base_name}.png")

        # Check if the output file already exists
        if os.path.exists(output_path):
            overwrite = input(f"{output_path} already exists. Do you want to overwrite it? (y/n): ").lower()
            if overwrite != 'y':
                print(f"Skipped {output_path}")
                return

        # Open the image file
        with Image.open(image_path) as img:
            # Convert to PNG and save
            img.save(output_path, 'PNG')
            print(f"Converted {image_path} to {output_path}")
    except Exception as e:
        print(f"Error converting {image_path}: {e}")


def main():
    if len(sys.argv) < 2:
        print("Please provide the image file paths as arguments.")
        print("Example: python convert_to_png.py image1.jpg image2.png")
        sys.exit(1)

    # Loop through each image file passed as an argument
    for image_path in sys.argv[1:]:
        if os.path.isfile(image_path):
            convert_image_to_png(image_path)
        else:
            print(f"{image_path} is not a valid file.")


if __name__ == "__main__":
    main()
