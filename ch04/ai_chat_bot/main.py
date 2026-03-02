import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """应用程序入口"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 设置应用程序样式
    app.setStyleSheet("""
        QMainWindow {
            background-color: #F5F5F5;
        }
        QWidget {
            font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
        }
    """)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
