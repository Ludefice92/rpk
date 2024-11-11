import sys
if __name__ == '__main__':
    secondWorstScore = sys.maxsize * 2 + 1
    worstScore = sys.maxsize * 2 + 1
    nestedScoreList = []
    for i in range(int(input())):
        name = input()
        score = float(input())
        nestedScoreList.append([name,score])
        if score < worstScore:
            secondWorstScore = worstScore 
            worstScore = score
        elif worstScore < score < secondWorstScore:
            secondWorstScore = score
    namesToPrint = [name for name, score in nestedScoreList if score == secondWorstScore]
    
    for name in sorted(namesToPrint):
        print(name)
    
