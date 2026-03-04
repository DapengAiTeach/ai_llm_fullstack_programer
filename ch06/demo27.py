# 找出列表 `[23, 56, 12, 89, 34]` 中的最大值和对应的索引。

arr = [23, 56, 12, 89, 34]

# 假设第1个元素是最大值
max_index = 0
max_value = arr[max_index]

# 遍历找最大值
for i in range(1, len(arr)):
    if arr[i] > max_value:
        max_index = i
        max_value = arr[i]

# 打印结果
print("最大值：", max_value)
print("索引：", max_index)