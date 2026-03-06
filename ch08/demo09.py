# 学生成绩字典{姓名：分数}
students = {"张三": 98, "李四": 90, "王五": 100}

# 按key排序
students1 = dict(sorted(students.items()))
print(students1, type(students1))

# 按value排序
students2 = dict(sorted(students.items(), key=lambda item: item[1]))
print(students2, type(students2))

# 按value降序
students3 = dict(sorted(students.items(), key=lambda item: item[1], reverse=True))
print(students3, type(students3))