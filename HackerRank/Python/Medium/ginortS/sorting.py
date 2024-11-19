# Enter your code here. Read input from STDIN. Print output to STDOUT
s = input()
alphabeticallowerstr = ""
alphabeticalupperstr = ""
odddigstr = ""
evendigstr = ""
for i in range(len(s)):
    if s[i].isdigit(): 
        if int(s[i]) % 2 == 0: evendigstr += s[i]
        else: odddigstr += s[i]
    else: 
        if s[i].islower(): alphabeticallowerstr += s[i]
        else: alphabeticalupperstr += s[i]

print(''.join(sorted(alphabeticallowerstr) + sorted(alphabeticalupperstr) + sorted(odddigstr) + sorted(evendigstr)))
