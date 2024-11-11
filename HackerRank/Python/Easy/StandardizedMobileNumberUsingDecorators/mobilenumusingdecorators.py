def wrapper(f):
    def fun(l):
        # complete the function
        numbers = []
        for num in l:
            if num.startswith('0'): num = num[1:]
            if num.startswith('91') and len(num)!=10: num = num[2:]
            if num.startswith('+91') and len(num)!=10: num = num[3:]
            numbers.append(f"+91 {num[-10:-5]} {num[-5:]}")
        f(numbers)
    return fun

@wrapper
def sort_phone(l):
    print(*sorted(l), sep='\n')

if __name__ == '__main__':
    l = [input() for _ in range(int(input()))]
    sort_phone(l) 


