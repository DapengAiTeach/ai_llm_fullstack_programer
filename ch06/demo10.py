# 打印 1-100 中所有能被 7 整除但不能被 5 整除的数。
for i in range(1, 101):
    if i % 7 == 0 and i % 5 != 0:
        print(i)
