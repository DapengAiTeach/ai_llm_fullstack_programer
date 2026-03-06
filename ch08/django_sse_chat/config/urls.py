from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 主程序路由
    path('', include('apps.index.urls')),
    # 聊天机器人路由
    path('chatbot/', include('apps.chatbot.urls')),
    # 图片处理路由
    path('image_tool/', include('apps.image_tool.urls')),
    # 后台管理路由
    path('admin/', admin.site.urls),
]
