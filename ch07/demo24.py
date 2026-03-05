tarr = 8, 88, 888
print(tarr)

# 用 _ 忽略中间的值
x, _, y = tarr
print(x, y) # 8 888

# 如果是多个元素是否可以呢？
tarr = 8, 88, 888, 8888
print(tarr)

# 下面这种写法不可以
# _ 最多只能忽略1个元素
# x, _*, y = tarr
