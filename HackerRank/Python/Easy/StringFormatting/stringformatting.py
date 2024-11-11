def print_formatted(number):
    # your code goes here
    printWidth = len(bin(number))-2 #-2 excludes bin prefix
    for i in range(1,number+1):
        print(f"{i:>{printWidth}d} {oct(i)[2:]:>{printWidth}} {hex(i)[2:].upper():>{printWidth}} {bin(i)[2:]:>{printWidth}}")

if __name__ == '__main__':
    n = int(input())
    print_formatted(n)