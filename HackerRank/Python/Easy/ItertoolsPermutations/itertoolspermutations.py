# Enter your code here. Read input from STDIN. Print output to STDOUT
from itertools import permutations

S, k = input().split()
k = int(k)

permList = list(permutations(S,k))

for curPerm in sorted(permList):
    permStr = ""
    for i in range(k):
        permStr += curPerm[i]
    print(f"{permStr}")
