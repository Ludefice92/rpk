# Enter your code here. Read input from STDIN. Print output to STDOUT
from collections import namedtuple

N = int(input())
colNames = input().split()
studentMarkList = []
totalMarks = 0
nameN = ""
markN = 0
idN = 0
classN = 0
#doing most of this to show I can do this with a namedtuple...not actually necessary to solve the problem
for i in range(N):
    curIn = input().split()
    for j in range(len(colNames)):
        if colNames[j] == "ID":
            idN = int(curIn[j])
        elif colNames[j] == "MARKS":
            markN = int(curIn[j])
        elif colNames[j] == "NAME":
            nameN = curIn[j]
        elif colNames[j] == "CLASS":
            classN = int(curIn[j])
    tupleN = namedtuple(nameN,'ID MARK CLASS') 
    tupleNset = tupleN(ID = idN, MARK = markN, CLASS = classN)
    studentMarkList.append(tupleNset)
    
    #actually needed part
    totalMarks += studentMarkList[i].MARK

print(f"{(totalMarks/N):.2f}")
