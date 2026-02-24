import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv("../.env")

# 初始化常量
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

# 创建 OpenAI 客户端
client = OpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_API_KEY,
)

# 消息列表
messages = [
    {"role": "system", "content": "你是一个Python专家，并且你是一个CSDN的技术博主"},
    {"role": "user", "content": "请写一篇技术博客，详细的讲解：什么是Python"}
]

# 创建聊天
completion = client.chat.completions.create(
    # 模型名称
    model=MODEL,
    # 聊天内容
    messages=messages,
    # 开启流式输出
    stream=True,
)

# 处理流式输出
for chunk in completion:
    print(chunk.choices[0].delta.content, end="", flush=True)
print()
