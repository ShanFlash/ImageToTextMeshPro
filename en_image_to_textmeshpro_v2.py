import os
import time
import sys
from PIL import Image
import numpy as np
from fractions import Fraction
from tqdm import tqdm


def image_to_textmeshpro(image_path, output_path, include_alpha, font_size):
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    data = np.array(img)

    hex_colors = []
    with tqdm(total=height, desc=f"[PROGRESS] Converting {os.path.basename(image_path)}", ncols=100) as pbar:
        for y in range(height):
            current_color = None
            count = 0
            for x in range(width):
                r, g, b, a = data[y, x]
                if a > 0:
                    if include_alpha:
                        hex_color = f"#{r:02X}{g:02X}{b:02X}{a:02X}"
                    else:
                        hex_color = f"#{r:02X}{g:02X}{b:02X}"
                    if hex_color == current_color:
                        count += 1
                    else:
                        if current_color is not None:
                            hex_colors.append(f"<color={current_color}>{'█' * count}</color>")
                        current_color = hex_color
                        count = 1
                else:
                    if current_color is not None:
                        hex_colors.append(f"<color={current_color}>{'█' * count}</color>")
                        current_color = None
                        count = 0
            if current_color is not None:
                hex_colors.append(f"<color={current_color}>{'█' * count}</color>")
            hex_colors.append("\\n")
            pbar.update(1)
    output_content = f"<size={font_size}>" + "".join(hex_colors).replace("\n", "\\n") + "</size>"

    with open(output_path, "w", encoding='utf-8') as f:
        f.write(output_content)

    output_size = os.path.getsize(output_path) / (1024 * 1024)
    output_size_str = f"{output_size:.2f} MB" if output_size >= 1 else f"{output_size * 1024:.2f} KB"

    print(f"\033[92m[SUCCESS] Conversion successful!\033[0m")
    print(f"\033[92m[SUCCESS] Output file size: {output_size_str}\033[0m")
    print(f"\033[92m[SUCCESS] Output file path: {os.path.abspath(output_path)}\033[0m")


def parse_font_size(input_size):
    input_size = input_size.strip()

    if input_size.endswith('%'):
        return input_size
    elif '/' in input_size:
        return input_size
    else:
        try:
            return float(input_size)
        except ValueError:
            raise ValueError("Invalid font size format")


def truncate_filename(filename, max_length=20):
    if len(filename) > max_length:
        return filename[:max_length - 3] + "..."
    return filename


def print_dynamic_line(length):
    print("=" * length)


def get_color_mode(image_path):
    with Image.open(image_path) as img:
        bands = img.getbands()
        return "RGBA" if 'A' in bands else "RGB"


def show_example_usage():
    print("=" * 100)

    print("\033[94m[INFO] Basic Operations:\033[0m")
    print("1. Choose input image (supports PNG, JPG, JPEG, etc.)")
    print("2. Choose whether to include alpha channel")
    print("3. Set font size, supports integers, floats, percentages, fractions")
    print("4. Convert to TMP rich text labels")

    print("\033[94m[INFO] Font size examples:\033[0m")
    print("Font size can be:")
    print(" - Integer (e.g., 10)")
    print(" - Float (e.g., 1.5)")
    print(" - Percentage (e.g., 50%)")
    print(" - Fraction (e.g., 2/3)")

    print("\033[94m[INFO] Example of TMP rich text labels after conversion:\033[0m")
    example_text = """
    - Without alpha channel
    <size=1><color=#FF0000>█████</color><color=#00FF00>████████</color><color=#0000FF>██████████</color></size>

    - With alpha channel
    <size=1><color=#FF0000FF>█████</color><color=#00FF0080>████████</color><color=#0000FF00>██████████</color></size>
    """
    print(example_text)

    print("=" * 100)


