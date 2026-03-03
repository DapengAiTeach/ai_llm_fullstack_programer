# 第1周有2只兔子，此后每周兔子的数量都增加上周数量的2倍，且期间没有兔子死亡，求第10周共有多少只兔子。
week = 1
rabbit = 2
while week < 10:
    print(f"第{week:02d}周有{rabbit}只兔子")
    rabbit += 2 * rabbit
    week += 1
else: # 如果while循环正常结束，则走这个语句
    print(f"第{week:02d}周有{rabbit}只兔子")
