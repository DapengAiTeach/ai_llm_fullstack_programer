import copy

tmp_arr = [8, 88, 888]
arr = [1, 2, tmp_arr]

# 列表浅拷贝的四种方法
# 方法1：切片
arr1 = arr[:]
print(arr1)

# 方法2：list()构造函数
arr2 = list(arr)
print(arr2)

# 方法3：copy.copy方法
arr3 = copy.copy(arr)
print(arr3)

# 方法4：list.copy()方法（Python 3.3+）
arr4 = arr.copy()
print(arr4)

print("-"*33)

# 浅拷贝会受到内置元素的影响，这种影响非常糟糕，会带来极大的安全风险
tmp_arr.append(888888)
# 我明明没有修改 arr1 arr2 arr3 arr4，却全部被自动修改了
print(arr1)
print(arr2)
print(arr3)
print(arr4)