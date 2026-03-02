# 给 AI 提示词，问 AI大模型是什么
message = "你是一个专业的Python工程师，请你给小白讲解：AI大模型是什么？"

# 编码
encoded_message = message.encode("utf-8")
print(encoded_message)

# 解码
decoded_message = encoded_message.decode("utf-8")
print(decoded_message)
