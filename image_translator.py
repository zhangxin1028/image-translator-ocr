#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
图片文字翻译和替换脚本 (Tesseract OCR + Googletrans + Pillow)

功能：
1. 使用 Tesseract OCR 识别图片中的英文文本及其位置。
2. 使用 googletrans 将英文文本翻译成中文。
3. 使用 Pillow 擦除原英文文本，并在原位置写入翻译后的中文文本。
"""
from __future__ import print_function
import pytesseract
from PIL import Image, ImageDraw, ImageFont
from googletrans import Translator
import os

# ====================================================================
# 【❗ 关键配置区域 ❗】
# Tesseract 路径已根据您提供的信息硬编码
# ====================================================================

# 1. 您的 Tesseract.exe 完整路径 (根据您的配置："C:\Users\lenovo\Desktop\C-PROJECT\tesseract.exe")
TESSERACT_PATH = r'C:\Users\lenovo\Desktop\C-PROJECT\tesseract.exe'

# 2. 中文字体文件路径
# 请确保此路径指向您系统中存在的字体文件 (例如：simsun.ttc, msyh.ttc, wqy-zenhei.ttc 等)
# 字体文件通常位于 C:\Windows\Fonts\
FONT_PATH = "simsun.ttc"

# 3. 待处理的输入和输出文件路径
INPUT_IMAGE_FILE = "input_en.png"
OUTPUT_IMAGE_FILE = "output_zh_cn.png"

# ====================================================================
# 初始化和主函数
# ====================================================================

try:
    # 设置 Tesseract 路径 (必须在任何调用 pytesseract 之前)
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
except Exception:
    # 如果路径设置失败，打印提示 (虽然我们在 try/except 外部已经设置了，但保留一个防御性检查)
    print(f"❌ 警告：无法设置 Tesseract 路径，请检查 {TESSERACT_PATH} 是否正确。")

# 初始化翻译器
# 注意：googletrans 是非官方库，可能会因 Google 服务端变动而失效。
translator = Translator()


def translate_image_text(image_path, output_path, target_lang='zh-cn'):
    """
    执行 OCR、翻译和图像替换的主流程
    """
    print(f"--- 🚀 正在处理图片: {image_path} ---")

    try:
        img = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"❌ 错误：找不到输入文件 {image_path}。请检查路径。")
        return

    # 尝试加载中文字体
    try:
        # 字体大小根据图片高度动态调整，防止文本过小或过大
        font_size = max(16, int(img.height / 50))
        font = ImageFont.truetype(FONT_PATH, font_size)
        print(f"✅ 字体加载成功: {FONT_PATH}, 大小: {font_size}")
    except IOError:
        print(f"❌ 警告：无法加载指定中文字体 {FONT_PATH}，请确保路径正确。使用默认字体。")
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(img)

    # 1. OCR 识别 (获取文本和位置)
    # output_type=Output.DICT 返回包含坐标信息的字典
    data = pytesseract.image_to_data(img, lang='eng', output_type=pytesseract.Output.DICT)
    n_boxes = len(data['level'])

    # 过滤掉置信度低于 60 的结果，以及空文本行
    valid_indices = [i for i in range(n_boxes) if data['conf'][i] > 60 and len(data['text'][i].strip()) > 1]
    print(f"🔍 识别到 {len(valid_indices)} 个有效文本块准备翻译。")

    # 2. 循环处理每个识别到的文本块
    for i in valid_indices:
        text = data['text'][i].strip()
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])

        # --- 2a. 翻译 ---
        try:
            # 翻译，并限制长度以防超时
            translation = translator.translate(text[:200], dest=target_lang).text
        except Exception as e:
            print(f"   ⚠️ 翻译失败: '{text[:20]}...' - 错误: {e}")
            continue

        # --- 2b. 擦除原文本 ---
        # 简化处理：用白色填充矩形区域。注意：这会破坏非白色背景。
        draw.rectangle([x, y, x + w, y + h], fill="white")

        # --- 2c. 渲染中文文本 (居中对齐) ---

        # 使用 textbbox 预估中文文本渲染后的尺寸
        try:
            text_bbox = draw.textbbox((0, 0), translation, font=font)
            text_w = text_bbox[2] - text_bbox[0]
            text_h = text_bbox[3] - text_bbox[1]
        except AttributeError:
            # 兼容旧版本 Pillow 的 getsize 方法
            text_w, text_h = draw.textsize(translation, font=font)

        # 居中对齐到原英文文本区域
        center_x = x + (w - text_w) / 2
        center_y = y + (h - text_h) / 2

        # 确保不超出边界
        center_x = max(x, center_x)
        center_y = max(y, center_y)

        draw.text((center_x, center_y), translation, fill=(0, 0, 0), font=font)

        print(f"   ☑️ 成功翻译: '{text}' -> '{translation}'")

    # 3. 保存结果
    img.save(output_path)
    print(f"\n🎉 处理完成。结果已保存到 {output_path}")


if __name__ == '__main__':
    if not os.path.exists(INPUT_IMAGE_FILE):
        print("\n========================================================")
        print(f"❗ 请注意 ❗：找不到默认输入文件 '{INPUT_IMAGE_FILE}'。")
        print("请在脚本所在的目录下放置一张英文图片，并命名为 input_en.png")
        print("========================================================\n")
    else:
        translate_image_text(INPUT_IMAGE_FILE, OUTPUT_IMAGE_FILE)