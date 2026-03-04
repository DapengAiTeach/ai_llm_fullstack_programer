message = "人生苦短，我用Python"

# 找到 t 的位置，然后结束
for index, char in enumerate(message):
    if char == "t":
        print(index, char)
        break