# Enter your code here. Read input from STDIN. Print output to STDOUT
import numpy as np
np.set_printoptions(legacy='1.13')

myarr = list(map(float,input().split()))

print(f"{np.floor(myarr)}")
print(f"{np.ceil(myarr)}")
print(f"{np.rint(myarr)}")
