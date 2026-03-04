# 列表删除元素的四种方法
arr = [8,88,888,8888,88888,888888]

# 方法1：remove() - 删除第一个匹配的值
arr.remove(888)
print(arr)

# 方法2：pop() - 按索引删除（默认删最后一个），并返回该值
arr.pop()
print(arr)

# 方法3：del 语句 - 按索引或切片删除
del arr[2]
print(arr)

# 方法4：clear() - 清空整个列表
arr.clear()
print(arr)