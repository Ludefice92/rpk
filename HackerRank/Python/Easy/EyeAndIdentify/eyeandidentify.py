import numpy as np
np.set_printoptions(legacy='1.13')

N, M = list(map(int,input().split()))
print(f"{np.eye(N,M)}")
