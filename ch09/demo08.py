def add(a=3, b=33):
    return a + b

# 调用时省略，就会使用默认值
print(add())

# 按照位置覆盖第1个参数
print(add(88))

# 只覆盖某一个参数
print(add(b=88))

# 按照参数名
print(add(b=88, a=99))

# 按照位置
print(add(99, 88))