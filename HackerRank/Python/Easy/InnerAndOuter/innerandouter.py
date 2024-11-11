import numpy as np

A = list(map(int,input().split()))
B = list(map(int,input().split()))

print(f"{np.inner(A,B)}")
print(f"{np.outer(A,B)}")
