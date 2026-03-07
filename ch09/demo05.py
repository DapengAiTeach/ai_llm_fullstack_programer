def calc_area(width, height):
    """
    计算矩形的面积
    """
    # 边界条件，宽或高为0时，面积为0
    if not width or not height:
        # return 会立即结束函数并返回
        return 0.0

    return width * height


print(calc_area(5, 3))
