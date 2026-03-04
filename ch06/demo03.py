# 用法1：range(stop) - 从0开始，到stop-1结束
for i in range(3):
    print(i, end=" ")
print("\n---------------")

# 用法2：range(start, stop) - 从start开始，到stop-1结束
for i in range(1, 4):
    print(i, end=" ")
print("\n---------------")

# 用法3：range(start, stop, step) - 带步长（间隔）
for i in range(1, 6, 2):
    print(i, end=" ")
print("\n---------------")

# 倒着数：步长为负数
for i in range(5, 0, -1):
    print(i, end=" ")
print("\n---------------")
