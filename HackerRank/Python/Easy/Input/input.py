# Enter your code here. Read input from STDIN. Print output to STDOUT
x, k = list(map(int,input().split()))

poly = input()
pOfX = eval(poly)
if pOfX == k:
    print("True")
else:
    print("False")
