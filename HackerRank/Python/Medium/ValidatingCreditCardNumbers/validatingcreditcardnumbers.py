# Enter your code here. Read input from STDIN. Print output to STDOUT
import re

def is_valid_card(card_num):
    pat = r"^(?:[456]\d{3}-\d{4}-\d{4}-\d{4}|[456]\d{15})$"
    if not re.match(pat,card_num): return "Invalid"
    card_num = card_num.replace("-","")
    if re.search(r"(\d)\1{3,}", card_num): return "Invalid" #checking for 4+ consecutive repeated digits
    return "Valid"

n = int(input())
for _ in range(n):
    card_num = input().strip()
    print(is_valid_card(card_num))
