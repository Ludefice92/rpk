# Enter your code here. Read input from STDIN. Print output to STDOUT
n = int(input())
rollN = list(map(int,input().split()))
b = int(input())
rollB = list(map(int,input().split()))

print(f"{len(set(rollN).symmetric_difference(rollB))}")
