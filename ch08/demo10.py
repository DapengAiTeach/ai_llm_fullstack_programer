d1 = {"a":1,"b":2}
d2 = {"b":3,"c":4}

# 合并方法1：用 | 运算符，创建一个新字典
d3 = d1 | d2
print(d3, type(d3))

# 合并方法2：用 update() 方法
d1.update(d2)
print(d1, type(d1))

# 合并方法3：用 ** 运算符，创建一个新字典
d3 = {**d1, **d2}
print(d3, type(d3))

# 合并方法4：用 |= 运算符，就地更新
d1 |= d2
print(d1, type(d1))