from collections import Counter

# Enter your code here. Read input from STDIN. Print output to STDOUT
x = int(input())
shoeSizes = list(map(int,input().split()))
n = int(input())
moneyEarned = 0
for cust in range(n):
    size, price = map(int,input().split())
    for curSize in range(x):
        if size == shoeSizes[curSize]: 
            moneyEarned += price
            del(shoeSizes[curSize])
            x -=1
            break
            
print(f"{moneyEarned}")
        
