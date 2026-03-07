import copy

arr = [1,2,[3,4,[5,6]]]
arr1 = copy.deepcopy(arr)

# 修改原本
arr[2][2][0] = 100
print(arr)
print(arr1)