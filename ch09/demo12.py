# 全局变量
num1 = 8


def add(a, b):
    # 局部变量
    c = 88
    # 函数内部是可以访问全局变量的
    return a + b + num1 + c


print(add(1, 2))

# 局部变量不能在全局访问
# print(c) # 错误的
