# 金字塔高度
height = 5

# 打印金字塔
for i in range(height):
    # 空格数量
    spaces = " " * (height - i - 1)
    # 星号数量
    stars = "*" * (2 * i + 1)
    # 打印空格和星号
    print(spaces + stars)