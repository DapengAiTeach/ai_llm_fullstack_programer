# 元组存储MySQL连接信息
db_config = ("localhost", 3306, "root", "root", "python")
host, port, user, password, database = db_config
print("主机：", host)
print("端口：", port)
print("用户：", user)
print("密码：", password)
print("数据库：", database)
