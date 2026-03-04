# 统计字符串 "Hello World 123" 中字母、数字、空格和其他字符的数量。
message = "Hello World 123"

# 字母数量
count_letter = 0
# 数字数量
count_digit = 0
# 空格数量
count_space = 0
# 其他数量
count_other = 0

# 遍历字符串进行统计
for ch in message:
    if ch.isalpha():
        count_letter += 1
    elif ch.isdigit():
        count_digit += 1
    elif ch.isspace():
        count_space += 1
    else:
        count_other += 1

# 打印统计结果
print("字母数量：", count_letter)
print("数字数量：", count_digit)
print("空格数量：", count_space)
print("其他数量：", count_other)