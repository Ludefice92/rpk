# Enter your code here. Read input from STDIN. Print output to STDOUT
import re
S = input()

regmatch = re.search(r"([a-zA-Z0-9])\1",S)

if regmatch:
    print(regmatch.group(1))
else:
    print(-1)
