# Enter your code here. Read input from STDIN. Print output to STDOUT
from itertools import product

listver = []
setver = set(listver)
K, M = map(int, input().split())

for i in range(K):
    elements = list(map(int, input().split()))
    for val in range(1,len(elements)):
        setver.add(elements[val])
    listver.append(list(setver))
    setver.clear()
    
maxval = 0
for combination in product(*listver):
    curval = sum(x**2 for x in combination) % M
    maxval = max(maxval, curval)

print(maxval)
