from django.urls import path
from . import views

# 应用名称
app_name = 'home'

urlpatterns = [
    # 首页路由
    path('', views.home, name='home'),
]
