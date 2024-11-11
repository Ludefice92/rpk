# Enter your code here. Read input from STDIN. Print output to STDOUT
import re

S = input()

regpat = r'(?<=[qwrtypsdfghjklzxcvbnmQWRTYPSDFGHJKLZXCVBNM])([aeiouAEIOU]{2,})(?=[qwrtypsdfghjklzxcvbnmQWRTYPSDFGHJKLZXCVBNM])'
regmatch = re.findall(regpat,S)

if regmatch:
    for match in regmatch:
        print(match)
else:
    print(-1)
