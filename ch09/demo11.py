def add(a, b, *args, c=10, d=20, **kwargs):
    return a + b + c + d + sum(args) + sum(kwargs.values())

print(add(1, 2))
print(add(1, 2, 3, 4, 5))
print(add(1, 2, 3, 4, 5, c=100, d=200))

