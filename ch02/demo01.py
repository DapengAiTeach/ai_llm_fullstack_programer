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
    {"role": "system", "content": "你是一个幽默的段子手，你喜欢用东北方言讲关于三国的历史笑话"},
    {"role": "user", "content": "请给我讲一个笑话"},
]

# 创建聊天
completion = client.chat.completions.create(
    # 模型名称
    model=MODEL,
    # 聊天内容
    messages=messages,
)

# 打印结果
print(completion.choices[0].message.content)