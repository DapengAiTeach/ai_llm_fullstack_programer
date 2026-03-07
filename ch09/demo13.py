# 声明全局变量
count = 0

def add():
    # 声明要修改全局变量
    global count
    # 修改全局变量
    count+=1

for i in range(3):
    add()
    print(count)

