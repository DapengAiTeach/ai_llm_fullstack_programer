# 1、方式1：使用小括号（最常用）
t1 = (1, 2, 3)
print(t1, type(t1))

# 2、方式2：省略小括号（Python允许）
t2 = 1, 2, 3
print(t2, type(t2))

# 3、方式3：使用tuple()函数
t3 = tuple([1, 2, 3])
print(t3, type(t3))

# 4、方式4：创建空元组
t4 =  ()
print(t4, type(t4))

# 5、方式5：创建单元素元组（注意逗号！）
t5 = 1,
print(t5, type(t5))
t6 = (1,)
print(t6, type(t6))