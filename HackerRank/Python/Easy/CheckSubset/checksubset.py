# Enter your code here. Read input from STDIN. Print output to STDOUT
T = int(input())

for _ in range(T):
    numElemA = int(input())
    elemA = set(map(int,input().split()))
    numElemB = int(input())
    elemB = set(map(int,input().split()))
    found = False

    if elemA.issubset(elemB):
        print("True")
        continue
        
    print("False")
