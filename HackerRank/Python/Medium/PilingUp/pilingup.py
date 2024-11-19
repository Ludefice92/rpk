# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys

t = int(input())
for _ in range(t):
    n = int(input())
    blocks = list(map(int,input().split()))
    curblock = 293583905809523 #arbitrarily large size to start
    canvertstack = True
    while n>0:
        if blocks[0] > blocks[len(blocks)-1]:
            if blocks[0] <= curblock:
                curblock = blocks[0]
                blocks.pop(0)
            else:
                canvertstack = False
                break
        else:
            if blocks[len(blocks)-1] <= curblock:
                curblock = blocks[len(blocks)-1]
                blocks.pop(len(blocks)-1)
            else:
                canvertstack = False
                break
        n -= 1
    if canvertstack: print("Yes")
    else: print("No")
