# 去除字符串左右两边的空格
message = "   Hello World 123   "
message = message.strip()
print(message, end="---\n")

# 去除字符串左边的空格
message = "   Hello World 123   "
message = message.lstrip()
print(message, end="---\n")

# 去除字符串右边的空格
message = "   Hello World 123   "
message = message.rstrip()
print(message, end="---\n")
