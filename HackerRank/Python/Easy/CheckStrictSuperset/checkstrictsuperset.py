# Enter your code here. Read input from STDIN. Print output to STDOUT
elemA = set(map(int,input().split()))
n = int(input())
numSuperset = 0
for _ in range(n):
    curSet = set(map(int,input().split()))
    if elemA.issuperset(curSet): numSuperset+=1
if numSuperset == n:
    print("True")
else:
    print("False")
