import numpy as np

N, M = map(int,input().split())
mat = []
for _ in range(N):
    mat.append(list(map(int,input().split())))
npmat = np.array(mat)
print(f"{np.transpose(npmat)}")
print(f"{npmat.flatten()}")
