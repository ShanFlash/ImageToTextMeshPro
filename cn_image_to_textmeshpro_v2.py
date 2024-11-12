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
    with tqdm(total=height, desc=f"[PROGRESS] 转换 {os.path.basename(image_path)}", ncols=100) as pbar:
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

    print(f"\033[92m[SUCCESS] 转换成功！\033[0m")
    print(f"\033[92m[SUCCESS] 输出文件大小: {output_size_str}\033[0m")
    print(f"\033[92m[SUCCESS] 输出文件路径: {os.path.abspath(output_path)}\033[0m")


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
            raise ValueError("无效的字体大小格式")


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

    print("\033[94m[INFO] 基本操作：\033[0m")
    print("1. 选择输入图像（支持PNG、JPG、JPEG等常见的位图格式）")
    print("2. 选择是否包含透明度通道")
    print("3. 设置字体大小，支持整数、浮点数、百分数、分数")
    print("4. 转换为TMP富文本标签")

    print("\033[94m[INFO] 像素大小设置示例：\033[0m")
    print("像素大小可以是：")
    print(" - 整数（例如：10）")
    print(" - 浮点数（例如：1.5）")
    print(" - 百分数（例如：50%）")
    print(" - 分数（例如：2/3）")

    print("\033[94m[INFO] 转换后生成的TMP富文本标签示例：\033[0m")
    example_text = """
    - 不带有透明度通道
    <size=1><color=#FF0000>█████</color><color=#00FF00>████████</color><color=#0000FF>██████████</color></size>

    - 带有透明度通道
    <size=1><color=#FF0000FF>█████</color><color=#00FF0080>████████</color><color=#0000FF00>██████████</color></size>
    """
    print(example_text)

    print("=" * 100)


if __name__ == "__main__":
    print("\033[97m[WELCOME] 欢迎使用图片转TMP富文本标签工具！\033[0m")
    print("\033[97m[WELCOME] 本工具可以将指定格式的图片转换为适用于Unity引擎的TMP富文本标签!\033[0m")
    print("\033[97m[WELCOME] 作者: www.bilibili.com@是闪闪闪闪闪\033[0m")

    show_example_usage()

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
            print(
                f"\033[91m[ERROR] 没有在输入文件夹内找到图像文件，请将需要转换的图片放入 {input_folder} 文件夹中再运行程序！\033[0m")
            print("当前窗口将在5秒后关闭...")
            time.sleep(5)
            sys.exit()

        print(f"\033[94m[INFO] 已找到 {len(images)} 个图像文件。\033[0m")

        while True:
            print("\033[94m[INFO] 请选择需要转换为TMP富文本标签的图片:\033[0m")
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
                    f"\033[96m({str(i + 1).zfill(2)})\033[91m | {truncated_img_name:<{max_filename_length}} \033[92m| 图片格式: {img.split('.')[-1]:<6} \033[93m| 大小: {img_size_str:<{max_size_length}} \033[94m| 分辨率: {resolution_str:<{max_resolution_length}} \033[95m| 颜色模式: {color_mode_str:<{max_color_mode_length}}\033[0m")

            print_dynamic_line(100)

            while True:
                user_input = input("\033[96m[INPUT] 请输入相应的图片编号进行选择或输入 '0' 退出: \033[0m")
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
                            color_mode_str = get_color_mode(selected_image)

                            print(
                                f"\033[94m[INFO] 你选择的图片为： \033[96m({str(choice + 1).zfill(2)}) \033[91m{images[choice]} \033[92m｜ 大小: {img_size_str} \033[93m｜ 分辨率: {img_width}x{img_height} Pix \033[95m｜ 颜色模式: {color_mode_str}\033[0m")

                            if img_size_mb > 3 or img_width > 2048 or img_height > 2048:
                                print(
                                    f"\033[93m[WARNING] 图片 {images[choice]} 体积过大，后续打开其输出文件可能导致文本编辑器崩溃！\033[0m")
                                confirm = input(
                                    f"\033[93m[INPUT] 你确定要对图片 {images[choice]} 进行转换吗 (Yes/No)? \033[0m").strip().lower() or 'no'
                                if confirm not in ['yes', 'y']:
                                    continue

                            while True:
                                include_alpha = input(
                                    "\033[96m[INPUT] 是否包含透明度通道? (Yes/No): \033[0m").strip().lower()
                                if include_alpha in ['yes', 'y']:
                                    include_alpha = True
                                    break
                                elif include_alpha in ['no', 'n']:
                                    include_alpha = False
                                    break
                                else:
                                    print("\033[91m[ERROR] 输入无效，请输入 'Yes' 或 'No'。\033[0m")

                            while True:
                                font_size = input("\033[96m[INPUT] 请设置像素大小，支持整数/浮点数/百分数/分数 (默认为 1): \033[0m").strip()
                                try:
                                    font_size = parse_font_size(font_size)
                                    break
                                except ValueError:
                                    print("\033[91m[ERROR] 字体大小格式错误，请重新输入。\033[0m")

                            output_file_name = f"{os.path.splitext(images[choice])[0]}.txt"
                            output_path = os.path.join(output_folder, output_file_name)
                            image_to_textmeshpro(selected_image, output_path, include_alpha, font_size)

                        except Exception as e:
                            print(f"\033[91m[ERROR] 图片处理失败: {e}\033[0m")

                        continue_conversion = input(
                            "\033[96m[INPUT] 是否继续转换其他图片? (Yes/No): \033[0m").strip().lower()
                        if continue_conversion not in ['yes', 'y']:
                            print("\033[92m[SUCCESS] 已退出进程。\033[0m")
                            print("当前窗口将在5秒后关闭...")
                            time.sleep(5)
                            sys.exit()
                        break
                    else:
                        print("\033[91m[ERROR] 无效的输入，请输入有效的图片编号！\033[0m")

                except ValueError:
                    print("\033[91m[ERROR] 输入无效，请输入有效的数字！\033[0m")

    except KeyboardInterrupt:
        print("\033[92m[SUCCESS] 程序被用户中断。\033[0m")
        print("当前窗口将在5秒后关闭...")
        time.sleep(5)
        sys.exit()
