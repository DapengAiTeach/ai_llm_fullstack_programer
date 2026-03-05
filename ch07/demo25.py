# 用户信息，是嵌套的
user_info = "张三", ("男", 18)

# 如何解包？
# 这种方式就叫做嵌套解包
name, (sex, age) = user_info
print('用户名：%s，性别：%s，年龄：%d' % (name, sex, age))
