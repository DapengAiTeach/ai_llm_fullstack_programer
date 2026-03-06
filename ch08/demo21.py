s1 = {1, 2}
s2 = {2, 3}

# 方法1：用 | 运算符
s3 = s1 | s2
print(s3, type(s3))

# 方法2：用 union 函数
s3 = s1.union(s2)
print(s3, type(s3))