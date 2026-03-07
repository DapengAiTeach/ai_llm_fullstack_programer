def add(**kwargs):
    print(type(kwargs)) # <class 'dict'>
    return sum(kwargs.values())

print(add(a=1, b=2, c=3))