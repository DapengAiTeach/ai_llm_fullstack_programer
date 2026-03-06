msg = "hello world"

def char_frequency(text):
    """
    统计字符串中每个字符出现的次数，返回字典。
    忽略空格，不区分大小写。
    """
    result = {}
    # 先转换为小写
    text = text.lower()
    # 遍历每个字符
    for char in text:
        # 忽略空格
        if char == " ":
            continue
        # 判断字符是否已经出现过，进行统计
        if char in result:
            result[char] += 1
        else:
            result[char] = 1
    return  result

# 调用函数
print(char_frequency(msg))