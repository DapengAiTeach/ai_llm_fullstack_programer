students = [
    {"name": "张三", "scores": {"语文": 85, "数学": 90, "英语": 78}},
    {"name": "李四", "scores": {"语文": 92, "数学": 88, "英语": 95}},
    {"name": "王五", "scores": {"语文": 78, "数学": 85, "英语": 80}},
]

# 1. 计算每个学生的平均分
students1 = [
    {
        "name": student["name"],
        "avg_score": sum(student["scores"].values()) / len(student["scores"]),
    }
    for student in students
]
print(students1)

# 2. 找出平均分最高的学生
students2 = sorted(students1, key=lambda item: item["avg_score"], reverse=True)
print(students2[0])

# 3. 按平均分从高到低排序输出
for student in students2:
    print(f"{student['name']}：{student['avg_score']:.2f}")

