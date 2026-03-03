import re
from pathlib import Path
from config import logger, AD_REMOVE_EXTENSIONS
from PyQt6.QtCore import QThread, pyqtSignal


class AdRemoverWorker(QThread):
    """去广告工作线程,用于后台处理文件重命名"""
    # 日志信号
    log_signal = pyqtSignal(str)
    # 进度信号
    progress_signal = pyqtSignal(int)
    # 完成信号，参数1为总项目数量,参数2为被重命名的项目数量
    finished_signal = pyqtSignal(int, int)

    def __init__(self, directory_path, ad_patterns, file_extensions=None):
        super().__init__(parent=None)
        # 目录路径
        self.directory_path = directory_path
        # 广告匹配规则
        self.ad_patterns = ad_patterns
        # 支持的文件扩展名
        self.file_extensions = file_extensions or AD_REMOVE_EXTENSIONS

    def remove_advertisements_from_name(self, name):
        """从文件名中删除广告词"""
        new_name = name
        for pattern in self.ad_patterns:
            # 替换广告词为空
            new_name = re.sub(pattern, '', new_name, flags=re.IGNORECASE)
        return new_name.strip()

    def run(self):
        """执行文件和文件夹重命名操作"""
        # 先判断文件夹是否存在
        directory = Path(self.directory_path)
        if not directory.exists():
            self.log_signal.emit(f"错误: 指定的目录不存在 {self.directory_path}")
            self.finished_signal.emit(0, 0)
            return

        # 处理目录
        logger.info(f"开始处理目录 {self.directory_path}")
        logger.info(f"广告规则数量: {len(self.ad_patterns)}")

        # 获取所有文件和文件夹,按照路径长度降序排列,确保先处理深层文件和文件夹
        all_items = list(directory.rglob('*'))
        all_items.sort(key=lambda x: len(str(x)), reverse=True)

        # 总项目数量
        total_items = len(all_items)
        # 被重命名的项目数量
        renamed_count = 0
        # 处理完成的项目数量
        processed_count = 0

        # 先处理文件
        for item in all_items:
            # 记录处理进度
            processed_count += 1
            progress = int((processed_count / total_items) * 100) if total_items > 0 else 100
            self.progress_signal.emit(progress)

            # 如果是文件类型
            if item.is_file():
                # 检查文件扩展名
                if item.suffix.lower() not in self.file_extensions:
                    continue

                # 获取信息
                filename = item.name
                stem = item.stem
                suffix = item.suffix

                # 处理文件名,不包括扩展名
                new_stem = self.remove_advertisements_from_name(stem)
                if new_stem != stem:
                    # 重命名文件
                    new_filename = new_stem + suffix
                    # 防止重命名以后为空文件
                    if not new_filename.strip():
                        new_filename = f"file_{renamed_count}{suffix}"
                    # 新的文件路径
                    new_path = item.parent / new_filename
                    # 处理文件名冲突
                    if new_path.exists():
                        counter = 1
                        while new_path.exists():
                            new_filename = f"{new_stem}_{counter}{suffix}"
                            new_path = item.parent / new_filename
                            counter += 1
                    # 执行重命名文件的操作
                    try:
                        item.rename(new_path)
                        self.log_signal.emit(f"文件: {filename} -> {new_filename}")
                        logger.info(f"文件重命名成功: {filename} -> {new_filename}")
                        renamed_count += 1
                    except Exception as e:
                        error_msg = f"文件重命名失败 {filename}: {e}"
                        self.log_signal.emit(error_msg)
                        logger.error(error_msg)

            # 重新获取文件夹列表,因为文件可能已经被重命名,路径可能变化
            all_folders = [d for d in directory.rglob('*') if d.is_dir()]
            all_folders.sort(key=lambda x: len(str(x)), reverse=True)

            # 再处理文件夹
            for folder in all_folders:
                # 文件夹的名字
                folder_name = folder.name
                # 新的文件夹名字
                new_folder_name = self.remove_advertisements_from_name(folder_name)
                # 如果需要修改
                if new_folder_name != folder_name:
                    # 防止重命名以后为空文件夹
                    if not new_folder_name.strip():
                        new_folder_name = f"folder_{renamed_count}"
                    # 新的文件夹路径
                    new_path = folder.parent / new_folder_name
                    # 处理文件夹名冲突
                    if new_path.exists():
                        counter = 1
                        while new_path.exists():
                            new_folder_name = f"{new_folder_name}_{counter}"
                            new_path = folder.parent / new_folder_name
                            counter += 1
                    # 执行文件夹的重命名操作
                    try:
                        folder.rename(new_path)
                        self.log_signal.emit(f"文件夹: {folder_name} -> {new_folder_name}")
                        logger.info(f"文件夹重命名成功: {folder_name} -> {new_folder_name}")
                        renamed_count += 1
                    except Exception as e:
                        error_msg = f"文件夹重命名失败 {folder_name}: {e}"
                        self.log_signal.emit(error_msg)
                        logger.error(error_msg)

        logger.info(f"处理完成, 共处理 {processed_count} 个项目, 重命名了 {renamed_count} 个项目")
        self.finished_signal.emit(processed_count, renamed_count)
