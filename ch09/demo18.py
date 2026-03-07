arr = [8, 88, 888]

# 借助lambda+map实现列表元素的批量操作
newarr = list(map(lambda item: item * 2, arr))
print(newarr)