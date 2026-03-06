# 1、issubset()：A 是否是 B 的子集（A ⊆ B）
s1 = {1, 2}
s2 = {1, 2, 3}
print(s1.issubset(s2))

# 2、issuperset()：B 是否是 A 的超集（B ⊇ A）
print(s2.issuperset(s1))

# 3、isdisjoint()：A 和 B 是否不相交（没有共同元素）
s1 = {1, 2}
s2 = {3, 4}
print(s1.isdisjoint(s2))