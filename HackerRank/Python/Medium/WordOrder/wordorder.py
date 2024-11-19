# Enter your code here. Read input from STDIN. Print output to STDOUT
n = int(input())
distinctwords = {}
for _ in range(n):
    word = input()
    if word not in distinctwords.keys():
        distinctwords[word] = 1
    else:
        distinctwords[word] += 1
print(f"{len(distinctwords)}")
for key in distinctwords.keys():
    print(f"{distinctwords.get(key)} ",end='')
