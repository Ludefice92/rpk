def getInt(curInstr, getFirstInt):
    sections = curInstr.split() #split string based on whitespace
    
    if getFirstInt and len(sections) == 2:
        return int(sections[1])
    elif getFirstInt and len(sections) == 3:
        return int(sections[2])
    elif not getFirstInt:
        return int(sections[1])

if __name__ == '__main__':
    N = int(input())
    xList = []
    for i in range(N):
        curInstr = input()
        if 'insert' in curInstr:
            curInt = getInt(curInstr,True)
            curIndex = getInt(curInstr,False)
            xList.insert(curIndex,curInt)
        elif 'print' in curInstr:
            print(f"{xList}")
        elif 'remove' in curInstr:
            xList.remove(int(curInstr[-1]))
        elif 'append' in curInstr:
            curInt = getInt(curInstr,True)
            xList.append(curInt)
        elif 'sort' in curInstr:
            xList.sort()
        elif 'pop' in curInstr:
            xList.pop(len(xList)-1)
        elif 'reverse' in curInstr:
            xList.reverse()
            
