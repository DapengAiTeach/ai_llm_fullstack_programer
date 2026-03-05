from django.urls import path
from . import views

# 应用名称
app_name = "image_tool"

# 路由列表
urlpatterns = [
    path('', views.index, name='index'),
]
