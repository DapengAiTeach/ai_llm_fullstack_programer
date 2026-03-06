s = {8, 88, 888}

# 删除指定元素
s.remove(8)
print(s)

# 删除指定元素，元素不存在不会报错
s.discard(8)
print(s)

# 删除并返回集合中的随机元素
s.pop()
print(s)

# 清空集合
s.clear()
print(s)