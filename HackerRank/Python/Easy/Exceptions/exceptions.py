# Enter your code here. Read input from STDIN. Print output to STDOUT
t = int(input())
for i in range(t):
    try:
        a, b = map(int,input().split())
        print(f"{int(a/b)}")
    except ZeroDivisionError as e:
        print(f"Error Code: integer division or modulo by zero")
    except ValueError as e:
        print(f"Error Code: {e}")
