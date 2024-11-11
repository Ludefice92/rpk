import numpy as np
# Enter your code here. Read input from STDIN. Print output to STDOUT
polyList = list(map(float,input().split()))
x = int(input())

print(f"{np.polyval(polyList,x)}")
