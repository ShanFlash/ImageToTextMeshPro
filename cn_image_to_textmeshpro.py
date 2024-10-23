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

    print(f"\033[92m[SUCCESS] 转换成功！\033[0m")
    print(f"\033[92m[SUCCESS] 输出文件大小: {output_size_str}\033[0m")
    print(f"\033[92m[SUCCESS] 输出文件路径: {os.path.abspath(output_path)}\033[0m")

if __name__ == "__main__":
    print("\033[97m[WELCOME] 欢迎使用图片转TMP富文本标签工具！\033[0m")
    print("\033[97m[WELCOME] 本工具可以将指定格式的图片转换为适用于Unity引擎的TMP富文本标签!\033[0m")
    print("\033[97m[WELCOME] 作者: www.bilibili.com@是闪闪闪闪闪\033[0m")

    input_folder = "Input"
    output_folder = "Output"

    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
        print(f"\033[93m[INFO] 没有找到输入文件夹，已自动创建 '{input_folder}' 文件夹。\033[0m")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"\033[93m[INFO] 没有找到输出文件夹，已自动创建 '{output_folder}' 文件夹。\033[0m")

    try:
        images = [
            f for f in os.listdir(input_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
        ]

        if not images:
            print(f"\033[91m[ERROR] 没有在输入文件夹内找到图像文件，请将需要转换的图片放入 {input_folder} 文件夹中再运行程序！\033[0m")
            print("当前窗口将在5秒后关闭...")
            time.sleep(5)
            sys.exit()

        print(f"\033[94m[INFO] 已找到 {len(images)} 个图像文件。\033[0m")

        while True:
            print("\033[94m[INFO] 请选择需要转换为TMP富文本标签的图片:\033[0m")
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
                    f"\033[96m({str(i + 1).zfill(2)}) {img:<{max_filename_length}}  ｜ 大小: {img_size_str:<{max_size_length}} ｜ 分辨率: {resolution_str:<{max_resolution_length}}  ｜ 颜色模式: {color_mode_str:<{max_color_mode_length}}\033[0m")

            while True:
                user_input = input("\033[95m[INPUT] 请输入相应的图片编号进行选择或输入 '0' 退出: \033[0m")
                if user_input == '0':
                    print("\033[92m[SUCCESS] 已退出进程。\033[0m")
                    print("当前窗口将在5秒后关闭...")
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
                                f"\033[94m[INFO] 你选择的图片为： ({str(choice + 1).zfill(2)}) {images[choice]}  ｜ 大小: {img_size_str}  ｜ 分辨率: {img_width}x{img_height} Pix  ｜ 颜色模式: {color_mode_str}\033[0m")

                            if img_size_mb > 3 or img_width > 2048 or img_height > 2048:
                                print(
                                    f"\033[93m[WARNING] 图片 {images[choice]} 体积过大，后续打开其输出文件可能导致文本编辑器崩溃！\033[0m")
                                confirm = input(
                                    f"\033[93m[INPUT] 你确定要对图片 {images[choice]} 进行转换吗 (Yes/No)? \033[0m").strip().lower() or 'no'
                                if confirm not in ['yes', 'y']:
                                    continue

                            print("\033[94m[INFO] 正在转码为TMP富文本标签，请耐心等待...\033[0m")

                            base_name = os.path.splitext(images[choice])[0]
                            output_file = os.path.join(output_folder, f"{base_name}.txt")

                            image_to_textmeshpro(selected_image, output_file)

                            continue_input = input(
                                "\033[95m[INPUT] 是否继续进行转换 (Yes/No)? \033[0m").strip().lower()
                            if continue_input in ['yes', 'y']:
                                break
                            else:
                                print("\033[92m[SUCCESS] 已退出进程。\033[0m")
                                print("当前窗口将在5秒后关闭...")
                                time.sleep(5)
                                sys.exit()
                        except Exception as e:
                            print(f"\033[91m[ERROR] 发生未知错误: {e}！请检查文件是否可以访问！\033[0m")
                            continue
                    else:
                        print("\033[91m[ERROR] 无效的选择，请输入一个有效的数字！\033[0m")
                except ValueError:
                    print("\033[91m[ERROR] 无效的输入，请输入一个整数！\033[0m")
    except Exception:
        print("\033[91m[ERROR] 发生未知错误！\033[0m")
