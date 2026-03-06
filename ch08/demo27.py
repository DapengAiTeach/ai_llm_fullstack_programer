def unique_ordered(seq):
    """
    去除列表中的重复元素，保持原有顺序
    """
    # 通过字典去重
    seen = {}
    # 保持顺序的列表
    result = []
    # 遍历集合
    for item in seq:
        if item not in seen:
            seen[item] = True
            result.append(item)
    return result


# 测试
data = [3, 1, 2, 3, 4, 1, 5, 2]
result = unique_ordered(data)
print(result)  # [3, 1, 2, 4, 5]
