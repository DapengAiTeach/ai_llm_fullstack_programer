"""
AI 聊天服务层
处理与 AI 相关的业务逻辑，包括流式聊天响应
"""

from .openai_client import client, MODEL


def generate_chat_stream(message):
    """
    流式生成 AI 聊天响应
    
    Args:
        message: 用户输入的消息
        
    Yields:
        str: SSE 格式的数据块，格式为 "data: 内容\n\n"
    """
    if not message or not message.strip():
        yield "data: 请输入有效的消息\n\n"
        yield "data: [DONE]\n\n"
        return

    # 构建消息列表
    messages = [
        {"role": "system", "content": "你是个幽默有趣的聊天机器人"},
        {"role": "user", "content": message}
    ]

    try:
        # 创建流式聊天完成请求
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,  # 启用流式输出
        )

        # 逐块处理响应
        for chunk in completion:
            # 获取当前块的内容增量
            delta = chunk.choices[0].delta
            
            # 检查是否有内容
            if delta.content:
                # 对内容进行 SSE 编码（处理换行符等特殊字符）
                content = delta.content.replace('\n', '\\n')
                yield f"data: {content}\n\n"

        # 发送结束标记
        yield "data: [DONE]\n\n"

    except Exception as e:
        # 错误处理
        error_msg = str(e).replace('\n', ' ')
        yield f"data: [ERROR] {error_msg}\n\n"
        yield "data: [DONE]\n\n"
