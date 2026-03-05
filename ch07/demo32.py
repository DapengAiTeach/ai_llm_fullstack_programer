import math


def distance(point1, point2):
    """
    求两个点的距离
    :param point1: 点1，(x1, y1)
    :param point2: 点2，(x2, y2)
    :return: 距离
    """
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# 定义两个点
point1 = (1, 1)
point2 = (4, 5)
print("两个点的距离是：", distance(point1, point2))
