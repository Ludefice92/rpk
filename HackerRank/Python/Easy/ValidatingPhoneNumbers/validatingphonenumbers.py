# Enter your code here. Read input from STDIN. Print output to STDOUT
N = int(input())
for _ in range(N):
    curPhoneNumber = input()
    curPhoneNumber.strip()
    valid = True
    if curPhoneNumber[0].isdigit() and (len(curPhoneNumber) != 10 or (int(curPhoneNumber[0]) < 7 or int(curPhoneNumber[0]) > 9)):
        print("NO")
    else:
        for i in range(len(curPhoneNumber)):
            if not curPhoneNumber[i].isdigit():
                print("NO")
                valid = False
                break
        if valid: print("YES")
