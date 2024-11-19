# Enter your code here. Read input from STDIN. Print output to STDOUT
import itertools

N = int(input())
charlist = input().split()
K = int(input())

if 'a' not in charlist:
    print(0)
else:
    numOfA = 0
    charlistCombinations = list(itertools.combinations(charlist, K))
    for comb in charlistCombinations:
        if 'a' in comb:
           numOfA+=1
    if numOfA==0: print(0)
    else: print(f"{numOfA/len(charlistCombinations)}")
