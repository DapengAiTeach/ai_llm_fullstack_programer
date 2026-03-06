from collections import Counter

message = "A,B,C,B,B,C"
# 自动统计字符串中每个字符出现的次数
counts = Counter(message.split(','))
print(counts)

# 查看最常见的前2个
print(counts.most_common(2))