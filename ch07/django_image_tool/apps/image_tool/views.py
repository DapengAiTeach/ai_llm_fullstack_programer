import base64
from django.shortcuts import render


def index(request):
    image_data = None
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        # 读取文件内容并转为 base64
        image_b64 = base64.b64encode(image.read()).decode()
        # 获取文件类型
        content_type = image.content_type
        image_data = f'data:{content_type};base64,{image_b64}'
    context = {
        'image_data': image_data
    }
    return render(request, 'image_tool/index.html', context)
