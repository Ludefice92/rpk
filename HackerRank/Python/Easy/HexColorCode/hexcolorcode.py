import re

regex = re.compile(r'(?<!^)(#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}))(?!\w)')
N = int(input())

for _ in range(N):
    line = input().strip()
    matches = regex.findall(line)
    for match in matches:
        print(match)
