import numpy as np

N = int(input())
A = []
for _ in range(N):
    A.append(list(map(float,input().split())))
print(f"{round(np.linalg.det(A),2)}")
