# Enter your code here. Read input from STDIN. Print output to STDOUT
numElemA = int(input())
elemA = set(map(int,input().split()))
numSets = int(input())

for _ in range(numSets):
    instr = input().split()
    elemB = set(map(int,input().split()))
    
    if "intersection_update" in instr:
        elemA.intersection_update(elemB)
    elif "symmetric_difference_update" in instr:
        elemA.symmetric_difference_update(elemB)
    elif "difference_update" in instr:
        elemA.difference_update(elemB)
    elif "update" in instr:
        elemA.update(elemB)
print(f"{sum(elemA)}")
