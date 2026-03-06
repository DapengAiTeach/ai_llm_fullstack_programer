user_info = dict(name="张三", age=18, sex="男")
print(user_info)

# 常用来删除字典元素的方法有：
# 方式 1：del 语句，直接删除，无返回值
del user_info["name"]
print(user_info)

# 方式 2：pop()，删除并返回值，键不存在可设默认值
age = user_info.pop("age", "")
print(age, user_info)

# 方式 3：popitem()，删除并返回最后插入的键值对，LIFO顺序
user_info.popitem()
print(user_info)

# * 方式 4：clear()，清空字典
user_info = dict(name="张三", age=18, sex="男")
user_info.clear()
print(user_info)