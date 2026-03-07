from django.shortcuts import render
from django.http import StreamingHttpResponse
from .services import generate_chat_stream


def index(request):
    return render(request, 'index/index.html')


def stream_chat(request):
    """
    SSE 流式聊天接口
    返回 StreamingHttpResponse，支持 Server-Sent Events
    前端使用 EventSource 接收流式数据
    """
    # 从 GET 或 POST 参数中获取消息
    message = request.GET.get('message', request.POST.get('message', ''))

    # 创建流式响应
    response = StreamingHttpResponse(
        generate_chat_stream(message),
        content_type='text/event-stream'
    )

    # 设置SSE相关的响应头
    response['Cache-Control'] = 'no-cache'
    # 禁用Nginx缓冲
    # response["X-Accel-Buffering"] = "no"

    return response
