import itertools

def minion_game(string):
    # your code goes here
    vowels = set("aeiouAEIOU")
    kevinscore = 0
    stuartscore = 0
    for i in range(len(string)):
        if s[i] in vowels:
            kevinscore += len(string) - i
        else:
            stuartscore += len(string) - i

    if kevinscore == stuartscore: print("Draw")
    elif kevinscore > stuartscore: print(f"Kevin {kevinscore}")
    elif stuartscore > kevinscore: print(f"Stuart {stuartscore}")    
    

if __name__ == '__main__':
    s = input()
    minion_game(s)