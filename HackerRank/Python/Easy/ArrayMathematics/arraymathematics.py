import numpy as np

N, M = map(int,input().split())
arrA = []
arrB = []
#get arrA
for _ in range(N):
    arrA.append(list(map(int,input().split())))
#get arrB
for _ in range(N):
    arrB.append(list(map(int,input().split())))
print(f"{np.add(arrA,arrB)}")
print(f"{np.subtract(arrA,arrB)}")
print(f"{np.multiply(arrA,arrB)}")
print(f"{np.floor_divide(arrA,arrB)}")
print(f"{np.mod(arrA,arrB)}")
print(f"{np.power(arrA,arrB)}")
