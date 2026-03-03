import sys
from ui import MainWindow
from config import logger
from PyQt6.QtWidgets import QApplication

logger.info("程序启动")

app = QApplication(sys.argv)
app.setStyle("Fusion")
window = MainWindow()
window.show()

logger.info("主窗口显示")
exit_code = app.exec()
logger.info(f"程序退出，退出码：{exit_code}")
sys.exit(exit_code)
