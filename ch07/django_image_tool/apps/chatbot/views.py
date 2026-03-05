from django.shortcuts import render
from .openai_client import client, MODEL


def index(request):
    # 拿到传递过来的用户消息
    message = request.POST.get('message', '')
    answer = ""

    # 用户消息非空
    if message:
        # 进行AI聊天
        messages = [
            {"role": "system", "content": "你是有个幽默有趣的聊天机器人"},
            {"role": "user", "content": message}
        ]

        # 创建聊天
        completion = client.chat.completions.create(
            # 模型名称
            model=MODEL,
            # 聊天内容
            messages=messages,
        )
        answer = completion.choices[0].message.content

    # 传递个网页的消息
    context = {
        "answer": answer
    }
    return render(request, 'chatbot/index.html', context)
