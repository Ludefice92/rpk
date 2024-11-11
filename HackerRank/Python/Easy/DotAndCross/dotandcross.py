import numpy as np

N = int(input())
A=[]
B=[]
for _ in range(N):
    A.append(list(map(int,input().split())))
for _ in range(N):
    B.append(list(map(int,input().split())))
print(f"{np.matmul(np.array(A),np.array(B))}")
