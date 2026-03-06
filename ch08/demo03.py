user_info = {"name": "张三"}

# 新增age
user_info["age"] = 18
print(user_info)

# 如果key已存在则修改
# 修改 name
user_info["name"] = "李四"
print(user_info)

# 批量修改或新增，修改age，新增gender
user_info.update({"age": 19, "gender": "男"})
print(user_info)
