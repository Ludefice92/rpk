# Enter your code here. Read input from STDIN. Print output to STDOUT
import numpy as np
N, M = list(map(int,input().split()))
twodimarray = []
for _ in range(N):
    twodimarray.append(list(map(int,input().split())))
minax1 = np.min(twodimarray,axis=1)
print(f"{np.max(minax1)}")
