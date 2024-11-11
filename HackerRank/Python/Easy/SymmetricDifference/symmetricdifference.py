# Enter your code here. Read input from STDIN. Print output to STDOUT
M = int(input())
mInts = set(list(map(int,input().split())))
N = int(input())
nInts = set(list(map(int,input().split())))

diff1 = mInts.difference(nInts)
diff2 = nInts.difference(mInts)
diff1.update(diff2)
for i in sorted(diff1):
    print(f"{i}")
