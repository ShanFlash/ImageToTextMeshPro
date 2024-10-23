import os
import time
import sys
from PIL import Image
import numpy as np

def image_to_textmeshpro(image_path, output_path):
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    data = np.array(img)

    hex_colors = []
    for y in range(height):
        current_color = None
        count = 0
        for x in range(width):
            r, g, b, a = data[y, x]
            if a > 0:
                hex_color = f"#{r:02X}{g:02X}{b:02X}{a:02X}"
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

    output_content = "<size=1>" + "".join(hex_colors).replace("\n", "\\n") + "</size>"

    with open(output_path, "w", encoding='utf-8') as f:
        f.write(output_content)

    output_size = os.path.getsize(output_path) / (1024 * 1024)
    output_size_str = f"{output_size:.2f} MB" if output_size >= 1 else f"{output_size * 1024:.2f} KB"

    print(f"\033[92m[SUCCESS] Conversion successful!\033[0m")
    print(f"\033[92m[SUCCESS] Output file size: {output_size_str}\033[0m")
    print(f"\033[92m[SUCCESS] Output file path: {os.path.abspath(output_path)}\033[0m")

if __name__ == "__main__":
    print("\033[97m[WELCOME] Welcome to the Image to TMP Rich Text Tag Tool!\033[0m")
    print("\033[97m[WELCOME] This tool can convert specified format images into TMP rich text tags for Unity!\033[0m")
    print("\033[97m[WELCOME] Author: www.bilibili.com@是闪闪闪闪闪\033[0m")

    input_folder = "Input"
    output_folder = "Output"

    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
        print(f"\033[93m[INFO] Input folder not found, created '{input_folder}' folder automatically.\033[0m")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"\033[93m[INFO] Output folder not found, created '{output_folder}' folder automatically.\033[0m")

    try:
        images = [
            f for f in os.listdir(input_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
        ]

        if not images:
            print(f"\033[91m[ERROR] No image files found in the input folder, please place the images to convert in the {input_folder} folder and run the program again!\033[0m")
            print("The current window will close in 5 seconds...")
            time.sleep(5)
            sys.exit()

        print(f"\033[94m[INFO] Found {len(images)} image files.\033[0m")

        while True:
            print("\033[94m[INFO] Please select the image to convert to TMP rich text tag:\033[0m")
            max_filename_length = max(len(img) for img in images)
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
                color_mode = Image.open(img_path).convert('RGB').getbands()
                color_mode_str = "RGB" if 'A' not in color_mode else "RGBA"
                resolution_str = f"{img_width}x{img_height} Pix"

                print(
                    f"\033[96m({str(i + 1).zfill(2)}) {img:<{max_filename_length}}  ｜ Size: {img_size_str:<{max_size_length}} ｜ Resolution: {resolution_str:<{max_resolution_length}}  ｜ Color Mode: {color_mode_str:<{max_color_mode_length}}\033[0m")

            while True:
                user_input = input("\033[95m[INPUT] Please enter the corresponding image number to select or input '0' to exit: \033[0m")
                if user_input == '0':
                    print("\033[92m[SUCCESS] Process exited.\033[0m")
                    print("The current window will close in 5 seconds...")
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
                            color_mode = Image.open(selected_image).convert('RGB').getbands()
                            color_mode_str = "RGB" if 'A' not in color_mode else "RGBA"

                            print(
                                f"\033[94m[INFO] You selected the image: ({str(choice + 1).zfill(2)}) {images[choice]}  ｜ Size: {img_size_str}  ｜ Resolution: {img_width}x{img_height} Pix  ｜ Color Mode: {color_mode_str}\033[0m")

                            if img_size_mb > 3 or img_width > 2048 or img_height > 2048:
                                print(
                                    f"\033[93m[WARNING] Image {images[choice]} is too large, subsequent opening of its output file may cause the text editor to crash!\033[0m")
                                confirm = input(
                                    f"\033[93m[INPUT] Are you sure you want to convert the image {images[choice]} (Yes/No)? \033[0m").strip().lower() or 'no'
                                if confirm not in ['yes', 'y']:
                                    continue

                            print("\033[94m[INFO] Converting to TMP rich text tag, please wait...\033[0m")

                            base_name = os.path.splitext(images[choice])[0]
                            output_file = os.path.join(output_folder, f"{base_name}.txt")

                            image_to_textmeshpro(selected_image, output_file)

                            continue_input = input(
                                "\033[95m[INPUT] Do you want to continue converting (Yes/No)? \033[0m").strip().lower()
                            if continue_input in ['yes', 'y']:
                                break
                            else:
                                print("\033[92m[SUCCESS] Process exited.\033[0m")
                                print("The current window will close in 5 seconds...")
                                time.sleep(5)
                                sys.exit()
                        except Exception as e:
                            print(f"\033[91m[ERROR] An unknown error occurred: {e}! Please check if the file is accessible!\033[0m")
                            continue
                    else:
                        print("\033[91m[ERROR] Invalid selection, please enter a valid number!\033[0m")
                except ValueError:
                    print("\033[91m[ERROR] Invalid input, please enter an integer!\033[0m")
    except Exception:
        print("\033[91m[ERROR] An unknown error occurred!\033[0m")
