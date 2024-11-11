cube = lambda x: x**3

def fibonacci(n):
    # return a list of fibonacci numbers
    fib = [0]
    a = 0
    b = 1
    if n == 0:
        return []
    else:
        for i in range(1, n):
            a, b = b, a + b
            fib.append(a)
    return fib

if __name__ == '__main__':
    n = int(input())
    print(list(map(cube, fibonacci(n))))