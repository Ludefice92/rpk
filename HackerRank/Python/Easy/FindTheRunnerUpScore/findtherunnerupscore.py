if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().split()))
    originalMax = max(arr)
    arr = [val for val in arr if val != originalMax] #remake arr with the original max values removed
    print(f"{max(arr)}")
            
