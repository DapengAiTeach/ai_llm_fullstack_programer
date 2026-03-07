def show_info(name, age):
    print("用户名：", name)
    print("年龄：", age)
    print("--------------")

# 正确的调用
show_info("张三", 18)
# 位置错误
show_info(18, "张三")