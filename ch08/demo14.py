# 创建空集合
s = set()
print(s, type(s))

# 创建有元素的集合
s = {8, 88, 888}
print(s, type(s))

# 注意：空 {} 创建的是字典
d = {}
print(d, type(d))

# 集合可以自动去重
s = {1, 1, 1, 2, 2, 3, 4, 5, 5, 5}
print(s)
