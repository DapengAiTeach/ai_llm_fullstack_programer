arr = [3, 33, 2, 22, 1, 11]

# 方法1：sort() - 原地排序（修改原列表，返回None）
arr.sort(reverse=True)
print(arr)

# 方法2：sorted() - 返回新列表（不修改原列表）
arr = sorted(arr, reverse=False)
print(arr)
