# Enter your code here. Read input from STDIN. Print output to STDOUT
from itertools import combinations_with_replacement

S, k = input().split()
k = int(k)
combList = combinations_with_replacement(sorted(S),k)
for comb in combList:
    print(f"{"".join(comb)}")
