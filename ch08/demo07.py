from collections import defaultdict

# 水果字典
fruits = {}
# 这段代码会报错
# 因为普通字典不会初始化值
# fruits["apple"].append("苹果")

# 而下面这段代码不会报错
# 是因为defaultdict会自动初始化值
fruits2 = defaultdict(list)
fruits2["apple"].append("苹果")
print(fruits2)