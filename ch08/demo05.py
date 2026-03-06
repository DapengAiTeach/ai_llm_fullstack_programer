user_info = {"name": "张三", "age": 18, "sex": "男"}

# 常用的遍历字典的方式有：
# 方式1：遍历所有key
for key in user_info:
    print(key, user_info[key])
print("-" * 33)

# 方式2：遍历所有的value
for value in user_info.values():
    print(value)
print("-" * 33)

# 方式3：同时遍历key和value
for key, value in user_info.items():
    print(key, value)
