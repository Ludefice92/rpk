def average(array):
    # your code goes here
    setX = set(array)
    return sum(setX)/len(setX)

if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().split()))
    result = average(arr)
    print(result)