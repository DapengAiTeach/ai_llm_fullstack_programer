import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
# 相对路径，相对于 manage.py 所在的路径
load_dotenv(".env")

# 初始化常量
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

# 创建OpenAI客户端
client = OpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_API_KEY,
)