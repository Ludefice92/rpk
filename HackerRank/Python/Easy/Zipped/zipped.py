# Enter your code here. Read input from STDIN. Print output to STDOUT
N, X = map(int,input().split())
marks = []

for _ in range(X):
    marks.append(list(map(float,input().split())))
for studentMarks in zip(*marks):
    curAvg = sum(studentMarks)/X;
    print(f"{curAvg}")
