# Enter your code here. Read input from STDIN. Print output to STDOUT
n = int(input())
rollN = set(map(int,input().split()))
N = int(input())
curInstr = []
for i in range(N):
    curInstr = input().split()
    if curInstr[0] == "pop":
        if rollN:
            rollN.pop()
    elif curInstr[0] == "remove":
        curVal = int(curInstr[1])
        if curVal in rollN:
            rollN.remove(curVal)
    elif curInstr[0] == "discard":
        rollN.discard(int(curInstr[1]))

print(f"{sum(rollN)}")
