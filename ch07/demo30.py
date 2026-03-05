# 定义一个元组
tarr = 8,88,888
print(tarr)

# 转换为列表
arr = list(tarr)
print(arr, type( arr))

# 可以追加数据了
arr.append(8888)

# 转换回元组
tarr = tuple(arr)
print(tarr, type(tarr))