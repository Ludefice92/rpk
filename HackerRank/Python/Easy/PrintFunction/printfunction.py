if __name__ == '__main__':
    n = int(input())
    s = ""
    for i in range(n+1):
        if i==0: continue
        s += str(i)
    print(f"{s}")
