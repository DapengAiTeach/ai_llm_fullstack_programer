year = 2000
if (year % 400 == 0) or (year % 100 != 0 and year % 4 == 0):
    print("闰年")
else:
    print("平年")