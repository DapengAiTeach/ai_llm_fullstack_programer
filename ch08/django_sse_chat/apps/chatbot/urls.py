from django.urls import path
from . import views

# 应用名称
app_name = "chatbot"

# 路由列表
urlpatterns = [
    # 聊天机器人首页
    path('', views.index, name='index'),
]
