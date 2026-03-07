arr = list(range(8))
print(arr)

# 借助lambda+filter实现列表元素的筛选
newarr = list(filter(lambda item: item % 2 == 0, arr))
print(newarr)