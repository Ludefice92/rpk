# Enter your code here. Read input from STDIN. Print output to STDOUT
from itertools import groupby

S = input()
groups = [(len(list(group)),key) for key,group in groupby(S)]
output = ' '.join(f"({count}, {char})" for count, char in groups)
print(output)
