# 学生的成绩
scores = (85, 92, 78, 65, 55, 88, 92, 70)

# 求最高分，最低分，平均分
max_score, min_score, avg_score = max(scores), min(scores), sum(scores) / len(scores)
print(f"最高分：{max_score}\t最低分：{min_score}\t平均分：{avg_score}")

# 以及大于90分以上的人数
count = sum(score > 90 for score in scores)
print(f"高于90分的人数：{count}")
