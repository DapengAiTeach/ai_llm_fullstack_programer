import copy

tmp_arr = [8, 88, 888]
arr = [1, 2, tmp_arr]

# 深拷贝
arr2 = copy.deepcopy(arr)
print(arr2)

# 深拷贝能够解决浅拷贝的安全风险
tmp_arr.append(888888)
print(arr2)
