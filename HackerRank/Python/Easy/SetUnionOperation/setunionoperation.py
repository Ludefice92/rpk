# Enter your code here. Read input from STDIN. Print output to STDOUT
n = int(input())
rollN = list(map(int,input().split()))
b = int(input())
rollB = list(map(int,input().split()))

unionNandB = set(rollN).union(rollB)
print(f"{len(unionNandB)}")
