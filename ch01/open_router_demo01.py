from openai import OpenAI

# 初始化常量
OPENAI_BASE_URL = "https://openrouter.ai/api/v1"
OPENAI_API_KEY = "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"
MODEL = "z-ai/glm-4.5-air:free"

# 创建 OpenAI 客户端
client = OpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_API_KEY,
)

# 消息列表
messages = [
    {"role": "system", "content": "你是一个严谨的技术助教"},
    {"role": "user", "content": "用一句话解释什么是大语言模型"}
]

# 创建聊天
completion = client.chat.completions.create(
    # 模型名称
    model=MODEL,
    # 聊天内容
    messages=messages,
)

print(completion.choices[0].message.content)
