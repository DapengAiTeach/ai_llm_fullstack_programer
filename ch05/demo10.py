from random import randint

# 月份
month = randint(1, 12)
print(f"当前月份为：{month} 月")

# 判断季节
if 3 <= month <= 5:
    print("当前是春季")
elif 6 <= month <= 8:
    print("当前是夏季")
elif 9 <= month <= 11:
    print("当前是秋季")
elif month == 12 or month <= 2:
    print("当前是冬季")
else:
    print("输入的月份有误")
