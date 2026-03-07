def outer():
    """外层函数"""
    count = 0

    def inner():
        """内层函数"""
        # 声明要修改外层的变量
        nonlocal count
        count += 2
        return count

    # 返回外层的count
    print("外层函数的count：",  count)
    return inner()

# 直接调用outer函数
print(outer())