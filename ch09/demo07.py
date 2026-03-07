def show_info(name, age):
    print("姓名：", name)
    print("年龄：", age)


# 关键字参数，可以不在意顺序
# 下面的结果是一样的
show_info(age=18, name="张三")
show_info(name="张三", age=18)
# 位置参数与关键字参数混用
show_info("张三", age=18)
