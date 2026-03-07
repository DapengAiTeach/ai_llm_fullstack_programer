def add(count=0):
    # 通过参数接收变量
    # 然后对变量修改，再返回
    return count+1

# 通过这种方式来避免使用全局变量
count = 0
for i in range(3):
    count = add(count)
    print(count)