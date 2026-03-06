import re


def text_similarity(text1, text2):
    """
    计算两段文本的杰卡德相似度
    J(A,B) = |A ∩ B| / |A ∪ B|
    """

    def preprocess(text):
        """预处理：转小写、去标点、分词、转集合"""
        # 转小写
        text = text.lower()
        # 去除标点（保留字母、数字、空格）
        text = re.sub(r'[^a-z0-9\s]', '', text)
        # 分词并转集合
        words = set(text.split())
        return words

    # 获取两个单词集合
    set1 = preprocess(text1)
    set2 = preprocess(text2)

    # 处理空集合情况
    if not set1 and not set2:
        return 1.0  # 两个都空，认为完全相同
    if not set1 or not set2:
        return 0.0  # 一个空一个非空，完全不同

    # 计算交集和并集
    intersection = set1 & set2
    union = set1 | set2

    # 计算杰卡德相似度
    similarity = len(intersection) / len(union)

    return similarity


# 测试
text1 = "Python is great and Python is easy"
text2 = "Python is powerful and easy to learn"

similarity = text_similarity(text1, text2)
print(f"\n相似度: {similarity:.2%}")