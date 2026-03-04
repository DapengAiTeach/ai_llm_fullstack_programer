# 将 `[1, 2, 2, 3, 4, 4, 5]` 去重，保持原有顺序。

arr = [1, 2, 2, 3, 4, 4, 5]
unique_arr = []

# 遍历原来的数组
for i in arr:
    # 如果当前元素不在新的数组中，则添加
    if i not in unique_arr:
        unique_arr.append(i)
# 打印
print(unique_arr)