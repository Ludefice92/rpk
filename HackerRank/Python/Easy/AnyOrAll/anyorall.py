# Enter your code here. Read input from STDIN. Print output to STDOUT
N = int(input())
nList = list(map(int,input().split()))

if all(num > 0 for num in nList):
    if(any(str(num) == str(num)[::-1] for num in nList)):
        print("True")
    else:
        print("False")
else:
    print("False")
#for curNum in nList:
 #   if curNum
