# Enter your code here. Read input from STDIN. Print output to STDOUT
from collections import deque

N = int(input())
deq = deque()
for _ in range(N):
    instr = list(input().split())
    if instr[0] == "append":
        deq.append(instr[1])
    elif instr[0] == "appendleft":
        deq.appendleft(instr[1])
    elif instr[0] == "pop":
        deq.pop()
    elif instr[0] == "popleft":
        deq.popleft()

for elem in deq:
    print(f"{elem} ",end='')
