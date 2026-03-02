from decimal import Decimal

# 张三的钱包余额
money = Decimal("0.1")
print(f"张三的钱包余额为：{money} 元")

# 张三做任务，赚了0.2元
money += Decimal("0.2")
print(f"张三赚了0.2元，余额为：{money} 元")


