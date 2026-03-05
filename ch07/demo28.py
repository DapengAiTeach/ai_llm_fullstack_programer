# 学生信息：[(姓名，年龄，成绩)]
students = [
    ("张三", 18, 80),
    ("李四", 19, 90),
    ("王五", 20, 100),
    ("赵六", 21, 95),
    ("孙七", 22, 85)
]
# 查看所有学生信息
for student in students:
    name, age, score = student
    print(f"姓名：{name}\t年龄：{age}\t分数：{score}")
