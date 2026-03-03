from django.shortcuts import render


def home(request):
    """首页视图函数"""
    return render(request, 'home/index.html')
