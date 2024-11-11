# Enter your code here. Read input from STDIN. Print output to STDOUT
from collections import defaultdict

defdict = defaultdict(list)

n, m = map(int,input().split())
A = [input().strip() for _ in range(n)]
B = [input().strip() for _ in range(m)]

E = list(enumerate(A))

for _ in E:
    defdict[_[1]].append(_[0]+1)
    
for b in B:
    if b in A:
        print(*defdict[b])
    else:
        print(-1)    
