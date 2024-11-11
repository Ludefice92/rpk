# Enter your code here. Read input from STDIN. Print output to STDOUT
from itertools import combinations

s,k = list(input().split())
s = sorted(s)
k = int(k)

for i in range(1,k+1):
    for comb in combinations(s,i):        
        print(''.join(comb))