if __name__ == "__main__":
    print("\033[97m[WELCOME] Welcome to the Image to TMP Rich Text Tag tool!\033[0m")
    print("\033[97m[WELCOME] This tool can convert images to TMP rich text tags suitable for Unity engine!\033[0m")
    print("\033[97m[WELCOME] Author: www.bilibili.com@是闪闪闪闪闪\033[0m")

    show_example_usage()

    input_folder = "Input"
    output_folder = "Output"

    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
        print(f"\033[93m[INFO] No input folder found, '{input_folder}' has been created automatically.\033[0m")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"\033[93m[INFO] No output folder found, '{output_folder}' has been created automatically.\033[0m")

    try:
        images = [
            f for f in os.listdir(input_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
        ]

        if not images:
            print(
                f"\033[91m[ERROR] No image files found in the input folder. Please place images in the {input_folder} folder and rerun the program!\033[0m")
            print("The window will close in 5 seconds...")
            time.sleep(5)
            sys.exit()

        print(f"\033[94m[INFO] Found {len(images)} image files.\033[0m")

        while True:
            print("\033[94m[INFO] Please choose an image to convert to TMP rich text tags:\033[0m")
            print_dynamic_line(100)

            max_filename_length = max(len(truncate_filename(img)) for img in images)
            max_size_length = 10
            max_resolution_length = max(
                len(f"{Image.open(os.path.join(input_folder, img)).size[0]}x{Image.open(os.path.join(input_folder, img)).size[1]} Pix")
                for img in images)
            max_color_mode_length = max(len("RGB"), len("RGBA"))

            for i, img in enumerate(images):
                img_path = os.path.join(input_folder, img)
                img_size = os.path.getsize(img_path) / (1024 * 1024)
                img_size_str = f"{img_size:.2f} MB" if img_size >= 1 else f"{img_size * 1024:.2f} KB"
                img_width, img_height = Image.open(img_path).size
                color_mode_str = get_color_mode(img_path)
                resolution_str = f"{img_width}x{img_height} Pix"
                truncated_img_name = truncate_filename(img)

                print(
                    f"\033[96m({str(i + 1).zfill(2)})\033[91m | {truncated_img_name:<{max_filename_length}} \033[92m| Format: {img.split('.')[-1]:<6} \033[93m| Size: {img_size_str:<{max_size_length}} \033[94m| Resolution: {resolution_str:<{max_resolution_length}} \033[95m| Color Mode: {color_mode_str:<{max_color_mode_length}}\033[0m")

            print_dynamic_line(100)

            while True:
                user_input = input("\033[96m[INPUT] Enter the image number to select or '0' to exit: \033[0m")
                if user_input == '0':
                    print("\033[92m[SUCCESS] Process exited.\033[0m")
                    print("The window will close in 5 seconds...")
                    time.sleep(5)
                    sys.exit()

                try:
                    choice = int(user_input) - 1
                    if 0 <= choice < len(images):
                        selected_image = os.path.join(input_folder, images[choice])

                        try:
                            img_size_mb = os.path.getsize(selected_image) / (1024 * 1024)
                            img_size_str = f"{img_size_mb:.2f} MB" if img_size_mb >= 1 else f"{img_size_mb * 1024:.2f} KB"
                            img_width, img_height = Image.open(selected_image).size
                            color_mode_str = get_color_mode(selected_image)

                            print(
                                f"\033[94m[INFO] You selected image: \033[96m({str(choice + 1).zfill(2)}) \033[91m{images[choice]} \033[92m| Size: {img_size_str} \033[93m| Resolution: {img_width}x{img_height} Pix \033[95m| Color Mode: {color_mode_str}\033[0m")

                            if img_size_mb > 3 or img_width > 2048 or img_height > 2048:
                                print(
                                    f"\033[93m[WARNING] Image {images[choice]} is large, opening the output file might crash text editors!\033[0m")
                                confirm = input(
                                    f"\033[93m[INPUT] Are you sure you want to convert image {images[choice]}? (Yes/No): \033[0m").strip().lower() or 'no'
                                if confirm not in ['yes', 'y']:
                                    continue

                            while True:
                                include_alpha = input(
                                    "\033[96m[INPUT] Include alpha channel? (Yes/No): \033[0m").strip().lower()
                                if include_alpha in ['yes', 'y']:
                                    include_alpha = True
                                    break
                                elif include_alpha in ['no', 'n']:
                                    include_alpha = False
                                    break
                                else:
                                    print("\033[91m[ERROR] Invalid input. Please enter 'Yes' or 'No'.\033[0m")

                            while True:
                                font_size = input("\033[96m[INPUT] Set font size (integer/float/percent/fraction, default 1): \033[0m").strip()
                                try:
                                    font_size = parse_font_size(font_size)
                                    break
                                except ValueError:
                                    print("\033[91m[ERROR] Invalid font size format. Please try again.\033[0m")

                            output_file_name = f"{os.path.splitext(images[choice])[0]}.txt"
                            output_path = os.path.join(output_folder, output_file_name)
                            image_to_textmeshpro(selected_image, output_path, include_alpha, font_size)

                        except Exception as e:
                            print(f"\033[91m[ERROR] Image processing failed: {e}\033[0m")

                        continue_conversion = input(
                            "\033[96m[INPUT] Continue converting other images? (Yes/No): \033[0m").strip().lower()
                        if continue_conversion not in ['yes', 'y']:
                            print("\033[92m[SUCCESS] Process exited.\033[0m")
                            print("The window will close in 5 seconds...")
                            time.sleep(5)
                            sys.exit()
                        break
                    else:
                        print("\033[91m[ERROR] Invalid input. Please enter a valid image number!\033[0m")

                except ValueError:
                    print("\033[91m[ERROR] Invalid input. Please enter a valid number!\033[0m")

    except KeyboardInterrupt:
        print("\033[92m[SUCCESS] Program interrupted by user.\033[0m")
        print("The window will close in 5 seconds...")
        time.sleep(5)
        sys.exit()
