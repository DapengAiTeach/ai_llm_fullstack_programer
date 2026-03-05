# 此时 \t 是制表符，会有空格
message1 = "a\tb\tc"
print(message1)

# 使用r原始字符串，\t 就是 \t，不是空格
message2 = r"a\tb\tc"
print(message2)