# Enter your code here. Read input from STDIN. Print output to STDOUT
N = int(input())
s = set()
for i in range(N):
    s.add(input())
print(f"{len(s)}")
