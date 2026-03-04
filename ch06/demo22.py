# 生成1-10的平方数列表
arr = []
for i in range(1, 11):
    arr.append(i ** 2)
print(arr)

# 用列表推导式一次性搞定
arr2 = [i ** 2 for i in range(1, 11)]
print(arr2)

# 带条件的推导式，只保留偶数
arr3 = [i ** 2 for i in range(1, 11) if i % 2 == 0]
print(arr3)

# 嵌套推导式，适合二维列表
arr4 = [[i + j for i in range(1, 4)] for j in range(1, 4)]
print(arr4)