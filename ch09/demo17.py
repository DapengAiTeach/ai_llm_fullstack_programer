# 学生分数列表
students = [("张三", 98), ("李四", 90), ("王五", 100)]
# 按照分数降序
students.sort(key=lambda item: item[1], reverse=True)
print(students)