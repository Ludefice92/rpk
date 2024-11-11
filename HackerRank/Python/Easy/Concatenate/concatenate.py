# Enter your code here. Read input from STDIN. Print output to STDOUT
import numpy as np

N, M, P = list(map(int,input().split()))
nmarr = []
mparr = []
for _ in range(N):
    nmarr.append(list(map(int,input().split())))
for _ in range(M):
    mparr.append(list(map(int,input().split())))    

print(f"{np.concatenate((nmarr,mparr),axis=0)}")
