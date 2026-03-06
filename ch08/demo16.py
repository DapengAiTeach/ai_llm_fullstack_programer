# 基本集合推导式
s = {x for x in range(1, 10)}
print(s, type(s))

# 带条件的推导式，只保留偶数
s2 = {x for x in range(1, 10) if x % 2 == 0}
print(s2, type(s2))