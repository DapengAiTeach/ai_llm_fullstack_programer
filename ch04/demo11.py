x = 88
# bin(x)，将x转换为二进制字符串
print(bin(x))
# oct(x)，将x转换为八进制字符串
print(oct(x))
# hex(x)，将x转换为十六进制字符串
print(hex(x))
print("--" * 8)

# int(x, base)，将x转换为一个整数，x如果是字符串，可以用base指定进制
print("0b1011000", 2)
print("0o10", 8)
print("0x10", 16)
print("888")
print("--" * 8)

# float(x)，将x转换为浮点数
print(float("88.8"))

# 注意：这两个方法支持中文，使用的应该是 UTF-8 编码
# ord(x)，将字符转换为它的ASCII编码值
print(ord("a"))
print(ord("中"))
# chr(x)，将一个整数转换为Unicode字符
print(chr(97))
print(chr(20013))
