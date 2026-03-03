# 男人相亲要求：1、性别女 2、年龄18-25 3、月收入50W-80W
# 条件1
gender = '女'
# 条件2
age = 18
# 条件
income = 50

# 三个条件同时满足，才比较满意
if gender == '女' and 18 <= age <= 25 and 50 <= income <= 80:
    print("相亲成功")
else:
    print("相亲失败")
