# 创建集合
# 1、从列表创建（最常用：去重！）
s = set([8, 88, 88, 888, 888])
print(s, type(s))

# 2、从字符串创建（每个字符成为元素）
s = set('aaabbbccc')
print(s, type(s))

# 3、从元组创建
s = set(('a', 'b', 'c'))
print(s, type(s))

# 4、从字典创建（只保留键）
s = set({'a': 1, 'b': 2, 'c': 3})
print(s, type(s))