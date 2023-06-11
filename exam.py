def fibonacci(n):
    if n <= 0:
        return "n musbat son bo'lishi kerak"
    elif n == 1:
        return 1
    elif n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


fibonacci_son = [0, 1]
while fibonacci_son[-1] + fibonacci_son[-2] <= 150:
    fibonacci_son.append(fibonacci_son[-1] + fibonacci_son[-2])

print(fibonacci_son)

print(fibonacci(7))
