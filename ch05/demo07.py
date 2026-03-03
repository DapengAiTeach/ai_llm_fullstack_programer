num = "888"

# 判断是否为某个具体对象
print(num is not int)
print(num is str)

# 判断是否为某个类的对象
print(not isinstance(num, int))
print(isinstance(num, str))