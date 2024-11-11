# Enter your code here. Read input from STDIN. Print output to STDOUT
T = int(input())

for _ in range(T):
    curVal = input()
    dotCount = 0
    invalidReached = False
    for curChar in curVal:
        if (not curChar.isdigit()) and curChar != '.' and curChar != '+' and curChar!= "-":
            print("False")
            invalidReached = True
            break
        if '.' == curChar: dotCount+=1
    if invalidReached: continue
    if dotCount == 1:
        try:
            float(curVal)
            print("True")
        except ValueError:
            print("False")
    else:
        print("False")
    
