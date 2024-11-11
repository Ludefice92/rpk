# Enter your code here. Read input from STDIN. Print output to STDOUT
from collections import OrderedDict

N = int(input())
ordDict = OrderedDict()
for _ in range(N):
    *item_name, net_price = input().split()
    item_name = " ".join(item_name)
    net_price = int(net_price)
    if item_name in ordDict:
        ordDict[item_name] += net_price
    else:
        ordDict[item_name] = net_price
    
for item_name, net_price in ordDict.items():
    print(f"{item_name} {net_price}")
