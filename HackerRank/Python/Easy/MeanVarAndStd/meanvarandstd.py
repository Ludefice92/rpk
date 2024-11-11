# Enter your code here. Read input from STDIN. Print output to STDOUT
import numpy as np

N, M = list(map(int,input().split()))
arr = []
for _ in range(N):
    arr.append(list(map(int,input().split())))
print(f"{np.mean(arr,axis=1)}")
print(f"{np.var(arr,axis=0)}")
print(round(np.std(arr, axis = None), 11))
