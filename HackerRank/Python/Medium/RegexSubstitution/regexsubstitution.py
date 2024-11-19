# Enter your code here. Read input from STDIN. Print output to STDOUT
import re
n = int(input())

for _ in range(n):
    txt = input()
    txt = re.sub(r"(?<= )&&(?= )", "and", txt)
    txt = re.sub(r"(?<= )\|\|(?= )", "or", txt)
    print(txt)
