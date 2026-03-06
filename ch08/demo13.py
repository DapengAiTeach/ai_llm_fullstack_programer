from collections import Counter


def word_frequency(text, top_n=5):
    """
    统计英文文本中单词出现的频率，返回出现次数最多的前 N 个单词及其次数
    :param text: 英文文本
    :param top_n: 前n个
    :return: 出现次数最多的前 N 个单词及其次数
    """
    # 1. 忽略大小写
    text = text.lower()

    # 2. 去除标点符号（只保留字母和数字）
    text = "".join(ch for ch in text if ch.isalnum() or ch == " ")
    counter = Counter(text.split())

    # 3. 返回列表，格式为 `[('word', count), ...]`
    return counter.most_common(top_n)


text = "Hello, world! Hello everyone. Welcome to the world of Python. Python is great, and the world is beautiful."
top_3 = word_frequency(text, 3)
print(top_3)
