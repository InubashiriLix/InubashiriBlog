from PIL import Image

# 灰度字符集，代表从暗到亮的灰度
ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']


# 将图片大小调整为更小的比例
def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # 调整高度比例
    resized_image = image.resize((new_width, new_height))
    return resized_image


# 将图片转换为灰度图
def grayify(image):
    return image.convert("L")


# 将每个像素映射为 ASCII 字符
def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel // 25]  # 灰度范围从0到255，这里除以25来映射到字符集
    return ascii_str


# 完整的图片转 ASCII 的函数
def image_to_ascii(image_path, output_txt_path="output.txt"):
    try:
        # 打开图片
        image = Image.open(image_path)
    except Exception as e:
        print(f"无法打开图片 {image_path}: {e}")
        return

    # 调整大小和灰度化
    image = resize_image(image)
    image = grayify(image)

    # 将图片转换为 ASCII 字符串
    ascii_str = pixels_to_ascii(image)

    # 将 ASCII 字符串格式化为图片的宽度
    img_width = image.width
    ascii_img = "\n".join([ascii_str[i:i + img_width] for i in range(0, len(ascii_str), img_width)])

    # 将 ASCII 图像保存到 txt 文件中
    with open(output_txt_path, "w") as f:
        f.write(ascii_img)

    print(f"ASCII 图片已保存到 {output_txt_path}")


image_path = r"C:\Users\lixin\Desktop\output\test\1.jpg"  # 这里替换为你的图片路径
output_txt_path = "output_image.txt"  # 替换为你想要保存的 .txt 文件路径
image_to_ascii(image_path, output_txt_path)
