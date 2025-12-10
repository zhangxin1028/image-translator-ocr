# 📷 Image-Translator-OCR: 图片文字自动翻译与替换工具

## 🌟 项目简介

这是一个使用 Python 实现的自动化工具，旨在将图片（如流程图、截图、示意图）中的**英文文本**自动识别、翻译成**中文**，并将翻译后的中文文本重新渲染到原图的相应位置。

本项目结合了光学字符识别 (OCR)、机器翻译 (MT) 和图像处理技术，适用于快速汉化非复杂背景图片中的文本内容。

## ✨ 主要功能

* **英文 OCR 识别：** 使用 Tesseract 引擎识别图片中的英文文本及其精确坐标。
* **机器翻译：** 使用 Google Translate API（通过 `googletrans` 库）将识别的英文批量翻译成中文。
* **图像替换：** 使用 Pillow 库擦除原英文文本区域，并在相同位置写入翻译后的中文文本，并尝试居中对齐。

## ⚙️ 环境与依赖要求

运行此脚本需要以下环境和软件包：

### 1. 外部引擎要求

您必须在操作系统中安装 **Tesseract OCR 引擎本体**。

* **下载地址：** [Tesseract-OCR 官方 GitHub 或下载页面](https://github.com/tesseract-ocr/tesseract)
* **配置路径：** 请确保在 `image_translator.py` 脚本中，`TESSERACT_PATH` 变量指向您系统上 `tesseract.exe` 文件的正确路径。

### 2. Python 依赖库

请使用 `pip` 在您的项目虚拟环境中安装所需的 Python 库：

```bash
pip install pytesseract pillow googletrans==4.0.0-rc1
