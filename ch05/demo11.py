from random import randint

# 月份
month = randint(1, 12)
print(f"当前月份为：{month} 月")

# 改为使用 match case 语句
match month:
    case 3 | 4 | 5:
        print("当前是春季")
    case 6 | 7 | 8:
        print("当前是夏季")
    case 9 | 10 | 11:
        print("当前是秋季")
    case 12 | 1 | 2:
        print("当前是冬季")
    case _:  # 匹配任意值，相当于 else
        print("输入的月份有误")
