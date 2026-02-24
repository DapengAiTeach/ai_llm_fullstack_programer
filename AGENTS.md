# AI LLM 全栈工程师课程项目

## 项目概述

这是一个面向 AI 大模型全栈工程师学习的 Python 教学项目。项目包含 OpenAI/OpenRouter API 的使用示例，以及文件批处理工具脚本。代码注释和文档主要使用中文。

## 技术栈

- **编程语言**: Python 3.11+
- **核心依赖**:
  - `openai==2.21.0` - OpenAI Python SDK，用于与 LLM API 交互
  - `python-dotenv==1.2.1` - 环境变量管理
  - `pyqt6==6.10.2` - GUI 开发框架（预留）

## 项目结构

```
.
├── .env                  # 环境变量配置文件（包含 API 密钥，不提交到 Git）
├── .env.example          # 环境变量示例文件
├── .gitignore           # Git 忽略文件配置
├── requirements.txt     # 生产环境依赖
├── requirements-dev.txt # 开发环境依赖
├── tmp.py               # 文件批量重命名工具（去除文件名中的广告词）
├── ch01/                # 第一章：OpenAI API 基础示例
│   ├── __init__.py      # 模块初始化文件（空）
│   ├── open_router_demo01.py  # 基础聊天示例（硬编码配置）
│   ├── open_router_demo02.py  # 基础聊天示例（环境变量配置）
│   └── demo03_stream.py       # 流式输出聊天示例
└── venv/                # Python 虚拟环境目录
```

## 代码组织

### 章节结构 (chXX/)

- `ch01/` - 第一章：OpenAI API 基础调用
  - 演示如何使用 OpenAI SDK 调用大语言模型 API
  - 包含非流式和流式两种调用方式
  - 展示硬编码配置与环境变量配置两种模式

### 工具脚本

- `tmp.py` - 批量文件重命名工具
  - 功能：递归处理目录中的文件，去除文件名中的广告词
  - 用途：清理从网络下载的课程资源文件名

## 开发规范

### 语言

- 代码注释使用中文
- 变量命名遵循 Python 规范（snake_case）
- 文档和说明使用中文

### 配置管理

- **敏感信息**（API 密钥、Base URL 等）必须存放在 `.env` 文件中
- `.env` 文件已添加到 `.gitignore`，禁止提交到版本控制
- 参考 `.env.example` 创建本地 `.env` 文件

### 环境变量

项目使用的环境变量：

```bash
OPENAI_BASE_URL=https://openrouter.ai/api/v1  # API 基础 URL
OPENAI_API_KEY=你的API Key                      # API 密钥
MODEL=glm-4.5-air                             # 默认模型名称
```

## 运行和测试

### 环境准备

1. 创建虚拟环境（如尚未创建）：
   ```bash
   python -m venv venv
   ```

2. 激活虚拟环境：
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 配置环境变量：
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填入你的 API 密钥
   ```

### 运行示例

```bash
# 运行第一章示例
cd ch01
python open_router_demo01.py
python open_router_demo02.py
python demo03_stream.py
```

### 运行工具脚本

```bash
# 编辑 tmp.py 中的 directory_path 变量为目标目录
python tmp.py
```

## API 提供商

项目使用 [OpenRouter](https://openrouter.ai/) 作为 API 提供商：

- **Base URL**: `https://openrouter.ai/api/v1`
- **支持的模型**: glm-4.5-air, z-ai/glm-4.5-air:free 等
- **特点**: 兼容 OpenAI API 格式，支持多种大语言模型

## 安全注意事项

1. **永远不要将 API 密钥提交到 Git**
   - `.env` 文件已在 `.gitignore` 中
   - 代码中不应出现硬编码的 API 密钥（demo01 为教学示例，实际开发应使用环境变量）

2. **API 密钥管理**
   - 生产环境应使用更安全的密钥管理方案
   - 定期轮换 API 密钥

## Git 忽略规则

```
venv          # 虚拟环境目录
.idea         # IDE 配置
.env          # 环境变量（包含敏感信息）
__pycache__   # Python 缓存
tmp*          # 临时文件
```

## 依赖版本

### 生产依赖 (requirements.txt)
- openai==2.21.0
- python-dotenv==1.2.1
- pyqt6==6.10.2

### 开发依赖 (requirements-dev.txt)
- openai==2.21.0
- python-dotenv==1.2.1

## 注意事项

- 本项目为教学项目，代码以演示和学习为目的
- 部分示例代码（如 open_router_demo01.py）为了简洁使用了硬编码密钥，实际项目应始终使用环境变量
- 使用 OpenRouter API 需要有效的 API 密钥
