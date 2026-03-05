import base64
from io import BytesIO
from PIL import Image
from django.shortcuts import render

def index(request):
    image_data = None
    if request.method == 'POST' and request.FILES.get('image'):
        # 读取上传的图片到 Pillow
        img = Image.open(request.FILES['image'])

        # 修改尺寸
        img_resized = img.resize((960, 600), Image.LANCZOS)
        if img_resized.mode in ('RGBA', 'LA', 'P'):
            img_resized = img_resized.convert('RGB')

        # 转 base64
        buffer = BytesIO()
        img_resized.save(buffer, format='JPEG', quality=95)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        image_data = f'data:image/jpeg;base64,{img_base64}'

    context = {
        'image_data': image_data
    }
    return render(request, 'image_tool/index.html', context)
