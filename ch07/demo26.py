def get_user_info():
    """获取用户信息"""
    # 本质上返回的是元组
    return "张三", "男", 33

# 接收
user_info = get_user_info()
print(user_info, type(user_info)) # ('张三', '男', 33) <class 'tuple'>

# 所以，我们可以直接解包接收
name, sex, age = get_user_info()
print('用户名：%s，性别：%s，年龄：%d' % (name, sex, age))