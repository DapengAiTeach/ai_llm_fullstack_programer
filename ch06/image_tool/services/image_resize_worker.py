from pathlib import Path
from PIL import Image
from PyQt6.QtCore import QThread, pyqtSignal
from config import logger, SUPPORTED_IMAGE_EXTENSIONS


class ImageResizeWorker(QThread):
    """图片尺寸调整工作线程"""
    # 日志信号
    log_signal = pyqtSignal(str)
    # 预览信号，发送处理后的图片路径
    preview_signal = pyqtSignal(str)
    # 完成信号
    # 参数1：是否成功
    # 参数2：图片路径
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, image_path, width, height, output_path=None, preview_only=True):
        super().__init__(parent=None)
        self.image_path = image_path
        self.width = width
        self.height = height
        self.output_path = output_path
        self.preview_only = preview_only
        self._is_running = True

    def run(self):
        """执行图片尺寸调整"""
        # 检查是否继续执行
        if not self._is_running:
            return

        # 检查图片文件是否存在
        image_path = Path(self.image_path)
        if not image_path.exists():
            self.log_signal.emit(f"错误: 图片文件不存在 {self.image_path}")
            self.finished_signal.emit(False, "图片文件不存在")
            return

        # 检查文件扩展名
        if image_path.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
            self.log_signal.emit(f"错误: 不支持的图片格式 {image_path.suffix}")
            self.finished_signal.emit(False, "不支持的图片格式")
            return

        self.log_signal.emit(f"正在处理图片: {image_path.name}")
        self.log_signal.emit(f"目标尺寸: {self.width} x {self.height}")

        try:
            # 打开图片
            with Image.open(self.image_path) as img:
                # 获取原始图片尺寸
                original_size = img.size
                self.log_signal.emit(f"原始尺寸: {original_size[0]} x {original_size[1]}")

                # 检查是否继续执行
                if not self._is_running:
                    return

                # 调整尺寸
                resized_img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)

                # 如果图片是 RGBA 模式且保存为 JPEG，需要转换为 RGB
                if resized_img.mode == 'RGBA':
                    # 创建白色背景
                    background = Image.new('RGB', resized_img.size, (255, 255, 255))
                    background.paste(resized_img, mask=resized_img.split()[3])  # 使用 alpha 通道作为 mask
                    resized_img = background
                elif resized_img.mode != 'RGB' and resized_img.mode != 'L':
                    # 其他非 RGB 模式也转换为 RGB
                    resized_img = resized_img.convert('RGB')

                if self.preview_only:
                    # 预览模式：保存到临时文件
                    preview_path = image_path.parent / f"preview_{image_path.name}"
                    resized_img.save(preview_path)
                    self.preview_signal.emit(str(preview_path))
                    self.log_signal.emit(f"预览已生成: {preview_path.name}")
                    self.finished_signal.emit(True, str(preview_path))
                else:
                    # 保存模式
                    if self.output_path:
                        output_path = Path(self.output_path)
                    else:
                        # 默认在原文件名后添加 _resized
                        output_path = image_path.parent / f"{image_path.stem}_resized{image_path.suffix}"

                    resized_img.save(output_path)
                    self.log_signal.emit(f"图片已保存: {output_path.name}")
                    self.finished_signal.emit(True, str(output_path))

        except Exception as e:
            error_msg = f"处理图片时出错: {e}"
            self.log_signal.emit(error_msg)
            logger.error(error_msg)
            self.finished_signal.emit(False, str(e))

    def stop(self):
        """停止线程"""
        self._is_running = False
        self.wait()
