# Enter your code here. Read input from STDIN. Print output to STDOUT
n, m = map(int,input().split())
arr = list(map(int,input().split()))
A = set(map(int,input().split()))
B = set(map(int,input().split()))
happiness = 0
for elem in arr:
    if elem in A: happiness += 1
    if elem in B: happiness -= 1
print(happiness)
