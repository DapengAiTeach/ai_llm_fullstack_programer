from collections import namedtuple

# 定义一个namedtuple
Person = namedtuple('Person', ['name', 'age', 'sex'])

# 创建一个Person对象
p1 = Person('张三', 18, '男')

# 访问属性
print("姓名：", p1.name)
print("年龄：", p1.age)
print("性别：", p1.sex)

# 依旧可以通过索引访问
print("姓名：", p1[0], "年龄：", p1[1], "性别：", p1[2])

# namedtuple对象是不可变对象
# 下面的代码会报错
# p1.name = '张三丰'
# print("修改后的姓名：", p1.name)