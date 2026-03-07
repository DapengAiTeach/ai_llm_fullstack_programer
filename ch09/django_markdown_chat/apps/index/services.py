from .openai_client import client, MODEL


def generate_chat_stream(message):
    """
    生成AI流式聊天响应
    SSE 格式的数据块：data: 内容\n\n
    """
    # 如果没有消息，返回错误信息
    if not message or not message.strip():
        yield "data: 请输入有效的消息\n\n"
        yield "data: [DONE]\n\n"
        return

    # 构建消息列表
    messages = [
        {
            "role": "system",
            "content": "你是一个AI大模型老师，叫做张大鹏，你很幽默，学识渊博，通晓中国上下五千年历史，尤其是三国的历史，擅长引经据典。"
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
                content = (delta.content.replace("\n", "\\n")
                           .replace("\r", "\\r"))
                yield f"data: {content}\n\n"

        # 发送结束标记
        yield "data: [DONE]\n\n"
    except Exception as e:
        # 处理异常
        err_msg = (str(e).replace("\n", "\\n")
                   .replace("\r", "\\r"))
        yield f"data: [ERROR]{err_msg}\n\n"
        yield "data: [DONE]\n\n"
