from django.urls import path
from . import views

# 应用名称
app_name = 'index'

# 路由列表
urlpatterns = [
    # 首页
    path('', views.index, name='index'),
]
