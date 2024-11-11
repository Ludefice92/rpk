# Enter your code here. Read input from STDIN. Print output to STDOUT
K = int(input())
roomNums = sorted(list(map(int,input().split())))

for i in range(0,len(roomNums),K):
    if i < len(roomNums)-K:
        if roomNums[i] != roomNums[i+K-1]:
            print(f"{roomNums[i]}")
            break
    else:
        print(f"{roomNums[i]}")
