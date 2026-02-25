import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

# 创建应用程序
app = QApplication(sys.argv)

# 创建窗口
window = QWidget()
# 窗口标题
window.setWindowTitle("大鹏聊天室")
# 窗口大小：宽度400，高度300
window.resize(400, 300)

# 添加标签
label = QLabel("你好，张老师！", parent=window)
# 标签位置：距离左边100，距离顶部80
label.move(100, 80)
# 设置标签样式
label.setStyleSheet("font-size: 20px; color: blue;")

# 显示窗口
window.show()

# 运行应用程序
sys.exit(app.exec())