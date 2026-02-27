import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

# 创建应用程序
app = QApplication(sys.argv)

# 创建窗口
window = QWidget()
# 窗口标题
window.setWindowTitle("大鹏聊天室")
# 窗口大小：宽度400，高度300
window.resize(400, 300)

# 创建垂直布局
layout = QVBoxLayout()

# 添加标签
label = QLabel("你好，张老师！")
# 设置标签样式
label.setStyleSheet("font-size: 20px; color: blue;")
# 设置标签对齐方式为水平居中
label.setAlignment(Qt.AlignmentFlag.AlignCenter)

# 将标签添加到布局，并通过 addStretch 实现垂直居中
layout.addStretch(1)
layout.addWidget(label)
layout.addStretch(1)

# 设置窗口布局
window.setLayout(layout)

# 显示窗口
window.show()

# 运行应用程序
sys.exit(app.exec())