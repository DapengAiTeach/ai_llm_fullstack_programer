# # 创建字典的5种方式
# 1、方式 1：花括号直接创建（最常用）
user_info = {"name": "张三", "age": 18, "sex": "男"}
print(user_info, type(user_info))

# 2、方式 2：使用 dict() 构造函数
user_info = dict(name="张三", age=18, sex="男")
print(user_info, type(user_info))

# 3、方式 3：从键序列创建（搭配 fromkeys）
user_info = dict.fromkeys(["name", "age", "sex"], "")
print(user_info, type(user_info))

# 4、方式 4：字典推导式（Pythonic 风格）
user_info = {key: "" for key in ["name", "age", "sex"]}
print(user_info, type(user_info))

# 5、方式 5：使用 zip 合并两个列表
user_info = dict(zip(["name", "age", "sex"], ["张三", 18, "男"]))
print(user_info, type(user_info))