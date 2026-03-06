class_a = {"张三", "李四", "王五", "赵六", "孙七"}
class_b = {"李四", "周八", "吴九", "王五", "郑十"}

# 1. 找出两个班级的共同学生（交集）
print(class_a.intersection(class_b))

# 2. 找出只在 A 班的学生（差集）
print(class_a.difference(class_b))

# 3. 找出只在 B 班的学生（差集）
print(class_b.difference(class_a))

# 4. 找出所有不重复的学生（并集）
print(class_a.union(class_b))

# 5. 找出恰好只在一个班级的学生（对称差集）
print(class_a.symmetric_difference(class_b))

# 6. 判断 A 班是否是 B 班的子集
print(class_a.issubset(class_b))
