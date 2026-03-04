arr = [8, 88, 88, 888, 888]

# 方法1：index() - 查找值的索引（返回第一个匹配的）
print(arr.index(88))  # 1

# 方法2：count() - 统计出现次数
print(arr.count(88))  # 2

# 方法3：in / not in - 判断是否存在（返回True/False）
print(88 in arr)
print(88.8 not in arr)
