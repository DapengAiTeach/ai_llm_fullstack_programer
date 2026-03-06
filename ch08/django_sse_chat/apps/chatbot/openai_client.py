import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv(".env")

# 初始化常量
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

# 创建 OpenAI 客户端
client = OpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_API_KEY,
)