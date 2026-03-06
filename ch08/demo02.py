user_info = dict(name="张三", age=18, sex="男")

# 通过[]访问
username = user_info["name"]
print("用户名：",  username)

# 通过get()访问
username = user_info.get("name")
print("用户名：",  username)