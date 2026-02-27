import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox,
)
from PyQt6.QtCore import Qt


class LoginWindow(QWidget):
    """登录窗口类"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("用户登录")
        self.setFixedSize(400, 350)

        # 主布局：垂直居中
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 20, 50, 20)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)

        # 顶部弹性空间，让内容垂直居中
        main_layout.addStretch(1)

        # 标题
        title_label = QLabel("用户登录")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = title_label.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # 标题和内容间距
        main_layout.addSpacing(30)

        # 账号
        username_label = QLabel("账号：")
        main_layout.addWidget(username_label)
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("请输入账号")
        self.username_edit.setFixedHeight(30)
        self.username_edit.returnPressed.connect(self.handle_login)
        main_layout.addWidget(self.username_edit)
        main_layout.addSpacing(10)

        # 密码
        password_label = QLabel("密码：")
        main_layout.addWidget(password_label)
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("请输入密码")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setFixedHeight(30)
        self.password_edit.returnPressed.connect(self.handle_login)
        main_layout.addWidget(self.password_edit)
        main_layout.addSpacing(20)

        # 登录按钮
        self.login_btn = QPushButton("登录")
        self.login_btn.setFixedHeight(35)
        self.login_btn.clicked.connect(self.handle_login)
        main_layout.addWidget(self.login_btn)

        # 底部弹性空间，让内容垂直居中
        main_layout.addStretch(1)

    def handle_login(self):
        """处理用户登录按钮点击"""
        # 获取用户输入的账号和密码
        username = self.username_edit.text().strip()
        if not username:
            QMessageBox.warning(self, "错误", "请输入账号")
            self.username_edit.setFocus()
            return
        password = self.password_edit.text().strip()
        if not password:
            QMessageBox.warning(self, "错误", "请输入密码")
            self.password_edit.setFocus()
            return
        # 判断账号和密码是否正确
        if username == "admin" and password == "admin123456":
            QMessageBox.information(self, "提示", "登录成功")
        else:
            QMessageBox.critical(self, "错误", "账号或密码错误")
            self.password_edit.clear()
            self.password_edit.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
