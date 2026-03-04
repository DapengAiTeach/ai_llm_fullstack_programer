# 列表创建的四种方式
# 方式1：直接创建（最常用）
arr1 = [1, 2, 3, 4, 5]
print(arr1, type(arr1))

# 方式2：使用 list() 构造函数
arr2 = list("12345")
print(arr2, type(arr2))

# 方式3：列表推导式（进阶，后面详细讲）
arr3 = [i for i in range(1, 6)]
print(arr3, type(arr3))

# 方式4：创建重复元素的列表
arr4 = [0] * 5
print(arr4, type(arr4))