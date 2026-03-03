from random import randint

# 余额
balance = randint(1, 100)
print(f"当前余额为：{balance} 元")

# 商品价格
price = 50

# 判断余额是否充足
if balance >= price:
    balance -= price
    print(f"购买成功，当前余额：{balance} 元")
else:
    print("余额不足，请充值")