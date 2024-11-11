# Enter your code here. Read input from STDIN. Print output to STDOUT
import numpy as np

if __name__ == '__main__':
    n, m = map(int,input().split())
    arr2d = np.zeros((n,m), dtype=int)
    for i in range(n):
        arrvals = list(map(int,input().split()))
        arr2d[i] = arrvals
            
    arrSum = np.sum(arr2d,axis=0)
    arrProduct = np.prod(arrSum)
    
    print(f"{arrProduct}")
