# Enter your code here. Read input from STDIN. Print output to STDOUT
T = int(input())
for _ in range(T):
    UID = input()
    if not UID.isalnum() or len(UID) != 10:
        print("Invalid")
        continue
    isvalid = True
    charsSoFar = set()
    uppercasecount=0
    digcount=0
    
    for char in UID:
        if char in charsSoFar:
            print("Invalid")
            isvalid = False
            break
        charsSoFar.add(char)
        if char.isupper(): uppercasecount+=1
        if char.isdigit(): digcount+=1
    if isvalid and uppercasecount>=2 and digcount>=3:
        print("Valid")
    elif isvalid:
        print("Invalid")
