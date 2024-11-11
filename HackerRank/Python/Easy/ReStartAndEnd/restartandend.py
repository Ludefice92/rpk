# Enter your code here. Read input from STDIN. Print output to STDOUT
S = input()
k = input()

substrFound = False

for i in range(len(S) - len(k) + 1):
    if S[i:i+len(k)] == k:
        substrFound = True
        print((i,i+len(k)-1))
        
if not substrFound:
    print((-1,-1))
