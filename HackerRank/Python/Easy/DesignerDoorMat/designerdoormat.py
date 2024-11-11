# Enter your code here. Read input from STDIN. Print output to STDOUT
N, M = map(int,input().split())
dash = '-'
lineperpat = '.|.'
patprod = 1 #garbage val
welstr = "WELCOME"
for i in range(1,N//2+2):
    if i == (N//2 + 1):
        print((dash*(((M-len(welstr))//2)) + welstr + (dash*(((M-len(welstr))//2)))))
        break
    patprod = (i*2)-1
    print((dash*(M//2-(len(lineperpat)*patprod)//2)) + lineperpat*patprod + (dash*(M//2-(len(lineperpat)*patprod)//2)))
for i in range(N//2,0,-1):
    patprod = (i*2)-1
    print((dash*(M//2-(len(lineperpat)*patprod)//2)) + lineperpat*patprod + (dash*(M//2-(len(lineperpat)*patprod)//2)))
