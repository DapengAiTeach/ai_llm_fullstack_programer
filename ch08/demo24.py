s1 = {1, 2}
s2 = {2, 3}

# 对称差集：在s1或s2中，但不同时在s1和s2中的元素
# 方法1：用 ^ 运算符
s3 = s1 ^ s2
print(s3, type(s3))

# 方法2：通过 symmetric_difference() 方法
s3 = s1.symmetric_difference(s2)
print(s3, type(s3))