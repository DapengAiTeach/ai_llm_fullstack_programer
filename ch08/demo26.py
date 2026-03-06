s = {8, -88, 888}

# 1、for 循环遍历（顺序不固定）
for item in s:
    print(item, end=" ")
print("\n--------------")

# 2、带索引的遍历（需要 enumerate 手动枚举）
for index, item in enumerate(s):
    print(index, item, end=" , ")
print("\n--------------")

# 3、sorted(s) 排序后遍历
for item in sorted(s):
    print(item, end=" ")