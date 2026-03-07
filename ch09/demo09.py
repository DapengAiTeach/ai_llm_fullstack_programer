def add(*args):
    """任意多个数相加"""
    # 本质是一个元组
    print(args, type(args)) # <class 'tuple'>
    return sum(args)


print(add(1, 2, 3, 4, 5))
