from .openai_client import client, MODEL
from .prompt_loader import get_system_prompt


def generate_chat_stream(message):
    """
    生成AI流式聊天响应
    SSE 格式的数据块：data: 内容\n\n
    """
    # 如果没有消息，返回错误信息
    if not message or message.strip() == '':
        yield "data: 请输入有效的消息\n\n"
        yield "data: [DONE]\n\n"
        return

    # 获取系统提示词（支持热更新）
    try:
        system_prompt = get_system_prompt()
    except FileNotFoundError:
        # 如果提示词文件不存在，使用默认提示词
        system_prompt = "你是一个AI助手，请使用 Markdown 格式回答用户的问题。"

    # 构建消息列表
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": message
        }
    ]

    try:
        # 创建流式聊天
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
        )

        # 处理流式响应
        for chunk in completion:
            # 获取当前块的内容增量
            delta = chunk.choices[0].delta
            # 检查是否有内容
            if delta.content:
                # 对内容进行 SSE 编码，处理换行符等特殊字符
                content = delta.content.replace("\n", "\\n").replace("\r", "\\r")
                yield f"data: {content}\n\n"

        # 发送结束标记
        yield "data: [DONE]\n\n"
    except Exception as e:
        # 处理异常
        err_msg = str(e).replace("\n", "\\n").replace("\r", "\\r")
        yield f"data: [ERROR]{err_msg}\n\n"
        yield "data: [DONE]\n\n"
