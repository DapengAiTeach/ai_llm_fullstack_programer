def make_multiply(x):
    """创建一个乘法函数"""
    # 是一个嵌套函数
    def multiply(y):
        """执行乘法运算"""
        # 内部函数使用了外层函数的 x
        return x * y

    # 返回的是内层函数名
    return multiply

# 创建一个乘2的函数
multiply2 = make_multiply(2)
print(multiply2(5)) # 10

# 创建一个乘3的函数
multiply3 = make_multiply(3)
print(multiply3(5)) # 15