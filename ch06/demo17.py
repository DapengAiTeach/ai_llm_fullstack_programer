# 列表添加元素的三种方式
arr = [8, 88, 888]

# 方法1：append() - 在末尾添加一个元素
arr.append(8888)
print(arr)

# 方法2：extend() - 在末尾添加多个元素（合并列表）
arr.extend([88888, 888888])
print(arr)

# 方法3：insert() - 在指定位置插入
arr.insert(2,8.88)
print(arr)