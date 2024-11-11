# Enter your code here. Read input from STDIN. Print output to STDOUT
n = int(input())
studN = list(map(int,input().split()))
b = int(input())
studB = list(map(int,input().split()))

bothNandB = set(studN).intersection(studB)
print(f"{len(bothNandB)}")
