def convert_temperature(value, from_scale, to_scale):
    """
    温度转换器
    :param value: 温度的值
    :param from_scale: 只能是 "C" 或 "F"
    :param to_scale: 只能是 "C" 或 "F"
    :return: 转换以后的值
    """
    result = 0.0
    if from_scale == "C" and to_scale == "F":
        result = value * 9 / 5 + 32
    elif from_scale == "F" and to_scale == "C":
        result = (value - 32) * 5 / 9
    elif from_scale == to_scale:
        result = value
    else:
        return "Error: 无效的温标"
    return round(result, 2)


# 测试用例
print(convert_temperature(0, "C", "F"))  # 32.0
print(convert_temperature(100, "C", "F"))  # 212.0
print(convert_temperature(32, "F", "C"))  # 0.0
print(convert_temperature(98.6, "F", "C"))  # 37.0
print(convert_temperature(25, "C", "C"))  # 25.0
print(convert_temperature(25, "C", "K"))  # Error: 无效的温标
