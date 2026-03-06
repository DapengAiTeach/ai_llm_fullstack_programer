from django.http import StreamingHttpResponse
from django.shortcuts import render
from .services import generate_chat_stream


def index(request):
    """
    聊天页面入口
    
    仅渲染页面模板，所有聊天逻辑通过 SSE 流式接口处理
    """
    return render(request, 'chatbot/index.html')


def stream_chat(request):
    """
    SSE 流式聊天接口
    
    返回 StreamingHttpResponse，支持 Server-Sent Events
    前端使用 EventSource 接收流式数据
    """
    # 从 GET 或 POST 参数中获取消息
    message = request.GET.get('message', '') or request.POST.get('message', '')

    # 创建流式响应
    response = StreamingHttpResponse(
        generate_chat_stream(message),
        content_type='text/event-stream'
    )

    # 设置 SSE 相关响应头
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'  # 禁用 Nginx 缓冲

    return response
