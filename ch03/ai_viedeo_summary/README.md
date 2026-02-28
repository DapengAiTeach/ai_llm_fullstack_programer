# 智能视频统计工具

基于 PyQt6 开发的视频文件统计工具，支持扫描目录中的视频文件、统计总时长和大小，并支持导出列表。

## 功能特性

- 📁 选择目录扫描视频文件
- 📊 统计视频数量、总时长、总大小
- 📋 以表格形式展示视频信息
- 💾 导出视频列表为 TXT 文件
- 🎨 简洁的图形界面

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行程序

```bash
python main.py
```

## 打包为 EXE

### 方式一：目录模式（推荐）

打包为文件夹，启动快、体积小、不易被杀毒软件误报。

```bash
python build.py
```

打包完成后，可执行文件位于：
```
dist/VideoStatsTool/VideoStatsTool.exe
```

### 方式二：单文件模式

打包为单个 EXE 文件，方便分发但启动较慢。

```bash
python build.py --onefile
```

打包完成后，可执行文件位于：
```
dist/VideoStatsTool.exe
```

### 其他打包选项

```bash
# 清理后重新打包
python build.py --clean

# 调试模式（显示控制台窗口）
python build.py --console

# 组合使用
python build.py --clean --onefile
```

### 配置打包参数

编辑 `build.py` 文件顶部的配置区域：

```python
# ==================== 配置区域（按需修改）====================
APP_NAME = "VideoStatsTool"           # 应用名称
MAIN_SCRIPT = "main.py"               # 入口文件
ICON_FILE = ""                        # 图标路径，如 "assets/icon.ico"
ONEFILE = False                       # True=单文件, False=目录（推荐）
CONSOLE = False                       # True=显示控制台, False=仅窗口（调试用）
# ==========================================================
```

### 添加应用图标

1. 准备 `.ico` 格式的图标文件（推荐尺寸：256x256）
2. 将图标放入项目目录，如 `assets/icon.ico`
3. 修改配置：`ICON_FILE = "assets/icon.ico"`
4. 重新打包

### 分发程序

打包完成后，将以下文件/文件夹分发给用户即可：

**目录模式：**
```
dist/VideoStatsTool/      # 整个文件夹压缩为 zip
```

**单文件模式：**
```
dist/VideoStatsTool.exe   # 单个可执行文件
```

## 项目结构

```
.
├── main.py              # 主程序入口
├── build.py             # 打包脚本
├── requirements.txt     # 依赖列表
├── README.md            # 项目说明
├── config/              # 配置模块
├── entity/              # 实体类
├── services/            # 业务逻辑
├── ui/                  # UI 界面
└── utils/               # 工具函数
```

## 技术栈

- Python 3.x
- PyQt6 - GUI 框架
- OpenCV - 视频信息读取
- Loguru - 日志记录

## 许可证

MIT License
