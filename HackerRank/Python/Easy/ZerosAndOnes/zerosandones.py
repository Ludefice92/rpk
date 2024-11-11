# Enter your code here. Read input from STDIN. Print output to STDOUT
import numpy as np

intlist = list(map(int,input().split()))
print(f"{np.zeros(intlist,dtype=int)}")
print(f"{np.ones(intlist,dtype=int)}")
