# 循环打印1-9
for i in range(1, 10):
    # end参数，默认值是 \n 换行
    # 如果想要不换行，就需要重置这个参数
    # flush 参数，默认值是 False
    # 作用是刷新缓冲区，将数据写入到终端
    print(i, end="", flush=True)
