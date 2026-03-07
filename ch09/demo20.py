# 通过递归函数求阶乘
def factorial(n):
    if n == 1:
        print(1)
        return 1
    else:
        print(n, "*", end=" ")
    return n * factorial(n - 1)

result = factorial(5)
print("\n-------------")
print(result)